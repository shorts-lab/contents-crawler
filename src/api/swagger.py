import os
import json
from flask_swagger_ui import get_swaggerui_blueprint

def setup_swagger(app):
    """Setup Swagger UI"""
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Crawler API"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Create static directory for swagger.json if it doesn't exist
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Create swagger.json file
    swagger_data = {
        "swagger": "2.0",
        "info": {
            "title": "Crawler API",
            "description": "API for crawling and scheduling content from various platforms",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "paths": {
            "/api/crawl-now": {
                "post": {
                    "summary": "Immediately crawl and save data to database",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "platform": {
                                        "type": "string",
                                        "enum": ["naver", "pann", "dcinside"],
                                        "description": "Platform to crawl"
                                    },
                                    "keyword": {
                                        "type": "string",
                                        "description": "Keyword to search for"
                                    },
                                    "pages": {
                                        "type": "integer",
                                        "description": "Number of pages to crawl",
                                        "default": 1
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        },
                        "500": {
                            "description": "Error during crawling"
                        }
                    }
                }
            },
            "/api/crawl": {
                "post": {
                    "summary": "Manually trigger a crawl job",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "platform": {
                                        "type": "string",
                                        "enum": ["naver", "pann", "dcinside"],
                                        "description": "Platform to crawl"
                                    },
                                    "keyword": {
                                        "type": "string",
                                        "description": "Keyword to search for"
                                    },
                                    "pages": {
                                        "type": "integer",
                                        "description": "Number of pages to crawl",
                                        "default": 1
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            },
            "/api/schedule": {
                "post": {
                    "summary": "Schedule a recurring crawl job",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "platform": {
                                        "type": "string",
                                        "enum": ["naver", "pann", "dcinside"],
                                        "description": "Platform to crawl"
                                    },
                                    "keyword": {
                                        "type": "string",
                                        "description": "Keyword to search for"
                                    },
                                    "pages": {
                                        "type": "integer",
                                        "description": "Number of pages to crawl",
                                        "default": 1
                                    },
                                    "schedule_type": {
                                        "type": "string",
                                        "enum": ["interval", "cron"],
                                        "description": "Type of scheduling: 'interval' for minutes-based or 'cron' for cron expression",
                                        "default": "interval"
                                    },
                                    "minutes": {
                                        "type": "integer",
                                        "description": "Minutes between crawls (for interval scheduling)",
                                        "default": 5
                                    },
                                    "cron": {
                                        "type": "string",
                                        "description": "Cron expression for scheduling (for cron scheduling)",
                                        "default": "0 0 * * *"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            },
            "/api/contents": {
                "get": {
                    "summary": "Get crawled contents with pagination",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "default": 1,
                            "description": "Page number"
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "default": 10,
                            "description": "Items per page"
                        },
                        {
                            "name": "platform",
                            "in": "query",
                            "type": "string",
                            "description": "Filter by platform"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            },
            "/api/contents/{content_id}": {
                "get": {
                    "summary": "Get a specific content by ID",
                    "parameters": [
                        {
                            "name": "content_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                            "description": "Content identifier"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        },
                        "404": {
                            "description": "Content not found"
                        }
                    }
                }
            }
        }
    }

    with open(os.path.join(static_dir, 'swagger.json'), 'w') as f:
        json.dump(swagger_data, f)
        
    return swagger_ui_blueprint