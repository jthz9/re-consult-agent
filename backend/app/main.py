"""
재생에너지 AI 가이드 - 메인 애플리케이션
FastAPI 백엔드 API 서버
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# FastAPI 앱 생성
app = FastAPI(
    title="재생에너지 AI 가이드 API",
    description="정책/제도/RAG/예측/실시간 데이터 통합 상담 시스템 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI 라우트
@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "재생에너지 AI 가이드 API 서버",
        "version": "1.0.0",
        "services": {
            "api": "http://localhost:8000",
            "frontend": "http://localhost:3000",
            "chroma": "http://localhost:8001"
        }
    }

@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "services": {
            "fastapi": "running",
            "chroma": "running"
        }
    }

@app.get("/api/chatbot/status")
def chatbot_status():
    """챗봇 상태 확인"""
    try:
        from app.agents.chatbot_agent import ChatbotAgent
        agent = ChatbotAgent()
        system_info = agent.get_system_info()
        return {
            "status": "ready",
            "system_info": system_info
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/api/chat")
def chat_with_bot(message: str):
    """챗봇과 대화하는 API 엔드포인트"""
    try:
        from app.agents.chatbot_agent import ChatbotAgent
        agent = ChatbotAgent()
        response = agent.chat(message)
        return {
            "status": "success",
            "message": message,
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/rag/search")
def rag_search(query: str, k: int = 3):
    """RAG 검색 API 엔드포인트"""
    try:
        from app.tools.rag_tools.rag_pipeline import RAGPipeline
        rag = RAGPipeline()
        result = rag.query(query)
        return {
            "status": "success",
            "query": query,
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/system/info")
def system_info():
    """시스템 정보 API 엔드포인트"""
    try:
        from app.tools.rag_tools.rag_pipeline import RAGPipeline
        rag = RAGPipeline()
        embedding_info = rag.get_embedding_model_info()
        
        return {
            "status": "success",
            "system_info": {
                "embedding_model": embedding_info,
                "vectorstore_path": rag.persist_directory,
                "collection_name": rag.collection_name
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 