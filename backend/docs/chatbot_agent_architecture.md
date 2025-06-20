# 챗봇 AI 에이전트 아키텍처

## 🎯 핵심 개념: 챗봇 = AI 에이전트

### 목표

- **챗봇 자체가 하나의 AI 에이전트**
- **사용자 질문 분석 → 적절한 도구 선택 → 결과 통합 → 응답**
- **단일 에이전트가 여러 도구를 지능적으로 활용**

---

## 🏗️ 아키텍처 구조

### 전체 시스템 플로우

```
사용자 질문 → 챗봇 AI 에이전트 → 의도 분석 → 도구 선택 → 도구 실행 → 결과 통합 → 응답
```

### 도구 선택 로직

```
질문 분석 → 의도 분류 → 도구 선택
├── 정책/정보 질문 → RAG 도구
├── 발전량 예측 질문 → ML 도구
├── 복합 질문 → RAG + ML 도구 (병렬)
└── 기타 질문 → 기본 응답
```

---

## 🤖 챗봇 AI 에이전트 구현

### 1. 메인 에이전트 클래스

```python
# app/agents/chatbot_agent.py
from typing import Dict, List, Any, Tuple
from app.tools.rag_tools.rag_pipeline import RAGPipeline
from app.tools.ml_tools.prediction import PredictionTool
from app.tools.api_tools.weather import WeatherTool
from app.core.intent_classifier import IntentClassifier
from app.core.response_integrator import ResponseIntegrator

class ChatbotAgent:
    """챗봇 AI 에이전트 - 사용자 질문에 따라 적절한 도구 선택"""

    def __init__(self):
        # 도구들 초기화
        self.rag_tool = RAGPipeline()
        self.prediction_tool = PredictionTool()
        self.weather_tool = WeatherTool()

        # 분석 도구들
        self.intent_classifier = IntentClassifier()
        self.response_integrator = ResponseIntegrator()

        # 대화 컨텍스트
        self.conversation_history = []

    def process_message(self, user_input: str) -> str:
        """사용자 메시지 처리"""

        # 1. 의도 분석
        intent = self.intent_classifier.classify(user_input)

        # 2. 도구 선택 및 실행
        results = self.execute_tools(user_input, intent)

        # 3. 결과 통합
        final_response = self.response_integrator.integrate(results, intent)

        # 4. 대화 히스토리 업데이트
        self.update_conversation_history(user_input, final_response)

        return final_response

    def execute_tools(self, user_input: str, intent: str) -> Dict[str, Any]:
        """의도에 따라 적절한 도구 실행"""

        results = {}

        if intent == "policy_info":
            # 정책/정보 질문 → RAG 도구
            results["rag"] = self.rag_tool.query(user_input)

        elif intent == "prediction":
            # 발전량 예측 질문 → ML 도구
            parsed_data = self.parse_prediction_request(user_input)
            results["ml"] = self.prediction_tool.predict(
                location=parsed_data["location"],
                capacity=parsed_data["capacity"]
            )

        elif intent == "comprehensive":
            # 복합 질문 → RAG + ML 도구 병렬 실행
            results["rag"] = self.rag_tool.query(user_input)

            parsed_data = self.parse_prediction_request(user_input)
            results["ml"] = self.prediction_tool.predict(
                location=parsed_data["location"],
                capacity=parsed_data["capacity"]
            )

        elif intent == "weather":
            # 기상 정보 질문 → API 도구
            location = self.extract_location(user_input)
            results["weather"] = self.weather_tool.get_weather(location)

        else:
            # 기본 응답
            results["default"] = self.generate_default_response(user_input)

        return results

    def parse_prediction_request(self, user_input: str) -> Dict[str, Any]:
        """발전량 예측 요청 파싱"""
        # 자연어에서 위치와 용량 추출
        # 예: "수원 5kW 설치 시 발전량" → {"location": "수원", "capacity": 5.0}
        return self.extract_prediction_parameters(user_input)

    def update_conversation_history(self, user_input: str, response: str):
        """대화 히스토리 업데이트"""
        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now()
        })
```

### 2. 의도 분류기

