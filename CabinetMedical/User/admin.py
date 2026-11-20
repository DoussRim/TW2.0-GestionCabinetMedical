from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from User.models import User, Patient, Specialty,Doctor
from django.contrib.auth.forms import UserCreationForm#Q2.2
# Register your models here.
from .models import User
from RendezVous.models import Appointment
from RendezVous.admin import AppointmentInline#Q2.4

####Question 2.2#################
class PatientCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Patient
        fields = ("username", "national_id", "phone", "birth_date")

@admin.register(Patient)#Equivalent de :admin.site.register(Patient, PatientAdmin)
class PatientAdmin(UserAdmin):
    # Formulaire de création
    add_form = PatientCreationForm
    #add_fieldsets définit l’affichage de la page « Ajouter ». 
    # Il doit contenir password1 et password2, qui ne font pas partie 
    # de fields mais sont déclarés par UserCreationForm. 
    # Sans add_fieldsets, la page n’afficherait que username et les 
    # mots de passe.
    add_fieldsets = (
        (None, {
            "fields": ("username", "national_id", "phone", "birth_date",
                       "password1", "password2"),
        }),
    )

    # Formulaire de modification
    fieldsets = UserAdmin.fieldsets + (
        ("Patient", {"fields": ("national_id", "phone", "birth_date")}),
    )
    ####Question 2.3#################
    def get_readonly_fields(self, request, obj=None):
        return ["national_id"] if obj else []
        #création (obj est None) : liste vide, donc le CIN est modifiable et on peut le saisir ;
        #modification (obj existe) : le CIN s’affiche en texte simple, sans zone de saisie.
    ####Question 2.4#################
    search_fields = ["last_name", "first_name", "national_id"]
    ####Question 2.5#################
    inlines = [AppointmentInline]
#Ajout de Doctor dans Admin
# class DoctorAdmin(UserAdmin):
#     pass
# admin.site.register(Doctor, DoctorAdmin)
####Question 2.6.1#################
class DoctorCreationForm(UserCreationForm):
    """Formulaire de création : permet de saisir le numéro d'inscription à l'ordre."""

    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ("username", "license_number", "phone")


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    add_form = DoctorCreationForm####Question 2.6.1#################
    ####Question 2.6.1#################
    add_fieldsets = (
        (None, {
            "fields": ("username", "license_number", "phone",
                       "password1", "password2"),
        }),
    )
    ####Question 2.6.1#################
    def get_readonly_fields(self, request, obj=None):
        # license_number : modifiable à la création seulement
        return ["license_number"] if obj else []
    ####Question 2.6.2#################
    fieldsets = UserAdmin.fieldsets + (
        ("Doctor", {"fields": ("license_number", "phone", "specialites")}),
    )
    filter_horizontal = ["specialites"]
    ####Question 2.6.3#################
    search_fields = ["license_number", "last_name", "first_name"]
    ####Question 2.6.1#################