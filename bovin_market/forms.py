from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profil
from .models import Bovin, Commande


class InscriptionForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('vendeur', 'Vendeur'),
    ]

    email = forms.EmailField(required=True)
    telephone = forms.CharField(max_length=20, required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profil.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                telephone=self.cleaned_data.get('telephone', '')
            )
        return user


class ConnexionEtape1Form(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150
    )

class ConnexionEtape2Form(forms.Form):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )




class BovinEtape1Form(forms.Form):
    nom = forms.CharField(
        max_length=100,
        label='Nom du bœuf'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Description'
    )
    poids_total = forms.FloatField(
        label='Poids total (kg)'
    )
    type_vente = forms.ChoiceField(
        choices=[('kg', 'Par Kilogramme'), ('lot', 'Par Lot')],
        label='Type de vente'
    )
    prix_par_kg = forms.DecimalField(
        max_digits=10, decimal_places=2,
        required=False,
        label='Prix par kg (FCFA)'
    )
    prix_par_lot = forms.DecimalField(
        max_digits=10, decimal_places=2,
        required=False,
        label='Prix par lot (FCFA)'
    )
    poids_lot = forms.FloatField(
        required=False,
        label='Poids d\'un lot (kg)'
    )
    nombre_lots = forms.IntegerField(
        required=False,
        label='Nombre de lots'
    )
    date_abattage = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date d\'abattage'
    )
    race = forms.ChoiceField(
    choices=[
        ('zebu', 'Zébu'),
        ('gobra', 'Gobra'),
        ('djakoré', 'Djakoré'),
        ('ndama', 'N\'Dama'),
        ('metis', 'Métis'),
        ('autre', 'Autre'),
    ],
    label='Race'
)


class BovinEtape2Form(forms.Form):
    photo = forms.ImageField(
        required=False,
        label='Photo du bœuf'
    )


class BovinModifierForm(forms.ModelForm):
    class Meta:
        model = Bovin
        fields = [
        'nom', 'race', 'description', 'photo', 'poids_total',
        'type_vente', 'prix_par_kg', 'prix_par_lot',
        'poids_lot', 'nombre_lots', 'date_abattage', 'statut'
    ]
        widgets = {
            'date_abattage': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }