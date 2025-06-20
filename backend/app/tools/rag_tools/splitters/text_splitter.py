from typing import List
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.schema import Document

class TextSplitter:
    """텍스트 분할기 클래스"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] = None
    ):
        """텍스트 분할기 초기화
        
        Args:
            chunk_size: 청크 크기
            chunk_overlap: 청크 간 중복 크기
            separators: 텍스트 분할 구분자 리스트
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        
        # 기본 텍스트 분할기
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False
        )
        
        # 마크다운 헤더 분할기
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header1"),
                ("##", "header2"),
                ("###", "header3"),
            ]
        )
    
    def split_text(self, text: str) -> List[str]:
        """텍스트를 청크로 분할
        
        Args:
            text: 분할할 텍스트
            
        Returns:
            List[str]: 분할된 텍스트 청크 리스트
        """
        return self.text_splitter.split_text(text)
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """문서 리스트를 청크로 분할
        
        Args:
            documents: 분할할 문서 리스트
            
        Returns:
            List[Document]: 분할된 문서 청크 리스트
        """
        return self.text_splitter.split_documents(documents)
    
    def split_markdown(self, markdown_text: str) -> List[Document]:
        """마크다운 텍스트를 헤더 기준으로 분할
        
        Args:
            markdown_text: 분할할 마크다운 텍스트
            
        Returns:
            List[Document]: 분할된 마크다운 문서 리스트
        """
        return self.markdown_splitter.split_text(markdown_text) 