```python
# app/core/intent_classifier.py
import re
from typing import Dict, List

class IntentClassifier:
    """사용자 의도 분류"""

    def __init__(self):
        # 의도별 키워드 정의
        self.intent_keywords = {
            "policy_info": [
                "무엇", "뭐", "어떤", "정책", "제도", "방법", "절차",
                "지원금", "보조금", "REC", "RE100", "설치", "비용",
                "신청", "자격", "조건", "혜택"
            ],
            "prediction": [
                "예상", "예측", "얼마나", "몇", "분석", "계산",
                "발전량", "절약", "수익", "투자", "회수", "경제성",
                "월별", "연간", "일별"
            ],
            "weather": [
                "날씨", "기상", "일조량", "햇빛", "태양", "기온",
                "습도", "강수량"
            ],
            "comprehensive": [
                "종합", "전체", "모든", "상세", "자세", "완전",
                "비용과", "발전량과", "정책과"
            ]
        }

    def classify(self, user_input: str) -> str:
        """사용자 입력의 의도 분류"""

        user_input_lower = user_input.lower()

        # 키워드 기반 분류
        intent_scores = {}

        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input_lower)
            intent_scores[intent] = score

        # 복합 의도 감지
        if intent_scores.get("policy_info", 0) > 0 and intent_scores.get("prediction", 0) > 0:
            return "comprehensive"

        # 가장 높은 점수의 의도 반환
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)

        return "policy_info"  # 기본값
```

### 3. 응답 통합기

```python
# app/core/response_integrator.py
from typing import Dict, Any

class ResponseIntegrator:
    """여러 도구의 결과를 통합하여 일관된 응답 생성"""

    def integrate(self, results: Dict[str, Any], intent: str) -> str:
        """결과 통합"""

        if intent == "policy_info":
            return self.format_policy_response(results["rag"])

        elif intent == "prediction":
            return self.format_prediction_response(results["ml"])

        elif intent == "comprehensive":
            return self.format_comprehensive_response(results["rag"], results["ml"])

        elif intent == "weather":
            return self.format_weather_response(results["weather"])

        else:
            return results.get("default", "죄송합니다. 답변을 생성할 수 없습니다.")

    def format_policy_response(self, rag_result: Dict) -> str:
        """정책 정보 응답 포맷"""
        answer = rag_result["answer"]
        documents = rag_result.get("documents", [])

        response = f"{answer}\n\n"

        if documents:
            response += "📋 참고 문서:\n"
            for i, doc in enumerate(documents[:3], 1):
                response += f"{i}. {doc['content'][:100]}...\n"

        return response

    def format_prediction_response(self, ml_result: Dict) -> str:
        """예측 결과 응답 포맷"""
        prediction = ml_result["prediction"]
        confidence = ml_result.get("confidence", 0)

        response = f"📊 발전량 예측 결과:\n\n"
        response += f"• 연간 예상 발전량: {prediction['annual']:,}kWh\n"
        response += f"• 월별 발전량: 여름 {prediction['summer']}kWh, 겨울 {prediction['winter']}kWh\n"
        response += f"• 예측 신뢰도: {confidence:.1%}\n\n"
        response += f"💡 이 예측은 해당 지역의 일조량과 기온 데이터를 기반으로 계산되었습니다."

        return response

    def format_comprehensive_response(self, rag_result: Dict, ml_result: Dict) -> str:
        """종합 응답 포맷"""
        response = "🌱 태양광 설치 종합 상담 결과:\n\n"

        # 정책 정보
        response += "📋 정책/제도 정보:\n"
        response += f"{rag_result['answer']}\n\n"

        # 예측 결과
        prediction = ml_result["prediction"]
        response += "📊 발전량 예측:\n"
        response += f"• 연간 예상 발전량: {prediction['annual']:,}kWh\n"
        response += f"• 월별 발전량: 여름 {prediction['summer']}kWh, 겨울 {prediction['winter']}kWh\n\n"

        # 경제성 분석
        response += "💰 경제성 분석:\n"
        response += f"• 설치비용: {prediction['cost']:,}만원\n"
        response += f"• 20년 총 절약액: {prediction['savings']:,}만원\n"
        response += f"• 투자 회수 기간: {prediction['payback']}년\n\n"

        response += "💡 이 분석은 최신 정책 정보와 지역별 기상 데이터를 종합하여 제공됩니다."

        return response
```

---

## 🔄 실제 작동 시나리오

### 시나리오 1: 정책 질문

```
👤 사용자: "REC가 무엇인가요?"

🤖 챗봇 에이전트:
1. 의도 분석: "policy_info" (정책/정보 질문)
2. 도구 선택: RAG 도구
3. 도구 실행: RAG 파이프라인으로 REC 정보 검색
4. 결과 통합: 정책 정보 응답 포맷
5. 응답: "REC(신재생에너지 공급인증서)는 신재생에너지로 생산된 전력을 인증하는 제도입니다..."

📋 실행 과정:
사용자 → 챗봇 에이전트 → 의도분석 → RAG 도구 → 결과 통합 → 응답
```

