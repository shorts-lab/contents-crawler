from flask import jsonify, request
import logging
from ..utils.scheduler import run_crawler_job

logger = logging.getLogger(__name__)

def register_routes(app, scheduler):
    """Register API routes"""

    @app.route('/api/crawl', methods=['POST'])
    def crawl_endpoint():
        """Immediately crawl and save data to database"""
        data = request.json
        platform = data.get('platform', 'dcinside')
        keyword = data.get('keyword', '연애')
        pages = data.get('pages', 1)
        
        try:
            # Use the centralized crawler function
            if platform == 'all':
                # Crawl dcinside with PANN
                results, total_count = run_crawler_job('dcinside', keyword, pages, include_pann=True)
            else:
                # Crawl specified platform with PANN included by default
                results, total_count = run_crawler_job(platform, keyword, pages)
            
            return jsonify({
                'status': 'success',
                'message': f'Successfully crawled and saved {total_count} items',
                'count': total_count,
                'results': results
            })
        except Exception as e:
            logger.error(f"Error during crawling: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Error during crawling: {str(e)}'
            }), 500

    @app.route('/')
    def index():
        """Get API status"""
        return jsonify({
            'status': 'running',
            'message': 'Crawler service is running',
            'version': '1.0.0'
        })

