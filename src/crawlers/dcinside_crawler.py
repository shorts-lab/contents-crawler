from bs4 import BeautifulSoup
import requests
import time
import random
import logging
from .base_crawler import BaseCrawler, retry

logger = logging.getLogger(__name__)

class DCInsideCrawler(BaseCrawler):
    """Crawler for DCInside"""
    
    @retry(max_attempts=3)
    def crawl(self):
        """Crawl DCInside posts based on keyword search"""
        results = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for page in range(1, self.max_pages + 1):
            params = {
                'id': 'loveconsultation',
                'page': page,
                's_type': 'search_subject_memo',
                's_keyword': self.keyword
            }
            
            try:
                logger.info(f"Crawling DCInside page {page}/{self.max_pages}")
                response = self._make_request("https://gall.dcinside.com/board/lists/", params, headers)
                
                soup = BeautifulSoup(response.content, 'html.parser')
                posts = soup.select('tr.ub-content') or soup.select('.gall_list tbody tr')
                
                if not posts:
                    logger.warning(f"No posts found on page {page}")
                    continue
                
                for post in posts:
                    title_elem = post.select_one('.gall_tit a') or post.select_one('td a')
                    if title_elem and title_elem.get_text(strip=True):
                        title = title_elem.get_text(strip=True)
                        href = title_elem.get('href', '')
                        if href:
                            link = "https://gall.dcinside.com" + href if href.startswith('/') else href
                            logger.info(f"Collecting post: {title}")
                            
                            results.append({
                                'title': title,
                                'url': link,
                                'content': title,  # DCInside doesn't allow easy content extraction
                                'platform': 'dcinside',
                                'author': ''
                            })
                
                # Add random delay between requests
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logger.error(f"Error crawling page {page}: {str(e)}")
                continue
        
        return self.process_results(results, "dcinside")
    
    @retry(max_attempts=2)
    def _make_request(self, url, params, headers):
        """Make HTTP request with retry logic"""
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response