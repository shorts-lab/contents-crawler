# 통합 크롤러 - 네이버 블로그 & PANN NATE & 디시인사이드

네이버 블로그, PANN NATE, 디시인사이드에서 키워드 검색을 통해 게시글을 수집하는 크롤러입니다.

## 기능

- **네이버 블로그 크롤링**: 키워드로 블로그 글 검색 및 본문 수집
- **PANN NATE 크롤링**: 키워드로 게시글 검색 및 본문 수집
- **디시인사이드 크롤링**: 키워드로 게시글 검색 및 수집
- **스케줄링**: APScheduler를 통한 자동 크롤링 스케줄링
- **REST API**: Flask 기반 API 제공
- **Swagger 문서화**: API 자동 문서화 및 테스트 인터페이스 제공
- **데이터베이스 저장**: 수집된 데이터를 데이터베이스에 저장

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

2. 데이터베이스 설정:

```bash
python setup_db.py
```

이 스크립트는 SQLite 또는 PostgreSQL 데이터베이스를 설정하고 필요한 테이블을 생성합니다.

## 사용 방법

### 서버 실행 (API 서버)

```bash
python app.py
```

또는 Gunicorn으로 실행:

```bash
gunicorn app:app
```

### 명령줄 인터페이스 사용

```bash
python cli.py --platform naver --keyword "검색어" --pages 3 --output "results.json"
```

### GUI 인터페이스 사용

```bash
python gui.py
```

### 테스트 실행

```bash
python -m unittest discover tests
```

### Swagger UI

API 문서화와 테스트를 위한 Swagger UI를 제공합니다:

```
http://localhost:5001/swagger/
```

Swagger UI를 통해 다음을 할 수 있습니다:

- API 엔드포인트 문서 확인
- 요청/응답 모델 확인
- API 직접 테스트

## Cloudtype 배포

이 프로젝트는 Cloudtype에 배포할 수 있도록 구성되어 있습니다.

1. Cloudtype 계정 생성 및 로그인
2. 새 프로젝트 생성
3. GitHub 저장소 연결
4. 배포 설정:
   - 런타임: Python
   - 시작 명령어: `gunicorn app:app`
   - 포트: 5001
   - 환경 변수 설정: DATABASE_URL 등

## 파일 구조

```
shorts-maker/
├── app.py                  # 메인 Flask 애플리케이션
├── cli.py                  # 명령줄 인터페이스 진입점
├── gui.py                  # GUI 인터페이스 진입점
├── requirements.txt        # 필요한 패키지 목록
├── Procfile               # Cloudtype 배포용 설정 파일
├── .env                   # 환경 변수 설정 파일
├── setup_db.py            # 데이터베이스 설정 스크립트
├── static/                # 정적 파일 디렉토리
│   └── swagger.json       # Swagger API 문서
├── tests/                 # 테스트 디렉토리
│   ├── __init__.py        # 테스트 패키지 초기화
│   └── test_crawlers.py   # 크롤러 테스트
└── src/                   # 소스 코드 디렉토리
    ├── api/               # API 관련 모듈
    │   ├── __init__.py    # API 패키지 초기화
    │   ├── routes.py      # API 라우트 정의
    │   └── swagger.py     # Swagger 설정
    ├── crawlers/          # 크롤러 모듈
    │   ├── __init__.py    # 크롤러 패키지 초기화
    │   ├── base_crawler.py # 기본 크롤러 클래스
    │   ├── naver_crawler.py # 네이버 블로그 크롤러
    │   ├── pann_crawler.py # PANN NATE 크롤러
    │   └── dcinside_crawler.py # 디시인사이드 크롤러
    ├── interfaces/        # 사용자 인터페이스 모듈
    │   ├── __init__.py    # 인터페이스 패키지 초기화
    │   ├── cli.py         # 명령줄 인터페이스
    │   └── gui.py         # GUI 인터페이스
    ├── models/            # 데이터베이스 모델
    │   ├── __init__.py    # 모델 패키지 초기화
    │   ├── database.py    # 데이터베이스 설정
    │   └── content.py     # 컨텐츠 모델
    └── utils/             # 유틸리티 모듈
        ├── __init__.py    # 유틸리티 패키지 초기화
        ├── browser.py     # 브라우저 관련 유틸리티
        └── config.py      # 설정 관련 유틸리티
```
