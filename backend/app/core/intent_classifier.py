"""
의도 분류기 (Intent Classifier)
사용자 질문의 의도를 분석하여 적절한 도구 선택을 위한 분류
"""

import re
from typing import Dict, List, Tuple


class IntentClassifier:
    """사용자 의도 분류"""

    def __init__(self):
        # 의도별 키워드 정의
        self.intent_keywords = {
            "policy_info": [
                "무엇", "뭐", "어떤", "정책", "제도", "방법", "절차",
                "지원금", "보조금", "REC", "RE100", "설치", "비용",
                "신청", "자격", "조건", "혜택", "제도", "규정", "법령",
                "인증", "승인", "허가", "등록", "신고", "절차", "서류",
                "금융지원", "금융", "지원", "사업", "프로그램", "검증",
                "탄소검증", "탄소", "인증서", "인증", "제도"
            ],
            "prediction": [
                "예상", "예측", "얼마나", "몇", "분석", "계산",
                "발전량", "절약", "수익", "투자", "회수", "경제성",
                "월별", "연간", "일별", "시간별", "계절별",
                "효율", "성능", "생산량", "발전", "생산"
            ],
            "weather": [
                "날씨", "기상", "일조량", "햇빛", "태양", "기온",
                "습도", "강수량", "구름", "맑음", "흐림", "비",
                "바람", "풍속", "풍력", "기후", "온도"
            ],
            "comprehensive": [
                "종합", "전체", "모든", "상세", "자세", "완전",
                "비용과", "정책과", "경제성과", "분석과",
                "비교", "대조", "함께", "동시에", "모두"
            ]
        }
        
        # 의도별 가중치 (더 구체적인 키워드에 높은 가중치)
        self.intent_weights = {
            "policy_info": {
                "REC": 3, "지원금": 3, "보조금": 3, "정책": 2, "제도": 2
            },
            "prediction": {
                "발전량": 3, "예측": 3, "경제성": 3, "수익": 2, "투자": 2
            },
            "weather": {
                "일조량": 3, "날씨": 2, "기상": 2, "기온": 2
            },
            "comprehensive": {
                "종합": 3, "전체": 2, "모든": 2, "비교": 2
            }
        }

    def classify(self, user_input: str) -> str:
        """사용자 입력의 의도 분류"""
        
        if not user_input or not user_input.strip():
            return "policy_info"  # 기본값
        
        user_input_lower = user_input.lower()
        
        # 키워드 기반 분류
        intent_scores = self._calculate_intent_scores(user_input_lower)
        
        # 복합 의도 감지
        if self._is_comprehensive_intent(intent_scores):
            return "comprehensive"
        
        # 가장 높은 점수의 의도 반환
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return "policy_info"  # 기본값
    
    def _calculate_intent_scores(self, user_input: str) -> Dict[str, float]:
        """의도별 점수 계산"""
        
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = 0.0
            
            # 기본 키워드 매칭
            for keyword in keywords:
                if keyword in user_input:
                    # 가중치 적용
                    weight = self.intent_weights.get(intent, {}).get(keyword, 1)
                    score += weight
            
            # 정규표현식을 사용한 더 정확한 매칭
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, user_input):
                    weight = self.intent_weights.get(intent, {}).get(keyword, 1)
                    score += weight * 0.5  # 정확한 매칭에 추가 점수
            
            if score > 0:
                intent_scores[intent] = score
        
        return intent_scores
    
    def _is_comprehensive_intent(self, intent_scores: Dict[str, float]) -> bool:
        """복합 의도인지 판단"""
        
        # 발전량 키워드가 명시적으로 있는 경우는 prediction 우선
        if intent_scores.get("prediction", 0) > 2:  # 발전량 키워드의 가중치가 높음
            return False
        
        # 정책 정보와 예측 의도가 모두 있는 경우
        policy_score = intent_scores.get("policy_info", 0)
        prediction_score = intent_scores.get("prediction", 0)
        
        if policy_score > 0 and prediction_score > 0:
            return True
        
        # 종합 키워드가 명시적으로 있는 경우
        comprehensive_score = intent_scores.get("comprehensive", 0)
        if comprehensive_score > 1:  # 가중치를 고려한 임계값
            return True
        
        return False
    
    def get_intent_confidence(self, user_input: str) -> Tuple[str, float]:
        """의도 분류와 신뢰도 반환"""
        
        user_input_lower = user_input.lower()
        intent_scores = self._calculate_intent_scores(user_input_lower)
        
        if not intent_scores:
            return "policy_info", 0.0
        
        # 복합 의도 감지
        if self._is_comprehensive_intent(intent_scores):
            return "comprehensive", 0.9
        
        # 가장 높은 점수의 의도와 신뢰도 계산
        max_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[max_intent]
        
        # 전체 점수 대비 비율로 신뢰도 계산
        total_score = sum(intent_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return max_intent, confidence
    
    def get_intent_description(self, intent: str) -> str:
        """의도에 대한 설명 반환"""
        
        descriptions = {
            "policy_info": "정책/제도 정보 질문",
            "prediction": "발전량/경제성 예측 질문", 
            "weather": "기상 정보 질문",
            "comprehensive": "종합 분석 질문"
        }
        
        return descriptions.get(intent, "알 수 없는 의도")


# 테스트 함수
def test_intent_classifier():
    """의도 분류기 테스트"""
    
    classifier = IntentClassifier()
    
    test_cases = [
        ("REC가 무엇인가요?", "policy_info"),
        ("수원 5kW 설치 시 발전량은?", "prediction"),
        ("현재 날씨는 어떤가요?", "weather"),
        ("비용과 발전량을 종합적으로 알려주세요", "comprehensive"),
        ("태양광 설치 지원금은?", "policy_info"),
        ("투자 회수 기간은 얼마나 되나요?", "prediction"),
        ("일조량이 많은 지역은?", "weather"),
        ("정책과 경제성을 모두 분석해주세요", "comprehensive"),
    ]
    
    print("=== 의도 분류기 테스트 ===\n")
    
    for user_input, expected_intent in test_cases:
        intent, confidence = classifier.get_intent_confidence(user_input)
        description = classifier.get_intent_description(intent)
        
        status = "✅" if intent == expected_intent else "❌"
        
        print(f"{status} 입력: {user_input}")
        print(f"   예상: {expected_intent} | 실제: {intent} | 신뢰도: {confidence:.2f}")
        print(f"   설명: {description}")
        print()


if __name__ == "__main__":
    test_intent_classifier() 