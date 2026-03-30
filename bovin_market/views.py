from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bovin, Commande
from .forms import ConnexionEtape2Form, ConnexionEtape1Form ,InscriptionForm, BovinEtape1Form, BovinEtape2Form


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Connexion automatique après inscription
            login(request, user)

            # Cookie pour retenir le nom d'utilisateur
            response = redirect('catalogue')
            response.set_cookie('derniere_connexion', user.username, max_age=3600*24*30)
            return response
    else:
        form = InscriptionForm()

    return render(request, 'bovin_market/inscription.html', {'form': form})


def connexion_etape1(request):
    if request.method == 'POST':
        form = ConnexionEtape1Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Vérifier que l'utilisateur existe
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                # Sauvegarder le username en session
                request.session['username_connexion'] = username
                return redirect('connexion_etape2')
            else:
                messages.error(request, "Nom d'utilisateur introuvable.")
    else:
        # Pré-remplir avec le cookie si disponible
        initial_username = request.COOKIES.get('derniere_connexion', '')
        form = ConnexionEtape1Form(initial={'username': initial_username})

    return render(request, 'bovin_market/connexion_etape1.html', {'form': form})


def connexion_etape2(request):
    # Si étape 1 pas complétée, retour à l'étape 1
    if 'username_connexion' not in request.session:
        return redirect('connexion_etape1')

    username = request.session['username_connexion']

    if request.method == 'POST':
        form = ConnexionEtape2Form(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Nettoyer la session
                request.session.pop('username_connexion', None)

                # Cookie pour retenir le username
                response = redirect('catalogue')
                response.set_cookie('derniere_connexion', username, max_age=3600*24*30)
                return response
            else:
                messages.error(request, 'Mot de passe incorrect.')
    else:
        form = ConnexionEtape2Form()

    return render(request, 'bovin_market/connexion_etape2.html', {
        'form': form,
        'username': username
    })


def deconnexion(request):
    logout(request)  # supprime la session ✅
    response = redirect('connexion')
    response.delete_cookie('derniere_connexion')
    return response




@login_required
def catalogue(request):
    bovins = Bovin.objects.filter(statut='disponible').order_by('-date_publication')
    return render(request, 'bovin_market/catalogue.html', {'bovins': bovins})


@login_required
def publier_boeuf_etape1(request):
    initial_data = request.session.get('boeuf_etape1', {})

    if request.method == 'POST':
        form = BovinEtape1Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Convertir tous les types non-JSON en string
            request.session['boeuf_etape1'] = {
                'nom': data['nom'],
                'description': data.get('description', ''),
                'poids_total': float(data['poids_total']),
                'type_vente': data['type_vente'],
                'prix_par_kg': str(data['prix_par_kg']) if data.get('prix_par_kg') else None,
                'prix_par_lot': str(data['prix_par_lot']) if data.get('prix_par_lot') else None,
                'poids_lot': float(data['poids_lot']) if data.get('poids_lot') else None,
                'nombre_lots': data.get('nombre_lots'),
                'date_abattage': str(data['date_abattage']),
            }
            return redirect('publier_boeuf_etape2')
    else:
        form = BovinEtape1Form(initial=initial_data)

    return render(request, 'bovin_market/publier_etape1.html', {
        'form': form,
        'etape': 1
    })

@login_required
def publier_boeuf_etape2(request):
    # Si l'étape 1 n'est pas complétée, retour à l'étape 1
    if 'boeuf_etape1' not in request.session:
        return redirect('publier_boeuf_etape1')

    if request.method == 'POST':
        form = BovinEtape2Form(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer les données de l'étape 1
            etape1 = request.session['boeuf_etape1']

            # Créer le bœuf
            boeuf = Bovin.objects.create(
                vendeur=request.user,
                nom=etape1['nom'],
                poids_total=etape1['poids_total'],
                type_vente=etape1['type_vente'],
                prix_par_kg=etape1.get('prix_par_kg'),
                prix_par_lot=etape1.get('prix_par_lot'),
                poids_lot=etape1.get('poids_lot'),
                nombre_lots=etape1.get('nombre_lots'),
                date_abattage=etape1['date_abattage'],
                description=etape1.get('description', ''),
                photo=form.cleaned_data.get('photo'),
                statut='disponible'
            )

            # Nettoyer la session
            del request.session['boeuf_etape1']

            messages.success(request, f'"{boeuf.nom}" publié avec succès !')
            return redirect('catalogue')
    else:
        form = BovinEtape2Form()

    return render(request, 'bovin_market/publier_etape2.html', {
        'form': form,
        'etape': 2,
        'etape1_data': request.session.get('boeuf_etape1', {})
    })


@login_required
def detail_boeuf(request, boeuf_id):
    boeuf = get_object_or_404(Bovin, id=boeuf_id)
    return render(request, 'bovin_market/detail_boeuf.html', {'boeuf': boeuf})





@login_required
def commander(request, boeuf_id):
    boeuf = get_object_or_404(Bovin, id=boeuf_id)

    if request.method == 'POST':
        # Vérifier que le boeuf n'est pas complet
        if boeuf.est_complet():
            messages.error(request, 'Ce bœuf est déjà entièrement commandé.')
            return redirect('detail_boeuf', boeuf_id=boeuf_id)

        kilos = request.POST.get('kilos')
        lots = request.POST.get('lots')
        telephone = request.POST.get('telephone')

        Commande.objects.create(
            client=request.user,
            bovin=boeuf,
            kilos=float(kilos) if kilos else None,
            lots=int(lots) if lots else None,
            telephone=telephone,
            statut='en_attente'
        )

        messages.success(request, 'Commande passée avec succès !')
        return redirect('detail_boeuf', boeuf_id=boeuf_id)

    return redirect('detail_boeuf', boeuf_id=boeuf_id)


@login_required
def dashboard_vendeur(request):
    # Vérifier que c'est bien un vendeur
    if request.user.profil.role != 'vendeur':
        return redirect('catalogue')

    bovins = Bovin.objects.filter(vendeur=request.user).order_by('-date_publication')

    # Récupérer toutes les commandes liées aux bovins du vendeur
    commandes = Commande.objects.filter(
        bovin__vendeur=request.user
    ).order_by('-date_commande')

    return render(request, 'bovin_market/dashboard_vendeur.html', {
        'bovins': bovins,
        'commandes': commandes
    })


@login_required
def changer_statut_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    # Vérifier que c'est bien le vendeur de ce boeuf
    if commande.bovin.vendeur != request.user:
        return redirect('catalogue')

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in ['confirmée', 'annulée']:
            commande.statut = nouveau_statut
            commande.save()

            # Mettre à jour le statut du boeuf si complet
            if commande.bovin.est_complet():
                commande.bovin.statut = 'complet'
                commande.bovin.save()

            messages.success(request, f'Commande {nouveau_statut} avec succès !')

    return redirect('dashboard_vendeur')


@login_required
def mes_commandes(request):
    # Vérifier que c'est bien un client
    if request.user.profil.role != 'client':
        return redirect('catalogue')

    commandes = Commande.objects.filter(
        client=request.user
    ).order_by('-date_commande')

    return render(request, 'bovin_market/mes_commandes.html', {
        'commandes': commandes
    })


    