from extensions import db
from datetime import datetime

class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    price = db.Column(db.Float)
    hours = db.Column(db.Integer)
    urgent = db.Column(db.Boolean)

    def serialize(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "phone": self.phone,
            "address": self.address,
            "service_type": self.service_type,
            "scheduled_date": self.scheduled_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "price": self.price,
            "hours": self.hours,
            "urgent": self.urgent
        }

    def __repr__(self):
        return f"<ServiceRequest {self.client_name}>"
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
