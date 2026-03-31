# boeuf/models.py

from django.db import models
from django.contrib.auth.models import User


class Bovin(models.Model):

    TYPE_VENTE_CHOICES = [
        ('kg', 'Par Kilogramme'),
        ('lot', 'Par Lot'),
    ]

    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('complet', 'Complet'),
        ('abattu', 'Abattu'),
    ]

    RACE_CHOICES = [
    ('zebu', 'Zébu'),
    ('gobra', 'Gobra'),
    ('djakoré', 'Djakoré'),
    ('ndama', 'N\'Dama'),
    ('metis', 'Métis'),
    ('autre', 'Autre'),
]

    # Infos de base
    vendeur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bovins'
    )
    nom = models.CharField(max_length=100)
    race = models.CharField(max_length=50, choices=RACE_CHOICES, default='zebu', verbose_name='Race')
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos_bovin/', blank=True, null=True)
    date_abattage = models.DateField()
    date_publication = models.DateTimeField(auto_now_add=True)

    # Poids et vente
    poids_total = models.FloatField(help_text="Poids total en kg")
    type_vente = models.CharField(
        max_length=10,
        choices=TYPE_VENTE_CHOICES,
        default='kg'
    )

    # Prix selon le type de vente
    prix_par_kg = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    prix_par_lot = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    poids_lot = models.FloatField(
        null=True, blank=True,
        help_text="Poids d'un lot en kg (si vente par lot)"
    )
    nombre_lots = models.IntegerField(
        null=True, blank=True,
        help_text="Nombre total de lots disponibles"
    )

    # Statut
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='disponible'
    )

    def __str__(self):
        return f"{self.nom} - {self.statut}"

    def kilos_commandés(self):
        """Total des kilos déjà commandés"""
        total = sum(
            c.kilos for c in self.commandes.filter(
                statut__in=['en_attente', 'confirmée']
            ) if c.kilos
        )
        return total

    def lots_commandés(self):
        """Total des lots déjà commandés"""
        total = sum(
            c.lots for c in self.commandes.filter(
                statut__in=['en_attente', 'confirmée']
            ) if c.lots
        )
        return total

    def est_complet(self):
        """Retourne True si tout est commandé"""
        if self.type_vente == 'kg':
            return self.kilos_commandés() >= self.poids_total
        else:
            return self.lots_commandés() >= self.nombre_lots

    def stock_restant(self):
        """Kilos ou lots encore disponibles"""
        if self.type_vente == 'kg':
            return self.poids_total - self.kilos_commandés()
        else:
            return self.nombre_lots - self.lots_commandés()


class Commande(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmée', 'Confirmée'),
        ('annulée', 'Annulée'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    bovin = models.ForeignKey(
        Bovin,
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    kilos = models.FloatField(null=True, blank=True)
    lots = models.IntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    def __str__(self):
        if self.bovin.type_vente == 'kg':
            return f"{self.client.username} → {self.kilos}kg de {self.bovin.nom}"
        else:
            return f"{self.client.username} → {self.lots} lot(s) de {self.bovin.nom}"

    def prix_total(self):
        from decimal import Decimal
        if self.bovin.type_vente == 'kg' and self.kilos:
            return Decimal(str(self.kilos)) * self.bovin.prix_par_kg
        elif self.bovin.type_vente == 'lot' and self.lots:
            return Decimal(str(self.lots)) * self.bovin.prix_par_lot
        return 0




class Profil(models.Model):
    ROLE_CHOICES = [
        ('vendeur', 'Vendeur'),
        ('client', 'Client'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def creer_profil(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'profil'):
            Profil.objects.create(user=instance, role='client')