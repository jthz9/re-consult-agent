# 프로젝트 구조 분석 및 최적화 제안

## 🎯 현재 상태 분석

### ✅ 완성된 시스템

- **RAG 시스템**: LangChain 기반 완전 구현
- **크롤링**: KNREC FAQ 데이터 수집
- **Docker 환경**: 컨테이너화 완료
- **CLI 인터페이스**: 기본 RAG QA

### 🚧 구현 예정 시스템

- **Gradio 챗봇**: 웹 인터페이스
- **ML 시스템**: 발전량 예측 모델
- **챗봇 AI 에이전트**: 단일 에이전트 시스템
- **API 도구**: 외부 API 연동

---

## 🏗️ 최적 디렉토리 구조 제안

```
re-consult-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 진입점
│   │
│   ├── core/                      # 핵심 설정 및 유틸리티
│   │   ├── __init__.py
│   │   ├── config.py              # 환경 설정
│   │   ├── logger.py              # 로깅 설정
│   │   ├── exceptions.py          # 커스텀 예외
│   │   └── intent_classifier.py   # 의도 분류기
│   │
│   ├── agents/                    # 에이전트 (신규)
│   │   ├── __init__.py
│   │   └── chatbot_agent.py       # 챗봇 AI 에이전트 (단일)
│   │
│   ├── tools/                     # 도구 모음 (기존 확장)
│   │   ├── __init__.py
│   │   ├── rag_tools/             # RAG 도구 (기존)
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py    # RAG 파이프라인
│   │   │   ├── crawlers/          # 크롤러
│   │   │   ├── embeddings/        # 임베딩
│   │   │   ├── loaders/           # 문서 로더
│   │   │   ├── splitters/         # 텍스트 분할
│   │   │   ├── retrievers/        # 검색기
│   │   │   ├── vectorstores/      # 벡터 스토어
│   │   │   └── utils/             # 유틸리티
│   │   │
│   │   ├── ml_tools/              # ML 도구 (신규)
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py      # 발전량 예측 도구
│   │   │   ├── economics.py       # 경제성 분석 도구
│   │   │   └── data_processor.py  # 데이터 전처리
│   │   │
│   │   └── api_tools/             # API 도구 (신규)
│   │       ├── __init__.py
│   │       ├── weather.py         # 기상청 API
│   │       ├── power.py           # 전력거래소 API
│   │       └── base_api.py        # API 베이스 클래스
│   │
│   ├── ml/                        # ML 시스템 (신규)
│   │   ├── __init__.py
│   │   ├── models/                # 모델 정의
│   │   │   ├── __init__.py
│   │   │   ├── lstm_model.py      # LSTM 발전량 예측
│   │   │   ├── transformer_model.py # Transformer 모델
│   │   │   └── base_model.py      # 베이스 모델 클래스
│   │   │
│   │   ├── training/              # 모델 훈련
│   │   │   ├── __init__.py
│   │   │   ├── trainer.py         # 훈련기
│   │   │   ├── data_loader.py     # 데이터 로더
│   │   │   └── callbacks.py       # 콜백 함수
│   │   │
│   │   ├── inference/             # 모델 추론
│   │   │   ├── __init__.py
│   │   │   ├── predictor.py       # 예측기
│   │   │   ├── model_manager.py   # 모델 관리
│   │   │   └── cache.py           # 추론 결과 캐시
│   │   │
│   │   └── data/                  # ML 데이터 처리
│   │       ├── __init__.py
│   │       ├── preprocessor.py    # 전처리
│   │       ├── feature_engineering.py # 특성 엔지니어링
│   │       └── validation.py      # 데이터 검증
│   │
│   ├── web/                       # 웹 인터페이스 (신규)
│   │   ├── __init__.py
│   │   ├── gradio_app.py          # Gradio 메인 앱
│   │   ├── fastapi_app.py         # FastAPI 앱
│   │   │
│   │   ├── components/            # Gradio 컴포넌트
│   │   │   ├── __init__.py
│   │   │   ├── chat_interface.py  # 채팅 인터페이스
│   │   │   ├── document_viewer.py # 문서 뷰어
│   │   │   ├── settings_panel.py  # 설정 패널
│   │   │   ├── ml_dashboard.py    # ML 대시보드
│   │   │   └── session_manager.py # 세션 관리
│   │   │
│   │   ├── api/                   # FastAPI 엔드포인트
│   │   │   ├── __init__.py
│   │   │   ├── chat.py            # 챗봇 API
│   │   │   ├── ml.py              # ML API
│   │   │   └── health.py          # 헬스체크
│   │   │
│   │   └── utils/                 # 웹 유틸리티
│   │       ├── __init__.py
│   │       ├── agent_wrapper.py   # 에이전트 래퍼
│   │       └── html_templates.py  # HTML 템플릿
│   │
│   └── utils/                     # 공통 유틸리티
│       ├── __init__.py
│       ├── helpers.py             # 헬퍼 함수
│       ├── validators.py          # 데이터 검증
│       └── constants.py           # 상수 정의
│
├── data/                          # 데이터 디렉토리
│   ├── crawled_data/              # 크롤링 데이터 (기존)
│   │   └── knrec_faq_selenium_20250618_110452.json
│   │
│   ├── ml_data/                   # ML 데이터 (신규)
│   │   ├── raw/                   # 원시 데이터
│   │   ├── processed/             # 전처리된 데이터
│   │   ├── features/              # 특성 데이터
│   │   └── splits/                # 훈련/검증/테스트 분할
│   │
│   ├── models/                    # 훈련된 모델 (신규)
│   │   ├── lstm/                  # LSTM 모델
│   │   ├── transformer/           # Transformer 모델
│   │   └── checkpoints/           # 체크포인트
│   │
│   └── vectorstores/              # 벡터 스토어 (기존)
│       └── chroma/
│
├── cli/                           # CLI 인터페이스 (기존)
│   ├── __init__.py
│   ├── rag_qa.py                  # RAG QA CLI
│   ├── ml_cli.py                  # ML CLI (신규)
│   └── chatbot_cli.py             # 챗봇 CLI (신규)
│
├── tests/                         # 테스트 (신규)
│   ├── __init__.py
│   ├── test_rag/                  # RAG 테스트
│   ├── test_ml/                   # ML 테스트
│   ├── test_agents/               # 에이전트 테스트
│   ├── test_web/                  # 웹 테스트
│   └── test_integration/          # 통합 테스트
│
├── docs/                          # 문서 (기존)
│   ├── README.md
│   ├── api_docs.md                # API 문서
│   ├── ml_docs.md                 # ML 문서
│   └── deployment.md              # 배포 가이드
│
├── scripts/                       # 스크립트 (신규)
│   ├── setup.sh                   # 환경 설정
│   ├── train_ml.py                # ML 모델 훈련
│   ├── deploy.sh                  # 배포 스크립트
│   └── backup.sh                  # 백업 스크립트
│
├── docker-compose.yml             # Docker Compose (기존 확장)
├── Dockerfile                     # Dockerfile (기존 확장)
├── requirements.txt               # 의존성 (기존 확장)
└── README.md                      # 프로젝트 README
```

---

## 🚀 개발 우선순위 및 단계별 계획

### Phase 1: 챗봇 AI 에이전트 구현 (1-2주)

**목표**: 단일 챗봇 에이전트 구축

#### 1.1 디렉토리 구조 생성

```bash
mkdir -p app/agents
mkdir -p app/core
mkdir -p app/web/{components,api,utils}
```

#### 1.2 핵심 파일 구현

- `app/agents/chatbot_agent.py` - 챗봇 AI 에이전트
- `app/core/intent_classifier.py` - 의도 분류기
- `app/core/response_integrator.py` - 응답 통합기
- `app/web/gradio_app.py` - Gradio 앱

#### 1.3 Docker 환경 업데이트

- `docker-compose.yml`에 Gradio 서비스 추가
- `requirements.txt`에 Gradio 의존성 추가

### Phase 2: ML 시스템 기반 구축 (2-3주)

**목표**: 발전량 예측 ML 시스템 구축

#### 2.1 ML 디렉토리 구조 완성

```bash
mkdir -p app/ml/{models,training,inference,data}
mkdir -p app/tools/ml_tools
mkdir -p data/ml_data/{raw,processed,features,splits}
mkdir -p data/models/{lstm,transformer,checkpoints}
```

#### 2.2 핵심 ML 컴포넌트 구현

