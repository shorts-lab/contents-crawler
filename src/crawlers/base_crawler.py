from abc import ABC, abstractmethod
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1):
    """Retry decorator for crawler methods"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempts} failed: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator

class BaseCrawler(ABC):
    """Base class for all crawlers"""
    
    def __init__(self, keyword, max_pages=1):
        self.keyword = keyword
        self.max_pages = max_pages
        logger.info(f"Initializing {self.__class__.__name__} with keyword '{keyword}' for {max_pages} pages")
    
    @abstractmethod
    def crawl(self):
        """Crawl content and return results"""
        pass
    
    def process_results(self, results, platform):
        """Process and standardize crawled results"""
        processed = []
        for item in results:
            # Ensure all required fields are present
            processed_item = {
                'title': item.get('title', 'No Title'),
                'content': item.get('content', '') or item.get('text', ''),
                'url': item.get('url', ''),
                'author': item.get('author', ''),
                'platform': item.get('platform', platform)
            }
            processed.append(processed_item)
        
        logger.info(f"Processed {len(processed)} results from {platform}")
        return processed