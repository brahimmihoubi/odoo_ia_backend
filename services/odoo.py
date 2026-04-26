import xmlrpc.client

ODOO_URL = "http://localhost:8069"
ODOO_DB = "your_db_name"

def get_odoo_connection(username: str, password: str):
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, username, password, {})

        if not uid:
            return None, None

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

        return uid, models

    except Exception as e:
        print("Odoo connection error:", e)
        return None, None