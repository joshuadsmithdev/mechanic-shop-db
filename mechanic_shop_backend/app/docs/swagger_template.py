# app/docs/swagger_template.py
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Mechanic Shop API",
        "version": "1.0.0",
        "description": "API for mechanics, customers, vehicles, and service tickets."
    },
    # For Render: keep https + your live host (no https:// prefix in host)
    "schemes": ["https"],
    "host": "render-7ll8.onrender.com",  # ← replace with your actual Render host
    "basePath": "/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Bearer token, format: **Bearer &lt;token&gt;**'
        }
    },
    "definitions": {
        "Error": {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        },
        "LoginPayload": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"}
            }
        },
        "TokenResponse": {
            "type": "object",
            "properties": {"token": {"type": "string"}}
        },
        "Mechanic": {
            "type": "object",
            "properties": {
                "mechanic_id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "address": {"type": "string"},
                "phone": {"type": "string"},
                "salary": {"type": "string"}
            }
        },
        "MechanicCreate": {
            "type": "object",
            "required": ["name", "email"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"},
                "address": {"type": "string"},
                "phone": {"type": "string"},
                "salary": {"type": "string"}
            }
        },
        "ServiceTicket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "vin": {"type": "string"},
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["open", "in_progress", "closed", "open"]},
                "total_cost": {"type": "number"},
                "date_in": {"type": "string", "format": "date-time"},
                "date_out": {"type": "string", "format": "date-time"}
            }
        },
        "ServiceTicketCreate": {
            "type": "object",
            "required": ["description"],
            "properties": {
                "vehicle_id": {"type": "integer"},
                "vin": {"type": "string"},
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["open", "in_progress", "closed", "open"]}
            }
        }
    }
}
