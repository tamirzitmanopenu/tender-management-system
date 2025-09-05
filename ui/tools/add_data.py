import warnings

from tools.api import post


def register_business(company_name: str, business_id: str):
    payload = {"company_name": company_name, "business_id": business_id}

    resp = post("/businesses", json=payload)

    if getattr(resp, "ok", False):
        return resp.json()
    elif resp.status_code == 409:
        warnings.warn("העסק כבר קיים")
        return None
    else:
        raise Exception("נכשלה יצירת העסק")


def register_business_category_selection(project_id: str, business_category_items: list[dict[str, str]]):
    payload = {
        "project_id": project_id,
        "items": business_category_items
    }

    resp = post("/businesses-category-selections", json=payload)

    if getattr(resp, "ok", False):
        return resp.json()
    else:
        raise Exception("אירעה שגיאה בשמירת הבחירה")


def register_business_category(category_id: str,
                               business_id: str,
                               review: str = None,
                               rating_score: float = None,
                               supplier_contact_username: str = None):
    payload = {
        "category_id": category_id,
        "business_id": business_id,
    }

    # Only include optional fields if they are provided
    if review is not None:
        payload["review"] = review

    if rating_score is not None:
        payload["rating_score"] = str(rating_score)

    if supplier_contact_username is not None:
        payload["supplier_contact_username"] = supplier_contact_username

    resp = post("/business-category", json=payload)

    if getattr(resp, "ok", False):
        return resp.json()
    else:
        raise Exception("אירעה שגיאה ביצירת שיוך קטגוריה לעסק")
