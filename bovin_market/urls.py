from django.urls import path
from . import views
from django.contrib import admin

admin.site.site_header = "🐂 Bovin Market Administration"
admin.site.site_title = "Bovin Market"
admin.site.index_title = "Tableau de bord administrateur"

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion_etape1, name='connexion'),
    path('connexion/etape2/', views.connexion_etape2, name='connexion_etape2'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),



    path('catalogue/', views.catalogue, name='catalogue'),
    path('publier/etape1/', views.publier_boeuf_etape1, name='publier_boeuf_etape1'),
    path('publier/etape2/', views.publier_boeuf_etape2, name='publier_boeuf_etape2'),
    path('boeuf/<int:boeuf_id>/', views.detail_boeuf, name='detail_boeuf'),
    path('boeuf/<int:boeuf_id>/commander/', views.commander, name='commander'),
    path('dashboard/', views.dashboard_vendeur, name='dashboard_vendeur'),
    path('commande/<int:commande_id>/statut/', views.changer_statut_commande, name='changer_statut_commande'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('profil/', views.profil, name='profil'),
    path('boeuf/<int:boeuf_id>/modifier/', views.modifier_boeuf, name='modifier_boeuf'),
]