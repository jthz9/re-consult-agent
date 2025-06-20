#!/usr/bin/env python3
"""
크롤링된 데이터를 벡터 DB에 로드하는 스크립트
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.rag_tools.rag_pipeline import RAGPipeline

def clean_crawled_data(data):
    # 데이터 생략 없이 원본 데이터 그대로 반환
    return data

def load_crawled_data():
    """크롤링된 데이터를 벡터 DB에 로드"""
    try:
        # 크롤링된 데이터 파일 경로
        data_file = "data/crawled_data/knrec_faq_selenium_20250618_110452.json"
        
        print(f"📂 데이터 파일 로드 중: {data_file}")
        
        # JSON 파일 읽기
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 총 {len(data)}개의 FAQ 데이터를 찾았습니다.")
        
        # 데이터 정리 (... 제거)
        print("🧹 데이터 정리 중...")
        cleaned_data = clean_crawled_data(data)
        print(f"✅ {len(cleaned_data)}개의 정리된 데이터를 생성했습니다.")
        
        # 문서 형식으로 변환
        documents = []
        for item in cleaned_data:
            # 제목과 내용을 결합
            content = f"제목: {item.get('title', '')}\n내용: {item.get('content', '')}"
            
            document = {
                'content': content,
                'metadata': {
                    'title': item.get('title', ''),
                    'source': 'knrec_faq',
                    'article_id': item.get('article_id', ''),
                    'category': item.get('category', '')
                }
            }
            documents.append(document)
        
        print(f"📝 {len(documents)}개의 문서를 벡터 DB에 로드 중...")
        
        # 1. OpenAI 임베딩으로 벡터 DB 생성
        print("\n🔧 OpenAI 임베딩으로 벡터 DB 생성 중...")
        try:
            rag_openai = RAGPipeline(embedding_type="openai")
            rag_openai.load_documents(documents)
            print(f"✅ OpenAI 벡터 DB 생성 완료: {rag_openai.persist_directory}")
        except Exception as e:
            print(f"⚠️ OpenAI 벡터 DB 생성 실패: {str(e)}")
        
        # 2. HuggingFace 임베딩으로 벡터 DB 생성
        print("\n🔧 HuggingFace 임베딩으로 벡터 DB 생성 중...")
        try:
            rag_hf = RAGPipeline(embedding_type="huggingface")
            rag_hf.load_documents(documents)
            print(f"✅ HuggingFace 벡터 DB 생성 완료: {rag_hf.persist_directory}")
        except Exception as e:
            print(f"⚠️ HuggingFace 벡터 DB 생성 실패: {str(e)}")
        
        print("\n🎉 모든 벡터 DB 생성이 완료되었습니다!")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

def test_query():
    """테스트 질문으로 개선사항 확인"""
    try:
        print("\n🧪 개선사항 테스트 중...")
        
        # 테스트 질문
        test_questions = [
            "탄소검증제란?",
            "REC 제도란 무엇인가요?",
            "태양광 설치 비용은 얼마인가요?"
        ]
        
        # 1. OpenAI 임베딩 테스트
        print("\n🔍 OpenAI 임베딩 테스트:")
        try:
            rag_openai = RAGPipeline(embedding_type="openai")
            for question in test_questions:
                print(f"\n❓ 질문: {question}")
                result = rag_openai.query(question)
                print(f"📝 답변: {result['answer'][:200]}...")
        except Exception as e:
            print(f"⚠️ OpenAI 테스트 실패: {str(e)}")
        
        # 2. HuggingFace 임베딩 테스트
        print("\n🔍 HuggingFace 임베딩 테스트:")
        try:
            rag_hf = RAGPipeline(embedding_type="huggingface")
            for question in test_questions:
                print(f"\n❓ 질문: {question}")
                result = rag_hf.query(question)
                print(f"📝 답변: {result['answer'][:200]}...")
        except Exception as e:
            print(f"⚠️ HuggingFace 테스트 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("🚀 크롤링 데이터 로드 및 테스트")
    print("=" * 50)
    
    # 1. 데이터 로드
    if load_crawled_data():
        print("\n" + "=" * 50)
        
        # 2. 테스트 실행
        test_query()
        
        print("\n🎉 모든 작업이 완료되었습니다!")
        print("이제 'python cli/rag_qa.py'로 RAG 시스템을 사용할 수 있습니다.")
    else:
        print("❌ 데이터 로드에 실패했습니다.")

if __name__ == "__main__":
    main() 