import os
import uuid

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory

from app.services.skn_converter import get_project_tasks
from utilities import now_iso


class FileService:
    def __init__(self, db, upload_folder):
        # אתחול השירות עם חיבור לבסיס הנתונים
        self.db = db
        self.upload_folder = upload_folder

    def save_file(self, file: FileStorage, project_id: str) -> str:
        """ שומר את הקובץ בתיקיית ההעלאות של האפליקציה ומחזיר את הנתיב לשמירה בבסיס הנתונים"""
        short_id = uuid.uuid4().hex[:4]  # 4 hex chars
        storage_name = secure_filename(f"{short_id}_proj{project_id}_{file.filename}")
        storage_path = os.path.join(self.upload_folder, storage_name)

        # Save the file on the computer
        file.save(storage_path)

        return storage_path

    def insert_file_record(self, uploaded_by: str, project_id: str, storage_path: str, file_type: str):
        storage_name = os.path.basename(storage_path)

        # Insert the record to the DB
        return self.db.execute(
            "INSERT INTO File (name, uploaded_by, file_type, file_path, uploaded_at, project_id) "
            "VALUES (?,?,?,?,?,?)",
            (storage_name, uploaded_by, file_type, storage_path, now_iso(), project_id)
        )

    def get_files_by_project(self, project_id: str):
        # שליפת רשומות קבצים מבסיס הנתונים לפי מזהה פרויקט
        return self.db.get_table_record(table='File', filters={'project_id': project_id})

    def get_file_record(self, file_id: str):
        return self.db.get_table_record(table='File', filters={'file_id': file_id}, query_one_only=True)

    def download(self, filename: str):
        upload_folder = self.upload_folder
        os.makedirs(upload_folder, exist_ok=True)
        return send_from_directory(upload_folder, filename)

    @staticmethod
    def process_skn_to_db(skn_file_path: str, project_id: str) -> dict:
        """ עיבוד קובץ SKN (כתב כמויות), הוספת המשימות והקטגוריות החדשות לבסיס הנתונים עבור מזהה הפרויקט הנתון """
        result = {'new_categories': 0, 'new_project_tasks': 0}
        category_service = current_app.config["CategoryService"]
        project_task_service = current_app.config["ProjectTaskService"]
        project_tasks = get_project_tasks(skn_file_path=skn_file_path)
        for task in project_tasks:
            category_id = category_service.category_by_normalized(name=task.category_name)
            if category_id is None:
                category_id = category_service.insert_category(task.category_name)
                result['new_categories'] += 1
                print(f"category was added {category_id}")
            project_task_id = project_task_service.insert_project_task(project_id=project_id,
                                                                       category_id=category_id,
                                                                       description=task.desc,
                                                                       sub_category=task.sub_category_name,
                                                                       unit=task.unit,
                                                                       quantity=float(task.quantity)
                                                                       )
            result['new_project_tasks'] += 1
            print(f"project_task_id was added {project_task_id}")
        return result
