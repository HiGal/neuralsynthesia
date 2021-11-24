import numpy as np
import torch
import clip
import sys
import librosa
from matplotlib import pyplot as plt
from tqdm import tqdm

from src.utils import handle_srt
import cv2

sys.path.append(".")
from feed_forward_vqgan_clip.main import load_vqgan_model, CLIP_DIM, clamp_with_grad, synth
import torchvision

if __name__ == '__main__':
    model_path = "cc12m_32x1024_mlp_mixer.th"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    net = torch.load(model_path).to(device)
    config = net.config
    vqgan_config = config.vqgan_config
    vqgan_checkpoint = config.vqgan_checkpoint
    clip_model = config.clip_model
    clip_dim = CLIP_DIM
    perceptor = clip.load(clip_model, jit=False)[0].eval().requires_grad_(False).to(device)
    model = load_vqgan_model(vqgan_config, vqgan_checkpoint).to(device)
    z_min = model.quantize.embedding.weight.min(dim=0).values[None, :, None, None]
    z_max = model.quantize.embedding.weight.max(dim=0).values[None, :, None, None]

    bs = 12

    soundtrack, _ = librosa.load("../joji-run.mp3", sr=44100)
    sentences, samples, times = handle_srt("../Joji-Run.srt")
    times.append(librosa.get_duration(y=soundtrack, sr=44100))

    toks = clip.tokenize(sentences, truncate=True)

    feats = perceptor.encode_text(toks.to(device)).float()

    H_list = []
    for i in range(len(sentences) - 1):
        t = times[i]
        t_next = times[i + 1]
        dt = t_next - t
        nb_interm = round(30 * dt)
        alpha = torch.linspace(0, 1, nb_interm).view(-1, 1).to(device)
        Hi = feats[i:i + 1] * (1 - alpha) + feats[i + 1:i + 2] * alpha
        H_list.append(Hi)
    H = torch.cat(H_list)
    xr_list = []
    with torch.no_grad():
        for i in tqdm(range(0, len(H), bs)):
            z = net(H[i:i + bs])
            z = clamp_with_grad(z, z_min.min(), z_max.max())
            xr = synth(model, z)
            xr_list.append(xr.cpu())
    del model, perceptor, H, feats, toks, net
    # xr_list = torch.cat(xr_list)
    xr_list = torch.cat(xr_list).permute(0, 2, 3, 1).numpy() * 255
    xr_list = xr_list.astype(np.uint8)

    out = cv2.VideoWriter('project.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, (256, 256))
    for img in tqdm(xr_list):
        out.write(img)
    out.release()

    # grid = torchvision.utils.make_grid(xr.cpu(), nrow=len(xr))
    # out_path = "gen.png"
    # torchvision.transforms.functional.to_pil_image(grid).save(out_path)
    # for i, img in enumerate(xr_list):
    #     torchvision.transforms.functional.to_pil_image(img).save(f"image_{i:05d}.png")
