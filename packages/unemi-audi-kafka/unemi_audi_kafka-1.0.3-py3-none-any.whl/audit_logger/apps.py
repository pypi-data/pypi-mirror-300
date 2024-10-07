from django.apps import AppConfig
from django.apps import apps
from django.db import connection
from .logger import AuditLogger

class AuditLoggerConfig(AppConfig):
    name = 'audit_logger'

    def ready(self):
        # Automatically register all models for auditing
        self.register_all_audit_logs()

    def register_all_audit_logs(self):
        """Register all models for auditing."""
        all_models = apps.get_models()
        for model in all_models:
            # You can add a check to make sure the table exists
            if self.table_exists(model._meta.db_table):
                AuditLogger.register_auditoria_logs(model)
            else:
                print(f"Skipping AUDITORIA {model.__name__}, table does not exist.")

    def table_exists(self, table_name):
        """Check if the table exists in the database."""
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'")
            return cursor.fetchone() is not None
