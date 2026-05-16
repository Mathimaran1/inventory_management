# Inventory and Purchase System

## Project Overview

The Inventory and Purchase System is a backend API project developed using FastAPI and MongoDB.

This system helps manage:

- Inventory Items
- Suppliers
- Purchases
- Stock Levels
- User Authentication

The project follows a clean folder structure and includes proper validation, error handling, MongoDB integration, and REST API principles.

---

## Features

- Create and manage inventory items
- Create and manage suppliers
- Record purchases
- Track stock levels
- Low stock alerts
- Stock summary
- Filter items by category
- Filter doctors by specialization
- JWT authentication
- Rate limiting
- Proper validation using Pydantic
- Proper HTTP status codes
- Clean JSON responses
- MongoDB integration

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- MongoDB
- Beanie ODM
- Motor (async driver)
- Pydantic
- Python Jose (JWT)
- Passlib / Bcrypt
- SlowAPI (rate limiting)
- Python Dotenv

---

## Project Structure

```
inventory_management/
│
├── app/
│   ├── main.py
│   │
│   ├── config/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── settings.py
│   │
│   ├── models/
│   │   ├── item_model.py
│   │   ├── supplier_model.py
│   │   ├── purchase_model.py
│   │   └── user_model.py
│   │
│   ├── schemas/
│   │   ├── item_schema.py
│   │   ├── supplier_schema.py
│   │   ├── purchase_schema.py
│   │   └── auth_schema.py
│   │
│   ├── routes/
│   │   ├── item_routes.py
│   │   ├── supplier_routes.py
│   │   ├── purchase_routes.py
│   │   └── auth_routes.py
│   │
│   ├── services/
│   │   ├── item_service.py
│   │   ├── supplier_service.py
│   │   ├── purchase_service.py
│   │   └── auth_service.py
│   │
│   ├── middleware/
│   │   └── rate_limit.py
│   │
│   └── utils/
│       ├── helper.py
│       └── response_handler.py
│
├── tests/
│   └── test_suppliers.py
│
├── .env
├── .gitignore
├── requirements.txt
└── pyproject.toml
```

---

## Prerequisites

Before running the project, make sure the following are installed:

- Python
- MongoDB
- Git

---

## Environment Variables

Create a `.env` file in the project root folder.

Add the following values:

MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=inventory_db
SECRET_KEY=your-strong-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

---

## Install Required Packages

pip install -r requirements.txt

---

## Run the Project

uvicorn app.main:app --reload

Server will run at:

http://127.0.0.1:8000

---

## Swagger API Documentation

FastAPI automatically generates Swagger UI.

Open:

http://127.0.0.1:8000/docs

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |
| GET | `/auth/me` | Get current user profile |
| POST | `/suppliers/` | Create a supplier |
| GET | `/suppliers/` | List all suppliers |
| GET | `/suppliers/{id}` | Get supplier by ID |
| PUT | `/suppliers/{id}` | Update supplier |
| DELETE | `/suppliers/{id}` | Delete supplier |
| POST | `/items/` | Add new item |
| GET | `/items/` | List all items |
| GET | `/items/summary` | Stock summary |
| GET | `/items/low-stock` | Low stock alert list |
| GET | `/items/{id}` | Get item by ID |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |
| PATCH | `/items/{id}/reduce-stock` | Reduce stock quantity |
| POST | `/purchases/` | Record a purchase |
| GET | `/purchases/` | List all purchases |
| GET | `/purchases/{id}` | Get purchase by ID |

---

## Sample API Flow

Step 1 — Register User

Step 2 — Login and Get JWT Token

Step 3 — Create Supplier

Step 4 — Add Inventory Item

Step 5 — Record Purchase

Step 6 — Check Stock Summary

Step 7 — Check Low Stock Alerts

---

## Validation Included

The project includes:

- Required field validation
- JWT token validation
- Supplier existence checking
- Item existence checking
- Purchase existence checking
- Stock quantity validation

---

## Error Handling

The project uses FastAPI HTTPException for:

- User not found
- Supplier not found
- Item not found
- Purchase not found
- Invalid credentials
- Unauthorized access
- Rate limit exceeded

---

## HTTP Status Codes Used

| Status Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created Successfully |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Resource Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Important Notes

- MongoDB automatically generates _id
- _id is removed before returning response
- Sensitive values are stored in .env
- .env is ignored using .gitignore
- JWT token required for protected endpoints
- APIs are tested using Swagger UI

---

## API Testing

You can test APIs using:

- Swagger UI
- Postman
