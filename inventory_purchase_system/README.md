# Inventory and Purchase System

A production-ready REST API backend built with **FastAPI**, **MongoDB**, and **Beanie ODM**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.115 |
| Database | MongoDB (via Motor async driver) |
| ODM | Beanie (Pydantic v2) |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Rate Limiting | SlowAPI |
| Runtime | Python 3.11+ |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
inventory_purchase_system/
│
├── app/
│   ├── main.py                    # FastAPI app, lifespan, routers, middleware
│   │
│   ├── config/
│   │   ├── database.py            # MongoDB + Beanie initialization
│   │   ├── security.py            # JWT creation/verification, password hashing
│   │   └── settings.py            # Pydantic settings from .env
│   │
│   ├── models/                    # Beanie ODM Documents (MongoDB collections)
│   │   ├── supplier_model.py
│   │   ├── item_model.py
│   │   ├── purchase_model.py
│   │   └── user_model.py
│   │
│   ├── schemas/                   # Pydantic request/response schemas
│   │   ├── response_schema.py
│   │   ├── supplier_schema.py
│   │   ├── item_schema.py
│   │   ├── purchase_schema.py
│   │   └── auth_schema.py
│   │
│   ├── routes/                    # FastAPI route handlers (thin layer)
│   │   ├── supplier_routes.py
│   │   ├── item_routes.py
│   │   ├── purchase_routes.py
│   │   └── auth_routes.py
│   │
│   ├── services/                  # Business logic (called by routes)
│   │   ├── supplier_service.py
│   │   ├── item_service.py
│   │   ├── purchase_service.py
│   │   └── auth_service.py
│   │
│   ├── middleware/
│   │   └── rate_limit.py          # SlowAPI limiter config
│   │
│   ├── utils/
│   │   ├── helper.py              # get_current_user dependency, document serializer
│   │   ├── response_handler.py    # success_response(), error_response() builders
│   │   └── validators.py          # ObjectId validation, input sanitizers
│   │
│   ├── constants/
│   │   └── messages.py            # All response messages and error codes
│   │
│   └── exceptions/
│       └── custom_exception.py    # Typed HTTP exceptions
│
├── tests/
│   └── test_suppliers.py
│
├── .env                           # Environment variables (git-ignored)
├── .env.example                   # Template for .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.11 or higher
- MongoDB running locally (`mongod`) or a MongoDB Atlas URI

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/inventory-purchase-system.git
cd inventory_purchase_system
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your values
```

Minimum required `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=inventory_db
SECRET_KEY=your-strong-secret-key-at-least-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Generate a strong secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Start MongoDB (if running locally)

```bash
# Windows (if MongoDB is installed as a service)
net start MongoDB

# macOS/Linux
mongod --dbpath /data/db
```

---

## Running the Application

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT | No |
| GET | `/auth/me` | Get current user profile | Yes |

### Suppliers

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/suppliers/` | Create a supplier | Yes |
| GET | `/suppliers/` | List all suppliers | Yes |
| GET | `/suppliers/?city=Chennai` | Filter suppliers by city | Yes |
| GET | `/suppliers/{id}` | Get supplier by ID | Yes |
| PUT | `/suppliers/{id}` | Update supplier | Yes |
| DELETE | `/suppliers/{id}` | Delete supplier | Yes |

### Inventory Items

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/items/` | Add new item | Yes |
| GET | `/items/` | List all items | Yes |
| GET | `/items/?category=Electronics` | Filter by category | Yes |
| GET | `/items/summary` | Stock summary | Yes |
| GET | `/items/low-stock` | Low stock alert list | Yes |
| GET | `/items/{id}` | Get item by ID | Yes |
| PUT | `/items/{id}` | Update item | Yes |
| DELETE | `/items/{id}` | Delete item | Yes |
| PATCH | `/items/{id}/reduce-stock` | Reduce stock quantity | Yes |

### Purchases

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/purchases/` | Record a purchase | Yes |
| GET | `/purchases/` | List all purchases | Yes |
| GET | `/purchases/{id}` | Get purchase by ID | Yes |

---

## API Usage Examples

### 1. Register a user

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### 2. Login and get JWT token

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in_minutes": 60,
    "username": "john_doe"
  }
}
```

Set the token as a variable for subsequent requests:
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Create a supplier

