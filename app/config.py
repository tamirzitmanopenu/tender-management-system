import os


class Config:
    """Application configuration."""

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "db", "tender-management-system.db")
        ),
    )
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads")),
    )
