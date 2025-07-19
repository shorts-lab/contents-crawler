from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import time
import logging
from .base_crawler import BaseCrawler, retry
from ..utils.browser import get_chrome_driver

logger = logging.getLogger(__name__)

class NaverCrawler(BaseCrawler):
    """Crawler for Naver Blog"""
    
    @retry(max_attempts=3)
    def crawl(self):
        """Crawl Naver Blog posts based on keyword search"""
        driver = get_chrome_driver()
        results = []

        try:
            for page in range(1, self.max_pages + 1):
                base_url = "https://section.blog.naver.com/Search/Post.naver"
                encoded_keyword = urllib.parse.quote(self.keyword)
                url = f"{base_url}?pageNo={page}&rangeType=ALL&orderBy=recentdate&keyword={encoded_keyword}"
                
                logger.info(f"Crawling Naver Blog page {page}/{self.max_pages}")
                driver.get(url)
                time.sleep(3)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                blog_cards = soup.select("div.list_search_post > div")
                
                if not blog_cards:
                    logger.warning(f"No blog cards found on page {page}")
                    continue

                for card in blog_cards:
                    link_tag = card.select_one("a.desc_inner")
                    if not link_tag:
                        continue
                        
                    link = link_tag["href"]
                    title = link_tag.text.strip()
                    logger.info(f"Collecting blog: {title}")
                    
                    try:
                        content = self._extract_content(driver, link)
                        results.append({
                            "title": title,
                            "url": link,
                            "content": content,
                            "platform": "naver",
                            "author": ""
                        })
                    except Exception as e:
                        logger.error(f"Error extracting content for '{title}': {str(e)}")
        finally:
            driver.quit()
        
        return self.process_results(results, "naver")
    
    @retry(max_attempts=2)
    def _extract_content(self, driver, link):
        """Extract content from a blog post"""
        driver.get(link)
        time.sleep(2)
        
        # Try to switch to iframe if exists
        frame = driver.find_elements(By.CSS_SELECTOR, "iframe#mainFrame")
        if frame:
            driver.switch_to.frame(frame[0])
            time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        content_div = (
            soup.select_one("div.se-main-container") or
            soup.select_one("div#postViewArea") or
            soup.select_one("div#contentArea")
        )

        if not content_div:
            return "(본문을 찾을 수 없습니다)"
            
        return content_div.get_text(separator="\n").strip()