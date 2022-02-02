import os


def get_database_uri() -> str:
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432
    password = os.environ.get("DB_PASSWORD", "123")
    user, db_name = "blog", "blog"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
