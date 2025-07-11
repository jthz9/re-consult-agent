# 재생에너지 AI 가이드 구현 로드맵

## 🏗️ 기술 원칙

- **모든 대화형 AI/에이전트/메모리/도구/체인/워크플로우 관련 기술은 LangChain 표준 컴포넌트를 우선적으로 사용한다.**
- 커스텀 기능도 LangChain의 Chain, Tool, Memory 등 표준 인터페이스로 래핑한다.
- 백엔드 핵심 로직은 LangChain 기반으로만 구성한다.

## 🎯 프로젝트 개요

### 목표

- **챗봇 AI 에이전트**: 사용자 질문에 따라 적절한 도구 선택
- **RAG 시스템**: 정책/제도 정보 제공
- **ML 시스템**: 발전량 예측 및 경제성 분석
- **웹 인터페이스**: Gradio 기반 사용자 친화적 UI

### 핵심 아키텍처

```
사용자 질문 → 챗봇 AI 에이전트 → 의도 분석 → 도구 선택 → 결과 통합 → 응답
```

---

## 📊 구현 진행 상황 (Phase별)

### **Phase 1: 챗봇 AI 에이전트 구현** ✅ **완료**

#### **목표**: 기본 챗봇 에이전트 구축

#### **1.1 RAG 시스템 (100%)** ✅

- [x] LangChain 기반 RAG 파이프라인 구현
- [x] ChromaDB 벡터 스토어 설정
- [x] 한국어 임베딩 모델 (KR-SBERT-V40K) 적용
- [x] OpenAI 임베딩 모델 연동 및 자동 fallback 구현
- [x] 임베딩 모델별 벡터스토어 분리
- [x] KNREC FAQ 데이터 크롤링 (1,802개 항목)
- [x] 문서 로더 및 텍스트 분할기 구현
- [x] 검색 및 답변 생성 기능

#### **1.2 Docker 환경 (100%)** ✅

- [x] Docker Compose 설정
- [x] ChromaDB 서비스 구성
- [x] 크롤러 서비스 구성
- [x] 볼륨 마운트 설정

#### **1.3 CLI 인터페이스 (100%)** ✅

- [x] 기본 RAG QA CLI 구현
- [x] 챗봇 에이전트 CLI 통합 테스트
- [x] 임베딩/시스템 정보 출력 기능

#### **1.4 프로젝트 구조 (100%)** ✅

- [x] 디렉토리 구조 설계 및 리팩토링
- [x] 아키텍처 문서화
- [x] 기술 스택 정의

#### **1.5 챗봇 AI 에이전트 (100%)** ✅

- [x] 의도 분류기 구현 및 테스트
- [x] 응답 통합기 구현 및 테스트
- [x] 챗봇 에이전트 클래스 구현 및 통합 테스트
- [x] 실제 RAG 파이프라인 연동
- [x] 임베딩 모델별 벡터스토어 자동 분기 및 관리

### **Phase 2: Gradio 웹 인터페이스** ✅ **완료**

#### **목표**: 사용자 친화적 웹 인터페이스 구축

#### **2.1 기본 Gradio 앱**

- [x] 메인 Gradio 앱 구조
- [x] 챗봇 에이전트 연동
- [x] 기본 채팅 인터페이스

#### **2.2 고급 컴포넌트**

- [x] 문서 뷰어 (검색 결과 표시)
- [x] 설정 패널 (모델 파라미터 조정)
- [x] 세션 관리 (대화 히스토리)
- [x] 예시 질문 기능

#### **2.3 UI/UX 개선**

- [x] 재생에너지 테마 적용
- [x] 반응형 레이아웃
- [x] 로딩 인디케이터
- [x] 에러 처리 UI

#### **2.4 RAG 시스템 통합 테스트**

- [x] 웹 인터페이스에서 RAG 질의 테스트
- [x] 검색 결과 표시 기능 검증
- [x] 응답 품질 및 속도 테스트
- [x] 사용자 경험 최적화

### **Phase 3: API 도구 구현** 📋 **준비**

#### **목표**: 공공 데이터 API 연동 및 도구 구축

#### **3.1 API 베이스 클래스 구현**

