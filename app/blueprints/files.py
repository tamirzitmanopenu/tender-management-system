from flask import Blueprint, jsonify, send_from_directory, url_for, current_app
from flask import request

from utilities import log_event, actor_from_headers

bp = Blueprint("files", __name__)


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


@bp.get("/files/<file_id>")
def get_file(file_id: str):
    service = current_app.config["FileService"]
    row = service.get_file_record(file_id)
    if not row:
        return jsonify({"error": f"Could not find file record for file_id {file_id}"}), 400

    return jsonify({
        "file_id": file_id,
        "file_name": row["name"],
        "file_type": row["file_type"],
        "download_url": url_for("files.download_file", filename=row["name"], _external=True)
    })


@bp.get("/files/download/<filename>")
def download_file(filename: str):
    folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(folder, filename)

