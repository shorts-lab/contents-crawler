# 통합 크롤러 - 네이버 블로그 & PANN NATE & 디시인사이드

네이버 블로그, PANN NATE, 디시인사이드에서 키워드 검색을 통해 게시글을 수집하는 크롤러입니다.

## 기능

- **네이버 블로그 크롤링**: 키워드로 블로그 글 검색 및 본문 수집
- **PANN NATE 크롤링**: 키워드로 게시글 검색 및 본문 수집
- **디시인사이드 크롤링**: 키워드로 게시글 검색 및 수집
- **스케줄링**: APScheduler를 통한 자동 크롤링 스케줄링
- **REST API**: Flask 기반 API 제공
- **Swagger 문서화**: API 자동 문서화 및 테스트 인터페이스 제공
- **데이터베이스 저장**: PostgreSQL/SQLite 데이터베이스 지원
- **Docker 지원**: Docker Compose를 통한 간편한 환경 구성

## 설치 방법

### 1. 기본 설치

```bash
pip install -r requirements.txt
```

### 2. Docker를 이용한 PostgreSQL 설정

```bash
# Docker Desktop 실행 후
docker-compose up -d
```

### 3. 서버 실행

```bash
python app.py
```

또는 Gunicorn으로 실행:

```bash
gunicorn app:app
```

### Swagger UI 접속

API 문서화 및 테스트: http://localhost:5001/swagger/

## 배포

### Cloudtype 배포

1. Cloudtype 계정 생성 및 GitHub 저장소 연결
2. 배포 설정:
   - 런타임: Python
   - 시작 명령어: `gunicorn app:app`
   - 포트: 5001
   - 환경 변수: DATABASE_URL 설정

### 로컬 개발 환경

```bash
# PostgreSQL 컨테이너 시작
docker-compose up -d

# .env 파일에서 로컬 DB 설정
DATABASE_URL=postgresql://contents-crawler:contents-crawler2025@localhost:5432/postgres
```

## 파일 구조

```
shorts-maker/
├── app.py                  # 메인 Flask 애플리케이션
├── docker-compose.yml      # PostgreSQL Docker 설정
├── requirements.txt        # Python 패키지 목록

├── .env                   # 환경 변수
├── Procfile               # 배포 설정
├── static/swagger.json    # API 문서
└── src/                   # 소스 코드
    ├── api/               # REST API
    ├── crawlers/          # 크롤링 엔진
    ├── interfaces/        # 인터페이스
    ├── models/            # 데이터베이스 모델
    └── utils/             # 유틸리티
```
