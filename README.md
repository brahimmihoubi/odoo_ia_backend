# Odoo AI Backend Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Project Directory Structure](#project-directory-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Configuration](#configuration)
7. [Authentication Flow](#authentication-flow)
8. [API Reference](#api-reference)
    - [Authentication](#authentication)
    - [CRM (Customer Relationship Management)](#crm-customer-relationship-management)
    - [Sales](#sales)
    - [Purchases](#purchases)
    - [Invoices](#invoices)
    - [Customers & Suppliers](#customers--suppliers)
    - [Companies](#companies)
    - [Dashboard](#dashboard)
9. [Services and Core Logic](#services-and-core-logic)
10. [Security Considerations](#security-considerations)
11. [Deployment](#deployment)

---

## Introduction

The **Odoo AI Backend** is a robust API middleware layer designed to bridge a custom frontend dashboard with an underlying Odoo 18 ERP instance. Built with **FastAPI**, this service provides a standardized RESTful interface, handling user authentication, session management, and real-time data synchronization with Odoo via XML-RPC. It enables secure, high-performance querying and manipulation of Odoo's business modules.

---

## Architecture Overview

The system architecture follows a layered approach:
- **Presentation / Routing Layer:** FastAPI routers (`routes/`) that define HTTP endpoints and handle incoming HTTP requests and responses.
- **Service / Business Logic Layer:** Python modules (`services/`) responsible for processing business rules, managing in-memory sessions, generating JSON Web Tokens (JWT), and communicating with the external system.
- **Data / Integration Layer:** XML-RPC client (`services/odoo.py`) that acts as the bridge to the Odoo ERP database.

### Workflow
1. Client sends a login request with Odoo credentials.
2. The backend authenticates directly against Odoo.
3. Upon success, an active session is stored in memory, and a JWT is returned to the client.
4. Subsequent requests include the JWT, which is decoded by the dependency injection system (`deps.py`) to verify authorization and retrieve the active Odoo XML-RPC connection before executing the operation.

---

## Technology Stack

- **Core Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.8+)
- **Server:** [Uvicorn](https://www.uvicorn.org/)
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Authentication:** JSON Web Tokens (JWT) via `python-jose`
- **Odoo Integration:** Standard Python `xmlrpc.client`

---

## Project Directory Structure

```text
odoo_ia_backend/
├── main.py                 # Application entry point & FastAPI instance
├── README.md               # Project documentation
├── routes/                 # API endpoint definitions by domain
│   ├── __init__.py
│   ├── auth.py             # Login and authentication endpoints
│   ├── companies.py        # Company data endpoints
│   ├── crm.py              # Leads and opportunities endpoints
│   ├── customers.py        # Customer management endpoints
│   ├── dashboard.py        # Aggregated KPI and metrics endpoints
│   ├── invoices.py         # Financial invoice endpoints
│   ├── purchases.py        # Purchase order endpoints
│   ├── sales.py            # Sales order endpoints
│   └── suppliers.py        # Supplier management endpoints
├── services/               # Core business logic and integrations
│   ├── __init__.py
│   ├── ai.py               # Future AI integrations and capabilities
│   ├── auth.py             # JWT generation and validation logic
│   ├── deps.py             # FastAPI dependencies (e.g., get_current_user)
│   ├── odoo.py             # Odoo XML-RPC connection management
│   └── session.py          # In-memory session tracking and storage
└── venv/                   # Python virtual environment
```

---

## Setup and Installation

### 1. Prerequisites
- **Python:** 3.8 or higher.
- **Odoo:** A running Odoo 18 instance with XML-RPC enabled.

### 2. Clone and Setup Environment
Clone the repository and navigate into the directory:
```bash
git clone <repository-url>
cd odoo_ia_backend
```

Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install fastapi uvicorn pydantic python-jose[cryptography]
```

### 4. Running the Server
Start the development server using Uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The application will be accessible at `http://localhost:8000`.
FastAPI automatically generates interactive Swagger API documentation at `http://localhost:8000/docs`.

---

## Configuration

Environmental and connection configurations are currently managed directly within the code. Before running the system, review the following variables:

**In `services/odoo.py`:**
- `ODOO_URL`: URL of the Odoo instance (Default: `http://localhost:8069`)
- `ODOO_DB`: The name of the Odoo database to connect to (Default: `odoo18_db`)

**In `services/auth.py`:**
- `SECRET_KEY`: Used for signing JWTs. (Must be changed in production)
- `ALGORITHM`: JWT signing algorithm (Default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token validity duration (Default: `60`)

---

## Authentication Flow

The backend employs a hybrid authentication strategy combining Odoo's native authentication with stateless JWTs for the REST API.

1. **Authentication Endpoint:** The client sends a `POST /api/auth/login` request with an Odoo `username` and `password`.
2. **Odoo Verification:** The `get_odoo_connection` service attempts to authenticate against the Odoo XML-RPC `common` endpoint.
3. **Session Creation:** If successful, the user's `uid` and `password` are cached in the in-memory session manager (`services/session.py`).
4. **Token Issuance:** A JWT is generated containing the user's `username` and `uid`.
5. **Authorized Requests:** For all subsequent requests to protected routes, the client must include the JWT in the `Authorization` header as a Bearer token (`Authorization: Bearer <token>`).

---

## API Reference

All routes (except login) require a valid JWT Bearer token in the `Authorization` header.

### Authentication
- **`POST /api/auth/login`**
  - **Payload:** `{"username": "user@example.com", "password": "password123"}`
  - **Response:** Returns the JWT access token and token type.

### CRM (Customer Relationship Management)
- **`GET /api/crm/`**
  - **Description:** Retrieves a list of active CRM leads and opportunities.
  - **Returns:** JSON object containing an array of lead records.
- **`POST /api/crm/`**
  - **Description:** Creates a new CRM lead.
  - **Payload Example:** `{"name": "New Opportunity", "expected_revenue": 50000.0, "partner_id": 12}`

### Sales
- **`GET /api/sales/`**
  - **Description:** Fetches current sales orders and quotations.

### Purchases
- **`GET /api/purchases/`**
  - **Description:** Fetches active purchase orders and vendor bills.

### Invoices
- **`GET /api/invoices/`**
  - **Description:** Retrieves financial invoices and their payment statuses.

### Customers & Suppliers
- **`GET /api/customers/`**
  - **Description:** Retrieves a list of partners classified as customers.
- **`GET /api/suppliers/`**
  - **Description:** Retrieves a list of partners classified as suppliers/vendors.

### Companies
- **`GET /api/companies/`**
  - **Description:** Retrieves system company configuration and details.

### Dashboard
- **`GET /api/dashboard/`**
  - **Description:** Aggregates KPIs and summary data from various modules to populate the frontend dashboard overview.

---

## Services and Core Logic

### `services/deps.py`
This module acts as the gatekeeper for protected routes. It exposes the `get_current_user` dependency which:
1. Extracts and verifies the JWT from the request header.
2. Retrieves the active session corresponding to the token.
3. Re-establishes the Odoo XML-RPC object connection.
4. Injects the connection details (`uid`, `models`, `password`) into the route handler.

### `services/odoo.py`
Manages the raw XML-RPC connection to Odoo. It handles the `common.authenticate` calls and provides access to the `object.execute_kw` wrapper needed to query Odoo models like `crm.lead` or `sale.order`.

### `services/session.py`
A lightweight, dictionary-based in-memory state manager. It maps a `username` to their current active Odoo `uid` and connection parameters, ensuring that the API doesn't need to re-authenticate with Odoo's database on every single HTTP request.

---

## Security Considerations

When preparing this application for a production environment, several critical security enhancements must be made:

1. **Environment Variables:** Hardcoded secrets (e.g., `SECRET_KEY` in `auth.py`, `ODOO_URL`, and database names) must be extracted to a `.env` file or a secure secrets manager.
2. **Session Storage Persistence:** The current session manager (`services/session.py`) relies on Python dictionary memory. If the server restarts, all sessions are lost. In a multi-worker production setup (e.g., using Gunicorn), this will cause session inconsistencies. It is highly recommended to replace this with a shared cache layer like **Redis**.
3. **CORS Restrictions:** In `main.py`, CORS is configured to allow all origins (`allow_origins=["*"]`). Update this list to explicitly include only the trusted frontend domains (e.g., `["https://dashboard.yourcompany.com"]`).
4. **HTTPS / TLS:** Ensure that both the connection between the frontend and this FastAPI backend, and the connection between this backend and Odoo, are secured using HTTPS.

---

## Deployment

For production deployments, do not use the raw `uvicorn` development server. Instead, use a robust process manager like **Gunicorn** combined with Uvicorn workers.

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
*(Note: As mentioned in the Security section, deploying with multiple workers (`-w 4`) requires migrating the session storage to a centralized database like Redis to prevent session fragmentation).*
