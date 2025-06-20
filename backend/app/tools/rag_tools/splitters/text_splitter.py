from typing import List
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.schema import Document
import re

class TextSplitter:
    """문장/단락 단위 + 고정 길이 제한 + 슬라이딩 윈도우 청킹 분할기"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # 기본 텍스트 분할기
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
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
    
    def chunk_text(self, text: str) -> List[str]:
        # 1. 단락 분리
        paragraphs = text.split('\n\n')
        sentences = []
        for para in paragraphs:
            # 2. 문장 분리
            para_sentences = re.split(r'(?<=[.!?])\s+', para.strip())
            sentences.extend([s for s in para_sentences if s])
        # 3. 고정 길이 청크 + 슬라이딩 윈도우
        chunks = []
        chunk = ""
        for sentence in sentences:
            if len(chunk) + len(sentence) + 1 <= self.chunk_size:
                chunk += sentence + " "
            else:
                if chunk:
                    chunks.append(chunk.strip())
                # 슬라이딩 윈도우: 마지막 overlap만큼 잘라서 다음 청크 시작
                if self.chunk_overlap > 0 and len(chunk) > self.chunk_overlap:
                    chunk = chunk[-self.chunk_overlap:] + sentence + " "
                else:
                    chunk = sentence + " "
        if chunk:
            chunks.append(chunk.strip())
        return chunks

    def split_text(self, text: str) -> List[str]:
        return self.chunk_text(text)
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        all_chunks = []
        for doc in documents:
            chunks = self.split_text(doc.page_content)
            for chunk in chunks:
                all_chunks.append(Document(
                    page_content=chunk,
                    metadata=doc.metadata
                ))
        return all_chunks
    
    def split_markdown(self, markdown_text: str) -> List[Document]:
        """마크다운 텍스트를 헤더 기준으로 분할
        
        Args:
            markdown_text: 분할할 마크다운 텍스트
            
        Returns:
            List[Document]: 분할된 마크다운 문서 리스트
        """
        return self.markdown_splitter.split_text(markdown_text) 