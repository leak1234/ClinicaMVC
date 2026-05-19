# Sistema de Gestión de Clínica Médica - MVC

Aplicación web desarrollada con Flask y SQLAlchemy siguiendo el patrón MVC.

## Estructura del Proyecto

```
clinica_mvc/
├── controllers/
│   ├── auth_controller.py
│   ├── medico_controller.py
│   ├── paciente_controller.py
│   └── consulta_controller.py
├── models/
│   ├── medico_model.py
│   ├── paciente_model.py
│   ├── consulta_model.py
│   └── usuario_model.py
├── views/
│   ├── auth_view.py
│   ├── medico_view.py
│   ├── paciente_view.py
│   └── consulta_view.py
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── medicos/
│   ├── pacientes/
│   └── consultas/
├── instance/          (generado automáticamente)
├── database.py
├── run.py
└── requirements.txt
```

## Funcionalidades

- **Login y Registro de usuarios** *(Extra)*
- CRUD completo de Médicos
- CRUD completo de Pacientes
- CRUD completo de Consultas
- **Historial médico por paciente**
- **Filtro de consultas por fecha**
- **Exportación de reporte CSV**

## Instalación

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
python run.py
```

Abrir en el navegador: http://127.0.0.1:5000

## Tecnologías

- Python 3.x
- Flask 3.0
- SQLAlchemy 2.0
- SQLite
- Bootstrap 5
