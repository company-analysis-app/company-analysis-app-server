# 기업 분석 웹 애플리케이션 백엔드

## 📌 개요
기업 정보를 수집하고, 사용자 선호도를 기반으로 기업 추천을 제공하는 FastAPI 백엔드입니다.

## 🚀 설치 및 실행 방법

### 1. 저장소 클론
```bash
$ git clone https://github.com/HanbinSeong/company-analysis-app-server.git
$ cd company-analysis-app-server
```
### 2. 환경설정
```bash
pip install -r requirements.txt
```

### 3. `.env` 설정
.env 파일을 프로젝트 루트에 생성하여 환경변수를 추가합니다. (예시)
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/companydb
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_CLIENT_SECRET=your_kakao_client_secret
DART_API_KEY=your_dart_api_key
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
GROQ_API_KEY=your_groq_api_key
```

### 3. 서버 구동
```bash
uvicorn main:app --reload
```

## 🛠️ 프로젝트 구조
```
backend
├── models                      # 데이터베이스 ORM 모델 정의
│   ├── __init__.py
│   ├── user.py
│   ├── company.py
│   ├── category.py
│   └── favorite.py
├── routers                     # API 라우터
│   ├── __init__.py
│   ├── auth.py
│   ├── companies.py
│   ├── users.py
│   └── recommendations.py
├── schemas                     # 데이터 검증 스키마 정의
│   ├── __init__.py
│   ├── user.py
│   ├── company.py
│   ├── auth.py
│   └── recommendation.py
├── database.py                 # 데이터베이스 연결 및 세션 관리
├── main.py                     # FastAPI 애플리케이션 설정 및 라우터 등록
├── requirements.txt            # Python 필요 패키지 라이브러리 목록
└── README.md
```

## 📃 주요 엔드포인트

- `/auth`: OAuth 로그인 및 인증
- `/companies`: 기업 정보 검색
- `/users`: 유저 정보 관리
- `/recommendations`: 사용자 선호도 기반 추천 제공

## 🔒 OAuth 설정
구글과 카카오 OAuth는 각각 개발자 콘솔에서 클라이언트 ID와 비밀키를 발급받아 `.env`에 설정합니다.

## 📦 DB Schema 예시
- `users`: 사용자 정보
- `companies`: 기업 정보
- `favorites`: 사용자 관심 기업
- `categories`: 기업 카테고리

## 📡 외부 API 사용
- DART API: 기업 재무 데이터
- Naver 뉴스 API: 최신 뉴스
- Groq API: 기업 정보 AI 요약 제공

## 🚧 향후 개발 계획
- DB 데이터 연동 및 실제 API 구현
- 프론트엔드와의 본격적인 연동 및 테스트