- [ ] API 도구 베이스 클래스 설계 (LangChain Tool 기반)
- [ ] 공통 에러 처리 및 재시도 로직
- [ ] API 키 관리 시스템
- [ ] 요청 제한 및 캐싱 로직

#### **3.2 기상청 API 연동**

- [ ] 기상청 공개 API 연동 (LangChain Tool로 래핑)
- [ ] 일일 기상 데이터 수집
- [ ] 지역별 기상 정보 조회
- [ ] 기상 데이터 전처리

#### **3.3 전력거래소 API 연동**

- [ ] 전력거래소 공개 API 연동 (LangChain Tool로 래핑)
- [ ] 전력 거래량 데이터 수집
- [ ] 전력 가격 정보 조회
- [ ] 전력 데이터 전처리

#### **3.4 API 도구 구현**

- [ ] 기상 데이터 도구 (WeatherTool, LangChain Tool)
- [ ] 전력 데이터 도구 (PowerTool, LangChain Tool)
- [ ] 데이터 조합 도구 (DataCombinationTool, LangChain Tool)
- [ ] 실시간 데이터 조회 도구

#### **3.5 챗봇 에이전트 통합**

- [ ] API 도구를 LangChain Tool로 에이전트에 추가
- [ ] 실시간 데이터 질문 처리 로직
- [ ] API 도구 선택 로직 개선
- [ ] 에러 처리 및 fallback 로직

### **Phase 4: ML 시스템 구축** 📋 **준비**

#### **목표**: 발전량 예측 ML 시스템 구축

#### **4.1 데이터 수집 및 전처리**

- [ ] API 도구를 통한 실시간 데이터 수집
- [ ] 기상 데이터와 전력 데이터 통합
- [ ] 데이터 전처리 파이프라인 구축 (LangChain Tool)
- [ ] 특성 엔지니어링 및 정규화

#### **4.2 ML 모델 구현**

- [ ] LSTM 모델 아키텍처 설계
- [ ] 모델 훈련 파이프라인 구현
- [ ] 하이퍼파라미터 튜닝 시스템
- [ ] 모델 평가 및 검증 시스템

#### **4.3 ML 도구 구현**

- [ ] 발전량 예측 도구 (PredictionTool, LangChain Tool)
- [ ] 경제성 분석 도구 (EconomicsTool, LangChain Tool)
- [ ] 데이터 전처리 도구 (DataProcessor, LangChain Tool)
- [ ] 모델 성능 모니터링 도구

#### **4.4 챗봇 에이전트 통합**

- [ ] ML 도구를 LangChain Tool로 에이전트에 추가
- [ ] 예측 질문 처리 로직 구현
- [ ] 복합 질문 처리 로직 개선
- [ ] ML 결과 시각화 기능

### **Phase 5: 시스템 통합 및 최적화** 📋 **준비**

#### **목표**: 전체 시스템 통합 및 최적화

#### **5.1 통합 테스트**

- [ ] 단위 테스트 완성
- [ ] 통합 테스트 구현
- [ ] 성능 테스트
- [ ] 사용자 시나리오 테스트

#### **5.2 최적화**

- [ ] 응답 속도 최적화
- [ ] 메모리 사용량 최적화
- [ ] 에러 처리 강화
- [ ] 로깅 시스템 개선

#### **5.3 문서화 및 배포**

- [ ] API 문서 완성
- [ ] 사용자 가이드 작성
- [ ] 배포 스크립트 작성
- [ ] 모니터링 설정

### **Phase 6: ReAct 에이전트 고도화** 📋 **준비**

#### **목표**: ReAct 패턴을 적용한 고급 에이전트 시스템 구축

#### **6.1 ReAct 아키텍처 설계**

- [ ] ReAct 패턴 분석 및 설계 (LangChain 기반)
- [ ] 사고(Reasoning) 모듈 구현
- [ ] 행동(Action) 모듈 구현
- [ ] 관찰(Observation) 모듈 구현
- [ ] 반복 루프 구현

#### **6.2 ReAct 에이전트 구현**

- [ ] LangChain ReAct Agent 구조로 구현
- [ ] 복잡한 시나리오 처리
- [ ] 테스트 및 검증

---

