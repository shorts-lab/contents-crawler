import argparse
import json
import logging
from ..crawlers import NaverCrawler, PannCrawler, DCInsideCrawler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Command line interface for the crawler"""
    parser = argparse.ArgumentParser(description='Integrated web crawler for Naver Blog, PANN NATE, and DCInside')
    parser.add_argument('--platform', type=str, required=True, choices=['naver', 'pann', 'dcinside'], 
                        help='Platform to crawl (naver, pann, dcinside)')
    parser.add_argument('--keyword', type=str, required=True, help='Keyword to search for')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to crawl')
    parser.add_argument('--output', type=str, required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    print(f"=== 통합 크롤러 === 플랫폼: {args.platform}, 키워드: {args.keyword}, 페이지: {args.pages}")
    
    if args.platform == "naver":
        crawler = NaverCrawler(args.keyword, args.pages)
    elif args.platform == "pann":
        crawler = PannCrawler(args.keyword, args.pages)
    else:  # dcinside
        crawler = DCInsideCrawler(args.keyword, args.pages)
    
    data = crawler.crawl()
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(data)}개의 글이 '{args.output}' 파일로 저장되었습니다.")