- `app/ml/models/lstm_model.py` - LSTM 모델
- `app/ml/training/trainer.py` - 훈련기
- `app/ml/inference/predictor.py` - 예측기
- `app/tools/ml_tools/prediction.py` - ML 도구

### Phase 3: API 도구 및 고급 기능 (2-3주)

**목표**: 외부 API 연동 및 시스템 통합

#### 3.1 API 도구 구현

- `app/tools/api_tools/weather.py` - 기상청 API
- `app/tools/api_tools/power.py` - 전력거래소 API

#### 3.2 고급 기능 구현

- 병렬 처리 최적화
- 대화 컨텍스트 강화
- 성능 모니터링

### Phase 4: 시스템 통합 및 최적화 (1-2주)

**목표**: 전체 시스템 통합 및 최적화

#### 4.1 통합 테스트

- 모든 컴포넌트 통합 테스트
- 성능 최적화
- 문서화 완성

---

## 🔧 기술 스택 확장 계획

### 현재 스택

- **RAG**: LangChain + ChromaDB
- **크롤링**: Scrapy + Selenium
- **컨테이너**: Docker + Docker Compose

### 추가 예정 스택

- **웹 인터페이스**: Gradio + FastAPI
- **ML**: TensorFlow/Keras + scikit-learn
- **에이전트**: 단일 챗봇 AI 에이전트
- **API**: 기상청 API + 전력거래소 API
- **모니터링**: Prometheus + Grafana

---

## 📋 즉시 실행 가능한 작업

### 1. 챗봇 에이전트 구현 시작

```bash
# 1. 디렉토리 생성
mkdir -p app/agents
mkdir -p app/core
mkdir -p app/web/{components,api,utils}

# 2. requirements.txt 업데이트
echo "gradio>=4.0.0" >> requirements.txt

# 3. 기본 파일 생성
touch app/agents/__init__.py
touch app/agents/chatbot_agent.py
touch app/core/__init__.py
touch app/core/intent_classifier.py
touch app/core/response_integrator.py
touch app/web/__init__.py
touch app/web/gradio_app.py
```

### 2. Docker Compose 업데이트

```yaml
# docker-compose.yml에 추가
services:
  gradio:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./app:/app/app
      - ./data:/app/data
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    command: python app/web/gradio_app.py
    depends_on:
      - chroma
```

### 3. 기본 챗봇 에이전트 구현

```python
# app/agents/chatbot_agent.py
from typing import Dict, Any
from app.tools.rag_tools.rag_pipeline import RAGPipeline
from app.core.intent_classifier import IntentClassifier
from app.core.response_integrator import ResponseIntegrator

class ChatbotAgent:
    """챗봇 AI 에이전트 - 사용자 질문에 따라 적절한 도구 선택"""

    def __init__(self):
        self.rag_tool = RAGPipeline()
        self.intent_classifier = IntentClassifier()
        self.response_integrator = ResponseIntegrator()

    def process_message(self, user_input: str) -> str:
        # 1. 의도 분석
        intent = self.intent_classifier.classify(user_input)

        # 2. 도구 선택 및 실행
        if intent == "policy_info":
            result = self.rag_tool.query(user_input)
        else:
            result = {"answer": "죄송합니다. 아직 해당 기능이 구현되지 않았습니다."}

        # 3. 응답 포맷팅
        return self.response_integrator.format_response(result, intent)
```

### 4. Gradio 앱에서 에이전트 사용

```python
# app/web/gradio_app.py
import gradio as gr
from app.agents.chatbot_agent import ChatbotAgent

def create_chatbot():
    chatbot_agent = ChatbotAgent()

    def chat(message, history):
        response = chatbot_agent.process_message(message)
        return response, history + [[message, response]]

    demo = gr.ChatInterface(
        fn=chat,
        title="재생에너지 AI 가이드",
        description="태양광, 풍력 등 재생에너지에 대한 모든 궁금증을 해결해드립니다"
    )

    return demo

if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

이 구조로 진행하면 단일 챗봇 에이전트가 사용자 질문에 따라 적절한 도구를 선택하고, 결과를 통합하여 포괄적인 상담 서비스를 제공할 수 있습니다.
