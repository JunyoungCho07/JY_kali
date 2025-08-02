from multiprocessing import Pool, cpu_count
import hashlib, itertools, string

def check_candidate(candidate):
    prefix = "8df7db8"
    target_hash = "c1871623d49deaa139f0f958357a94bca3c2c326"
    candidate_str = prefix + ''.join(candidate)
    h = hashlib.sha1(candidate_str.encode()).hexdigest()
    if h == target_hash:
        return candidate_str
    return None

if __name__ == '__main__':
    charset = string.digits + string.ascii_lowercase  # 범위 좀 줄이기
    pool = Pool(cpu_count())
    for result in pool.imap_unordered(check_candidate, itertools.product(charset, repeat=6), chunksize=1000):
        if result:
            print(f"Found: {result}")
            pool.terminate()
            break
