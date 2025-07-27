from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        permissions =[
            ("can_view_reports","Can view reports")
        ]