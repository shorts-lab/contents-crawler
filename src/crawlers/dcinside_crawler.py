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
                'exception_mode': 'recommend'
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
                            
                            try:
                                content = self._extract_content(link, headers)
                                results.append({
                                    'title': title,
                                    'url': link,
                                    'content': content,
                                    'platform': 'dcinside'
                                })
                            except Exception as e:
                                logger.error(f"Error extracting content for '{title}': {str(e)}")
                                # Fallback to using title as content if extraction fails
                                results.append({
                                    'title': title,
                                    'url': link,
                                    'content': title,
                                    'platform': 'dcinside'
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
        
    @retry(max_attempts=2)
    def _extract_content(self, url, headers):
        """Extract content from a post detail page"""
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content_div = soup.select_one('.write_div') or soup.select_one('.usertxt')
            
            if not content_div:
                return "(본문을 찾을 수 없습니다)"
                
            return content_div.get_text(separator="\n").strip()
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return "(본문 추출 중 오류 발생)"