### 시나리오 2: 발전량 예측 질문

```
👤 사용자: "수원 5kW 설치 시 월별 발전량은?"

🤖 챗봇 에이전트:
1. 의도 분석: "prediction" (예측 질문)
2. 도구 선택: ML 도구
3. 파라미터 추출: location="수원", capacity=5.0
4. 도구 실행: ML 모델로 발전량 예측
5. 결과 통합: 예측 결과 응답 포맷
6. 응답: "📊 발전량 예측 결과: 연간 6,570kWh, 여름 750kWh, 겨울 400kWh..."

📋 실행 과정:
사용자 → 챗봇 에이전트 → 의도분석 → ML 도구 → 결과 통합 → 응답
```

### 시나리오 3: 종합 상담 질문

```
👤 사용자: "수원 5kW 설치 시 비용과 발전량을 종합적으로 알려주세요"

🤖 챗봇 에이전트:
1. 의도 분석: "comprehensive" (복합 질문)
2. 도구 선택: RAG 도구 + ML 도구 (병렬)
3. 도구 실행:
   - RAG: 설치 비용, 지원금 정보
   - ML: 발전량 예측, 경제성 분석
4. 결과 통합: 종합 응답 포맷
5. 응답: "🌱 태양광 설치 종합 상담 결과: [정책정보 + 예측결과 + 경제성분석]"

📋 실행 과정:
사용자 → 챗봇 에이전트 → 의도분석 → [RAG, ML] 병렬 실행 → 결과 통합 → 응답
```

---

## 🎨 Gradio 통합

### Gradio 앱에서 에이전트 사용

```python
# app/web/gradio_app.py
import gradio as gr
from app.agents.chatbot_agent import ChatbotAgent

def create_chatbot():
    # 챗봇 에이전트 초기화
    chatbot_agent = ChatbotAgent()

    def chat(message, history):
        # 에이전트로 메시지 처리
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

---

## 🚀 시스템 장점

### 1. **단일 에이전트 아키텍처**

- 챗봇 자체가 하나의 지능적 에이전트
- 사용자에게 일관된 경험 제공
- 대화 컨텍스트 유지

### 2. **지능적 도구 선택**

- 질문 의도에 따른 자동 도구 선택
- 복합 질문 시 여러 도구 병렬 실행
- 결과 통합으로 포괄적 답변

### 3. **확장 가능성**

- 새로운 도구 쉽게 추가 가능
- 새로운 의도 분류 추가 용이
- 모듈화된 구조로 유지보수 용이

### 4. **사용자 친화적**

- 자연어 질문으로 모든 기능 접근
- 복잡한 기술적 세부사항 숨김
- 직관적인 상담 경험

---

이 구조로 구현하면 챗봇이 하나의 지능적 AI 에이전트로서 사용자 질문에 따라 적절한 도구를 선택하고, 결과를 통합하여 포괄적인 상담 서비스를 제공할 수 있습니다.

---

## 🧠 ReAct 에이전트 고도화

### ReAct 패턴이란?

**ReAct (Reasoning + Acting)**는 AI 에이전트가 복잡한 문제를 해결할 때 사고(Reasoning)와 행동(Acting)을 반복하는 패턴입니다.

```
사고(Reasoning) → 행동(Acting) → 관찰(Observation) → 사고(Reasoning) → ...
```

### 기존 에이전트 vs ReAct 에이전트

#### **기존 단순 에이전트**

```
질문 → 의도분석 → 도구선택 → 실행 → 응답
```

#### **ReAct 에이전트**

```
질문 → 사고 → 행동 → 관찰 → 사고 → 행동 → 관찰 → ... → 최종응답
```

### ReAct 에이전트 아키텍처

```python
# app/agents/react_agent.py
from typing import Dict, List, Any, Tuple
from app.agents.react_modules.reasoning import ReasoningModule
from app.agents.react_modules.action import ActionModule
from app.agents.react_modules.observation import ObservationModule

