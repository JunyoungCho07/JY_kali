import subprocess

# 예시용: 중국어 문자 몇 개만 넣어둠 (전체는 HZK 파일 등에서 구해도 됨)
char_list = ['中', '国', '汉', '字', '语', '言', '学', '习', '測', '試']

ans = []

for ch in char_list:
    utf8_bytes = ch.encode('utf-8')
    if len(utf8_bytes) < 3:
        continue

    # iconv를 subprocess로 호출
    try:
        result = subprocess.run(
            ['iconv', '-f', 'UTF-8', '-t', 'ISO-2022-CN-EXT'],
            input=utf8_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        encoded_bytes = result.stdout
        hexstr = encoded_bytes.hex()

        if len(hexstr) >= 8:
            fourth_byte = int(hexstr[6:8], 16)
            if 0x48 <= fourth_byte <= 0x4C:
                continue  # 제외되는 문자
            else:
                ans.append(ch)
    except subprocess.CalledProcessError:
        continue  # iconv 실패 시 무시

print("✅ 조건을 만족하는 문자들:", ans)
