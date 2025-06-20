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
            temperature=0.3  # 더 일관되고 구조화된 응답을 위해 낮춤
        )
        
        # 임베딩 모델 초기화 (embedding_type에 따라 강제 지정)
        self.embeddings = self._initialize_embeddings()
        
        # 벡터 저장소 초기화 (Chroma 사용)
        self.vectorstore = self._initialize_vectorstore()
        
        # 문서 로더 초기화
        self.document_loader = DocumentLoader()
        
        # 프롬프트 템플릿 설정
        self.prompt_template = ChatPromptTemplate.from_template("""
당신은 재생에너지 전문 AI 컨설턴트입니다.

답변 작성 원칙:
- 내용에 포함된 구체적인 정보, 수치, 절차 등을 중심으로 답변 작성
- 제목의 불완전한 부분은 무시하고, 내용의 완전한 정보만을 바탕으로 답변
- 핵심 정보를 간결하고 명확하게 전달
- 마크다운, 굵은 글씨, 특수 기호 등은 사용하지 말고 일반 텍스트로만 답변
- 문장이 중간에 끊기거나 불완전한 경우, 자연스럽게 이어서 완성된 문장으로 답변

아래 [이전 대화]와 [컨텍스트]의 정보만을 바탕으로 답변하세요.
특히 내용(content)에 포함된 완전한 정보를 우선적으로 활용하세요.

[이전 대화]
{history}

[컨텍스트]
{context}

[질문]
{question}

답변:
""")
        
        # RAG 체인 설정
        self.chain = (
            {"context": self.vectorstore.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        
        # 텍스트 분할기 초기화
        self.text_splitter = TextSplitter(
            chunk_size=500,  # 더 작은 청크 크기로 문장 중간 절단 방지
            chunk_overlap=100  # 적절한 중복 유지
        )
    
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
    
    def query(self, query: str, history: Optional[str] = None) -> Dict[str, Any]:
        """질문에 대한 답변 생성 (이전 대화 히스토리 포함)"""
        docs = self.vectorstore.similarity_search_with_score(query, k=5)
        filtered_docs = []
        for doc, score in docs:
            similarity_score = 1 / (1 + score)
            if similarity_score >= 0.3:
                filtered_docs.append(doc)
        if not filtered_docs:
            logger.warning(f"쿼리 '{query}'에 대한 관련 문서를 찾을 수 없습니다.")
            return {
                "answer": "죄송합니다. 제공된 컨텍스트에 해당 정보가 없습니다. 다른 질문을 해주시거나, 재생에너지 관련 질문을 구체적으로 말씀해 주세요.",
                "documents": []
            }
        context_parts = []
        seen_content = set()
        for doc in filtered_docs:
            content_hash = hash(doc.page_content.strip())
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                cleaned_content = doc.page_content.strip()
                if cleaned_content and not cleaned_content.endswith('...'):
                    sentences = cleaned_content.split('.')
                    valid_sentences = []
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if sentence and not sentence.endswith('...') and len(sentence) > 10:
                            valid_sentences.append(sentence)
                    if valid_sentences:
                        cleaned_content = '. '.join(valid_sentences) + '.'
                        context_parts.append(cleaned_content)
        context = "\n\n---\n\n".join(context_parts)
        # history가 없으면 빈 문자열로
        if history is None:
            history = ""
        # 답변 생성 (프롬프트에 history 추가)
        response = self.prompt_template.invoke({
            "history": history,
            "context": context,
            "question": query
        })
        response = self.llm.invoke(response)
        response = StrOutputParser().invoke(response)
        return {
            "answer": self._post_process_response(response),
            "documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in filtered_docs
            ]
        }
    
    def _post_process_response(self, response: str) -> str:
        """응답 후처리 - 가독성 향상
        
        Args:
            response: 원본 응답
            
        Returns:
            후처리된 응답
        """
        # 불필요한 공백 정리
        response = response.strip()
        
        # 연속된 줄바꿈 정리 (3개 이상을 2개로)
        import re
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        # 문장 끝 정리
        response = re.sub(r'\s+([.!?])', r'\1', response)
        
        # 마크다운 패턴 제거 (**텍스트** → 텍스트)
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        
        # 기타 마크다운 패턴 제거
        response = re.sub(r'\*(.*?)\*', r'\1', response)  # *텍스트* → 텍스트
        response = re.sub(r'`(.*?)`', r'\1', response)    # `텍스트` → 텍스트
        
        # 말줄임표로 끝나는 불완전한 문장 제거
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # 말줄임표로 끝나거나 너무 짧은 문장 제거
            if line and not line.endswith('...') and len(line) > 10:
                cleaned_lines.append(line)
        
        response = '\n'.join(cleaned_lines)
        
        # 참고 문서 섹션에서 불완전한 내용 제거
        if '📋 참고 문서:' in response:
            parts = response.split('📋 참고 문서:')
            main_content = parts[0].strip()
            response = main_content
        
        return response
    
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
    
    def rebuild_vectorstore(self, documents: List[Dict[str, Any]]) -> None:
        """벡터 저장소 재구성 (기존 데이터 삭제 후 새로운 분할 방식으로 재구성)
        
        Args:
            documents: 재구성할 문서 리스트
        """
        try:
            # 기존 벡터 저장소 삭제
            import shutil
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
                logger.info(f"기존 벡터 저장소를 삭제했습니다: {self.persist_directory}")
            
            # 새로운 벡터 저장소 초기화
            self.vectorstore = self._initialize_vectorstore()
            
            # 문서 재로드
            self.load_documents(documents)
            
            logger.info("벡터 저장소가 새로운 분할 방식으로 재구성되었습니다.")
            
        except Exception as e:
            logger.error(f"벡터 저장소 재구성 중 오류 발생: {str(e)}")
            raise 