class ReActAgent:
    """ReAct 패턴 기반 고급 에이전트"""

    def __init__(self):
        # ReAct 모듈들
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        self.observation = ObservationModule()

        # 설정
        self.max_iterations = 5
        self.thought_history = []
        self.conversation_context = {}

    def process_complex_query(self, user_input: str) -> str:
        """복잡한 질문을 ReAct 패턴으로 처리"""

        current_question = user_input
        iteration = 0
        final_answer = None

        while iteration < self.max_iterations:
            # 1. 사고(Reasoning) - 현재 상황 분석 및 다음 행동 계획
            thought = self.reasoning.analyze_and_plan(
                question=current_question,
                history=self.thought_history,
                context=self.conversation_context
            )
            self.thought_history.append(thought)

            # 2. 행동(Action) - 계획된 행동 실행
            action_result = self.action.execute(thought)

            # 3. 관찰(Observation) - 행동 결과 분석
            observation = self.observation.analyze_result(action_result)

            # 4. 다음 단계 결정
            if self.observation.is_complete(observation):
                final_answer = self.generate_final_answer(observation)
                break
            elif self.observation.needs_more_info(observation):
                current_question = self.generate_follow_up_question(observation)
                iteration += 1
            else:
                final_answer = self.generate_final_answer(observation)
                break

        return final_answer or self.generate_fallback_answer()
```

### ReAct 모듈 상세 구현

#### **1. 사고 모듈 (Reasoning)**

```python
# app/agents/react_modules/reasoning.py
class ReasoningModule:
    """사고 과정을 통한 다음 행동 계획"""

    def analyze_and_plan(self, question: str, history: List[str], context: Dict) -> str:
        """현재 상황을 분석하여 다음 행동 계획"""

        prompt = f"""
        현재 질문: {question}
        지금까지의 사고 과정: {history}
        대화 컨텍스트: {context}

        다음 중 하나를 선택하여 답변하세요:

        1. RAG_SEARCH: 정책/제도 정보 검색
           - 사용 시기: 정책, 제도, 절차 관련 질문
           - 예시: "REC 제도가 뭔가요?", "설치 지원금은?"

        2. ML_PREDICT: 발전량 예측 분석
           - 사용 시기: 발전량, 수익, 경제성 예측
           - 예시: "5kW 설치 시 발전량은?", "투자 회수 기간은?"

        3. API_FETCH: 실시간 데이터 조회
           - 사용 시기: 현재 날씨, 전력 가격 등 실시간 정보
           - 예시: "현재 수원 날씨는?", "REC 가격은?"

        4. CALCULATE: 계산 수행
           - 사용 시기: 수익 계산, 비용 비교 등
           - 예시: "20년 총 수익은?", "월별 절약액은?"

        5. FINAL_ANSWER: 최종 답변 생성
           - 사용 시기: 충분한 정보 수집 완료
           - 예시: 모든 필요한 정보를 종합하여 답변

        선택 이유와 함께 답변하세요.
        """

        return self.llm.generate(prompt)
```

#### **2. 행동 모듈 (Action)**

```python
# app/agents/react_modules/action.py
class ActionModule:
    """계획된 행동 실행"""

    def execute(self, thought: str) -> Dict[str, Any]:
        """사고 결과에 따라 도구 실행"""

        action_type = self.parse_action_type(thought)
        parameters = self.extract_parameters(thought)

        try:
            if action_type == "RAG_SEARCH":
                return self.execute_rag_search(parameters)
            elif action_type == "ML_PREDICT":
                return self.execute_ml_prediction(parameters)
            elif action_type == "API_FETCH":
                return self.execute_api_fetch(parameters)
            elif action_type == "CALCULATE":
                return self.execute_calculation(parameters)
            elif action_type == "FINAL_ANSWER":
                return self.generate_final_answer(parameters)
            else:
                return {"type": "unknown", "result": "알 수 없는 행동", "error": True}
        except Exception as e:
            return {"type": action_type, "result": f"실행 오류: {str(e)}", "error": True}

    def execute_rag_search(self, parameters: Dict) -> Dict[str, Any]:
        """RAG 검색 실행"""
        query = parameters.get("query", "")
        result = self.rag_tool.query(query)
        return {
            "type": "rag_search",
            "result": result,
            "success": True
        }

    def execute_ml_prediction(self, parameters: Dict) -> Dict[str, Any]:
        """ML 예측 실행"""
        location = parameters.get("location", "")
        capacity = parameters.get("capacity", 0)
        result = self.ml_tool.predict(location, capacity)
        return {
            "type": "ml_prediction",
            "result": result,
            "success": True
        }
