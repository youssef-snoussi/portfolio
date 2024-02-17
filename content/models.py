from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

STATUS_CHOICES = [
    ("Done", "done"),
    ("Postponed", "postponed"),
    ("In progess", "progess"),
    ("Canceled", "canceled")
    ]

STATUS_COLORS = {
    "done": "#8fce00",
    "postponed": "#2986cc",
    "progess": "#c90076",
    "canceled": "#f44336"
    }

class Project(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name=_("Status"))
    link = models.CharField(max_length=255, verbose_name=_("Link"))

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return f'{self.title} - {self.status}'

    def get_status_color(self):
        return STATUS_COLORS.get(self.status)