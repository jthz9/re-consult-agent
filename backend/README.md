# 재생에너지 AI 가이드 - 백엔드

**LangChain 기반 RAG + ML 통합 AI 상담 시스템**

## 🎯 프로젝트 개요

### 핵심 목표

- **LangChain Agent 기반 지능형 상담**: ReAct 패턴을 통한 동적 도구 선택
- **RAG 기반 지식 검색**: 재생에너지 정책 및 제도 정보 통합 검색
- **ML 기반 예측 시스템**: 발전량 예측 및 경제성 분석
- **실시간 데이터 통합**: 기상청, 전력거래소 API 연동

---

## 🏗️ LangChain 기반 시스템 아키텍처

### 컴포넌트 구성

#### 1. **LangChain Agent (오케스트레이터)**

- **ReAct Pattern**: 사용자 의도 분석 → 도구 선택 → 실행 → 결과 통합
- **대화 컨텍스트**: ConversationBufferWindowMemory로 멀티턴 대화 관리
- **도구 라우팅**: 질문 유형에 따라 최적 도구 조합 선택

#### 2. **RAG Tool (지식 기반)**

- **RAGTool**: 정책, 기술, 제도 등 모든 정보를 통합 검색
- **크롤링 데이터**: KNREC FAQ 등 재생에너지 관련 데이터 수집
- **벡터 검색**: Chroma DB를 활용한 의미 기반 검색

#### 3. **ML Tools (예측 및 분석)**

- **PredictionTool**: LSTM 기반 월별 발전량 예측
- **EconomicTool**: 20년 투자 수익성 분석
- **모델 관리**: Pytorch 기반 ML 모델

#### 4. **API Tools (실시간 데이터)**

- **WeatherTool**: 기상청 실시간 기상 데이터
- **PowerTool**: 전력거래소 SMP, REC 가격 정보

---

## 🛠️ 기술 스택

### LangChain 생태계

- **LangChain**: Agent, Tools, Memory, Chain 프레임워크
- **OpenAI API**: GPT-4o (LLM) + text-embedding-3-large
- **Sentence Transformers**: HuggingFace 한국어 임베딩 모델

### AI/ML 스택

- **Pytorch**: LSTM 신경망 구현
- **Scikit-learn**: 데이터 전처리 및 분석
- **Pandas/NumPy**: 데이터 처리

### 백엔드 & 데이터

- **FastAPI**: REST API 서버
- **Chroma**: Vector Database (LangChain 통합)
- **Pydantic**: 데이터 검증
- **SQLAlchemy**: 데이터베이스 ORM (필요시)

### 인프라 & 도구

- **Docker**: 컨테이너화
- **pytest**: 테스팅
- **Scrapy**: 웹 크롤링
- **Loguru**: 로깅

---

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── main.py                    # FastAPI 진입점
│   ├── agents/                    # LangChain Agent
│   │   ├── __init__.py
│   │   └── chatbot_agent.py       # 챗봇 에이전트
│   ├── core/                      # 핵심 로직
│   │   ├── __init__.py
│   │   ├── intent_classifier.py   # 의도 분류
│   │   └── response_integrator.py # 응답 통합
│   ├── tools/                     # LangChain Tools
│   │   ├── __init__.py
│   │   ├── rag_tools/             # RAG 관련 도구
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py    # RAG 파이프라인
│   │   │   ├── chains/            # RAG 체인
│   │   │   ├── core/              # RAG 핵심 로직
│   │   │   ├── crawlers/          # 크롤러
│   │   │   ├── embeddings/        # 임베딩
│   │   │   ├── loaders/           # 문서 로더
│   │   │   ├── retrievers/        # 검색기
│   │   │   ├── splitters/         # 텍스트 분할
│   │   │   ├── utils/             # 유틸리티
│   │   │   └── vectorstores/      # 벡터 스토어
│   │   ├── ml_tools/              # ML 관련 도구
│   │   │   ├── __init__.py
│   │   │   ├── inference/         # 추론
│   │   │   ├── models/            # 모델
│   │   │   └── training/          # 훈련
│   │   └── api_tools/             # API 관련 도구
│   │       └── __init__.py
│   ├── ml/                        # ML 모델
│   │   ├── __init__.py
│   │   ├── inference/             # 추론 엔진
│   │   ├── models/                # 모델 정의
│   │   └── training/              # 훈련 스크립트
│   └── langchain_config/          # LangChain 설정
├── data/
│   ├── crawled_data/              # 크롤링된 데이터
│   ├── ml_data/                   # ML 훈련 데이터
│   └── vectorstores/              # 벡터 스토어
├── cli/                           # CLI 인터페이스
│   └── rag_qa.py                  # RAG QA CLI
├── docs/                          # 문서
├── tests/                         # 테스트
├── requirements.txt               # Python 의존성
├── Dockerfile                     # Docker 설정
└── README.md                      # 이 파일
```

---

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd re-consult-agent/backend

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# OPENAI_API_KEY 설정 필요
```

