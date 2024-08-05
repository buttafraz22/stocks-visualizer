from django.db import models

LOG_TYPES = [
    ("DEBUG", 'Debug'),
    ("INFO", 'Info'),
    ("WARNING", "Warning"),
    ("CRITICAL", "Critical"),
    ("ERROR", "Error")
]

class Logs(models.Model):
    log_level = models.CharField(max_length=9, choices=LOG_TYPES)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()