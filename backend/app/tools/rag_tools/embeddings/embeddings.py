from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

class EmbeddingModel:
    """임베딩 모델 클래스"""
    
    def __init__(
        self,
        model_name: str = "jhgan/ko-sroberta-multitask",
        model_type: str = "huggingface",
        device: str = "cpu",
        normalize_embeddings: bool = True
    ):
        """임베딩 모델 초기화
        
        Args:
            model_name: 모델 이름
            model_type: 모델 타입 (huggingface 또는 openai)
            device: 실행 디바이스
            normalize_embeddings: 임베딩 정규화 여부
        """
        self.model_name = model_name
        self.model_type = model_type
        self.device = device
        self.normalize_embeddings = normalize_embeddings
        
        if model_type == "huggingface":
            self.model = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': device},
                encode_kwargs={'normalize_embeddings': normalize_embeddings}
            )
        elif model_type == "openai":
            self.model = OpenAIEmbeddings(
                model=model_name,
                openai_api_key=None  # 환경 변수에서 자동 로드
            )
        else:
            raise ValueError(f"지원하지 않는 모델 타입입니다: {model_type}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """문서 리스트를 임베딩
        
        Args:
            texts: 임베딩할 텍스트 리스트
            
        Returns:
            List[List[float]]: 임베딩 벡터 리스트
        """
        return self.model.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """단일 쿼리 텍스트를 임베딩
        
        Args:
            text: 임베딩할 쿼리 텍스트
            
        Returns:
            List[float]: 임베딩 벡터
        """
        return self.model.embed_query(text)
    
    def embed_documents_with_metadata(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """메타데이터가 포함된 문서 리스트를 임베딩
        
        Args:
            documents: 메타데이터가 포함된 문서 리스트
            
        Returns:
            List[Dict[str, Any]]: 임베딩된 문서 리스트
        """
        embedded_docs = []
        for doc in documents:
            content = doc.get('content', '')
            embedding = self.embed_query(content)
            doc['embedding'] = embedding
            embedded_docs.append(doc)
        return embedded_docs 