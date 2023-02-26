from authentication.models import User
from django.db import models

# Create your models here.


class Expense(models.Model):
    CATEGORY_OPTIONS = [
        ("ONLINE_SERVICES", "ONLINE_SERVICES"),
        ("TRAVEL", "TRAVEL"),
        ("RENT", "RENT"),
        ("FOOD", "FOOD"),
        ("OTHERS", "OTHERS"),
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return f"str(self.owner)'s {Expense}"
