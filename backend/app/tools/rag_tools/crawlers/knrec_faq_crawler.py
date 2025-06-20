from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain_community.document_loaders import JSONLoader
import json
import os
import time
from datetime import datetime

class KnrecFAQLoader:
    """한국에너지공단 신재생에너지센터 FAQ Selenium 크롤러"""
    
    def __init__(self):
        self.base_url = "https://www.knrec.or.kr/biz/faq/faq_list01.do"
        self.output_dir = "./data/crawled_data/langchain_crawler"
        os.makedirs(self.output_dir, exist_ok=True)
        self.faqs: List[Dict[str, Any]] = []
        self.processed_urls: set[str] = set()  # URL 기반 중복 체크
        self.article_counter = 0  # 게시글 번호 카운터
        
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 헤드리스 모드
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # WebDriver 초기화
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def crawl(self):
        """FAQ 크롤링 실행"""
        print("=== KNREC FAQ Selenium 크롤링 시작  ===")
        
        try:
            # 최종 페이지 확인
            current_page = 1
            while True:
                url = f"{self.base_url}?page={current_page + 1}"
                self.driver.get(url)
                time.sleep(2)
                
                # 간편검색 탭 클릭
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) a").click()
                    time.sleep(2)
                except Exception:
                    pass
                
                # FAQ 항목이 있는지 확인
                faq_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul.result_list li")
                if not faq_elements:
                    print(f"최종 페이지 확인: {current_page}페이지")
                    break
                
                current_page += 1
            
            # 전체 페이지 크롤링
            for page in range(1, current_page + 1):
                print(f"\n페이지 {page}/{current_page} 크롤링 중...")
                url = f"{self.base_url}?page={page}"
                
                try:
                    # 페이지 로드
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # 간편검색 탭 클릭 (첫 페이지가 아닌 경우)
                    if page > 1:
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) a").click()
                            time.sleep(2)
                        except Exception:
                            pass
                    
                    # FAQ 항목 추출
                    faq_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul.result_list li")
                    
                    for element in faq_elements:
                        try:
                            # 제목과 URL 추출
                            title = element.find_element(By.CSS_SELECTOR, "a").text.strip()
                            faq_url = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            
                            # URL 기반 중복 체크
                            if faq_url in self.processed_urls:
                                print(f"중복 FAQ 건너뛰기: {title[:30]}...")
                                continue
                            
                            # 상세 내용 추출
                            content = self._extract_detail_content(faq_url)
                            
                            # 게시글 번호 증가
                            self.article_counter += 1
                            
                            # FAQ 데이터 저장
                            faq = {
                                "article_id": f"article_{self.article_counter}",
                                "title": title,
                                "content": content,
                                "url": faq_url,
                                "source": "한국에너지공단 신재생에너지센터",
                                "document_type": "FAQ",
                                "crawled_at": datetime.now().isoformat()
                            }
                            
                            self.faqs.append(faq)
                            self.processed_urls.add(faq_url)  # 처리된 URL 추가
                            print(f"FAQ 추출 완료: [{faq['article_id']}] {title[:30]}...")
                            
                        except Exception as e:
                            print(f"FAQ 항목 처리 중 오류: {e}")
                            continue
                    
                except Exception as e:
                    print(f"페이지 {page} 처리 중 오류: {e}")
                    continue
            
            # 결과 저장
            filepath = self._save_results(self.faqs)
            print(f"\n=== 크롤링 완료: {len(self.faqs)}개 FAQ 추출됨 (Selenium) ===")
            print(f"=== 게시글 번호 범위: article_1 ~ article_{self.article_counter} ===")
            
            # LangChain DocumentLoader로 결과 불러오기
            self._load_with_langchain(filepath)
            
        finally:
            # WebDriver 종료
            self.driver.quit()
    
    def _extract_detail_content(self, url: str) -> str:
        """FAQ 상세 내용 추출"""
        try:
            # 새 탭에서 URL 열기
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # 내용 로딩 대기 (대기 시간 증가)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".faq_view_content"))
            )
            
            # 내용 추출
            content = self.driver.find_element(By.CSS_SELECTOR, ".faq_view_content").text
            
            # 탭 닫기
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return content
            
        except Exception as e:
            print(f"상세 내용 추출 중 오류: {e}")
            # 오류 발생 시 탭 정리
            try:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return ""
    
    def _save_results(self, faqs: List[Dict[str, Any]]) -> str:
        """크롤링 결과를 JSON 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"knrec_faq_langchain_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(faqs, f, ensure_ascii=False, indent=2)
        
        print(f"결과가 저장되었습니다: {filepath}")
        return filepath
    
    def _load_with_langchain(self, filepath: str):
        """LangChain DocumentLoader로 결과 불러오기"""
        try:
            # JSONLoader 초기화
            loader = JSONLoader(
                file_path=filepath,
                jq_schema='.[] | {content: .content, metadata: {article_id: .article_id, title: .title, url: .url, source: .source, document_type: .document_type, crawled_at: .crawled_at}}',
                text_content=False
            )
            
            # 문서 로드
            documents = loader.load()
            print(f"LangChain으로 {len(documents)}개 문서 로드 완료")
            
            return documents
            
        except Exception as e:
            print(f"LangChain 문서 로드 중 오류: {e}")
            return []

if __name__ == "__main__":
    loader = KnrecFAQLoader()
    loader.crawl() 