from typing import List, Dict, Any
from langchain_community.document_loaders import (
    TextLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredCSVLoader,
    UnstructuredRTFLoader,
    UnstructuredEPubLoader,
    UnstructuredEmailLoader,
    UnstructuredImageLoader,
    UnstructuredURLLoader,
    UnstructuredFileLoader,
    PyPDFLoader
)
from langchain.schema import Document
from app.tools.rag_tools.utils.logger import get_logger
import os
import glob

logger = get_logger(__name__)

class DocumentLoader:
    """문서 로더 클래스"""
    
    def __init__(self):
        """문서 로더 초기화"""
        self.loaders = {
            'txt': TextLoader,
            'json': JSONLoader,
            'md': UnstructuredMarkdownLoader,
            'html': UnstructuredHTMLLoader,
            'doc': UnstructuredWordDocumentLoader,
            'docx': UnstructuredWordDocumentLoader,
            'xls': UnstructuredExcelLoader,
            'xlsx': UnstructuredExcelLoader,
            'ppt': UnstructuredPowerPointLoader,
            'pptx': UnstructuredPowerPointLoader,
            'csv': UnstructuredCSVLoader,
            'rtf': UnstructuredRTFLoader,
            'epub': UnstructuredEPubLoader,
            'eml': UnstructuredEmailLoader,
            'jpg': UnstructuredImageLoader,
            'jpeg': UnstructuredImageLoader,
            'png': UnstructuredImageLoader,
            'pdf': PyPDFLoader,
            'url': UnstructuredURLLoader,
            'default': UnstructuredFileLoader
        }
    
    def load_documents(self, data: List[Dict[str, Any]]) -> List[Document]:
        """문서 로드
        
        Args:
            data: 로드할 문서 데이터 리스트
            
        Returns:
            Document 객체 리스트
        """
        documents = []
        
        for item in data:
            try:
                # 메타데이터 처리
                if 'metadata' in item:
                    # metadata 키가 있는 경우 (vectorstore_builder.py에서 전달하는 형태)
                    metadata = item['metadata']
                else:
                    # 기존 방식 (직접 키로 접근)
                    metadata = {
                        'source': item.get('source', ''),
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'crawl_date': item.get('crawl_date', ''),
                        'category': item.get('category', ''),
                        'tags': ','.join(item.get('tags', [])) if isinstance(item.get('tags', []), list) else str(item.get('tags', '')),
                        'author': item.get('author', ''),
                        'created_at': item.get('created_at', ''),
                        'updated_at': item.get('updated_at', '')
                    }
                
                # 컨텐츠 추출
                content = item.get('content', '')
                if not content:
                    logger.warning(f"컨텐츠가 없는 문서 건너뜀: {metadata}")
                    continue
                
                # Document 객체 생성
                doc = Document(
                    page_content=content,
                    metadata=metadata
                )
                documents.append(doc)
                
            except Exception as e:
                logger.error(f"문서 로드 중 오류 발생: {str(e)}")
                continue
        
        logger.info(f"총 {len(documents)}개 문서 로드 완료")
        return documents

    def load_directory(self, directory_path: str, glob_pattern: str = "*") -> List[Document]:
        """디렉토리에서 파일들을 로드
        
        Args:
            directory_path: 로드할 디렉토리 경로
            glob_pattern: 파일 패턴 (예: "*.txt", "*.pdf")
            
        Returns:
            Document 객체 리스트
        """
        documents = []
        
        if not os.path.exists(directory_path):
            logger.error(f"디렉토리가 존재하지 않습니다: {directory_path}")
            return documents
        
        # 파일 패턴으로 파일들 찾기
        pattern = os.path.join(directory_path, glob_pattern)
        files = glob.glob(pattern)
        
        for file_path in files:
            try:
                if os.path.isfile(file_path):
                    # 파일 확장자 추출
                    file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
                    
                    # 적절한 로더 선택
                    loader_class = self.loaders.get(file_ext, self.loaders['default'])
                    
                    # 로더 인스턴스 생성 및 로드
                    if file_ext == 'json':
                        loader = loader_class(file_path, jq_schema='.', text_content=False)
                    else:
                        loader = loader_class(file_path)
                    
                    file_docs = loader.load()
                    
                    # 메타데이터 추가
                    for doc in file_docs:
                        doc.metadata.update({
                            'source': file_path,
                            'filename': os.path.basename(file_path),
                            'file_type': file_ext
                        })
                    
                    documents.extend(file_docs)
                    
            except Exception as e:
                logger.error(f"파일 로드 중 오류 발생 ({file_path}): {str(e)}")
                continue
        
        logger.info(f"디렉토리에서 총 {len(documents)}개 문서 로드 완료: {directory_path}")
        return documents 