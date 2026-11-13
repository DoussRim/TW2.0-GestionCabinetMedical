from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone
# Create your models here.
class Specialty(models.Model):
    name = models.CharField("Spécialité", max_length=100, unique=True)
    #A ajouter lors de la manipulation de l'admin
    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
        ordering = ["name"]

    def __str__(self):
        return self.name


# Défini une seule fois, réutilisé par Doctor et Patient
phone_validator = RegexValidator(
    regex=r"^\d{8}$",
    message="Le numéro de téléphone doit contenir exactement 8 chiffres.",
)

def validate_past_date(value):
    """La date doit être antérieure à la date du jour."""
    if value >= timezone.localdate():
        raise ValidationError("La date doit être antérieure à la date du jour.")


class User(AbstractUser):
    pass
    #A ajouter lors de la manipulation de l'admin
    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

class Patient(User):
    
    national_id = models.CharField(
        "CIN",
        max_length=8,
        unique=True,
        validators=[RegexValidator(r"^\d{8}$", "Le CIN doit contenir exactement 8 chiffres.")],
    )
    phone = models.CharField("téléphone", max_length=8, 
                             validators=[phone_validator])
    #1ère méthode
    birth_date = models.DateField("date de naissance", validators=[validate_past_date])

    telephone = models.CharField("téléphone", max_length=8,
                                 validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="Le numéro de téléphone doit contenir exactement 8 chiffres.",
            )
        ],
                                 )
    ##############################################""
    #2ème méthode
    #birth_date = models.DateField("date de naissance")
    #Cette méthode sert à une validation métier au niveau du modèle.
    #def clean(self):
    #C’est un nom spécial de Django. Il appelle automatiquement clean() 
    #pendant la validation du modèle, vous n’avez donc jamais à 
    # l’appeler vous-même. self est l’instance de Patient en cours de
    # validation.
    '''Situation	clean() appelée ?
        Formulaire (ModelForm, CreateView)	✅ Oui, pendant form.is_valid()
        Site d’administration Django	✅ Oui'''
    #self.birth_date pour vérifier que la date et valide ou n'est pas vide
    #==> Garde : si la date est vide ou invalide, Django gère déjà l'erreur
    '''def clean(self):
        if self.birth_date and self.birth_date >= timezone.localdate():
            #timezone.localdate() retourne la date du jour dans 
            # le fuseau horaire configuré dans settings.py (TIME_ZONE).
            raise ValidationError(
                {
                    "birth_date": "La date de naissance doit être antérieure à la date du jour."
                }
            )'''
    ################################################""
    def __str__(self):
        return f"{self.get_full_name() or self.username} (CIN {self.cin})"
    class Meta:
            verbose_name = "Patient"
            verbose_name_plural = "Patients"

class Doctor(User):
    # first_name, last_name, email, username, password : hérités de User
    license_number = models.CharField(
        "numéro d'inscription à l'ordre",
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6, message="Le numero doit contenir exactement 6 caractères.")],
    )
    phone = models.CharField("téléphone", max_length=8, validators=[phone_validator])
    # phone = models.CharField("téléphone", max_length=8,
    #                              validators=[
    #         RegexValidator(
    #             regex=r"^\d{8}$",
    #             message="le numero  de telephone doit contenir exactement 8 chiffres.....",
    #         )
    #     ],)

    specialites = models.ManyToManyField(
        Specialty, related_name="doctors", blank=True, verbose_name="spécialités"
    )


    def __str__(self):
        return f"Dr {self.get_full_name() or self.username} ({self.matricule_ordre})"
    #A ajouter lors de la manipulation de l'admin
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    

