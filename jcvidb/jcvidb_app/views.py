# from django.core.checks import messages
import os
import time
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User, Proteomic, Role
from .details_form import DetailsForm
from .protpost_form import ProtPostForm
from .registration_form import RegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password


def set_session_values(request):
    try:
        login_context = {"id": request.session['user_id'],
                         "last_name": request.session['last_name']}

        return login_context
    except:
        return None


def handle_uploaded_file(uploaded_file):
    upload_dir = 'uploads/'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(os.path.join(upload_dir, uploaded_file.name), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


def main(request):
    try:
        if request.session['user_id'] and request.session['last_name']:
            print("here")
            print(request.session['user_id'])
            print(request.session['last_name'])
            login_context = {"id": request.session['user_id'],
                             "last_name": request.session['last_name']}
    except:
        login_context = None
        print("no session found")
    print(request)
    if request != "POST":

        aProteomics_data_list = Proteomic.objects.all().values()
        paginator = Paginator(aProteomics_data_list, 5)
        page_number = request.GET.get('page')
        try:
            aProteomics_data = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            aProteomics_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            aProteomics_data = paginator.page(paginator.num_pages)

        return render(request, 'main.html', {'aProteomics_data': aProteomics_data, 'login_context': login_context})


def details(request, id):
    aProteomics_data = Proteomic.objects.get(id=id)
    print(aProteomics_data.id)
    template = loader.get_template('details.html')
    context = {
        'prot_data': aProteomics_data,
    }
    return HttpResponse(template.render(context, request))


def search(request):
    login_details = set_session_values(request)
    name = request.GET.get('PGAN_name', '')
    results_list = Proteomic.objects.filter(PGAN__icontains=name)
    print(len(results_list))

    page_number = request.GET.get('page')
    paginator = Paginator(results_list, 5)

    if page_number is None:
        page_number = 1

    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    print(page_number)
    print(name)
    if name == "":
        name = request.GET.get('query')
    return render(request, 'search.html', {'results': results, 'search_query': name,'login_context': login_details})


def create_User(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            print(password)
            hashed_password = make_password(password)
            form.instance.password = hashed_password
            form.save()
            messages.success(request, 'Form submitted successfully!')
            # time.sleep(2)
            form = RegistrationForm()
            return redirect('../')
        else:
            print(form.errors)
            form = RegistrationForm(form)
            messages.error(request, 'Form is invalid!')
            return render(request, 'registration_form.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration_form.html', {'form': form})


def sign_in(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['last_name']
    login_context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        # print(email)
        password = request.POST.get('password')
        # print(password)
        hashed_password = make_password(password)
        login_details = User.objects.get(email=email)
        if email == login_details.email and check_password(password, login_details.password):
            # Set session ID
            print("success")
            request.session['user_id'] = login_details.id  # Assuming user ID is 1
            request.session['last_name'] = login_details.lastname
            # Redirect to a new page (or render response)
            print(request.session['user_id'])
            print(request.session['last_name'])

            login_context = {"id": request.session['user_id'],
                             "last_name": request.session['last_name']}

            print("success")

            return redirect('../')  # Assuming 'dashboard' is the name of the URL pattern for the dashboard page
        else:
            # Display error message (optional)
            messages.error(request, 'Invalid username or password')

    return render(request, 'sign_in.html', context=login_context)


def sign_out(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['last_name']
    redirect('../')
    print('redirecting')
    return render(request, 'sign_in.html', context=None)


def prot_post(request):
    # print(request.session['user_id'])
    # print(request.session['last_name'])
    login_details = set_session_values(request)
    if login_details!=None:
        if request.method == 'POST':
            form = ProtPostForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = request.FILES['attachment']
                    handle_uploaded_file(uploaded_file)
                except:
                    form = ProtPostForm(form)
                    messages.error(request, 'Form is invalid!')
                    return render(request, 'prot_postform.html', {'form': form,'login_context': login_details})
                form.save(sessionid=request.session['user_id'])
                messages.success(request, 'Form submitted successfully!')
                form = ProtPostForm()
                return redirect('../')
            else:
                form = ProtPostForm(form)
                messages.error(request, 'Form is invalid!')
                return render(request, 'prot_postform.html', {'form': form,'login_context': login_details})
        else:
            form = ProtPostForm()
            return render(request, 'prot_postform.html', {'form': form,'login_context': login_details})
    else:
        redirect('./')
        return render(request, 'main.html')
