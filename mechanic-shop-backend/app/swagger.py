# app/swagger.py
swagger_spec = {
    "swagger": "2.0",
    "info": {
        "title": "Mechanic Shop API",
        "version": "1.0.0",
        "description": "API docs for the Mechanic Shop project."
    },
    # leave host out so Swagger UI uses the current host; you can set it later if desired
    # "host": "render-XXXX.onrender.com",
    "basePath": "/",
    "schemes": ["https", "http"],  # in production you can switch to ["https"]
    "consumes": ["application/json"],
    "produces": ["application/json"],

    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT in the format: **Bearer <token>**"
        }
    },

    "tags": [
        {"name": "Auth", "description": "Login endpoints"},
        {"name": "Mechanics", "description": "Mechanic management"},
        {"name": "Tickets", "description": "Service ticket management"},
        {"name": "Customers", "description": "Customer management"},
        {"name": "Inventory", "description": "Inventory management"},
        {"name": "Vehicles", "description": "Vehicle management"}
    ],

    "paths": {
        # ---------- Auth ----------
        "/login": {
            "post": {
                "tags": ["Auth"],
                "summary": "Customer login",
                "description": "Verify customer credentials and return a JWT.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "payload",
                        "required": True,
                        "schema": {"$ref": "#/definitions/LoginPayload"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "JWT token",
                        "schema": {"$ref": "#/definitions/TokenResponse"},
                        "examples": {"application/json": {"token": "Bearer eyJhbGciOi..."}}
                    },
                    "400": {"description": "Validation error", "schema": {"$ref": "#/definitions/Error"}},
                    "401": {"description": "Invalid credentials", "schema": {"$ref": "#/definitions/Error"}}
                }
            }
        },
        "/mechanics/login": {
            "post": {
                "tags": ["Auth"],
                "summary": "Mechanic login",
                "description": "Verify mechanic credentials and return a JWT.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "payload",
                        "required": True,
                        "schema": {"$ref": "#/definitions/LoginPayload"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "JWT token",
                        "schema": {"$ref": "#/definitions/TokenResponse"},
                        "examples": {"application/json": {"token": "Bearer eyJhbGciOi..."}}
                    },
                    "400": {"description": "Validation error", "schema": {"$ref": "#/definitions/Error"}},
                    "401": {"description": "Invalid credentials", "schema": {"$ref": "#/definitions/Error"}}
                }
            }
        },

        # ---------- Tickets ----------
        "/service_tickets/": {
            "get": {
                "tags": ["Tickets"],
                "summary": "List tickets",
                "description": "Return all service tickets.",
                "responses": {
                    "200": {
                        "description": "List of tickets",
                        "schema": {"type": "array", "items": {"$ref": "#/definitions/Ticket"}}
                    }
                }
            },
            "post": {
                "tags": ["Tickets"],
                "summary": "Create ticket",
                "description": "Create a new service ticket (provide **vin** or **vehicle_id**).",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "payload",
                        "required": True,
                        "schema": {"$ref": "#/definitions/TicketPayload"}
                    }
                ],
                "responses": {
                    "201": {"description": "Created", "schema": {"$ref": "#/definitions/Ticket"}},
                    "400": {"description": "Bad request", "schema": {"$ref": "#/definitions/Error"}},
                    "401": {"description": "Unauthorized", "schema": {"$ref": "#/definitions/Error"}}
                }
            }
        },

        # If you're exposing this route (you added it via app.add_url_rule in __init__.py)
        "/my-assigned-tickets": {
            "get": {
                "tags": ["Tickets"],
                "summary": "My assigned tickets (mechanic)",
                "description": "Return service tickets assigned to the logged-in mechanic.",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "List of tickets",
                        "schema": {"type": "array", "items": {"$ref": "#/definitions/Ticket"}}
                    },
                    "401": {"description": "Unauthorized", "schema": {"$ref": "#/definitions/Error"}}
                }
            }
        },

        # ---------- Mechanics (examples) ----------
        "/mechanics/": {
            "get": {
                "tags": ["Mechanics"],
                "summary": "List mechanics",
                "responses": {
                    "200": {
                        "description": "List of mechanics",
                        "schema": {"type": "array", "items": {"$ref": "#/definitions/Mechanic"}}
                    }
                }
            },
            "post": {
                "tags": ["Mechanics"],
                "summary": "Create mechanic",
                "parameters": [
                    {
                        "in": "body",
                        "name": "payload",
                        "required": True,
                        "schema": {"$ref": "#/definitions/MechanicPayload"}
                    }
                ],
                "responses": {
                    "201": {"description": "Created", "schema": {"$ref": "#/definitions/Mechanic"}},
                    "400": {"description": "Bad request", "schema": {"$ref": "#/definitions/Error"}}
                }
            }
        }
        # Add the rest of your routes here following the same pattern
    },

    "definitions": {
        # ----- Generic -----
        "Error": {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        },
        "TokenResponse": {
            "type": "object",
            "properties": {"token": {"type": "string"}}
        },

        # ----- Auth -----
        "LoginPayload": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"}
            }
        },

        # ----- Tickets -----
        "TicketPayload": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["open", "in_progress", "closed"]},
                "vehicle_id": {"type": "integer"},
                "vin": {"type": "string"}
            },
            "required": ["description"]
        },
        "Ticket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "vin": {"type": "string"},
                "description": {"type": "string"},
                "date_in": {"type": "string", "format": "date-time"},
                "date_out": {"type": "string", "format": "date-time"},
                "status": {"type": "string"},
                "total_cost": {"type": "number"}
            }
        },

        # ----- Mechanics -----
        "MechanicPayload": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "phone": {"type": "string"},
                "address": {"type": "string"},
                "salary": {"type": "number"},
                "password": {"type": "string"}
            },
            "required": ["name", "email"]
        },
        "Mechanic": {
            "type": "object",
            "properties": {
                "mechanic_id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "address": {"type": "string"},
                "salary": {"type": "number"}
            }
        }
    }
}
