from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

logger = logging.getLogger(__name__)

def get_chrome_driver():
    """Initialize Chrome driver with appropriate options for server deployment"""
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Set user agent to avoid detection
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # For Cloudtype deployment
        try:
            # Try to use ChromeDriverManager with specific path
            driver_path = ChromeDriverManager().install()
            # Make sure we're not using THIRD_PARTY_NOTICES file
            if "THIRD_PARTY_NOTICES" in driver_path:
                # Get the directory and use the actual chromedriver
                driver_dir = os.path.dirname(driver_path)
                for file in os.listdir(driver_dir):
                    if file.startswith("chromedriver") and not file.endswith(".zip") and not "NOTICES" in file:
                        driver_path = os.path.join(driver_dir, file)
                        break
            
            chrome_service = Service(driver_path)
            driver = webdriver.Chrome(service=chrome_service, options=options)
        except Exception as e:
            logger.warning(f"Failed to use ChromeDriverManager: {str(e)}. Trying alternative approach.")
            # Fallback to direct path for Mac M1/M2
            if os.path.exists("/usr/local/bin/chromedriver"):
                chrome_service = Service("/usr/local/bin/chromedriver")
            elif os.path.exists("/opt/homebrew/bin/chromedriver"):
                chrome_service = Service("/opt/homebrew/bin/chromedriver")
            else:
                # Last resort - try without specifying path
                chrome_service = Service()
            
            driver = webdriver.Chrome(service=chrome_service, options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        logger.info("Chrome WebDriver initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
        raise