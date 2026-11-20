
from django.contrib import admin

from .models import Appointment

from datetime import timedelta

from django.contrib import admin, messages
from django.db.models import Sum
from django.utils import timezone

from .models import Appointment


######Question 2.5
class AppointmentInline(admin.TabularInline):
    """Historique des rendez-vous, affiché sur la fiche du patient."""
    model = Appointment
    extra = 0#supprime la ligne vide que Django ajoute par défaut (3 lignes vides sinon). 
    #Ainsi, la fiche n’affiche que l’historique existant.
    fields = ("appointment_date", "doctor", "duration_minutes", "status")
    show_change_link = True#ajoute un lien « Modifier » sur chaque ligne, 
    #qui ouvre le rendez-vous complet.

###Question 3.8.3
class AppointmentDateFilter(admin.SimpleListFilter):
    """Filtre personnalisé : Aujourd'hui / Cette semaine / À venir."""
    title = "date du rendez-vous"
    parameter_name = "date_range"

    def lookups(self, request, model_admin):
        return [
            ("today", "Aujourd'hui"),
            ("week", "Cette semaine"),
            ("upcoming", "À venir"),
        ]

    def queryset(self, request, queryset):
        today = timezone.localdate()
        if self.value() == "today":
            return queryset.filter(appointment_date__date=today)
        if self.value() == "week":
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            return queryset.filter(appointment_date__date__range=(monday, sunday))
        if self.value() == "upcoming":
            return queryset.filter(appointment_date__gt=timezone.now())
        return queryset


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    ######Question 3.4.2
    list_display = (
        "appointment_date", "doctor", "patient",
        "status", "duration_minutes", 
        "doctor_confirmed_minutes_today",###Question 3.5
    )
    list_select_related = ("doctor", "patient")
    list_per_page = 10###Question 3.7
    #Question 3.8.1, 3.8.2 et AppointmentDateFilter Q3.8.3
    list_filter = ("status", "doctor", AppointmentDateFilter)
    ######Question 3.11
    autocomplete_fields = ["doctor", "patient"]
    readonly_fields = ("created_at", "updated_at")###Question 3.6
    ###Question 3.9
    actions = ["confirm_appointments", "cancel_appointments"]
    ######Question 3.10
    fieldsets = (
        ("Participants", {"fields": ("doctor", "patient")}),
        ("Planification", {"fields": ("appointment_date", "duration_minutes", "status")}),
        ("Dossier", {"fields": ("reason", "prescription")}),
        ("Suivi", {"fields": ("created_at", "updated_at")}),
    )
    ###Question 3.5
    @admin.display(description="Minutes confirmées aujourd'hui (médecin)")
    def doctor_confirmed_minutes_today(self, obj):
        total = Appointment.objects.filter(
            doctor=obj.doctor,
            status=Appointment.Status.CONFIRMED,
            appointment_date__date=timezone.localdate(),
        ).aggregate(total=Sum("duration_minutes"))["total"]
        #filter() Sélectionne les rendez-vous voulus 
        # (même médecin, confirmés, aujourd’hui)
        #sum()Fonction d’agrégation : additionne la valeur de duration_minutes 
        # de toutes ces lignes
        #aggregate()Exécute le calcul sur tout le jeu de lignes et donne le 
        # nom total au résultat
        return total or 0
    ###Question 3.9
    @admin.action(description="Confirmer les rendez-vous sélectionnés")
    def confirm_appointments(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.CONFIRMED, updated_at=timezone.now())
        self.message_user(request, f"{updated} rendez-vous confirmé(s).", messages.SUCCESS)
    ###Question 3.9
    @admin.action(description="Annuler les rendez-vous sélectionnés")
    def cancel_appointments(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.CANCELLED, updated_at=timezone.now())
        self.message_user(request, f"{updated} rendez-vous annulé(s).", messages.SUCCESS)



