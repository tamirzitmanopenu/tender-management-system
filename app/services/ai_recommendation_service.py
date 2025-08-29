import json

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class AIRecommendationService:
    def __init__(self, db):
        self.db = db
        self.ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_answer_from_openAI(self, prompt: str) -> str:
        response = self.ai_client.responses.create(
            model="gpt-5-nano-2025-08-07",
            input=prompt
        )

        return response.output_text

    def create_ai_prompt(self, project_id: str, category_id: str) -> str:
        category_row = self.db.get_table_record(table='Category', filters={'category_id': category_id},
                                                query_one_only=True)
        category_name = category_row["category_name"] if category_row else f"קטגוריה {category_id}"

        project_row = self.db.get_table_record(table='Project', filters={'project_id': project_id}, query_one_only=True)
        project_name = project_row["name"] if project_row else f"פרויקט {project_id}"

        query = """
        SELECT
            b.company_name,
            bc.business_category_id,
            SUM(pt.quantity * to2.price_offer) AS total_category_price,
            bc.rating_score               AS rating,
            bc.review                     AS review
        FROM ProjectTask pt
        JOIN Category c           ON c.category_id = pt.category_id
        JOIN TaskOffer to2        ON to2.project_task_id = pt.project_task_id
        JOIN TotalOffer t         ON t.total_offer_id = to2.total_offer_id
        JOIN BusinessCategory bc  ON bc.business_category_id = t.business_category_id
        JOIN Business b           ON b.business_id = bc.business_id
        WHERE pt.project_id = ?
          AND c.category_id = ?
        GROUP BY
            bc.business_category_id
        """
        rows = self.db.query_all(query, (project_id, category_id))
        suppliers = []
        for r in rows:
            suppliers.append({
                "company_name": r["company_name"],
                "total_category_price": float(r["total_category_price"]) if r[
                                                                                "total_category_price"] is not None else None,
                "rating": r.get("rating"),
                "review": (r.get("review") or "").strip(),
            })

        suppliers_json = json.dumps(suppliers, ensure_ascii=False)

        prompt = f"""אתה פועל כמומחה רכש והשוואות ספקים.
        יש לך נתונים אמיתיים ממסד נתונים עבור פרויקט {project_name}, בקטגוריה: "{category_name}".

        לכל ספק מוצגים שלושה פרמטרים מרכזיים:
        1) "total_category_price" – המחיר הכולל שהספק הציע לכל פריטי הקטגוריה בפרויקט.
        2) "rating" – דירוג מספרי (עד 5) של העסק בתחום/קטגוריה זו.
        3) "review" – חוות דעת טקסטואלית על העסק בתחום/קטגוריה זו.

        הנתונים (JSON) לכל הספקים:
        {suppliers_json}

        הנחיות:
        - בצע השוואה עניינית בין הספקים בקטגוריה זו על בסיס מחיר כולל, דירוג וחוות דעת.
        - חישוב פערי מחיר: עבור כל ספק, חשב פער באחוזים לעומת ההצעה הזולה ביותר.
        - השתמש בדירוג כמקדֵם איכות: אם פערי המחיר קטנים, תן משקל גבוה יותר לדירוג ולחוות הדעת; אם פערי המחיר גדולים, פרט את המשמעות התקציבית.
        - אם חסרים דירוג/חוות דעת לספק כלשהו, ציין זאת והצע דרך התמודדות (בדיקה נוספת, תנאי SLA, פיילוט מצומצם).
        - סיים בהמלצה מנומקת לבחירת הספק המועדף לקטגוריה, כולל 2–3 נימוקים קצרים וברורים.

        פורמט פלט נדרש ב-JSON (בעברית בלבד, ללא טקסט נוסף):
        {{
          "השוואה": [
            {{
              "ספק": "<company_name>",
              "מחיר כולל": <number>,
              "דירוג": <number or null>,
              "תקציר חוות דעת": "<תמצית עד 2 משפטים>",
              "חוזקות": ["<נקודה אחת או שתיים>"],
              "חולשות": ["<נקודה אחת או שתיים>"]
            }}
          ],
          "ניתוח-מחירים": {{
            "הזולה_ביותר": "<company_name>",
            "פערים_באחוזים_לעומת_הזולה": [
              {{"ספק": "<company_name>", "פער_%": <number>}}
            ]
          }},
          "המלצה": {{
            "ספק_מומלץ": "<company_name>",
            "מחיר_ספק_מומלץ": "<מחיר ספק מומלץ>",
            "נימוקים": ["<סיבה 1>", "<סיבה 2>", "<סיבה 3 אופציונלית>"]
          }}
        }}
        """
        return prompt


if __name__ == '__main__':
    from db.db import get_db

    repo = get_db()

    serv = AIRecommendationService(repo)
    ai_prompt = serv.create_ai_prompt(project_id='2', category_id='1')
    serv.get_answer_from_openAI(prompt=ai_prompt)
