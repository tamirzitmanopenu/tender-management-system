import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import List

import chardet

DEFAULT_UNIT = "יח'"

#מחזיר את יחידת המדידה המתאימה לפי מזהה שנמצא בקובץ SKN
def get_unit(unit_id: str) -> str:
    unit_map = {
        '01': "יח'",
        '02': 'מטר',
        '03': 'מ"ר',
        '04': 'מ"ק',
        '05': 'טון',
        '09': "קומפ'",
    }
    return unit_map.get(unit_id, DEFAULT_UNIT)

# מזהה קידוד של קובץ SKN
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Data class representing a task in the project
@dataclass
class ProjectTask:
    category_num: int
    sub_category_num: int
    section: int
    desc: str
    unit: str
    quantity: Decimal
    price: Decimal
    total_price: Decimal

    project_name: str = ""
    category_name: str = ""
    sub_category_name: str = ""


def parse_skn_line(line: str) -> ProjectTask:
    """Parse a single SKN line into a ProjectTask. ויוצר ממנה מופע של ProjectTask מנתח שורה אחת מקובץ SKN"""
    if len(line) < 33:
        raise ValueError("Line too short to parse")

    category = int(line[2:4])
    sub_category = int(line[2:6])
    section = int(line[6:10])
    unit = get_unit(str(line[10:12]))
    quantity = Decimal(line[12:18])
    price = Decimal(f"{line[19:30]}.{line[31:33]}")
    desc = line[33:].strip()
    total_price = quantity * price
    return ProjectTask(
        category_num=category,
        sub_category_num=sub_category,
        section=section,
        desc=desc,
        unit=unit,
        quantity=quantity,
        price=price,
        total_price=total_price,
    )

# קורא קובץ SKN שלם ומחזיר רשימה של אובייקטים מסוג ProjectTask
def get_project_tasks(skn_file_path: str) -> List[ProjectTask]:
    """Parse an SKN file into a list of ProjectTask objects."""
    items: List[ProjectTask] = []
    encoding = detect_encoding(skn_file_path)
    with open(skn_file_path, encoding=encoding) as f:
        for line in f:
            if not line.strip():
                continue
            if line.startswith("000000"):
                continue
            try:
                parsed_line = parse_skn_line(line)
                if parsed_line.category_num == 0:
                    project_name = parsed_line.desc
                elif parsed_line.section == 0:
                    if parsed_line.sub_category_num % 100:
                        sub_category_name = parsed_line.desc
                    else:
                        category_name = parsed_line.desc
                else:
                    parsed_line.project_name = project_name
                    parsed_line.category_name = category_name
                    parsed_line.sub_category_name = sub_category_name
                    items.append(parsed_line)
            except (ValueError, InvalidOperation, IndexError):
                if items:
                    continuation = re.sub(r"^[\d\s]+", "", line).strip()
                    items[-1].desc += " " + continuation
                continue
            except Exception as e:
                raise Exception(f"There was unexpected error during the process - {e}")
    return items

# הרצה לבדיקה עצמית (אם הקובץ מורץ ישירות)
if __name__ == '__main__':
    skn_path = r"path/to/file.skn"
    skn_items = get_project_tasks(skn_path)
