Limpiezas Costa Blanca – Backend API

API de gestión de servicios de limpieza desarrollada para administrar solicitudes de clientes en la empresa Limpiezas Costa Blanca.

Este proyecto permite crear, consultar, actualizar y eliminar solicitudes de servicio mediante una arquitectura backend construida con Flask y SQLAlchemy.

🚀 Tecnologías utilizadas

Python

Flask

SQLAlchemy

Flask-Migrate

SQLite

Git & GitHub

📌 Funcionalidades

Crear solicitudes de servicio (POST)

Listar todas las solicitudes (GET)

Actualizar el estado de una solicitud (PUT)

Eliminar solicitudes (DELETE)

Gestión de fechas correctamente tipadas

Persistencia de datos en base de datos relacional

📂 Estructura del proyecto
app.py
models.py
extensions.py
config.py
migrations/
requirements.txt

🛠️ Instalación local

1.Clonar el repositorio

2.Crear entorno virtual

3.Instalar dependencias:

pip install -r requirements.txt

4.Ejecutar migraciones:

flask db upgrade

5.Ejecutar la aplicación:

python app.py

📌 Estado del proyecto

✔ CRUD completo funcional
✔ Integrado con base de datos
✔ Preparado para conexión con frontend

👩‍💻 Autora

Desarrollado por Maria Fernanda Duarte,
Proyecto backend orientado a negocio real y portfolio profesional.

