from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from User.models import User, Patient, Medecin, Specialite


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Formulaire d'AJOUT : username + mots de passe (chiffrés) + champs supplémentaires
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "usable_password", "password1", "password2"),
        }),
        ("Informations personnelles", {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name"),
        }),
    )


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        ("Profil patient", {"classes": ("wide",), "fields": ("cin", "telephone", "date_naissance")}),
    )
    # Formulaire de MODIFICATION : les champs de UserAdmin + ceux du profil
    fieldsets = UserAdmin.fieldsets + (
        ("Profil patient", {"fields": ("cin", "telephone", "date_naissance")}),
    )
    readonly_fields = ()   # voir la remarque sur la clé primaire ci-dessous


@admin.register(Medecin)
class MedecinAdmin(UserAdmin):
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        ("Profil médecin", {"classes": ("wide",), "fields": ("matricule_ordre", "telephone", "specialites")}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Profil médecin", {"fields": ("matricule_ordre", "telephone", "specialites")}),
    )
    filter_horizontal = ("specialites",)


admin.site.register(Specialite)