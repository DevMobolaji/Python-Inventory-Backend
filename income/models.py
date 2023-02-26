from authentication.models import User
from django.db import models

# Create your models here.


class Income(models.Model):
    SOURCES_OPTIONS = [
        ("WORK", "WORK"),
        ("BUSINESSES", "BUSINESSES"),
        ("SIDE_HUSTLE", "SIDE_HUSTLE"),
        ("OTHERS", "OTHERS"),

    ]

    source = models.CharField(choices=SOURCES_OPTIONS, max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return f"str(self.owner)'s {Income}"
