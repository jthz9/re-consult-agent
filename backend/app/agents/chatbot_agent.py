"""
챗봇 AI 에이전트
사용자 질문에 따라 적절한 도구 선택 및 결과 통합
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import HumanMessage, AIMessage
import re

# 상위 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from app.core.intent_classifier import IntentClassifier
from app.core.response_integrator import ResponseIntegrator
from app.tools.rag_tools.rag_pipeline import RAGPipeline


class ChatbotAgent:
    """챗봇 AI 에이전트 - LangChain 메모리 적용"""

    def __init__(self):
        # 분석 도구들
        self.intent_classifier = IntentClassifier()
        self.response_integrator = ResponseIntegrator()
        self.rag_tool = RAGPipeline()
        self.ml_tool = MockMLTool()
        self.api_tool = MockAPITool()

        # LangChain 메모리 적용 (최근 10턴)
        self.memory = ConversationBufferWindowMemory(k=10, memory_key="chat_history", return_messages=True)

    def process_message(self, user_input: str) -> str:
        """사용자 메시지 처리 (LangChain 메모리 기반, 멀티턴 프롬프트 지원, 지시어 치환 고도화)"""
        try:
            self.memory.chat_memory.add_user_message(user_input)
            history_msgs = self.memory.chat_memory.messages[-10:-1]
            history_str = ""
            for msg in history_msgs:
                if isinstance(msg, HumanMessage):
                    history_str += f"사용자: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    history_str += f"챗봇: {msg.content}\n"
            intent, confidence = self.intent_classifier.get_intent_confidence(user_input)
            if intent == "followup":
                prev_msgs = self.memory.chat_memory.messages[-3:-1]  # 직전 질문/답변
                prev_context = ""
                prev_question = ""
                for msg in prev_msgs:
                    if isinstance(msg, HumanMessage):
                        prev_context += f"이전 질문: {msg.content}\n"
                        prev_question = msg.content
                    elif isinstance(msg, AIMessage):
                        prev_context += f"이전 답변: {msg.content}\n"
                # 1. 직전 질문에서 핵심 명사(가장 긴 단어)를 추출 (간단 버전)
                words = re.findall(r'[가-힣A-Za-z0-9]+', prev_question)
                keyword = max(words, key=len) if words else "이 제도"
                # 2. 후속질문 내 모든 지시어(조사 포함)를 keyword로 치환
                # ex: '이 제도의', '그런 경우에는', '이것은', '그 정책은' 등
                anaphora_pattern = r'(이|그|저)(런|것|제도|정책|내용|부분|경우)?(은|는|이|가|을|를|의)?'
                replaced_question = re.sub(anaphora_pattern, keyword, user_input)
                rag_input = f"{prev_context}후속 질문: {replaced_question}"
                results = self.execute_tools(rag_input, "policy_info", history=history_str)
            else:
                results = self.execute_tools(user_input, intent, history=history_str)
            final_response = self.response_integrator.integrate(results, intent)
            self.memory.chat_memory.add_ai_message(final_response)
            return final_response
        except Exception as e:
            error_msg = f"메시지 처리 중 오류가 발생했습니다: {str(e)}"
            return self.response_integrator.format_error_response(error_msg)

    def execute_tools(self, user_input: str, intent: str, history: str = "") -> Dict[str, Any]:
        """의도에 따라 적절한 도구 실행 (history 전달)"""
        results = {}
        if intent == "policy_info":
            results["rag"] = self.rag_tool.query(user_input, history=history)
        elif intent == "prediction":
            parsed_data = self.parse_prediction_request(user_input)
            results["ml"] = self.ml_tool.predict(
                location=parsed_data["location"],
                capacity=parsed_data["capacity"]
            )
        elif intent == "weather":
            location = self.extract_location(user_input)
            results["api"] = self.api_tool.get_weather(location)
        elif intent == "comprehensive":
            results["rag"] = self.rag_tool.query(user_input, history=history)
            parsed_data = self.parse_prediction_request(user_input)
            results["ml"] = self.ml_tool.predict(
                location=parsed_data["location"],
                capacity=parsed_data["capacity"]
            )
        else:
            results["default"] = self.generate_default_response(user_input)
        return results

    def parse_prediction_request(self, user_input: str) -> Dict[str, Any]:
        """발전량 예측 요청 파싱"""
        # 자연어에서 위치와 용량 추출
        # 예: "수원 5kW 설치 시 발전량" → {"location": "수원", "capacity": 5.0}
        
        # 간단한 파싱 로직 (실제로는 더 정교한 NLP 필요)
        location = "수원"  # 기본값
        capacity = 5.0     # 기본값
        
        # 위치 추출 (간단한 키워드 매칭)
        locations = ["수원", "서울", "부산", "대구", "인천", "광주", "대전", "울산"]
        for loc in locations:
            if loc in user_input:
                location = loc
                break
        
        # 용량 추출 (숫자 + kW 패턴)
        import re
        capacity_match = re.search(r'(\d+(?:\.\d+)?)\s*kw', user_input.lower())
        if capacity_match:
            capacity = float(capacity_match.group(1))
        
        return {
            "location": location,
            "capacity": capacity
        }

    def extract_location(self, user_input: str) -> str:
        """위치 정보 추출"""
        # 간단한 위치 추출 로직
        locations = ["수원", "서울", "부산", "대구", "인천", "광주", "대전", "울산"]
        for location in locations:
            if location in user_input:
                return location
        return "수원"  # 기본값

    def generate_default_response(self, user_input: str) -> str:
        """기본 응답 생성"""
        return "죄송합니다. 질문을 이해하지 못했습니다. 재생에너지 관련 질문을 해주세요."

    def get_conversation_history(self):
        """LangChain 메모리 기반 대화 히스토리 반환"""
        return self.memory.chat_memory.messages

    def clear_conversation_history(self):
        self.memory.clear()

    def get_embedding_model_info(self) -> Dict[str, str]:
        """현재 사용 중인 임베딩 모델 정보 반환"""
        return self.rag_tool.get_embedding_model_info()

    def get_system_info(self) -> Dict[str, Any]:
        """시스템 정보 반환"""
        return {
            "embedding_model": self.get_embedding_model_info(),
            "conversation_history_count": len(self.memory.chat_memory.messages),
            "max_history": 10
        }


# Mock 도구들 (실제 구현 전까지 사용)
class MockMLTool:
    """Mock ML 도구"""
    
    def predict(self, location: str, capacity: float) -> Dict[str, Any]:
        return {
            "prediction": {
                "annual": int(6570 * capacity / 5.0),
                "summer": int(750 * capacity / 5.0),
                "winter": int(400 * capacity / 5.0),
                "cost": int(1500 * capacity / 5.0),
                "savings": int(1200 * capacity / 5.0),
                "payback": 7
            },
            "confidence": 0.92
        }


class MockAPITool:
    """Mock API 도구"""
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        return {
            "location": location,
            "temperature": 25,
            "humidity": 60,
            "solar_radiation": 800,
            "description": "맑음"
        }


# 테스트 함수
def test_chatbot_agent():
    """챗봇 에이전트 테스트"""
    
    agent = ChatbotAgent()
    
    # 시스템 정보 출력
    system_info = agent.get_system_info()
    print("=== 챗봇 에이전트 시스템 정보 ===")
    print(f"임베딩 모델: {system_info['embedding_model']['type']} - {system_info['embedding_model']['name']}")
    print(f"모델 상태: {system_info['embedding_model']['status']}")
    print(f"대화 히스토리: {system_info['conversation_history_count']}/{system_info['max_history']}")
    print()
    
    test_cases = [
        "REC가 무엇인가요?",
        "수원 5kW 설치 시 발전량은?",
        "비용과 발전량을 종합적으로 알려주세요",
        "현재 수원 날씨는 어떤가요?",
        "태양광 설치 지원금은?"
    ]
    
    print("=== 챗봇 에이전트 테스트 ===\n")
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"테스트 {i}: {user_input}")
        print("-" * 50)
        
        response = agent.process_message(user_input)
        print(f"응답: {response}")
        
        # 대화 히스토리 확인
        history = agent.get_conversation_history()
        last_entry = history[-1] if history else None
        if last_entry:
            print(f"의도: {last_entry['intent']} (신뢰도: {last_entry['confidence']:.2f})")
        
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    test_chatbot_agent() 