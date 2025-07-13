# 통합 크롤러 - 네이버 블로그 & PANN NATE

네이버 블로그와 PANN NATE에서 키워드 검색을 통해 게시글을 수집하는 GUI 크롤러입니다.

## 기능

- **네이버 블로그 크롤링**: 키워드로 블로그 글 검색 및 본문 수집
- **PANN NATE 크롤링**: 키워드로 게시글 검색 및 본문 수집
- **GUI 인터페이스**: 사용하기 쉬운 그래픽 인터페이스
- **JSON 저장**: 수집된 데이터를 JSON 파일로 저장

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. Chrome 브라우저와 ChromeDriver 설치 필요

## 사용 방법

### GUI 버전 (권장)
```bash
python unified_gui_crawler.py
```

### 콘솔 버전
```bash
python unified_crawler.py
```

## 파일 구조

- `unified_gui_crawler.py`: GUI 크롤러 메인 파일
- `unified_crawler.py`: 크롤링 로직 및 콘솔 버전
- `requirements.txt`: 필요한 패키지 목록

## 주요 특징

1. **플랫폼 선택**: 네이버 블로그 또는 PANN NATE 선택 가능
2. **키워드 검색**: 원하는 키워드로 검색
3. **페이지 수 설정**: 크롤링할 페이지 수 지정
4. **실시간 진행률**: 크롤링 진행 상황 표시
5. **결과 미리보기**: 수집된 데이터 즉시 확인
6. **JSON 저장**: 결과를 JSON 파일로 저장

## 주의사항

- 웹사이트의 이용약관을 준수하여 사용하세요
- 과도한 요청으로 서버에 부하를 주지 않도록 주의하세요
- 개인정보가 포함된 데이터 처리 시 주의하세요