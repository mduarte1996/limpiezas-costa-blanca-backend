from flask import Flask, request, jsonify
from extensions import db, migrate
from models import ServiceRequest
from datetime import datetime
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

# PRIMERO CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

    scheduled_date = datetime.strptime(
        data["scheduled_date"], "%Y-%m-%d"
    ).date()

    new_request = ServiceRequest(
        client_name=data["client_name"],
        phone=data["phone"],
        address=data["address"],
        service_type=data["service_type"],
        scheduled_date=scheduled_date
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

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return jsonify({"token": "abc123"}), 200

    return jsonify({"error": "Credenciales incorrectas"}), 401