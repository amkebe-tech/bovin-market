from django.contrib import admin

from django.contrib import admin
from .models import Bovin, Commande, Profil


@admin.register(Bovin)
class BovinAdmin(admin.ModelAdmin):
    list_display = ['nom', 'vendeur', 'poids_total', 'type_vente', 'statut', 'date_abattage', 'date_publication']
    list_filter = ['statut', 'type_vente', 'date_abattage']
    search_fields = ['nom', 'vendeur__username']
    ordering = ['-date_publication']
    readonly_fields = ['date_publication']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['client', 'bovin', 'kilos', 'lots', 'statut', 'telephone', 'date_commande']
    list_filter = ['statut', 'date_commande']
    search_fields = ['client__username', 'bovin__nom']
    ordering = ['-date_commande']


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'telephone']
    list_filter = ['role']
    search_fields = ['user__username']
