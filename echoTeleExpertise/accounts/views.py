from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from mylib.notifications import get_summary_notifs
from django.http import HttpResponseForbidden
from echoTeleExpertise.consts import ete_email
from django.contrib import messages, auth
from django.core.mail import send_mail
from mylib.crypt import encrypt_val
from core.models import User
from re import search

from .forms import RegisterForm, EditProfileForm


def     activate_link(request, user):
    '''
    The link to activate the account ( string )
    '''
    return  'http://127.0.0.1:8000/verify_email/' + encrypt_val(user.email) + '/'

@ensure_csrf_cookie
def     register(request):
    '''
    Register a new user view
    '''
    if request.method == 'POST':
        # Get Form Values:
        form = RegisterForm(request.POST)
        values = request.POST
        if form.is_valid():
            # Get Informations:
            password = form.password
            password2 = form.password2
            cin = form.cleaned_data['cin']
            city = form.cleaned_data['city']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['city']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            speciality = form.cleaned_data['speciality']
            institution = form.cleaned_data['institution']
            # Check if passwords match:
            if password != password2:
                messages.error(request, 'Les deux mots de passe ne se match pas!')
                context = {
                    'form': form,
                    'values': values
                }
                return render(request, 'accounts/register.html', context)
            # Check if the password match requierements:
            if ((len(password) < 8) or (search('[0-9]', password) is None) or (search('[A-Z]', password) is None)):
                messages.warning(request, 'Veuillez utilisé un mot de passe fort (conbinaison de chiffres et lettres) avec une longueur qui dépasse 8 caractères!')
                context = {
                    'form': form,
                    'values': values
                }
                return render(request, 'accounts/register.html', context)
            # Ready to Register:
            User.objects.filter(email=email, is_verified_mail=False).delete()
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                speciality=speciality,
                institution=institution,
                cin=cin,
                phone=phone,
                address=address,
                city=city,
                password=password
            )
            # Send the Verification Email
            send_mail(
                # Subject
                'Bonjour Dr ' + last_name + ' ' + first_name,
                # Message
                "Pour Valider votre compte veuillez entrer ce lien:\n" + activate_link(request, user) +  "\n\nRavi de vous avoir parmi nos membres, echoTeleExpertise vous assure la confidentialité dans vos données avec une interface simple pour gérer vos demandes-dossiers.\n- Meryem Rkach",
                # From (Email)
                ## A variable that contain the ete mail
                ete_email,
                # To (Email)
                [email, ],
                # If the send fail do not affich any errors
                fail_silently = False
            )
            user.save()
            return render(request, 'accounts/validate_email.html', {})
    else:
        form = RegisterForm()
        values = {}
    context = {
        'form': form,
        'values': values
    }
    return render(request, 'accounts/register.html', context)

def     login(request):
    '''
    Login users view
    '''
    if request.method == 'POST':
        # Get user Infos:
        email = request.POST['email'].lower()
        password = request.POST['password']
        # Check if the user exist:
        if User.objects.filter(email=email).exists():
            # Authenticate:
            user = auth.authenticate(
                email=email,
                password=password
            )
            # Check if the user is authenticate:
            if user is not None:
                auth.login(request, user)
                # Check if the user account is vefified:
                if request.user.is_verified_mail == False:
                    messages.error(request, "Votre compte n'est pas verifier! Veuillez accéder au lien envoyer à votre email à l'inscription.")
                    return render(request, 'accounts/login.html', {})
                return redirect('news')
            messages.error(request, 'Mot de passe incorrect!')
        else:
            messages.error(request, "Cet email n'est pas enregister!")
        return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/login.html', {})


def     logout(request):
    '''
    Logout user view
    '''
    if request.method == 'POST':
        if request.user.is_staff == False:
            messages.success(request, 'Au revoir Dr ' + request.user.last_name + ' ' + request.user.first_name)
        auth.logout(request)
        return redirect('index')


def        edit_profile(request):
    '''
    Edit Profile of the user view
    '''
    if request.method == 'POST':
        # Get Form infos
        form = EditProfileForm(request.POST)
        values = request.POST
        if form.is_valid():
            # Get Informations
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            speciality = form.cleaned_data['speciality']
            institution = form.cleaned_dat['institution']
            biography = form.cleaned_data['biography']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            cin = form.cleaned_data['cin']
            online_status = request.POST.get('online_status', 'NONE')
            is_enable_mail = request.POST.get('is_enable_mail', 'NONE')
            # Update the user info:
            user = User.objects.get(pk=request.user.pk)
            user.last_name = last_name
            user.first_name = first_name
            user.speciality = speciality
            user.institution = institution
            user.address = address
            user.phone = phone
            user.city = city
            user.cin = cin
            if online_status != 'NONE':
                user.online_status = online_status
            if is_enable_mail == 'NONE' and user.is_enable_mail == True:
                user.is_enable_mail = False
            if is_enable_mail == 'SEND' and user.is_enable_mail == False:
                user.is_enable_mail = True
            user.biography = biography
            user.save()
            messages.success(request, 'Les modifications dans le profile sont enregister avec succès')
            return redirect('pages:telefiles')
    else:
        form = EditProfileForm()
        values = {} 
    context = {
        'form': form,
        'values': values,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'accounts/edit_profile.html', context)


def        upload_profile_img(request):
    '''
    choose the new profile image:
    whitout noticing i affect a POST request to update the photo in db
    then i render again the edit profile page
    '''
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        user.avatar = request.FILES.get('profile_img')
        user.save()
        return redirect('accounts:edit_profile')
    return HttpResponseForbidden('allowed only via POST')