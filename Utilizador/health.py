from sqlalchemy.exc import OperationalError
from sqlalchemy.sql.expression import text
from models import db

class HealthCheck:
    @classmethod
    def check_database_status(cls):
        try:
            # Execute a simple query to check the database status
            result = db.session.execute(text("SELECT 1"))
            # Check if the result is fetched successfully
            if result.scalar() == 1:
                return "OK"
            else:
                return "Error"
        except OperationalError as e:
            print(f"Error checking database status: {e}")
            return "Error"
