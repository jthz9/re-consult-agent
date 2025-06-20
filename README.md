# 재생에너지 AI 가이드

**재생에너지 상담 AI 에이전트**

재생에너지 관련 정책, 제도, RAG 검색, ML 예측, 실시간 데이터를 통합한 AI 상담 시스템입니다.

---

## 🎯 프로젝트 개요

### 핵심 목표

- **RAG 기반 AI 교육 시스템**: 복잡한 재생에너지 용어와 규정을 쉽게 설명
- **ML 기반 개인화 예측**: 정확한 발전량 예측 및 경제성 분석 서비스
- **대화형 상담 시스템**: 웹 인터페이스와 API를 통한 전문가 수준 상담

### 타겟 사용자

- **개인/가정**: 태양광 패널 설치를 고려하는 일반인
- **소상공인**: 카페, 식당 등 소규모 사업자
- **초보자**: 재생에너지 기초 지식이 없는 누구나

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Chroma)      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 전체 시스템 구성

1. **프론트엔드 (Next.js)**

   - React 기반 웹 인터페이스
   - 실시간 대시보드 및 챗봇
   - 데이터 시각화 및 ML 예측 결과 표시

2. **백엔드 (FastAPI + LangChain)**

   - LangChain Agent 기반 AI 상담 시스템
   - RAG, ML, API 도구 통합
   - RESTful API 제공

3. **데이터베이스 (Chroma)**
   - 벡터 데이터베이스
   - 재생에너지 관련 문서 저장
   - 임베딩 기반 검색

---

## 🚀 기술 스택

### 프론트엔드

- **Framework**: Next.js 15.3.4 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **State Management**: React Hooks (Custom Hooks)
- **Charts**: Recharts

### 백엔드

- **Framework**: FastAPI
- **AI/ML**: LangChain, OpenAI GPT-4, Sentence Transformers
- **Database**: Chroma (Vector DB)
- **ML Framework**: PyTorch
- **Language**: Python 3.11+

### 인프라

- **Containerization**: Docker & Docker Compose
- **API**: RESTful API
- **Testing**: pytest, Jest

---

## 📁 프로젝트 구조

```
re-consult-agent/
├── frontend/                    # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React 컴포넌트
│   │   ├── services/           # API 서비스
│   │   └── hooks/              # 커스텀 React 훅
│   ├── public/                 # 정적 파일
│   ├── package.json            # 프론트엔드 의존성
│   └── Dockerfile              # 프론트엔드 Docker
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py             # FastAPI 진입점
│   │   ├── agents/             # LangChain Agent
│   │   ├── tools/              # LangChain Tools
│   │   ├── core/               # 핵심 로직
│   │   └── ml/                 # ML 모델
│   ├── data/                   # 데이터 저장소
│   ├── requirements.txt        # 백엔드 의존성
│   └── Dockerfile              # 백엔드 Docker
├── docker-compose.yml          # 전체 시스템 Docker 설정
└── README.md                   # 이 파일
```

---

## 🎯 주요 기능

### 1. 대시보드

- 실시간 시스템 상태 모니터링
- 발전량 데이터 카드 (태양광, 풍력)
- 최근 활동 및 시스템 정보 표시

### 2. AI 챗봇

- 재생에너지 관련 질의응답
- 실시간 대화 인터페이스
- 백엔드 AI 모델과 연동

### 3. 발전량 시각화

- 실시간 발전량 차트
- Recharts 기반 데이터 시각화
- 다양한 차트 타입 지원

### 4. ML 예측

- 머신러닝 기반 발전량 예측
- 예측 결과 시각화
- 모델 성능 지표 표시

---

## 🚀 빠른 시작

### 1. 전체 시스템 실행 (Docker)

```bash
# 프로젝트 클론
git clone <repository-url>
cd re-consult-agent

# 환경변수 설정
cp .env.example .env
# OPENAI_API_KEY 설정 필요

# Docker Compose로 전체 시스템 실행
docker-compose up -d
```

### 2. 개별 실행

#### 프론트엔드

```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

#### 백엔드

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# http://localhost:8000/docs
```

### 3. 접속 정보

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Chroma DB**: http://localhost:8001

---

## 🎯 예상 사용자 경험

### 초보자 상담 시나리오

```
👤 사용자: "태양광 설치를 고려중인데 어떻게 시작해야 하나요?"

🤖 AI Agent:
[RAGTool 실행]
"태양광 발전은 태양빛을 전기로 변환하는 친환경 에너지입니다..."

👤 사용자: "우리 집(수원, 30평)에 설치하면 얼마나 절약되나요?"

🤖 AI Agent:
[WeatherTool 실행] → 수원 지역 기상 정보 수집
[PredictionTool 실행] → ML 모델로 월별 발전량 예측
[EconomicTool 실행] → 20년 경제성 분석

"수원 지역 기준 7kW 설치 시:
• 연간 예상 발전량: 8,760kWh (ML 예측)
• 월별 발전량: 여름 950kWh, 겨울 520kWh
• 20년 총 절약액: 2,800만원
• 투자 회수 기간: 10.2년"
```

---

## 🏆 프로젝트 주요 요소

### 1. **통합 AI 상담 시스템**

- 프론트엔드와 백엔드의 완전한 통합
- 실시간 웹 인터페이스를 통한 직관적인 상담
- LangChain Agent 기반 지능형 응답

### 2. **RAG + ML 통합 분석**

- 크롤링 기반 최신 정책 정보
- ML 기반 정확한 발전량 예측
- 실시간 API 데이터 반영

### 3. **전문가 수준의 종합 상담**

- 7개 전문 도구 통합으로 포괄적 분석
- 개인부터 기업까지 사용자별 맞춤 상담
- 이론부터 실행까지 단계별 가이드

### 4. **확장 가능한 아키텍처**

- 모듈화된 프론트엔드/백엔드 구조
- Docker 기반 일관된 실행 환경
- 새로운 기능 쉽게 추가 가능

---

## 개발 가이드

### 상세 문서

- **[프론트엔드 개발](./frontend/README.md)**: Next.js 기반 웹 인터페이스
- **[백엔드 개발](./backend/README.md)**: FastAPI + LangChain AI 시스템

### 환경 설정

- **전체 시스템**: Docker Compose를 통한 일관된 실행 환경
- **개별 개발**: 각 시스템별 독립적인 개발 환경 지원

---

## 📞 지원

### 문서

- [프론트엔드 문서](./frontend/README.md)
- [백엔드 문서](./backend/README.md)

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---
