from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.retrievers import (
    ContextualCompressionRetriever,
    MultiQueryRetriever
)
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from ..vectorstores.vector_store import VectorStore

class Retriever:
    """검색기 클래스 (Chroma 기반)"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        llm: Optional[ChatOpenAI] = None,
        search_type: str = "similarity",
        search_kwargs: Optional[Dict[str, Any]] = None
    ):
        """검색기 초기화
        
        Args:
            vector_store: 벡터 저장소 (Chroma 기반)
            llm: LLM 모델 (컨텍스트 압축에 사용)
            search_type: 검색 타입
            search_kwargs: 검색 파라미터
        """
        self.vector_store = vector_store
        self.llm = llm
        self.search_type = search_type
        self.search_kwargs = search_kwargs or {"k": 3}
        
        # 기본 검색기
        self.base_retriever = vector_store.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        
        # 컨텍스트 압축 검색기 (LLM이 제공된 경우)
        if llm is not None:
            compressor = LLMChainExtractor.from_llm(llm)
            self.retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=self.base_retriever
            )
        else:
            self.retriever = self.base_retriever
    
    def get_relevant_documents(
        self,
        query: str,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """관련 문서 검색
        
        Args:
            query: 검색 쿼리
            filter: 필터 조건
            
        Returns:
            List[Document]: 검색된 문서 리스트
        """
        if filter is not None:
            self.search_kwargs["filter"] = filter
            
        return self.retriever.get_relevant_documents(query)
    
    def get_relevant_documents_with_scores(
        self,
        query: str,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """점수가 포함된 관련 문서 검색
        
        Args:
            query: 검색 쿼리
            filter: 필터 조건
            
        Returns:
            List[tuple[Document, float]]: (문서, 점수) 튜플 리스트
        """
        if filter is not None:
            self.search_kwargs["filter"] = filter
            
        return self.vector_store.similarity_search_with_score(
            query=query,
            **self.search_kwargs
        )
    
    def create_multi_query_retriever(
        self,
        prompt_template: str,
        num_queries: int = 3
    ) -> None:
        """다중 쿼리 검색기 생성
        
        Args:
            prompt_template: 쿼리 생성 프롬프트 템플릿
            num_queries: 생성할 쿼리 수
        """
        if self.llm is None:
            raise ValueError("LLM이 초기화되지 않았습니다.")
            
        self.retriever = MultiQueryRetriever.from_llm(
            retriever=self.base_retriever,
            llm=self.llm,
            prompt_template=prompt_template,
            num_queries=num_queries
        ) 