### 2. 개발 서버 실행

```bash
# FastAPI 서버 시작
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API 문서 확인
http://localhost:8000/docs
```

### 3. Docker 실행

```bash
# Docker 이미지 빌드
docker build -t renewable-energy-backend .

# 컨테이너 실행
docker run -p 8000:8000 renewable-energy-backend
```

### 4. 전체 시스템 실행 (Docker Compose)

```bash
# 프로젝트 루트에서
docker-compose up backend
```

---

## 🔌 API 엔드포인트

### 기본 엔드포인트

- `GET /`: 루트 엔드포인트 (시스템 정보)
- `GET /health`: 헬스 체크
- `GET /docs`: API 문서 (Swagger UI)

### 챗봇 관련

- `GET /api/chatbot/status`: 챗봇 상태 확인
- `POST /api/chat`: 챗봇과 대화

### RAG 관련

- `GET /api/rag/search`: RAG 검색

### 시스템 정보

- `GET /api/system/info`: 시스템 정보

---

## 🎯 주요 기능

### 1. LangChain Agent 시스템

- **ReAct 패턴**: 사용자 의도 분석 및 동적 도구 선택
- **멀티턴 대화**: ConversationBufferWindowMemory 기반 대화 컨텍스트 관리
- **도구 조합**: 질문 유형에 따른 최적 도구 조합 선택

### 2. RAG 검색 시스템

- **벡터 검색**: Chroma DB 기반 의미 기반 검색
- **크롤링 데이터**: KNREC FAQ 등 재생에너지 관련 데이터 수집
- **임베딩 모델**: Sentence Transformers 한국어 임베딩

### 3. ML 예측 시스템

- **LSTM 모델**: 월별 발전량 예측
- **경제성 분석**: 20년 투자 수익성 계산
- **PyTorch 기반**: 딥러닝 모델 관리

### 4. 실시간 데이터 통합

- **기상 데이터**: 기상청 API 연동
- **전력 가격**: 전력거래소 SMP, REC 가격 정보
- **API 도구**: 실시간 데이터 수집 및 처리

---

## 🧪 테스트

### 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 테스트 파일
pytest tests/test_agents.py

# 커버리지 포함
pytest --cov=app tests/
```

### 테스트 구조

```
tests/
├── test_agents.py      # Agent 테스트
├── test_tools.py       # Tools 테스트
├── test_rag.py         # RAG 테스트
└── test_ml.py          # ML 테스트
```

---

## 📊 모니터링 및 로깅

### 로깅 설정

- **Loguru**: 구조화된 로깅 시스템
- **성능 모니터링**: API 응답 시간, 메모리 사용량 추적
- **에러 추적**: 시스템 에러율 및 예외 처리

---

## 🔒 보안

### API 보안

- **CORS 설정**: 적절한 크로스 오리진 정책
- **입력 검증**: Pydantic 기반 데이터 검증
- **API 키 관리**: 환경변수를 통한 민감 정보 관리

### 데이터 보안

- **환경변수**: 민감 정보 환경변수 관리
- **데이터 암호화**: 필요시 데이터 암호화 적용
- **접근 권한**: 시스템 접근 권한 제어

---

## 📈 성능 최적화

### 벡터 검색 최적화

- **인덱스 최적화**: Chroma DB 인덱스 튜닝
- **캐싱 전략**: 검색 결과 캐싱
- **배치 처리**: 대량 데이터 처리 최적화

### ML 모델 최적화

- **모델 양자화**: 추론 속도 개선
- **메모리 효율성**: 모델 메모리 사용량 최적화
- **배치 추론**: 대량 예측 처리

---

## 🚀 배포

### 프로덕션 빌드

```bash
# Docker 이미지 빌드
docker build -t renewable-energy-backend:latest .

# 프로덕션 실행
docker run -d -p 8000:8000 renewable-energy-backend:latest
```

### 환경별 설정

- **개발**: `development.env`
- **스테이징**: `staging.env`
- **프로덕션**: `production.env`

---

## 📈 개발 가이드

### 코딩 컨벤션

- **Python**: PEP 8 준수
- **타입 힌트**: 모든 함수에 타입 힌트 사용
- **문서화**: docstring 작성
- **테스트**: 새로운 기능에 대한 테스트 작성

### 새로운 기능 추가

1. **Agent 확장**: 새로운 도구 추가 및 Agent 로직 수정
2. **RAG 개선**: 새로운 데이터 소스 및 임베딩 모델 적용
3. **ML 모델**: 새로운 예측 모델 개발 및 통합
4. **API 엔드포인트**: 새로운 API 엔드포인트 추가

---

## 📞 지원

### 문서

- [프론트엔드 README](../frontend/README.md)
- [전체 프로젝트 README](../README.md)

### 개발 가이드

- LangChain Agent 개발 시 도구 조합 최적화
- RAG 시스템 성능 튜닝 및 데이터 품질 관리
- ML 모델 정확도 향상 및 새로운 예측 기능 추가

---