```bash
curl -X POST http://localhost:8000/suppliers/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_name": "Raj Electronics",
    "contact_number": "+91-9876543210",
    "city": "Chennai",
    "categories_supplied": ["Electronics", "Cables"],
    "active": true
  }'
```

### 4. Add an inventory item

```bash
curl -X POST http://localhost:8000/items/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_name": "Wireless Mouse",
    "category": "Electronics",
    "price": 499.99,
    "quantity": 100,
    "reorder_level": 20
  }'
```

### 5. Record a purchase

```bash
curl -X POST http://localhost:8000/purchases/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_id": "<supplier_id_from_step_3>",
    "item_id": "<item_id_from_step_4>",
    "purchase_quantity": 50
  }'
```

### 6. Get items filtered by category

```bash
curl -X GET "http://localhost:8000/items/?category=Electronics" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Reduce stock (when selling)

```bash
curl -X PATCH http://localhost:8000/items/<item_id>/reduce-stock \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reduce_by": 5}'
```

### 8. Get stock summary

```bash
curl -X GET http://localhost:8000/items/summary \
  -H "Authorization: Bearer $TOKEN"
```

### 9. Get low stock alerts

```bash
curl -X GET http://localhost:8000/items/low-stock \
  -H "Authorization: Bearer $TOKEN"
```

---

## Standard Response Format

### Success Response

```json
{
  "success": true,
  "message": "Supplier created successfully",
  "data": {
    "id": "64f1a2b3c4d5e6f7a8b9c0d1",
    "supplier_name": "Raj Electronics",
    "city": "Chennai",
    "active": true,
    "created_at": "2024-01-01T10:00:00Z"
  },
  "timestamp": "2024-01-01T10:00:00.123456Z"
}
```

### Error Response

```json
{
  "success": false,
  "message": "Supplier not found",
  "error_code": "SUPPLIER_404",
  "data": null,
  "timestamp": "2024-01-01T10:00:00.123456Z"
}
```

---

## Rate Limits

| Endpoint Group | Limit |
|---|---|
| `POST /auth/register` | 5 requests/minute |
| `POST /auth/login` | 5 requests/minute |
| All other endpoints | 20 requests/minute |

When a rate limit is exceeded, you receive:

```json
{
  "success": false,
  "message": "Rate limit exceeded. Try again later.",
  "error_code": "RATE_LIMIT_429"
}
```

---

## Swagger UI Usage

1. Open http://localhost:8000/docs
2. Click the **Authorize** button (lock icon, top right)
3. In the `HTTPBearer` field, enter your token (without "Bearer "):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Click **Authorize** → **Close**
5. All protected endpoints are now accessible from Swagger UI

---

## Running Tests

```bash
# Install pytest
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pip install pytest-cov
pytest tests/ -v --cov=app --cov-report=html
```

---

## MongoDB Setup

### Option 1: Local MongoDB

1. Install MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Start MongoDB: `mongod --dbpath /data/db`
3. Use `.env`: `MONGODB_URL=mongodb://localhost:27017`

### Option 2: MongoDB Atlas (Cloud)

1. Create a free cluster at https://cloud.mongodb.com
2. Get your connection string
3. Use `.env`: `MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

### Option 3: Docker

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

---

## Suggested Git Commit Messages

```bash
# Initial project setup
git commit -m "feat: initialize FastAPI project with folder structure"

# Database integration
git commit -m "feat: add MongoDB connection with Beanie ODM and Motor"

# Auth system
git commit -m "feat: implement JWT authentication with bcrypt password hashing"

# Supplier CRUD
git commit -m "feat: add supplier management CRUD endpoints"

# Inventory management
git commit -m "feat: add inventory item management with stock alerts"

# Purchase recording
git commit -m "feat: add purchase recording with automatic stock updates"

# Rate limiting
git commit -m "feat: add SlowAPI rate limiting on all endpoints"

# Error handling
git commit -m "feat: add global exception handlers and custom exceptions"

# Documentation
git commit -m "docs: add README with setup, API reference, and examples"
```

---

## Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | Application display name | `Inventory and Purchase System` |
| `APP_VERSION` | API version | `1.0.0` |
| `DEBUG` | Enable debug mode | `False` |
| `MONGODB_URL` | MongoDB connection URI | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `inventory_db` |
| `SECRET_KEY` | JWT signing secret (min 32 chars) | **REQUIRED** |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime | `60` |

---

## License

MIT License — free to use, modify, and distribute.
