"""
응답 통합기 (Response Integrator)
여러 도구의 결과를 통합하여 일관된 사용자 응답을 생성
"""
from typing import Dict, Any

class ResponseIntegrator:
    """여러 도구의 결과를 통합하여 일관된 응답 생성"""

    def format_policy_response(self, rag_result: Dict) -> str:
        """정책 정보 응답 포맷 (참고문서는 url만, 친근한 말투)"""
        answer = rag_result.get("answer", "정책 정보를 찾을 수 없어요.")
        documents = rag_result.get("documents", [])

        response = f"{answer}\n\n"
        # 참고문서 url만 제공, 없으면 생략
        urls = [doc.get("metadata", {}).get("url", "") for doc in documents if doc.get("metadata", {}).get("url", "")]
        if urls:
            response += "참고할 만한 자료 링크예요:\n"
            for i, url in enumerate(urls[:3], 1):
                response += f"{i}. {url}\n"
        return response

    def format_prediction_response(self, ml_result: Dict) -> str:
        """예측 결과 응답 포맷"""
        prediction = ml_result.get("prediction", {})
        confidence = ml_result.get("confidence", 0)

        response = "📊 발전량 예측 결과:\n\n"
        response += f"• 연간 예상 발전량: {prediction.get('annual', '?'):,}kWh\n"
        response += f"• 월별 발전량: 여름 {prediction.get('summer', '?')}kWh, 겨울 {prediction.get('winter', '?')}kWh\n"
        response += f"• 예측 신뢰도: {confidence:.1%}\n\n"
        response += "💡 이 예측은 해당 지역의 일조량과 기온 데이터를 기반으로 계산되었습니다."
        return response

    def format_comprehensive_response(self, rag_result: Dict, ml_result: Dict) -> str:
        """종합 응답 포맷"""
        response = "🌱 태양광 설치 종합 상담 결과:\n\n"
        # 정책 정보
        response += "📋 정책/제도 정보:\n"
        response += f"{rag_result.get('answer', '정책 정보를 찾을 수 없습니다.')}\n\n"
        # 예측 결과
        prediction = ml_result.get("prediction", {})
        response += "📊 발전량 예측:\n"
        response += f"• 연간 예상 발전량: {prediction.get('annual', '?'):,}kWh\n"
        response += f"• 월별 발전량: 여름 {prediction.get('summer', '?')}kWh, 겨울 {prediction.get('winter', '?')}kWh\n\n"
        # 경제성 분석
        response += "💰 경제성 분석:\n"
        response += f"• 설치비용: {prediction.get('cost', '?'):,}만원\n"
        response += f"• 20년 총 절약액: {prediction.get('savings', '?'):,}만원\n"
        response += f"• 투자 회수 기간: {prediction.get('payback', '?')}년\n\n"
        response += "💡 이 분석은 최신 정책 정보와 지역별 기상 데이터를 종합하여 제공됩니다."
        return response

    def format_error_response(self, error_msg: str) -> str:
        """에러 응답 포맷"""
        return f"❗ 오류: {error_msg}"

    def integrate(self, results: Dict[str, Any], intent: str) -> str:
        """의도에 따라 결과를 통합하여 최종 응답 생성"""
        if intent == "policy_info":
            return self.format_policy_response(results.get("rag", {}))
        elif intent == "prediction":
            return self.format_prediction_response(results.get("ml", {}))
        elif intent == "comprehensive":
            return self.format_comprehensive_response(results.get("rag", {}), results.get("ml", {}))
        elif intent == "weather":
            api_result = results.get("api", {})
            return f"{api_result.get('location', '')} 현재 날씨: {api_result.get('description', '')}, 온도: {api_result.get('temperature', '?')}°C, 습도: {api_result.get('humidity', '?')}%, 일사량: {api_result.get('solar_radiation', '?')}W/m²"
        else:
            return results.get("default", "죄송합니다. 답변을 생성할 수 없습니다.")

# 테스트 함수
def test_response_integrator():
    integrator = ResponseIntegrator()
    rag_result = {
        "answer": "REC(신재생에너지 공급인증서)는 신재생에너지로 생산된 전력을 인증하는 제도입니다.",
        "documents": [
            {"content": "REC는 Renewable Energy Certificate의 약자입니다."},
            {"content": "신재생에너지 공급인증서 제도는..."}
        ]
    }
    ml_result = {
        "prediction": {
            "annual": 6570,
            "summer": 750,
            "winter": 400,
            "cost": 1500,
            "savings": 1200,
            "payback": 7
        },
        "confidence": 0.92
    }
    print("[정책 정보 응답 예시]\n" + integrator.format_policy_response(rag_result) + "\n")
    print("[예측 결과 응답 예시]\n" + integrator.format_prediction_response(ml_result) + "\n")
    print("[종합 응답 예시]\n" + integrator.format_comprehensive_response(rag_result, ml_result) + "\n")
    print("[에러 응답 예시]\n" + integrator.format_error_response("데이터를 찾을 수 없습니다.") + "\n")

if __name__ == "__main__":
    test_response_integrator() 