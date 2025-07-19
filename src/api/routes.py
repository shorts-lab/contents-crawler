from flask import jsonify, request
import logging
from ..utils.scheduler import run_crawler

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
            # Use the same function that the scheduler uses
            saved_count = run_crawler(platform, keyword, pages)
            
            return jsonify({
                'status': 'success',
                'message': f'Successfully crawled and saved {saved_count} items from {platform}',
                'count': saved_count
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

