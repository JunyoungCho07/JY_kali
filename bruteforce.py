import hashlib
import itertools
import string

prefix = "84358a2"
target_hash = "2bc9a0a58f63e239bafb448e1025743dbccaac20"
# Brute force to find the string that hashes to the target hash
# The string is of the form "84358a2XXXXXX" where XXXXXX is a 6-digit number

charset = string.digits + string.ascii_lowercase

for candidate in itertools.product(charset, repeat=6):
    candidate_str = prefix + ''.join(candidate) # candidate is tuple --> join --> to string
    # Calculate the SHA-1 hash of the candidate string
    candidate_hash = hashlib.sha1(candidate_str.encode()).hexdigest()
    #description of encode: converts a string to bytes using the default encoding (UTF-8)
    # "hello".encode() → b"hello"
    # .hexdigest()는 hashlib 모듈에서 해시 객체(예: sha1 객체)에 대해서만 사용 가능하다.
    if candidate_hash == target_hash:
        print(f"Found matching string: {candidate_str}")
        break
else:
    print("No matching string found.")