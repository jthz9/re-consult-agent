#!/usr/bin/env python3
"""
RAG 질문-답변 CLI 도구
한국에너지공단 신재생에너지센터 FAQ 기반 질의응답
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.rag_tools.rag_pipeline import RAGPipeline

# ChatbotAgent CLI 모드 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from app.agents.chatbot_agent import ChatbotAgent

def ask_question(question: str):
    """RAG 시스템에 질문하기"""
    try:
        # RAG 파이프라인 로드
        print("🔧 RAG 파이프라인 로드 중...")
        rag = RAGPipeline()
        
        print(f"❓ 질문: {question}")
        print("🤔 답변 생성 중...")
        
        # 답변 생성
        result = rag.query(question)
        
        # 결과 출력
        print(f"\n📝 답변:\n{result['answer']}")
        
        # 참고 문서 정보
        if result['documents']:
            print(f"\n📚 참고 문서 ({len(result['documents'])}개):")
            for i, doc in enumerate(result['documents'], 1):
                # 메타데이터에서 제목과 출처 추출
                title = doc['metadata'].get('title', 'N/A')
                source = doc['metadata'].get('source', 'N/A')
                article_id = doc['metadata'].get('article_id', 'N/A')
                
                # 제목이 비어있으면 내용에서 추출
                if not title or title == 'N/A':
                    content = doc['content']
                    if '제목:' in content:
                        title = content.split('제목:')[1].split('\n')[0].strip()
                    else:
                        title = content[:50] + "..."
                
                print(f"  {i}. {title}")
                print(f"     출처: {source} (ID: {article_id})")
                print(f"     내용 미리보기: {doc['content'][:100]}...")
                print()
        else:
            print("\n⚠️ 참고 문서가 없습니다!")
        
        return result
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return None

def main():
    """메인 함수"""
    print("🚀 RAG 질문-답변 시스템")
    print("=" * 50)
    
    # 예시 질문들
    example_questions = [
        "탄소검증제는 의무제도인가요?",
        "태양광 설치 비용은 얼마인가요?",
        "REC 제도란 무엇인가요?",
        "ESS 설치가 필수인가요?"
    ]
    
    print("💡 예시 질문:")
    for i, q in enumerate(example_questions, 1):
        print(f"  {i}. {q}")
    
    print("\n" + "=" * 50)
    
    while True:
        try:
            # 사용자 입력
            question = input("\n❓ 질문을 입력하세요 (종료: quit, 예시: example): ").strip()
            
            if question.lower() in ['quit', 'exit', '종료']:
                print("👋 종료합니다.")
                break
            
            if question.lower() == 'example':
                print("\n💡 예시 질문들:")
                for i, q in enumerate(example_questions, 1):
                    print(f"  {i}. {q}")
                continue
            
            if not question:
                print("⚠️ 질문을 입력해주세요.")
                continue
            
            # 질문 처리
            ask_question(question)
            
        except KeyboardInterrupt:
            print("\n\n👋 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류: {str(e)}")

def run_chatbot_cli():
    print("\n재생에너지 AI 챗봇 (종료: exit 입력)\n")
    agent = ChatbotAgent()
    while True:
        user_input = input("[사용자] ")
        if user_input.strip().lower() in ["exit", "quit", "종료"]:
            print("[시스템] 챗봇을 종료합니다.")
            break
        response = agent.process_message(user_input)
        print(f"[챗봇] {response}\n")

if __name__ == "__main__":
    # 기존 코드가 있으면 유지, 없으면 바로 챗봇 CLI 실행
    if len(sys.argv) > 1 and sys.argv[1] == "chatbot":
        run_chatbot_cli()
    else:
        print("[INFO] 'python cli/rag_qa.py chatbot' 으로 챗봇 CLI를 실행할 수 있습니다.") 