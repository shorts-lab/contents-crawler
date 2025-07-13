from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import json
import time

class UnifiedCrawler:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
    
    # 네이버 블로그 크롤링
    def get_naver_search_url(self, keyword, page):
        base_url = "https://section.blog.naver.com/Search/Post.naver"
        encoded_keyword = urllib.parse.quote(keyword)
        return f"{base_url}?pageNo={page}&rangeType=ALL&orderBy=recentdate&keyword={encoded_keyword}"
    
    def extract_naver_content(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            frame = self.driver.find_elements(By.CSS_SELECTOR, "iframe#mainFrame")
            if frame:
                self.driver.switch_to.frame(frame[0])
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")

            content_div = soup.select_one("div.se-main-container") or \
                          soup.select_one("div#postViewArea") or \
                          soup.select_one("div#contentArea")

            if content_div:
                return content_div.get_text(separator="\n").strip()
            else:
                return "(본문을 찾을 수 없습니다)"
        except Exception as e:
            return f"(오류 발생: {e})"
    
    def crawl_naver_blog(self, keyword, max_pages=1):
        results = []
        for page in range(1, max_pages + 1):
            url = self.get_naver_search_url(keyword, page)
            print(f"🔎 네이버 블로그 페이지 {page} 크롤링 중...")
            self.driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            blog_cards = soup.select("div.list_search_post > div")

            for card in blog_cards:
                link_tag = card.select_one("a.desc_inner")
                if link_tag:
                    link = link_tag["href"]
                    title = link_tag.text.strip()
                    print(f"  → 블로그 수집 중: {title}")
                    content = self.extract_naver_content(link)
                    results.append({
                        "title": title,
                        "url": link,
                        "content": content,
                        "source": "naver_blog"
                    })
        return results
    
    # PANN NATE 크롤링
    def get_pann_search_url(self, keyword, page=1):
        base_url = "https://pann.nate.com/search/talk"
        encoded_keyword = urllib.parse.quote(keyword)
        return f"{base_url}?searchType=A&q={encoded_keyword}&page={page}"
    
    def extract_pann_content(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            content_div = soup.select_one("div.usertxt") or soup.select_one("div.content")
            if content_div:
                return content_div.get_text(separator="\n").strip()
            return "(본문을 찾을 수 없습니다)"
        except Exception as e:
            return f"(오류 발생: {e})"
    
    def crawl_pann_nate(self, keyword, max_pages=1):
        results = []
        for page in range(1, max_pages + 1):
            url = self.get_pann_search_url(keyword, page)
            print(f"🔎 PANN NATE 페이지 {page} 크롤링 중...")
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            post_links = soup.select("a.subject")
            
            for link in post_links:
                title = link.text.strip()
                post_url = "https://pann.nate.com" + link["href"]
                print(f"  → 게시글 수집 중: {title}")
                content = self.extract_pann_content(post_url)
                results.append({
                    "title": title,
                    "url": post_url,
                    "content": content,
                    "source": "pann_nate"
                })
        return results
    
    def crawl(self, platform, keyword, max_pages=1):
        self.setup_driver()
        try:
            if platform == "naver_blog":
                return self.crawl_naver_blog(keyword, max_pages)
            elif platform == "pann_nate":
                return self.crawl_pann_nate(keyword, max_pages)
            else:
                raise ValueError("지원하지 않는 플랫폼입니다.")
        finally:
            self.close_driver()

if __name__ == "__main__":
    crawler = UnifiedCrawler()
    
    print("=== 통합 크롤러 ===")
    print("1. 네이버 블로그")
    print("2. PANN NATE")
    
    choice = input("플랫폼을 선택하세요 (1 또는 2): ").strip()
    platform = "naver_blog" if choice == "1" else "pann_nate"
    
    keyword = input("검색할 키워드를 입력하세요: ").strip()
    pages = int(input("크롤링할 페이지 수를 입력하세요: "))
    
    data = crawler.crawl(platform, keyword, pages)
    
    filename = f"{platform}_{keyword}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(data)}개의 글이 '{filename}' 파일로 저장되었습니다.")