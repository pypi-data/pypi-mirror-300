import os


class CleanMigration:
    def __init__(self, app_name=None):
        self.app_name = app_name

    def run(self):
        target_dir = self.app_name if self.app_name else ""
        for root, dirs, files in os.walk("."):
            if "migrations" in root and "__pycache__" not in root and target_dir in root:
                for file in files:
                    if not file.startswith("__init__"):
                        os.remove(os.path.join(root, file))
