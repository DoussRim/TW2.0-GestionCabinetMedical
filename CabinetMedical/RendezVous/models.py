from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from User.models import Medecin
from User.models import Patient


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        CONFIRME = "CONFIRME", "Confirmé"
        ANNULE = "ANNULE", "Annulé"

    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="rendezvous"
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="rendezvous"
    )

    motif = models.TextField()

    ordonnance = models.FileField(
        upload_to="ordonnances/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
        null=True,
    )

    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE
    )

    duree_minutes = models.PositiveIntegerField(default=30)

    date_rdv = models.DateTimeField()

    date_creation = models.DateTimeField(auto_now_add=True)

    date_maj = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.date_rdv <= timezone.now():
            raise ValidationError(
                {
                    "date_rdv": "La date du rendez-vous doit être postérieure à la date et à l’heure actuelles."
                }
            )

    class Meta:
        unique_together = ("medecin", "date_rdv")

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.medecin} - "
            f"{self.date_rdv.strftime('%d/%m/%Y %H:%M')}"
        )