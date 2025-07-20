from datetime import datetime
import logging
from ..models import db, Content
from ..crawlers import NaverCrawler, PannCrawler, DCInsideCrawler

logger = logging.getLogger(__name__)

def save_crawled_data(data, platform):
    """Save crawled data to database"""
    saved_count = 0
    for item in data:
        url = item.get('url', '')
        # Skip items with 'javascript' or 'addc' in the URL
        if 'javascript' in url or 'addc' in url:
            logger.info(f"Skipping item with URL: {url}")
            continue
            
        content = Content(
            title=item.get('title', 'No Title'),
            content=item.get('content', '') or item.get('text', ''),
            url=url,
            platform=item.get('platform', platform)
        )
        db.session.add(content)
        saved_count += 1
    
    db.session.commit()
    return saved_count

def run_crawler_job(platform='dcinside', keyword='연애', pages=1, include_pann=True):
    """Centralized function to run crawler jobs and save results to database"""
    current_time = datetime.now()
    logger.info(f"\n\n=== CRAWLER RUNNING === {current_time} ====")
    
    results = {}
    total_count = 0
    
    try:
        # Run the specified platform crawler
        if platform != 'pann':
            logger.info(f"Starting {platform} crawler with keyword '{keyword}' for {pages} pages...")
            data = run_crawler_sync(platform, keyword, pages)
            saved_count = save_crawled_data(data, platform)
            logger.info(f"Successfully saved {saved_count} items from {platform}")
            results[platform] = saved_count
            total_count += saved_count
        
        # Always run PANN crawler if include_pann is True
        if include_pann and platform != 'pann':
            logger.info(f"Starting pann crawler with keyword '{keyword}' for 1 page...")
            pann_data = run_crawler_sync('pann', keyword, 1)
            pann_count = save_crawled_data(pann_data, 'pann')
            logger.info(f"Successfully saved {pann_count} items from pann")
            results['pann'] = pann_count
            total_count += pann_count
        elif platform == 'pann':
            logger.info(f"Starting pann crawler with keyword '{keyword}' for {pages} pages...")
            pann_data = run_crawler_sync('pann', keyword, pages)
            pann_count = save_crawled_data(pann_data, 'pann')
            logger.info(f"Successfully saved {pann_count} items from pann")
            results['pann'] = pann_count
            total_count += pann_count
        
        return results, total_count
    except Exception as e:
        logger.error(f"Error running crawler: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise e

def run_crawler(platform='dcinside', keyword='연애', pages=1):
    """Legacy function for backward compatibility"""
    logger.info(f"Running single crawler for {platform}")
    if platform == 'pann':
        results, total_count = run_crawler_job(platform, keyword, pages, include_pann=False)
    else:
        results, total_count = run_crawler_job(platform, keyword, pages, include_pann=False)
    return results.get(platform, 0)

def run_crawler_sync(platform, keyword, pages):
    """Run crawler synchronously and return results"""
    if platform == 'naver':
        crawler = NaverCrawler(keyword, pages)
    elif platform == 'pann':
        crawler = PannCrawler(keyword, pages)
    else:  # dcinside
        crawler = DCInsideCrawler(keyword, pages)
    
    return crawler.crawl()