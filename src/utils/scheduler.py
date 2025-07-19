from datetime import datetime
import logging
from ..models import db, Content
from ..crawlers import NaverCrawler, PannCrawler, DCInsideCrawler

logger = logging.getLogger(__name__)

def save_crawled_data(data, platform):
    """Save crawled data to database"""
    saved_count = 0
    for item in data:
        content = Content(
            title=item.get('title', 'No Title'),
            content=item.get('content', '') or item.get('text', ''),
            url=item.get('url', ''),
            author=item.get('author', ''),
            platform=item.get('platform', platform)
        )
        db.session.add(content)
        saved_count += 1
    
    db.session.commit()
    return saved_count

def run_crawler(platform='dcinside', keyword='연애', pages=1):
    """Run crawler job and save results to database"""
    current_time = datetime.now()
    logger.info(f"\n\n=== SCHEDULED CRAWLER RUNNING === {current_time} ====")
    logger.info(f"Starting {platform} crawler with keyword '{keyword}' for {pages} pages...")
    
    try:
        # Run the appropriate crawler
        data = run_crawler_sync(platform, keyword, pages)
        
        # Save data to database - we're already in an app context
        saved_count = save_crawled_data(data, platform)
        
        logger.info(f"Successfully saved {saved_count} items from {platform}")
        return saved_count
    except Exception as e:
        logger.error(f"Error running crawler: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise e

def run_crawler_sync(platform, keyword, pages):
    """Run crawler synchronously and return results"""
    if platform == 'naver':
        crawler = NaverCrawler(keyword, pages)
    elif platform == 'pann':
        crawler = PannCrawler(keyword, pages)
    else:  # dcinside
        crawler = DCInsideCrawler(keyword, pages)
    
    return crawler.crawl()