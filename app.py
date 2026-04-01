from flask import Flask, request, jsonify
from extensions import db, migrate
from models import ServiceRequest
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
 
app = Flask(__name__)
CORS(app)

# PRIMERO CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
jwt = JWTManager(app)

# LUEGO INICIALIZAR
db.init_app(app)
migrate.init_app(app, db)

# Y AL FINAL CREAR TABLAS
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Limpiezas Costa Blanca API running 🚀"}

@app.route("/service-request", methods=["POST"])
def create_service_request():
    data = request.get_json()

    # Validaciones básicas
    if not data.get("client_name") or not data.get("phone"):
        return {"error": "Nombre y teléfono son obligatorios"}, 400

    try:
        scheduled_date = datetime.strptime(
            data["scheduled_date"], "%Y-%m-%d"
        ).date()
    except:
        return {"error": "Fecha inválida o faltante"}, 400

    # Tipos seguros
    price = float(data.get("price", 0))
    hours = int(data.get("hours", 0))
    urgent = bool(data.get("urgent", False))

    new_request = ServiceRequest(
        client_name=data["client_name"],
        phone=data["phone"],
        address=data.get("address"),
        service_type=data.get("service_type"),
        scheduled_date=scheduled_date,
        price=price,
        hours=hours,
        urgent=urgent
    )

    db.session.add(new_request)
    db.session.commit()

    return {"message": "Solicitud creada exitosamente"}, 201

@app.route("/service-request", methods=["GET"])
def get_service_requests():
    services = ServiceRequest.query.all()

    result = []
    for service in services:
        result.append({
            "id": service.id,
            "client_name": service.client_name,
            "phone": service.phone,
            "address": service.address,
            "service_type": service.service_type,
            "status": service.status
        })

    return result, 200

# @app.route("/service-request", methods=["GET"])
# def get_service_requests():
#     requests = ServiceRequest.query.all()

#     return [request.serialize() for request in requests], 200 


# Endpoint para actualizar el estado de una solicitud

@app.route("/service-request/<int:id>", methods=["PUT"])
def update_service_request(id):
    data = request.get_json()

    service_request = ServiceRequest.query.get(id)

    if not service_request:
        return {"error": "Solicitud no encontrada"}, 404

    service_request.status = data.get("status", service_request.status)

    db.session.commit()

    return {
        "message": "Estado actualizado correctamente",
        "updated_request": service_request.serialize()
    }, 200

# Endpoint para eliminar una solicitud

@app.route("/service-request/<int:id>", methods=["DELETE"])
def delete_service_request(id):
    service_request = ServiceRequest.query.get(id)

    if not service_request:
        return {"error": "Solicitud no encontrada"}, 404

    db.session.delete(service_request)
    db.session.commit()

    return {"message": "Solicitud eliminada correctamente"}, 200

if __name__ == "__main__":
    app.run(debug=True) 


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if not user or user.password != data["password"]:
        return {"error": "Credenciales incorrectas"}, 401

    token = create_access_token(identity=user.id)

    return {"token": token}, 200

@app.route("/stats", methods=["GET"])
def get_stats():
    services = ServiceRequest.query.all()

    total_income = sum(s.price or 0 for s in services)
    total_services = len(services)

    return {
        "income": total_income,
        "services": total_services
    } 

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([r.serialize() for r in reviews]), 200

@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json

    new_review = Review(
        name=data.get("name"),
        message=data.get("message")
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify(new_review.serialize()), 201