from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.tools.rag_tools.embeddings.embeddings import EmbeddingModel
import os

class VectorStore:
    """RAG 시스템용 벡터 저장소 클래스 (Chroma 기반)"""
    
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        persist_directory: str = "./data/vectorstores",
        collection_name: str = "faq"
    ):
        """벡터 저장소 초기화
        
        Args:
            embedding_model: 임베딩 모델
            persist_directory: 저장 디렉토리
            collection_name: 컬렉션 이름
        """
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.vector_store = None
    
    def create_from_documents(
        self,
        documents: List[Document],
        persist: bool = True
    ) -> None:
        """문서 리스트로부터 벡터 저장소 생성
        
        Args:
            documents: 문서 리스트
            persist: 저장 여부
        """
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model.model,
            persist_directory=self.persist_directory if persist else None,
            collection_name=self.collection_name
        )
    
    def create_from_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        persist: bool = True
    ) -> None:
        """텍스트 리스트로부터 벡터 저장소 생성
        
        Args:
            texts: 텍스트 리스트
            metadatas: 메타데이터 리스트
            persist: 저장 여부
        """
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_model.model,
            metadatas=metadatas,
            persist_directory=self.persist_directory if persist else None,
            collection_name=self.collection_name
        )
    
    def load(self) -> None:
        """저장된 벡터 저장소 로드"""
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model.model,
            collection_name=self.collection_name
        )
    
    def add_documents(
        self,
        documents: List[Document],
        persist: bool = True
    ) -> None:
        """문서 추가
        
        Args:
            documents: 추가할 문서 리스트
            persist: 저장 여부
        """
        if self.vector_store is None:
            self.create_from_documents(documents, persist)
        else:
            self.vector_store.add_documents(documents)
            if persist:
                self.vector_store.persist()
    
    def similarity_search(
        self,
        query: str,
        k: int = 3,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """유사도 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 수
            filter: 필터 조건
            
        Returns:
            List[Document]: 검색된 문서 리스트
        """
        if self.vector_store is None:
            raise ValueError("벡터 저장소가 초기화되지 않았습니다.")
            
        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter
        )
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """유사도 점수가 포함된 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 수
            filter: 필터 조건
            
        Returns:
            List[tuple[Document, float]]: (문서, 점수) 튜플 리스트
        """
        if self.vector_store is None:
            raise ValueError("벡터 저장소가 초기화되지 않았습니다.")
            
        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter
        )
    
    def delete_collection(self) -> None:
        """컬렉션 삭제"""
        if self.vector_store is not None:
            self.vector_store.delete_collection()
            self.vector_store = None 