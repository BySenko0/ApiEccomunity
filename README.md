# ♻️ API de Recolección Comunitaria (FastAPI + MySQL + Alembic)

Este proyecto es una API construida con **FastAPI** y **SQLAlchemy** para gestionar el sistema de reciclaje de una comunidad. Se conecta con MySQL como base de datos, y está preparada para integrarse con Laravel para manejo de vistas frontend.

---

## ✅ Características principales

- Base de datos MySQL
- ORM con SQLAlchemy
- Migraciones con Alembic
- Autogeneración de tablas
- Modularidad por modelos, rutas, esquemas y CRUD
- Documentación Swagger (`/docs`)
- Compatible con Laravel como frontend

---

## ⚙️ Requisitos

- Python 3.10+
- MySQL Server
- pip / venv
- Git

---

## 🚀 Instalación del entorno

```bash
git clone https://github.com/lacabraloca1/ApiEccomunity.git
cd ApiEccomunity
python -m venv env
source env/bin/activate
pip install -r requirements.txt
🔐 Configuración .env
Crea un archivo .env en la raíz con lo siguiente:

env
Copy
Edit
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=ecommunity

DATABASE_URL=mysql+aiomysql://tu_usuario:tu_password@localhost:3306/ecommunity

🗃️ Crear Base de Datos desde Cero
Para entornos locales o nuevos desarrolladores, puedes ejecutar el siguiente script:

bash
Copy
Edit
python create_db_and_tables.py
Este script:

Conecta a MySQL con pymysql

Crea la base de datos ecommunity si no existe

Crea todas las tablas automáticamente a partir de los modelos

Nota: este método es ideal para ambientes nuevos, pero no gestiona cambios futuros como migraciones.

🔁 Migraciones con Alembic
Alembic permite mantener sincronizada la estructura de la base de datos con los modelos sin borrar datos.

Generar una nueva migración
bash
Copy
Edit
alembic revision --autogenerate -m "descripcion de cambio"
Aplicar migraciones
bash
Copy
Edit
alembic upgrade head
¿Dónde están las migraciones?
Las migraciones se guardan en alembic/versions/
Este directorio está ignorado en Git (.gitignore) para evitar conflictos entre ramas.

Cada desarrollador genera y aplica migraciones localmente.

📦 Estructura del proyecto
bash
Copy
Edit
├── alembic/
│   ├── env.py              
│   ├── script.py.mako
│   ├── versions/            
├── app/
│   ├── models/             
│   ├── schemas/             
│   ├── crud/                
│   ├── routers/            
│   ├── database.py          
│   └── main.py              
├── create_db_and_tables.py  
├── alembic.ini              
├── requirements.txt
├── .env
├── .gitignore
└── README.md
📑 Documentación automática
FastAPI genera automáticamente la documentación interactiva de todos los endpoints:


🛠️ Flujo recomendado de desarrollo
Acción	Herramienta
Crear base de datos inicial	create_db_and_tables.py
Generar migración por cambio de modelo	alembic revision --autogenerate
Aplicar cambios en DB sin perder datos	alembic upgrade head
Verificar conexión y rutas	Visitar /docs
📁 Buenas prácticas
Las migraciones no se suben a Git (alembic/versions/ está en .gitignore)

Cada developer puede aplicar o crear sus propios scripts locales

Laravel puede consumir esta API sin tocar directamente la base de datos

Toda la lógica está separada en capas: modelo, esquema, CRUD y rutas