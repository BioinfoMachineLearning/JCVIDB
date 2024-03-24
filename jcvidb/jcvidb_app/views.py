# from django.core.checks import messages
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render
from django.template import loader

from .models import User, Basic_data
from .datapost_form import DataPostForm
from .protupdate_form import ProtUpdateForm
from .registration_form import RegistrationForm

UPLOAD_DIR = '/Users/rajshekhorroy/JCVIDB/jcvidb/'

from django.http import HttpResponseNotFound, FileResponse
import os
from django.conf import settings

def download_file(request, file_name):
    # Define the directory where the files are stored
    # upload_dir = os.path.join(settings.BASE_DIR, 'media')
    upload_dir = os.path.join(UPLOAD_DIR, 'media')
    # Check if the file exists
    file_path = os.path.join(upload_dir, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        return HttpResponseNotFound("File not found")

    # Open the file and serve it as a response
    with open(file_path, 'rb') as file:
        # Determine the content type based on the file extension
        file_content = file.read()

    response = HttpResponse(file_content, content_type='application/octet-stream')

    # Set the Content-Disposition header to indicate attachment
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'

    return response


def set_session_values(request):
    try:
        login_context = {"id": request.session['user_id'],
                         "last_name": request.session['last_name'],
                         "admin": request.session['admin']}
        print("admin")
        print(request.session['admin'])
        print(login_context['admin'])
        return login_context
    except:
        return None


def handle_uploaded_file(uploaded_file):
    print('handle_uploaded_file')
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    with open(os.path.join(UPLOAD_DIR, uploaded_file.name), 'wb+') as destination:
        print('file uploaded')
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


def main(request):
    try:
        if request.session['user_id'] and request.session['last_name']:
            print("here")
            print(request.session['user_id'])
            print(request.session['last_name'])
            login_context = {"id": request.session['user_id'],
                             "last_name": request.session['last_name'],
                             "admin": request.session['admin']}
    except:
        login_context = None
        print("no session found")
    print(request)
    if request != "POST":

        aProteomics_data_list =   Basic_data.objects.filter(approved=1)
        paginator = Paginator(aProteomics_data_list, 10)
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
    login_context = set_session_values(request)
    aProteomics_data = Basic_data.objects.get(id=id)
    print(aProteomics_data.id)
    template = loader.get_template('details.html')
    context = {
        'prot_data': aProteomics_data,
        'login_context': login_context
    }
    return HttpResponse(template.render(context, request))


def search(request):
    login_details = set_session_values(request)
    name = request.GET.get('PGAN_name', '')
    results_list = Basic_data.objects.filter(PGAN__icontains=name)
    results_list =results_list.filter(approved=1)
    print(len(results_list))

    page_number = request.GET.get('page')
    paginator = Paginator(results_list, 10)

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
    return render(request, 'search.html', {'results': results, 'search_query': name, 'login_context': login_details})


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
    if 'last_name' in request.session:
        del request.session['last_name']
    if 'admin' in request.session:
        del request.session['admin']
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
            # print("success")
            request.session['user_id'] = login_details.id  # Assuming user ID is 1
            request.session['last_name'] = login_details.lastname
            if login_details.role_id == 3:
                request.session['admin'] = False
            else:
                request.session['admin'] = True

            login_context = {"id": request.session['user_id'],
                             "last_name": request.session['last_name'],
                             "admin": request.session['admin']}

            # print("success")

            return redirect('../')  # Assuming 'dashboard' is the name of the URL pattern for the dashboard page
        else:
            # Display error message (optional)
            messages.error(request, 'Invalid username or password')

    return render(request, 'sign_in.html', context=login_context)


def sign_out(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['last_name']
        del request.session['admin']
    redirect('../')
    print('redirecting')
    return render(request, 'sign_in.html', context=None)


def prot_post(request):
    # print(request.session['user_id'])
    # print(request.session['last_name'])
    login_details = set_session_values(request)
    if login_details != None:
        if request.method == 'POST':
            form = DataPostForm(request.POST, request.FILES)
            if form.is_valid():
                # try:
                #     uploaded_file = request.FILES['attachment']
                #     # handle_uploaded_file(uploaded_file)
                # except:
                #     form = DataPostForm(form)
                #     messages.error(request, 'Form is invalid!')
                #     return render(request, 'data_postform.html', {'form': form, 'login_context': login_details})

                instance_object = form.save(sessionid=request.session['user_id']).id
                messages.success(request, 'Form submitted successfully!')
                form = DataPostForm()
                return redirect('../file_upload/'+str(instance_object))
            else:
                print(form.errors)
                form = DataPostForm(form)
                messages.error(request, 'Form is invalid!')
                return render(request, 'data_postform.html', {'form': form, 'login_context': login_details})
        else:
            form = DataPostForm()
            return render(request, 'data_postform.html', {'form': form, 'login_context': login_details})
    else:
        redirect('./')
        return render(request, 'main.html')


def appprove_post(request):
    login_context = set_session_values(request)

    if request != "POST":
        aProteomics_data_list = Basic_data.objects.filter(approved=0)
        paginator = Paginator(aProteomics_data_list, 10)
        page_number = request.GET.get('page')
        try:
            aProteomics_data = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            aProteomics_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            aProteomics_data = paginator.page(paginator.num_pages)

        return render(request, 'approve_list.html',
                      {'aProteomics_data': aProteomics_data, 'login_context': login_context})


def update_prot(request, id):
    login_details = set_session_values(request)
    print(login_details['admin'])
    form = ProtUpdateForm()
    if login_details['admin'] == True:
        if request.method == 'GET':
            item = Basic_data.objects.get(id=id)
            form = ProtUpdateForm(instance=item)
            return render(request, 'update_prot.html',
                      {'prot_data': item, 'login_context': login_details})

        else:
            item = Basic_data.objects.get(id=id)
            form = ProtUpdateForm(instance=item)
            item.approved = 1
            item.save()
            return redirect('../approve_post')

            # ProtUpdateForm.cleaned_data['PGAN']=item.PGAN

            # return redirect('./' + str(id))
        # return render(request, 'update_prot.html', {'form': form, 'login_context': login_details})

def file_upload(request, context_id):
    if request.method == 'GET':
        print(context_id)
        login_details = set_session_values(request)
        print(login_details["id"])
        return render(request, 'file_upload.html',
                          { 'login_context': login_details})
    elif request.method == 'POST':
        return None