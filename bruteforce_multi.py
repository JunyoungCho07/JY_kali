# from multiprocessing import Pool, cpu_count
# import hashlib, itertools, string

# def check_candidate(candidate):
#     prefix = "9f7630b"
#     target_hash = "a50040e53fbc775c96bb9c652faa79463644589a"
#     candidate_str = prefix + ''.join(candidate)
#     h = hashlib.sha1(candidate_str.encode()).hexdigest()
#     if h == target_hash:
#         return candidate_str
#     return None

# if __name__ == '__main__':
#     charset = string.digits + string.ascii_lowercase  # 범위 좀 줄이기
#     pool = Pool(cpu_count())
#     for result in pool.imap_unordered(check_candidate, itertools.product(charset, repeat=6), chunksize=1000):
#         if result:
#             print(f"Found: {result}")
#             print(f"Found: {result[7:]}")
#             pool.terminate()
#             break






from multiprocessing import Pool, cpu_count
import hashlib, itertools, string
from functools import partial
import re  # 정규표현식으로 추출

def check_candidate(prefix, target_hash, candidate):
    candidate_str = prefix + ''.join(candidate)
    h = hashlib.sha1(candidate_str.encode()).hexdigest()
    if h == target_hash:
        return candidate_str
    return None

if __name__ == '__main__':
    # 1. 입력 받기
    line = input('입력 (예: sha1("869a005######") == "abcd..."):\n> ').strip()

    # 2. 정규식으로 prefix, 자리수, target hash 추출
    match = re.match(r'sha1\("([a-zA-Z0-9]*)(#+)"\)\s*==\s*"([a-fA-F0-9]{40})"', line)

    if not match:
        print("❌ 입력 형식이 잘못됐어요!")
        exit(1)

    prefix, sharp_part, target_hash = match.groups()
    repeat = len(sharp_part)

    print(f"\n🔍 분석 결과:")
    print(f"→ prefix: '{prefix}'")
    print(f"→ 자리수: {repeat}자리")
    print(f"→ target hash: {target_hash.lower()}\n")

    # 3. 브루트포싱 준비
    charset = string.digits + string.ascii_lowercase
    wrapped_check = partial(check_candidate, prefix, target_hash.lower())

    pool = Pool(cpu_count())
    try:
        for result in pool.imap_unordered(wrapped_check, itertools.product(charset, repeat=repeat), chunksize=1000):
            if result:
                print(f"\n✅ Found match: {result}")
                print(f"🔎 Suffix only: {result[len(prefix):]}")
                pool.terminate()
                break
        else:
            print("❌ No match found.")
    finally:
        pool.close()
        pool.join()
