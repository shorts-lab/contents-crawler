from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import time
import logging
from .base_crawler import BaseCrawler, retry
from ..utils.browser import get_chrome_driver

logger = logging.getLogger(__name__)

class PannCrawler(BaseCrawler):
    """Crawler for PANN NATE"""
    
    @retry(max_attempts=3)
    def crawl(self):
        """Crawl PANN NATE posts based on keyword search"""
        driver = get_chrome_driver()
        results = []
        
        try:
            for page in range(1, self.max_pages + 1):
                base_url = "https://pann.nate.com/search/talk"
                encoded_keyword = urllib.parse.quote(self.keyword)
                url = f"{base_url}?searchType=A&q={encoded_keyword}&page={page}"
                
                logger.info(f"Crawling PANN NATE page {page}/{self.max_pages}")
                driver.get(url)
                time.sleep(3)
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                post_links = soup.select("a.subject")
                
                if not post_links:
                    logger.warning(f"No posts found on page {page}")
                    continue
                
                for link in post_links:
                    title = link.text.strip()
                    post_url = "https://pann.nate.com" + link["href"]
                    logger.info(f"Collecting post: {title}")
                    
                    try:
                        content = self._extract_content(driver, post_url)
                        results.append({
                            "title": title,
                            "url": post_url,
                            "content": content,
                            "platform": "pann",
                            "author": ""
                        })
                    except Exception as e:
                        logger.error(f"Error extracting content for '{title}': {str(e)}")
        finally:
            driver.quit()
        
        return self.process_results(results, "pann")
    
    @retry(max_attempts=2)
    def _extract_content(self, driver, url):
        """Extract content from a post"""
        driver.get(url)
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        content_div = soup.select_one("div.usertxt") or soup.select_one("div.content")
        
        if not content_div:
            return "(본문을 찾을 수 없습니다)"
            
        return content_div.get_text(separator="\n").strip()