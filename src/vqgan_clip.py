import numpy as np
import torch
import clip
import sys
import translators
from tqdm import tqdm
import re

import cv2

sys.path.append("../feed_forward_vqgan_clip")
from feed_forward_vqgan_clip.main import load_vqgan_model as _load_vqgan_model
from feed_forward_vqgan_clip.main import CLIP_DIM, clamp_with_grad, synth
from src.gpt3 import load_tokenizer_and_model, generate


def load_vqgan_model(device="cuda:0"):
    model_path = "../feed_forward_vqgan_clip/cc12m_32x1024_mlp_mixer.th"
    net = torch.load(model_path).to(device)
    config = net.config
    vqgan_config = "../feed_forward_vqgan_clip/vqgan_imagenet_f16_16384.yaml"
    vqgan_checkpoint = "../feed_forward_vqgan_clip/vqgan_imagenet_f16_16384.ckpt"
    model = _load_vqgan_model(vqgan_config, vqgan_checkpoint).to(device)
    return model, net, config


def load_gpt_model(model_path):
    tokenizer, gpt3 = load_tokenizer_and_model(model_path)
    return tokenizer, gpt3


def generate_sentence(start_phrase, gpt3, tokenizer, n_grams=4):
    generated_sentence = generate(gpt3, tokenizer, start_phrase, num_beams=5, max_length=100)[0]
    translated_sentence = translators.google(generated_sentence, from_language='ru', to_language='en')
    words = re.findall("\w+", translated_sentence)
    sentences = []
    for i in range(0, len(words), n_grams):
        pair = " ".join(words[i:i + n_grams])
        sentences.append(pair)
    return sentences, generated_sentence


def load_perceptor(device="cuda:0"):
    clip_model = "ViT-B/32"
    clip_dim = CLIP_DIM
    perceptor = clip.load(clip_model, jit=False)[0].eval().requires_grad_(False).to(device)
    return perceptor


def generate_video(sentences, output_path, vqgan_model, mlp_mixer, perceptor, batch_size=6, device="cuda:0"):
    z_min = vqgan_model.quantize.embedding.weight.min(dim=0).values[None, :, None, None]
    z_max = vqgan_model.quantize.embedding.weight.max(dim=0).values[None, :, None, None]

    toks = clip.tokenize(sentences, truncate=True)

    feats = perceptor.encode_text(toks.to(device)).float()

    H_list = []
    for i in range(len(sentences) - 1):
        dt = 15 / len(sentences)
        nb_interm = round(30 * dt)
        alpha = torch.linspace(0, 1, nb_interm).view(-1, 1).to(device)
        Hi = feats[i:i + 1] * (1 - alpha) + feats[i + 1:i + 2] * alpha
        H_list.append(Hi)
    H = torch.cat(H_list)
    xr_list = []
    with torch.no_grad():
        for i in tqdm(range(0, len(H), batch_size)):
            z = mlp_mixer(H[i:i + batch_size])
            z = clamp_with_grad(z, z_min.min(), z_max.max())
            xr = synth(vqgan_model, z)
            xr_list.append(xr.cpu())
    xr_list = torch.cat(xr_list).permute(0, 2, 3, 1).numpy() * 255
    xr_list = xr_list.astype(np.uint8)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 30, (256, 256))
    for img in tqdm(xr_list):
        out.write(img)
    out.release()


if __name__ == '__main__':
    tokenizer, gpt3 = load_gpt_model("../rugpt3small_based_on_gpt2")
    vqgan_model, mlp_mixer, _ = load_vqgan_model()
    perceptor = load_perceptor()
    while True:
        start_story = input("Введите текст:\n")
        sentences, generated_sentence = generate_sentence(start_story, gpt3, tokenizer, n_grams=6)
        print(generated_sentence)
        generate_video(sentences, f"../results/{start_story}.mp4", vqgan_model, mlp_mixer, perceptor)
