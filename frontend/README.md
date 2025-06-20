# 재생에너지 AI 가이드 - 프론트엔드

**Next.js 기반 통합 AI 상담 시스템 프론트엔드**

## 🎯 프로젝트 개요

### 핵심 목표

- **통합 대시보드**: 실시간 시스템 상태 및 발전량 데이터 시각화
- **AI 챗봇 인터페이스**: 직관적인 대화형 상담 시스템
- **데이터 시각화**: 재생에너지 관련 통계 및 예측 결과 표시
- **반응형 웹 디자인**: 모든 디바이스에서 최적화된 사용자 경험

---

## 🏗️ Next.js 기반 시스템 아키텍처

### 컴포넌트 구성

#### 1. **레이아웃 시스템**

- **App Router**: Next.js 15 App Router 기반 페이지 라우팅
- **사이드바 네비게이션**: 6개 주요 기능 영역으로 구성
- **반응형 레이아웃**: 모바일, 태블릿, 데스크톱 최적화

#### 2. **상태 관리 시스템**

- **Custom Hooks**: 기능별 상태 관리 로직 분리
- **API 통신**: TypeScript 기반 타입 안전한 백엔드 연동
- **실시간 업데이트**: 자동 데이터 갱신 및 상태 동기화

#### 3. **컴포넌트 아키텍처**

- **기능별 분리**: Dashboard, Chatbot, Visualization, ML, Policy, Users
- **재사용성**: 공통 UI 컴포넌트 및 유틸리티 함수
- **타입 안전성**: TypeScript 인터페이스 기반 컴포넌트 설계

#### 4. **API 통신 시스템**

- **RESTful API**: 백엔드 FastAPI와의 HTTP 통신
- **에러 처리**: 사용자 친화적 에러 메시지 및 재시도 로직
- **캐싱 전략**: API 응답 캐싱 및 성능 최적화

---

## 🛠️ 기술 스택

### 프론트엔드 프레임워크

- **Next.js 15.3.4**: React 기반 풀스택 프레임워크
- **TypeScript 5**: 정적 타입 검사 및 개발 생산성 향상
- **React 18**: 컴포넌트 기반 UI 라이브러리

### 스타일링 & UI

- **Tailwind CSS 4**: 유틸리티 퍼스트 CSS 프레임워크
- **Lucide React**: 모던 아이콘 라이브러리
- **Recharts**: React 기반 차트 라이브러리 (예정)

### 상태 관리 & 데이터

- **React Hooks**: 함수형 컴포넌트 상태 관리
- **Custom Hooks**: 비즈니스 로직 분리 및 재사용
- **Fetch API**: 네이티브 HTTP 클라이언트

### 개발 도구

- **ESLint**: 코드 품질 관리
- **TypeScript**: 타입 안전성
- **Docker**: 컨테이너화

---

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # 루트 레이아웃
│   │   ├── page.tsx           # 메인 페이지
│   │   ├── globals.css        # 전역 스타일
│   │   └── favicon.ico        # 파비콘
│   ├── components/            # React 컴포넌트
│   │   ├── layout/            # 레이아웃 컴포넌트
│   │   │   └── Sidebar.tsx    # 사이드바 네비게이션
│   │   ├── dashboard/         # 대시보드 관련
│   │   │   └── DashboardContent.tsx
│   │   ├── chatbot/           # AI 챗봇 관련
│   │   │   └── ChatbotContent.tsx
│   │   ├── visualization/     # 데이터 시각화
│   │   │   └── VisualizationContent.tsx
│   │   ├── ml/                # ML 예측 관련
│   │   │   └── MLPredictionContent.tsx
│   │   ├── policy/            # 정책/제도 관련
│   │   │   └── PolicyContent.tsx
│   │   └── users/             # 사용자 관리
│   │       └── UsersContent.tsx
│   ├── services/              # API 서비스
│   │   └── api.ts             # 백엔드 API 클라이언트
│   └── hooks/                 # 커스텀 React 훅
│       ├── useSystemStatus.ts # 시스템 상태 관리
│       └── useChatbot.ts      # 챗봇 상태 관리
├── public/                    # 정적 파일
├── package.json               # 의존성 및 스크립트
├── tsconfig.json              # TypeScript 설정
├── next.config.ts             # Next.js 설정
├── Dockerfile                 # Docker 설정
└── README.md                  # 이 파일
```

---

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd re-consult-agent/frontend

# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env.local
# NEXT_PUBLIC_API_URL 설정 필요
```

### 2. 개발 서버 실행

```bash
# Next.js 개발 서버 시작
npm run dev

# 브라우저에서 확인
http://localhost:3000
```

### 3. Docker 실행

```bash
# Docker 이미지 빌드
docker build -t renewable-energy-frontend .

# 컨테이너 실행
docker run -p 3000:3000 renewable-energy-frontend
```

### 4. 전체 시스템 실행 (Docker Compose)

```bash
# 프로젝트 루트에서
docker-compose up frontend
```

---

## 🎯 주요 기능

### 1. 대시보드 (Dashboard)

- **실시간 시스템 상태**: 백엔드 API와 연동한 실시간 모니터링
- **발전량 데이터 카드**: 태양광, 풍력 발전량 정보 표시
- **최근 활동**: 시스템 활동 로그 및 통계
- **자동 갱신**: 30초 간격 자동 데이터 업데이트

### 2. AI 챗봇 (Chatbot)

