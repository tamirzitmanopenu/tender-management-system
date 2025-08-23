import os
import uuid

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app

from app.services.skn_converter import get_project_tasks
from utilities import now_iso


class FileService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def save_file(file: FileStorage, project_id: str) -> str:
        short_id = uuid.uuid4().hex[:4]  # 4 hex chars
        storage_name = secure_filename(f"{short_id}_proj{project_id}_{file.filename}")
        storage_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_name)

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

    def get_file_record(self, file_id: str):
        return self.db.query_one("Select * From File Where file_id = (?)", (file_id,))

    @staticmethod
    def process_skn_to_db(file_path: str, project_id: str):
        # project_service = current_app.config["ProjectService"]
        # category_service = current_app.config["CategoryService"]
        #
        # project_tasks = parse_skn_file(file_path)
        # project_categories
        # exist_categories = category_service.list_categories()
        #
        #
        # for task in project_tasks:
        #     project_service.insert_project_task(category_id=)  # foreach
        # # insert_category() # if needed
        pass
