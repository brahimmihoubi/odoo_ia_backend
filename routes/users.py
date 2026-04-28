from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Literal
from services.odoo import ODOO_DB
from services.deps import get_current_user
import xmlrpc.client

router = APIRouter()

class ThemePreference(BaseModel):
    theme: Literal["light", "dark"]

@router.get("/preferences")
def get_user_preferences(user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    
    try:
        user_data = models.execute_kw(
            ODOO_DB, uid, password, 
            "res.users", "read", 
            [[uid]], 
            {"fields": ["theme"]}
        )
        if user_data:
            # Default to light if field exists but is unset
            theme = user_data[0].get("theme") or "light"
            return {"theme": theme}
        raise HTTPException(status_code=404, detail="User not found in Odoo")
    except xmlrpc.client.Fault as e:
        # Fallback if the 'theme' custom field isn't installed in Odoo yet
        print(f"Odoo XML-RPC error: {e}")
        return {"theme": "light", "warning": "Theme field not found in Odoo. Did you install the custom module?"}
    except Exception as e:
        print(f"Error fetching user preferences: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with Odoo database")

@router.put("/preferences")
def update_user_preferences(pref: ThemePreference, user=Depends(get_current_user)):
    uid = user["uid"]
    models = user["models"]
    password = user["password"]
    
    try:
        success = models.execute_kw(
            ODOO_DB, uid, password, 
            "res.users", "write", 
            [[uid], {"theme": pref.theme}]
        )
        if success:
            return {"theme": pref.theme}
        raise HTTPException(status_code=400, detail="Failed to update theme in Odoo")
    except xmlrpc.client.Fault as e:
        print(f"Odoo XML-RPC error: {e}")
        raise HTTPException(status_code=500, detail="Error writing to Odoo. Theme field might not be installed.")
    except Exception as e:
        print(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with Odoo database")
