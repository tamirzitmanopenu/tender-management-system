import os

from flask import Blueprint, jsonify, send_from_directory, url_for, current_app
from flask import request

from utilities import log_event, actor_from_headers

bp = Blueprint("files", __name__)


# Upload a new file העלאת קובץ חדש
@bp.post("/files")
def store_file():
    service = current_app.config["FileService"]

    uploaded_by = actor_from_headers()

    project_id = request.form.get("project_id")  # string or None
    file_type = request.form.get("file_type", "other")  # boq or other

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        storage_path = service.save_file(file, project_id)
    except Exception as e:
        return jsonify({"error": f"Could not save file {e}"}), 500

    file_id = service.insert_file_record(uploaded_by, project_id, storage_path, file_type)

    log_event(f"A new file was added {file.filename} for project_id {project_id}")

    return jsonify({
        "file_id": file_id,
        "original_name": file.filename,
        "storage_path": storage_path
    }), 201


# Get files metadata and download URL קבלת מטא-נתונים של קובץ וקישור להורדה
@bp.get("/files/<project_id>")
def get_file(project_id: str):
    payload = []
    service = current_app.config["FileService"]
    rows = service.get_files_by_project(project_id=project_id)
    if not rows:
        return jsonify({"error": f"Could not find file records for project_id {project_id}"}), 400
    for row in rows:
        payload.append({
            "file_id": row["file_id"],
            "file_name": row["name"],
            "file_type": row["file_type"],
            "download_url": url_for("files.download_file", filename=row["name"], _external=True)
        })
    return jsonify(payload), 200


# Download a file הורדת קובץ
@bp.get("/files/download/<filename>")
def download_file(filename: str):
    folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(folder, filename)


# TODO: check the response - might be missing
# Process SKN file (bill of quantities) עיבוד קובץ SKN (כתב כמויות)
@bp.post("/files/<file_id>/process-skn")
def process_skn(file_id: str):
    """
    Parsing SKN (bill of quantities) file, insert its tasks and new categories into DB for the given project_id
    """
    file_service = current_app.config["FileService"]

    # --- Fetch file record ---
    row = file_service.get_file_record(file_id=file_id)
    if not row:
        return jsonify({"error": f"Could not find file record for file_id {file_id}"}), 404

    # Prefer file_path from DB if present, otherwise fall back to UPLOAD_FOLDER + name
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "")

    file_path = row.get("file_path", os.path.join(upload_folder, row["name"]))

    if not file_path:
        return jsonify({"error": "Could not resolve file path on disk."}), 500

    # Enforce extension
    if not file_path.lower().endswith(".skn"):
        return jsonify({"error": "File type not supported for SKN processing"}), 400

    # --- Process ---
    try:
        result = file_service.process_skn_to_db(skn_file_path=file_path, project_id=str(row['project_id']))

        # If you later make it return stats (e.g., inserted/count/duplicates), they’ll flow through.
        payload = {
            "message": "SKN file processed and tasks inserted (see server logs for details).",
            "file_id": file_id,
            "project_id": str(row['project_id'])
        }
        if isinstance(result, dict):
            payload.update(result)

        return jsonify(payload), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Failed processing SKN file: {e}")
        return jsonify({"error": "Failed processing SKN file", "details": str(e)}), 500