## 📋 다음 단계: Phase 2 Gradio 웹 인터페이스 구현

현재 **Phase 1이 완료**되었으므로, **Phase 2: Gradio 웹 인터페이스** 구현을 시작할 준비가 되었습니다.

### **Phase 2 구현 순서:**

1. **기본 Gradio 앱 구조** 생성 (LangChain Chain/Agent와 연동)
2. **챗봇 에이전트 연동**
3. **채팅 인터페이스** 구현
4. **RAG 시스템 통합 테스트**
5. **UI/UX 개선**

---

## 🚦 다음 실무 개발 순서 안내

1. **Gradio 웹 인터페이스 기본 구조 생성**

   - `app/web/gradio_app.py` 파일 생성
   - LangChain Chain/Agent와 연동되는 구조로 설계

2. **챗봇 에이전트와 Gradio 연동**

   - 입력/출력 함수 설계 (멀티턴 대화 지원)
   - LangChain 메모리(ConversationBufferWindowMemory) 적용

3. **채팅 UI 및 기능 구현**

   - 사용자 입력, 챗봇 응답, 대화 히스토리 표시
   - 예시 질문, 문서 뷰어, 설정 패널 등 고급 기능 추가

4. **RAG 시스템 연동 및 통합 테스트**

   - 실제 RAG 파이프라인과 연결하여 검색/답변 품질 검증

5. **UI/UX 개선 및 배포 준비**
   - 반응형 레이아웃, 테마, 에러 처리 등 개선
   - Docker 환경에서 통합 테스트

이 순서대로 진행하면 LangChain 기반의 표준화된 웹 챗봇 시스템을 빠르게 완성할 수 있습니다!

## 🛠️ 기술 스택

### 백엔드

- **Python 3.11**
- **FastAPI** - REST API 프레임워크
- **LangChain** - AI 에이전트 프레임워크
- **ChromaDB** - 벡터 데이터베이스
- **OpenAI** - 임베딩 및 LLM
- **Sentence Transformers** - 한국어 임베딩

### 프론트엔드

- **Gradio** - 웹 인터페이스
- **HTML/CSS/JavaScript** - UI 컴포넌트

### 인프라

- **Docker** - 컨테이너화
- **Docker Compose** - 멀티 컨테이너 관리
- **ChromaDB** - 벡터 저장소

### 개발 도구

- **pytest** - 테스트 프레임워크
- **Git** - 버전 관리
- **VS Code** - 개발 환경

## 📈 성과 지표

### 현재 달성도

- **Phase 1**: 100% 완료 ✅
- **Phase 2**: 100% 완료 ✅
- **전체 진행률**: 40% (2/5 단계 완료)

### 주요 성과

1. **RAG 시스템 완성**: KNREC FAQ 기반 지식 검색
2. **챗봇 에이전트 구현**: 의도 분류 및 도구 선택
3. **웹 인터페이스 구축**: 사용자 친화적 UI/UX
4. **Docker 환경 완성**: 개발-운영 환경 통합

## 🔄 다음 단계

### 즉시 진행 가능한 작업

1. **API 도구 개발 시작**
   - 기상 데이터 API 연동
   - 발전량 예측 API 구현
2. **ML 시스템 설계**
   - 데이터 수집 전략
   - 모델 아키텍처 설계

### 중장기 계획

1. **Phase 3 완료**: API 도구 개발
2. **Phase 4 시작**: ML 시스템 개발
3. **성능 최적화**: 응답 속도 및 정확도 개선

## 📝 참고 사항

### 아키텍처 결정사항

- **단일 챗봇 에이전트**: 복잡한 다중 에이전트 대신 단순하고 효율적인 구조
- **도구 기반 접근**: RAG, ML, API를 도구로 취급하여 모듈화
- **LangChain 메모리**: 대화 기록 관리 및 컨텍스트 유지

### 기술적 고려사항

- **임베딩 모델 분리**: OpenAI와 SBERT 병행 사용
- **벡터 저장소 분리**: 모델별 독립적 저장소 운영
- **Docker 통합**: 개발-운영 환경 일원화

---

**마지막 업데이트**: 2025-06-19
**현재 단계**: Phase 2 완료, Phase 3 준비 중
