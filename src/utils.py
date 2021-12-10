from datetime import datetime

def interpolation(embedding_a, embedding_b, alpha=0.):
    z_a2b = embedding_b - embedding_a
    z_c = embedding_a + alpha * z_a2b
    return z_c

def parse_time(time):
    time = datetime.strptime(time, '%H:%M:%S,%f').time()
    return 3600 * time.hour + 60 * time.minute + time.second + time.microsecond / 1e6

