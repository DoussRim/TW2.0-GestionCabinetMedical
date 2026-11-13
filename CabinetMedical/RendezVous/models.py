# AppointmentApp/models.py
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from User.models import Doctor,Patient

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    # Deux relations one-to-many indépendantes (pas de ManyToMany, pas de through)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="praticien",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="demandeur",
    )

    appointment_date = models.DateTimeField("date et heure du rendez-vous")
    duration_minutes = models.PositiveIntegerField("durée (minutes)", default=30)
    reason = models.TextField("motif")
    status = models.CharField(
        "statut", max_length=10, choices=Status.choices, default=Status.PENDING
    )

    # Ordonnance scannée, déposée par le médecin après la consultation
    prescription = models.FileField(
        "ordonnance",
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="Ce médecin a déjà un rendez-vous à cette date et heure.",
            )
        ]

    def __str__(self):
        return f"{self.patient} → {self.doctor} le {self.appointment_date:%d/%m/%Y %H:%M}"

    def clean(self):
        # La règle s'applique à la création ou si la date a été modifiée.
        # Un rendez-vous passé reste modifiable (ex. ajout de l'ordonnance).
        date_changed = self._state.adding or (
            not Appointment.objects.filter(
                pk=self.pk, appointment_date=self.appointment_date
            ).exists()
        )
        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError(
                {"appointment_date": "Le rendez-vous doit être postérieur à la date et l'heure actuelles."}
            )
