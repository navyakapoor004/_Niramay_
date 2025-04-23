from django.db import models

class Remedy(models.Model):
    symptom = models.CharField(max_length=255)  # Cold, Fever, etc.
    name = models.CharField(max_length=255)  # Tulsi, Ginger, etc.
    severity = models.CharField(
        max_length=10,
        choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')]
    )
    dosage = models.TextField()  # "Take 5 leaves twice a day"

    def __str__(self):
        return f"{self.name} ({self.severity})"
