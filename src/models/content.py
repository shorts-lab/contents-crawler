from datetime import datetime
from .database import db

class Content(db.Model):
    """Content model for storing crawled data"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(512), nullable=False)
    platform = db.Column(db.String(50), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Content {self.id}: {self.title}>'
        
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'platform': self.platform,
            'createdAt': self.createdAt.isoformat()
        }