```

#### **3. 관찰 모듈 (Observation)**

```python
# app/agents/react_modules/observation.py
class ObservationModule:
    """행동 결과 분석"""

    def analyze_result(self, action_result: Dict[str, Any]) -> str:
        """행동 결과를 분석하여 다음 단계 결정"""

        result_type = action_result.get("type")
        result_data = action_result.get("result")
        success = action_result.get("success", False)

        if not success:
            return f"실행 실패: {result_data}"

        if result_type == "rag_search":
            return self.analyze_rag_result(result_data)
        elif result_type == "ml_prediction":
            return self.analyze_ml_result(result_data)
        elif result_type == "api_fetch":
            return self.analyze_api_result(result_data)
        elif result_type == "calculate":
            return self.analyze_calculation_result(result_data)
        elif result_type == "final_answer":
            return "최종 답변 생성 완료"
        else:
            return f"결과 분석: {result_data}"

    def is_complete(self, observation: str) -> bool:
        """충분한 정보가 수집되었는지 확인"""
        complete_keywords = ["완료", "충분", "종합", "최종"]
        return any(keyword in observation for keyword in complete_keywords)

    def needs_more_info(self, observation: str) -> bool:
        """추가 정보가 필요한지 확인"""
        more_info_keywords = ["부족", "추가", "더", "상세"]
        return any(keyword in observation for keyword in more_info_keywords)
```

### ReAct 에이전트 사용 시나리오

#### **복잡한 종합 상담 시나리오**

```
👤 사용자: "수원에 5kW 태양광 설치 시 연간 발전량과 REC 수익, 그리고 정책 지원금을 종합적으로 분석해줘"

🤖 ReAct 에이전트 실행 과정:

1️⃣ 사고: "이 질문은 정책 정보, 발전량 예측, 경제성 분석이 모두 필요한 복합 질문이다. 먼저 정책 정보부터 조사해야겠다."
   행동: RAG_SEARCH - 태양광 설치 정책, REC 제도, 지원금 정보 검색
   관찰: "정책 정보 수집 완료. 태양광 설치 지원금 30%, REC 거래 제도 확인"

2️⃣ 사고: "정책 정보를 얻었으니, 이제 수원 지역 5kW 발전량을 예측해야겠다."
   행동: ML_PREDICT - 수원 5kW 발전량 예측
   관찰: "연간 발전량 6,570kWh 예측 완료. 월별 발전량도 계산됨"

3️⃣ 사고: "발전량과 REC 가격으로 수익을 계산하고, 설치 비용과 비교해야겠다."
   행동: CALCULATE - 수익성 분석, 투자 회수 기간 계산
   관찰: "경제성 분석 완료. 20년 총 수익 1,200만원, 투자 회수 7년"

4️⃣ 사고: "모든 필요한 정보를 수집했으니, 사용자에게 종합적인 답변을 제공하겠다."
   행동: FINAL_ANSWER - 종합 분석 결과 제공
   관찰: "최종 답변 생성 완료"

📋 최종 응답:
"🌱 수원 5kW 태양광 설치 종합 분석 결과:

📋 정책/제도 정보:
• 설치 지원금: 설치비용의 30% 지원
• REC 제도: 발전량에 따른 인증서 발급 및 거래 가능

📊 발전량 예측:
• 연간 발전량: 6,570kWh
• 월별 발전량: 여름 750kWh, 겨울 400kWh

💰 경제성 분석:
• 설치비용: 1,500만원 (지원금 적용 후 1,050만원)
• 20년 총 수익: 1,200만원 (전기료 절약 + REC 수익)
• 투자 회수 기간: 7년

💡 결론: 경제적으로 유리한 투자이며, 정책 지원도 충분합니다."
```

### ReAct vs 단순 에이전트 비교

| 구분          | 단순 에이전트 | ReAct 에이전트 |
| ------------- | ------------- | -------------- |
| **복잡도**    | 낮음          | 높음           |
| **처리 방식** | 1회 실행      | 반복 실행      |
| **사고 과정** | 숨겨짐        | 명시적         |
| **적용 시기** | 단순 질문     | 복잡한 질문    |
| **성능**      | 빠름          | 상대적 느림    |
| **정확도**    | 기본적        | 높음           |

### ReAct 에이전트 도입 전략

#### **1. 단계적 도입**

- Phase 1-5: 기본 챗봇 에이전트 구현
- Phase 6: ReAct 에이전트 고도화

#### **2. 질문 복잡도에 따른 선택**

```python
def select_agent(user_input: str) -> str:
    complexity = analyze_complexity(user_input)

    if complexity == "simple":
        return "simple_agent"
    elif complexity == "complex":
        return "react_agent"
    else:
        return "simple_agent"  # 기본값
```

#### **3. 하이브리드 접근**

- 단순 질문: 기존 에이전트
- 복잡한 질문: ReAct 에이전트
- 사용자 선택 옵션 제공

이렇게 ReAct 패턴을 도입하면 복잡한 재생에너지 상담 질문에 대해 더 정확하고 포괄적인 답변을 제공할 수 있습니다.