- **대화형 인터페이스**: 직관적인 채팅 UI
- **실시간 응답**: 백엔드 LangChain Agent와 연동
- **대화 기록**: 사용자 대화 히스토리 관리
- **상태 표시**: 챗봇 시스템 상태 및 연결 상태

### 3. 발전량 시각화 (Visualization)

- **실시간 차트**: Recharts 기반 발전량 데이터 시각화
- **다양한 차트 타입**: 라인, 바, 파이 차트 지원
- **인터랙티브 요소**: 줌, 필터링, 데이터 포인트 클릭

### 4. ML 예측 (ML Prediction)

- **예측 결과 표시**: 백엔드 ML 모델 결과 시각화
- **성능 지표**: 모델 정확도 및 신뢰도 표시
- **입력 폼**: 예측을 위한 사용자 입력 인터페이스

---

## 🔌 백엔드 연동

### API 엔드포인트

- `GET /health`: 시스템 헬스 체크
- `GET /api/chatbot/status`: 챗봇 상태 확인
- `POST /api/chat`: 챗봇 대화
- `GET /api/rag/search`: RAG 검색
- `GET /api/system/info`: 시스템 정보

### 데이터 흐름

```
사용자 인터랙션 → React 컴포넌트 → Custom Hook → API Service → 백엔드 FastAPI
                                    ↓
                                상태 업데이트 → UI 리렌더링
```

---

## 🎨 UI/UX 설계

### 디자인 시스템

- **색상 팔레트**: 재생에너지 테마 (녹색, 파란색, 주황색)
- **타이포그래피**: 가독성 중심의 폰트 시스템
- **아이콘**: Lucide React 기반 일관된 아이콘 사용
- **간격 시스템**: 8px 기반 그리드 시스템

### 반응형 디자인

- **모바일**: 768px 미만, 단일 컬럼 레이아웃
- **태블릿**: 768px-1024px, 사이드바 + 메인 콘텐츠
- **데스크톱**: 1024px 이상, 전체 레이아웃

### 사용자 경험

- **로딩 상태**: 스피너 및 진행률 표시
- **에러 처리**: 사용자 친화적 에러 메시지
- **접근성**: WCAG 가이드라인 준수
- **키보드 네비게이션**: 접근성 향상

---

## 🧪 테스트

### 테스트 실행

```bash
# 린팅
npm run lint

# 타입 체크
npx tsc --noEmit

# 빌드 테스트
npm run build
```

### 테스트 구조 (예정)

```
tests/
├── unit/           # 단위 테스트
├── integration/    # 통합 테스트
└── e2e/           # 엔드투엔드 테스트
```

---

## 📊 성능 최적화

### 번들 최적화

- **코드 스플리팅**: Next.js 자동 스플리팅
- **지연 로딩**: 동적 import를 통한 컴포넌트 지연 로딩
- **트리 쉐이킹**: 사용하지 않는 코드 제거

### 렌더링 최적화

- **React.memo**: 불필요한 리렌더링 방지
- **useCallback**: 함수 메모이제이션
- **useMemo**: 계산 결과 메모이제이션

### 캐싱 전략

- **API 캐싱**: 동일 요청 결과 캐싱
- **브라우저 캐시**: 정적 자산 캐싱
- **상태 캐싱**: 컴포넌트 상태 유지

---

## 🔒 보안

### 클라이언트 사이드 보안

- **환경변수**: 민감 정보 환경변수 관리
- **입력 검증**: 사용자 입력 XSS 방지
- **HTTPS**: 보안 통신 프로토콜 사용

### API 보안

- **CORS 설정**: 적절한 크로스 오리진 정책
- **API 키 관리**: 백엔드 API 키 보안 관리
- **에러 처리**: 민감 정보 노출 방지

---

## 🚀 배포

### 프로덕션 빌드

```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

### Docker 배포

```bash
# Docker 이미지 빌드
docker build -t renewable-energy-frontend:latest .

# 프로덕션 실행
docker run -d -p 3000:3000 renewable-energy-frontend:latest
```

### 환경별 설정

- **개발**: `development.env`
- **스테이징**: `staging.env`
- **프로덕션**: `production.env`

---

## 📈 개발 가이드

### 코딩 컨벤션

- **TypeScript**: 엄격 모드 사용
- **ESLint**: 코드 품질 규칙 준수
- **컴포넌트 네이밍**: PascalCase 사용
- **파일 구조**: 기능별 디렉토리 구성

### 새로운 기능 추가

1. **컴포넌트 생성**: 기능별 디렉토리에 컴포넌트 추가
2. **API 연동**: services/api.ts에 새로운 엔드포인트 추가
3. **상태 관리**: Custom Hook 생성
4. **라우팅**: 사이드바에 메뉴 추가

### 성능 고려사항

- **번들 크기**: 불필요한 의존성 제거
- **렌더링 최적화**: React.memo, useCallback 활용
- **이미지 최적화**: Next.js Image 컴포넌트 사용
- **코드 스플리팅**: 동적 import 활용

---

## 📞 지원

### 문서

- [백엔드 README](../backend/README.md)
- [전체 프로젝트 README](../README.md)

### 개발 가이드

- 새로운 기능 추가 시 백엔드 API와의 연동 확인
- TypeScript 타입 정의 업데이트
- 컴포넌트 테스트 작성 권장
- 성능 최적화 고려

---
