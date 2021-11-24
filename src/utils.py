from datetime import datetime

import librosa


def interpolation(embedding_a, embedding_b, alpha=0.):
    z_a2b = embedding_b - embedding_a
    z_c = embedding_a + alpha * z_a2b
    return z_c

def parse_time(time):
    time = datetime.strptime(time, '%H:%M:%S,%f').time()
    return 3600 * time.hour + 60 * time.minute + time.second + time.microsecond / 1e6


def handle_srt(path, sr=22050):
    text = open(path, 'r').read()
    splits = text.split('\n\n')
    times = []
    sents = []
    print(splits)
    for split in splits:
        if split:
            _, time, *sent = split.split('\n')
            sents.append(" ".join(sent))
            start, end = time.split(' --> ')
            start = parse_time(start)
            end = parse_time(end)
            times.append(start)
    times.append(end)
    samples = librosa.time_to_samples(times, sr)
    return sents, samples, times