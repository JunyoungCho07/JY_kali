# WebHacking CTF Writeup: Directory Listing & WebShell Exploitation

## 🧭 문제 환경 개요

- **대회 환경 주소**: `http://16.184.15.57:8090`
- **서버 정보**: Apache/2.4.59 (Debian)
- **주요 취약점**: 
  - 디렉토리 리스팅 (Directory Listing)
  - 계정 정보 유출 (JSON 파일)
  - 업로드 기능 통한 웹쉘 삽입
  - 웹쉘을 통한 서버 내부 명령 실행

---

## 🔍 전체 풀이 흐름

### 1. 디렉토리 리스팅 탐지

`/readflag/`, `/test/` 경로에 접근하자 **디렉토리 내부 파일 목록이 노출**됨.

- `/readflag/` 내부:
  - `_syg54MwfqH_taejin.php.php` : 의심스러운 웹쉘
  - `profile.json`, `pw.json` : 계정 정보 포함 가능성
  - `exploit123/`, `shell/` 등의 폴더 존재

- `/test/` 내부:
  - `profile.json`, `pw.json` : 로그인 정보 포함
  - `webshell.php_xxx_webshell.php` : 업로드된 웹쉘로 추정

---

### 2. 계정 정보 획득 및 로그인

- `/test/pw.json` 파일에 아래와 같은 정보 존재:

```json
{ "id": "test", "pw": "test" }
```

- 이를 통해 로그인 성공 → 게시판 및 신고 기능 접근 가능

---

### 3. 웹쉘 업로드 취약점 의심

- 신고 기능 혹은 게시판의 **파일 업로드 기능** 통해 `.php` 웹쉘이 업로드된 것으로 보임
- `webshell.php_xxx_webshell.php` 형태로 저장된 파일이 존재

---

### 4. 태진의 웹쉘 확인

- `/readflag/_syg54MwfqH_taejin.php.php` 에 접속하면 다음과 같은 메시지 출력:

```
Taejin Webshell Active from Report Page!
Use: ?cmd=command, ?file=filepath, ?flag=1
```

- 즉, **명령 실행 기능이 포함된 PHP 웹쉘**임

---

### 5. 웹쉘을 통한 플래그 획득

- 다음 명령어로 서버 내 파일 탐색:

```
?cmd=find / -type f -name "readflag*" 2>/dev/null
```

- 출력된 경로 중 실행 가능한 바이너리 추정 파일 실행:

```
?cmd=/readflag-LCRFGPti
```

- 최종적으로 **FLAG 획득 성공**:

```
cce2024{02b9223eea20669453fcdb0dbe22a5b93c67b0bf336b03f7d33178956132aafd}
```

---

## 🚨 보안 교훈

| 항목 | 문제점 | 대응 방안 |
|------|--------|------------|
| 디렉토리 리스팅 | 내부 파일 노출 | Apache에서 `Options -Indexes` 설정 |
| 민감 파일 노출 | `pw.json`에 인증정보 포함 | `.json`, `.env` 파일 외부 노출 방지 |
| 파일 업로드 취약점 | `.php` 업로드 가능 | 확장자 검사, MIME 검사, 실행 권한 제거 |
| 웹쉘 삽입 가능성 | 공격자 명령 실행 | 업로드 위치 제한, 권한 분리 등 필요 |

---

## ✅ 정리

이 문제는 **우연처럼 보이지만 매우 고전적인 웹 취약점 조합**을 활용하는 문제였다.  
실제 해킹 환경에서도 위와 같은 디렉토리 리스팅 → 계정 유출 → 업로드 → 웹쉘 삽입 → 명령 실행 흐름은 빈번하게 발생하므로, 실제 인프라 구축 시 이러한 보안 설정을 꼭 확인해야 한다.