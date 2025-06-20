import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.tools.rag_tools.loaders.document_loader import DocumentLoader
from app.tools.rag_tools.splitters.text_splitter import TextSplitter
from app.tools.rag_tools.utils.logger import get_logger

# 환경 변수 로드
load_dotenv()

logger = get_logger(__name__)

class RAGPipeline:
    """RAG(Retrieval-Augmented Generation) 파이프라인"""
    
    def __init__(
        self,
        model_name: str = "gpt-4o",
        primary_embedding_model: str = "text-embedding-3-small",
        backup_embedding_model: str = "snunlp/KR-SBERT-V40K-klueNLI-augSTS",
        persist_directory: str = "./app/tools/rag_tools/vectorstores/data",
        collection_name: str = "knrec_faq",
        embedding_type: str = "auto"  # 추가: 'openai', 'huggingface', 'auto'
    ):
        """RAG 파이프라인 초기화
        
        Args:
            model_name: LLM 모델 이름
            primary_embedding_model: 기본 임베딩 모델 (OpenAI)
            backup_embedding_model: 백업 임베딩 모델 (HuggingFace)
            persist_directory: 벡터 저장소 디렉토리
            collection_name: 컬렉션 이름
            embedding_type: 'openai', 'huggingface', 'auto'
        """
        self.model_name = model_name
        self.primary_embedding_model = primary_embedding_model
        self.backup_embedding_model = backup_embedding_model
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_type = embedding_type
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.5
        )
        
        # 임베딩 모델 초기화 (embedding_type에 따라 강제 지정)
        self.embeddings = self._initialize_embeddings()
        
        # 벡터 저장소 초기화 (Chroma 사용)
        self.vectorstore = self._initialize_vectorstore()
        
        # 문서 로더 초기화
        self.document_loader = DocumentLoader()
        
        # 프롬프트 템플릿 설정
        self.prompt_template = ChatPromptTemplate.from_template("""주어진 컨텍스트를 바탕으로 질문에 답변해주세요. 컨텍스트에 있는 정보만을 사용하여 답변하세요.

[컨텍스트]
{context}

[질문]
{question}

[답변 형식]
1. 핵심 답변: 컨텍스트에 있는 정보를 바탕으로 한 직접적인 답변
2. 상세 설명: 컨텍스트에서 관련된 정보를 인용하여 자세히 설명
3. 참고 사항: 컨텍스트에서 확인된 추가 정보나 주의사항

[주의사항]
- 컨텍스트에 있는 정보만을 사용하여 답변하세요
- 컨텍스트에 없는 정보는 생성하지 마세요
- 컨텍스트의 정보가 부족한 경우, "제공된 컨텍스트에 해당 정보가 없습니다"라고 답변하세요
- 답변은 항상 한국어로 작성하세요
- 컨텍스트의 정보를 왜곡하거나 과장하지 마세요

답변:""")
        
        # RAG 체인 설정
        self.chain = (
            {"context": self.vectorstore.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        
        # 텍스트 분할기 초기화
        self.text_splitter = TextSplitter()
    
    def _initialize_embeddings(self):
        """임베딩 모델 초기화 (embedding_type에 따라 강제 지정)"""
        base_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "vectorstores")
        if self.embedding_type == "openai":
            logger.info("OpenAI 임베딩 모델을 강제 사용합니다.")
            self.persist_directory = os.path.join(base_data_dir, "openai")
            return OpenAIEmbeddings(
                model=self.primary_embedding_model,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.embedding_type == "huggingface":
            logger.info("HuggingFace 임베딩 모델을 강제 사용합니다.")
            self.persist_directory = os.path.join(base_data_dir, "huggingface")
            return HuggingFaceEmbeddings(
                model_name=self.backup_embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            # 기존 auto fallback 로직
            try:
                if os.getenv("OPENAI_API_KEY"):
                    logger.info("OpenAI 임베딩 모델을 사용합니다.")
                    self.persist_directory = os.path.join(base_data_dir, "openai")
                    return OpenAIEmbeddings(
                        model=self.primary_embedding_model,
                        openai_api_key=os.getenv("OPENAI_API_KEY")
                    )
                else:
                    logger.warning("OPENAI_API_KEY가 설정되지 않았습니다. 백업 모델을 사용합니다.")
                    raise Exception("OpenAI API 키가 없습니다.")
            except Exception as e:
                logger.warning(f"OpenAI 임베딩 모델 초기화 실패: {str(e)}")
                logger.info("백업 임베딩 모델을 사용합니다.")
                self.persist_directory = os.path.join(base_data_dir, "huggingface")
                return HuggingFaceEmbeddings(
                    model_name=self.backup_embedding_model,
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
    
    def _initialize_vectorstore(self):
        """Chroma 벡터 저장소 초기화"""
        try:
            # 기존 Chroma 컬렉션이 있는지 확인
            if os.path.exists(self.persist_directory):
                logger.info(f"기존 Chroma 컬렉션을 로드합니다: {self.persist_directory}")
                return Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
            else:
                logger.info(f"새로운 Chroma 컬렉션을 생성합니다: {self.persist_directory}")
                # 빈 Chroma 컬렉션 생성
                return Chroma.from_texts(["초기화"], self.embeddings, persist_directory=self.persist_directory, collection_name=self.collection_name)
        except Exception as e:
            logger.warning(f"Chroma 컬렉션 로드 실패, 새로 생성합니다: {str(e)}")
            return Chroma.from_texts(["초기화"], self.embeddings, persist_directory=self.persist_directory, collection_name=self.collection_name)
    
    def get_embedding_model_info(self) -> Dict[str, str]:
        """현재 사용 중인 임베딩 모델 정보 반환"""
        model_type = "OpenAI" if isinstance(self.embeddings, OpenAIEmbeddings) else "HuggingFace"
        model_name = self.primary_embedding_model if model_type == "OpenAI" else self.backup_embedding_model
        
        return {
            "type": model_type,
            "name": model_name,
            "status": "primary" if model_type == "OpenAI" else "backup"
        }
    
    def load_documents(self, documents: List[Dict[str, Any]]) -> None:
        """문서 로드 및 벡터 저장소에 저장
        
        Args:
            documents: 로드할 문서 리스트
        """
        try:
            # 문서 로드
            loaded_docs = self.document_loader.load_documents(documents)
            
            # Chroma에 문서 추가
            self.vectorstore.add_documents(loaded_docs)
            
            # Chroma 저장
            self.vectorstore.persist()
            
            logger.info(f"총 {len(loaded_docs)}개 문서가 Chroma 벡터 저장소에 저장되었습니다.")
            
        except Exception as e:
            logger.error(f"문서 로드 중 오류 발생: {str(e)}")
            raise
    
    def get_relevant_documents(self, query: str, k: int = 3) -> List[Document]:
        """관련 문서 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 수
            
        Returns:
            검색된 문서 리스트
        """
        try:
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"문서 검색 중 오류 발생: {str(e)}")
            return []
    
    def query(self, query: str) -> Dict[str, Any]:
        """질문에 대한 답변 생성
        
        Args:
            query: 사용자 질문
            
        Returns:
            Dict[str, Any]: 답변과 관련 문서 정보
        """
        # 검색 실행 (기본 파라미터만 사용)
        docs = self.vectorstore.similarity_search_with_score(query, k=5)
        
        # 문서 필터링 (점수 기반)
        filtered_docs = []
        for doc, score in docs:
            # Chroma는 거리 기반이므로 점수가 낮을수록 유사도가 높음
            # 거리를 유사도 점수로 변환 (1 / (1 + distance))
            similarity_score = 1 / (1 + score)
            if similarity_score >= 0.3:  # 유사도 임계값
                filtered_docs.append(doc)
        
        # 컨텍스트 생성
        context = "\n\n".join([doc.page_content for doc in filtered_docs])
        
        # 답변 생성
        response = self.chain.invoke(query)
        
        return {
            "answer": response,
            "documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in filtered_docs
            ]
        }
    
    def load_directory(
        self,
        directory_path: str,
        glob_pattern: str = "**/*.*",
        persist: bool = True
    ) -> None:
        """디렉토리 내 문서 로드 및 벡터 저장소 생성
        
        Args:
            directory_path: 디렉토리 경로
            glob_pattern: 파일 패턴
            persist: 저장 여부
        """
        # 문서 로드
        loaded_docs = self.document_loader.load_directory(directory_path, glob_pattern)
        
        # 문서 분할
        split_docs = self.text_splitter.split_documents(loaded_docs)
        
        # Chroma에 문서 추가
        self.vectorstore.add_documents(split_docs)
        
        if persist:
            # Chroma 저장
            self.vectorstore.persist() 