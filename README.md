# Odoo AI Backend

## Overview
This repository contains the backend service for the Odoo AI Dashboard application. It is built using FastAPI and serves as an intermediary API layer that interacts with an Odoo 18 ERP instance via XML-RPC. The backend provides a standardized RESTful API for various business modules, handling authentication, session management, and data retrieval and manipulation.

## Architecture and Technology Stack
- **Framework:** FastAPI (Python)
- **Authentication:** JSON Web Tokens (JWT)
- **Integration:** Odoo XML-RPC API
- **Data Validation:** Pydantic

## Key Features
- **Seamless Odoo Integration:** Connects directly to an Odoo 18 instance using XML-RPC to query and manipulate data in real-time.
- **Secure Authentication:** Implements a custom authentication flow where users log in with their Odoo credentials, generating a JWT for subsequent API requests.
- **Session Management:** Maintains user sessions in-memory to persist connections with the Odoo server securely.
- **Modular Routing:** Well-organized API endpoints for different business domains such as CRM, Sales, Purchases, and Invoices.
- **CORS Support:** Configured to allow cross-origin requests from the frontend application.

## Project Structure
- `main.py`: The entry point of the FastAPI application, configuring CORS and registering all module routers.
- `routes/`: Contains all the API route definitions organized by business domain.
  - `auth.py`: Authentication and login endpoints.
  - `companies.py`: Endpoints for managing company data.
  - `crm.py`: Endpoints for Customer Relationship Management (Leads, Opportunities).
  - `customers.py`: Endpoints for customer and partner management.
  - `dashboard.py`: Aggregated data endpoints for dashboard visualizations.
  - `invoices.py`: Endpoints for financial invoices.
  - `purchases.py`: Endpoints for purchase orders and vendor management.
  - `sales.py`: Endpoints for sales orders and quotations.
  - `suppliers.py`: Endpoints for supplier management.
- `services/`: Core business logic and integrations.
  - `auth.py`: JWT token creation and verification logic.
  - `deps.py`: FastAPI dependencies, primarily for extracting and validating the current user from the JWT.
  - `odoo.py`: Handles the XML-RPC connection and authentication with the Odoo server.
  - `session.py`: In-memory session storage mapping usernames to Odoo connection details.

## API Endpoints Summary

### Authentication
- `POST /api/auth/login`: Authenticate against Odoo and receive a JWT.

### CRM
- `GET /api/crm/`: Retrieve a list of CRM leads and opportunities.
- `POST /api/crm/`: Create a new CRM lead.

### Sales
- `GET /api/sales/`: Retrieve sales orders.

### Purchases
- `GET /api/purchases/`: Retrieve purchase orders.

### Invoices
- `GET /api/invoices/`: Retrieve invoices.

### Customers and Suppliers
- `GET /api/customers/`: Retrieve customer records.
- `GET /api/suppliers/`: Retrieve supplier records.

### Dashboard
- `GET /api/dashboard/`: Retrieve aggregated metrics for the dashboard view.

### Companies
- `GET /api/companies/`: Retrieve company configurations.

## Setup and Installation

1. **Prerequisites**
   - Python 3.8+
   - Running Odoo 18 instance (default expected at `http://localhost:8069`)

2. **Environment Configuration**
   The application currently connects to the Odoo instance configured in `services/odoo.py`. Update the following variables if your environment differs:
   - `ODOO_URL`: The URL of your Odoo server.
   - `ODOO_DB`: The name of your Odoo database (default is `odoo18_db`).

3. **Install Dependencies**
   Ensure you have a virtual environment set up, then install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic python-jose
   ```

4. **Running the Server**
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.

## Security Considerations
- **Session Storage:** Currently, sessions are stored in-memory. For production deployments, consider migrating this to a centralized cache like Redis.
- **Secret Keys:** The JWT secret key in `services/auth.py` is hardcoded. It is strongly recommended to use environment variables to manage secrets in production environments.
- **CORS Policy:** The CORS policy currently allows all origins (`["*"]`). Restrict this to your specific frontend domains before deploying to production.
