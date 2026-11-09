from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.
class Specialite(models.Model):
    nom_specialite = models.CharField("spécialité", max_length=100, unique=True)

    class Meta:
        ordering = ["nom_specialite"]

    def __str__(self):
        return self.nom_specialite
class User(AbstractUser):
    email = models.EmailField("adresse e-mail", unique=True)
    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
class Patient(User):
    cin = models.CharField("CIN", max_length=8, primary_key=True)
    telephone = models.CharField("téléphone", max_length=8,
                                 validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="Le numéro de téléphone doit contenir exactement 8 chiffres.",
            )
        ],
                                 )
    date_naissance = models.DateField("date de naissance")
    def clean(self):
        if self.date_naissance >= timezone.localdate():
            raise ValidationError(
                {
                    "date_naissance": "La date de naissance doit être antérieure à la date du jour."
                }
            )
    def __str__(self):
        return f"{self.get_full_name() or self.username} (CIN {self.cin})"


class Medecin(User):
    matricule_ordre = models.CharField(
        "matricule de l'ordre", max_length=6, primary_key=True)
    telephone = models.CharField("téléphone", max_length=8,
                                 validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="le numero  de telephone doit contenir exactement 8 chiffres.....",
            )
        ],)
    specialites = models.ManyToManyField(
        Specialite, related_name="medecins", blank=True, verbose_name="spécialités"
    )
    def __str__(self):
        return f"Dr {self.get_full_name() or self.username} ({self.matricule_ordre})"

    

