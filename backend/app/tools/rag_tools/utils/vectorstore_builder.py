#!/usr/bin/env python3
"""
벡터스토어 생성 유틸리티
FAQ 데이터를 로드하여 벡터스토어를 생성하는 도구 (Chroma 기반)
"""

import json
import os
from typing import List, Dict, Any
from ..rag_pipeline import RAGPipeline

def create_faq_vectorstore(data_path: str = None, embedding_type: str = None):
    """FAQ 벡터스토어 생성 (Chroma 기반)
    
    Args:
        data_path: FAQ 데이터 파일 경로 (기본값: 자동 탐지)
        embedding_type: 임베딩 유형 (기본값: None)
    """
    if data_path is None:
        # 자동으로 최신 FAQ 데이터 파일 찾기
        crawled_data_dir = "./data/crawled_data"
        if not os.path.exists(crawled_data_dir):
            raise FileNotFoundError(f"크롤링 데이터 디렉토리를 찾을 수 없습니다: {crawled_data_dir}")
        
        faq_files = [f for f in os.listdir(crawled_data_dir) if f.startswith('knrec_faq') and f.endswith('.json')]
        if not faq_files:
            raise FileNotFoundError("FAQ 데이터 파일을 찾을 수 없습니다.")
        
        # 가장 최신 파일 선택
        faq_files.sort(reverse=True)
        data_path = os.path.join(crawled_data_dir, faq_files[0])
    
    print("🔧 RAG 파이프라인 초기화...")
    rag = RAGPipeline(embedding_type=embedding_type)
    
    print(f"📖 FAQ 데이터 로드 중: {data_path}")
    
    # 크롤링된 FAQ 데이터 로드
    with open(data_path, 'r', encoding='utf-8') as f:
        faq_data = json.load(f)
    
    print(f"📊 총 {len(faq_data)}개의 FAQ 데이터 로드됨")
    
    # FAQ 데이터를 문서 형태로 변환
    documents = []
    for i, faq in enumerate(faq_data):
        doc = {
            'content': f"제목: {faq.get('title', '')}\n내용: {faq.get('content', '')}",
            'metadata': {
                'title': faq.get('title', '')[:100],
                'source': 'knrec_faq',
                'article_id': faq.get('article_id', ''),
                'content': faq.get('content', ''),
                'url': faq.get('url', '')
            }
        }
        documents.append(doc)
    
    print("💾 벡터스토어에 저장 중...")
    
    # 문서 로드 및 벡터스토어에 저장
    rag.load_documents(documents)
    
    print("✅ FAQ 벡터스토어 생성 완료!")
    
    return rag

def rebuild_vectorstore():
    """Chroma 벡터스토어 재구축 (OpenAI, HuggingFace 모두)"""
    print("🔄 Chroma 벡터스토어 재구축 시작...")
    
    # 기존 벡터스토어 삭제
    openai_path = "./data/vectorstores/openai"
    huggingface_path = "./data/vectorstores/huggingface"
    for vectorstore_path in [openai_path, huggingface_path]:
        if os.path.exists(vectorstore_path):
            import shutil
            shutil.rmtree(vectorstore_path)
            print(f"🗑️ 기존 {vectorstore_path} 벡터스토어 삭제 완료")
    
    # OpenAI 임베딩용 벡터스토어 생성
    print("\n[OpenAI 임베딩] 벡터스토어 생성...")
    rag_openai = create_faq_vectorstore(embedding_type='openai')
    print("✅ OpenAI 임베딩 벡터스토어 생성 완료!")
    
    # HuggingFace 임베딩용 벡터스토어 생성
    print("\n[HuggingFace 임베딩] 벡터스토어 생성...")
    rag_hf = create_faq_vectorstore(embedding_type='huggingface')
    print("✅ HuggingFace 임베딩 벡터스토어 생성 완료!")
    
    print("\n🧪 테스트 검색 (OpenAI 임베딩)...")
    test_query = "탄소검증제"
    docs = rag_openai.get_relevant_documents(test_query, k=3)
    print(f"[OpenAI] '{test_query}' 검색 결과: {len(docs)}개 문서")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.metadata.get('title', 'N/A')}")
        print(f"     내용: {doc.page_content[:100]}...")
    print("\n🧪 테스트 검색 (HuggingFace 임베딩)...")
    docs = rag_hf.get_relevant_documents(test_query, k=3)
    print(f"[HuggingFace] '{test_query}' 검색 결과: {len(docs)}개 문서")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.metadata.get('title', 'N/A')}")
        print(f"     내용: {doc.page_content[:100]}...")
    print("\n✅ Chroma 벡터스토어 재구축 완료!")

if __name__ == "__main__":
    rebuild_vectorstore() 