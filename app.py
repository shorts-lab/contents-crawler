from flask import Flask, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import application components
from src.utils.config import load_config
from src.models import db
from src.api import register_routes
from src.api.swagger import setup_swagger

# Load configuration
config = load_config()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Setup Swagger documentation
setup_swagger(app)

# Initialize scheduler
scheduler = BackgroundScheduler({
    'apscheduler.timezone': 'UTC',
    'apscheduler.job_defaults.coalesce': True,
    'apscheduler.job_defaults.max_instances': 1
})
scheduler.start()

# Register API routes
register_routes(app, scheduler)

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Helper function to run functions with app context
def run_with_app_context(func, *args, **kwargs):
    """Run a function with app context"""
    with app.app_context():
        return func(*args, **kwargs)

# Setup initial scheduler
def setup_scheduler():
    from src.utils.scheduler import run_crawler
    
    logger.info("Setting up scheduled crawler to run every 5 minutes")
    job = scheduler.add_job(
        func=run_with_app_context,
        args=[run_crawler, 'dcinside', '연애', 1],
        id='default_dcinside',
        trigger='interval',
        minutes=5,
        replace_existing=True,
        misfire_grace_time=None  # Always run, even if misfired
    )
    
    logger.info(f"Next scheduled run at: {job.next_run_time}")

# Register shutdown function
def shutdown_scheduler(exception=None):
    if scheduler.running:
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down")

import atexit
atexit.register(shutdown_scheduler)

if __name__ == '__main__':
    # Setup the scheduler
    setup_scheduler()
    
    # Run the Flask app
    port = config['PORT']
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)