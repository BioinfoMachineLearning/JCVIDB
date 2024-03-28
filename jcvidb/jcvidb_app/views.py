# from django.core.checks import messages
import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .basic_data_display_object import file_data_display_object, col_data_display_object, basic_data_display_object, \
    user_data_display
from .models import User, Basic_data, column_data, File_data
from .datapost_form import DataPostForm, FileUploadPostForm, ColumnDataPostForm
from .protupdate_form import ProtUpdateForm
from .registration_form import RegistrationForm

# UPLOAD_DIR = '/Users/rajshekhorroy/JCVIDB/jcvidb/'
UPLOAD_DIR = '/Users/rajshekhorroy/JCVIDB/jcvidb/'
seperator = "_$_$_"
from django.http import HttpResponseNotFound, FileResponse
import os
from django.conf import settings


def get_csv_file_data(_file_name, columns_to_select, _page_number, _header_num):
    if _header_num > 0:
        # print(columns_to_select)
        upload_dir = os.path.join(UPLOAD_DIR, 'media')
        # print(upload_dir)
        file_path = os.path.join(upload_dir, _file_name)
        # print(file_path)
        if not os.path.exists(file_path):
            return []
        df = pd.read_excel(file_path, sheet_name=_page_number - 1, header=_header_num - 1)
        selected_columns_df = df.loc[:, columns_to_select]
        two_dimensional_array = selected_columns_df.values
        # print(two_dimensional_array)
        print(columns_to_select)

        my_2d_array = np.insert(two_dimensional_array, 0, columns_to_select, axis=0)
        return my_2d_array
    else:
        return None


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


# def handle_uploaded_file(uploaded_file):
#     print('handle_uploaded_file')
#     if not os.path.exists(UPLOAD_DIR):
#         os.makedirs(UPLOAD_DIR)
#     with open(os.path.join(UPLOAD_DIR, uploaded_file.name), 'wb+') as destination:
#         print('file uploaded')
#         for chunk in uploaded_file.chunks():
#             destination.write(chunk)


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

        aProteomics_data_list = Basic_data.objects.filter(approved=1)
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


def basic_data_display_mapper(_aProteomics_data):
    a_basic = basic_data_display_object()
    a_basic.id = _aProteomics_data.id
    a_basic.details = _aProteomics_data.details
    a_basic.references = _aProteomics_data.references
    a_basic.funding = _aProteomics_data.funding
    a_basic.createdBy = _aProteomics_data.createdBy
    a_basic.type = _aProteomics_data.type
    a_basic.approved = _aProteomics_data.approved
    a_basic.attachment = _aProteomics_data.attachment
    a_basic.creationDate = _aProteomics_data.creationDate

    return a_basic
def user_data_display_mapper(_user_data):
    an_user = user_data_display()
    an_user.id = _user_data.id
    an_user.firstname = _user_data.firstname
    an_user.lastname = _user_data.lastname
    an_user.role_id = _user_data.role_id
    an_user.email = _user_data.email
    an_user.occupation = _user_data.occupation
    an_user.phone = _user_data.phone
    an_user.instituation = _user_data.instituation
    an_user.approve = _user_data.approve

    return an_user

def details(request, id):
    login_context = set_session_values(request)
    aProteomics_data = Basic_data.objects.get(pk=id)

    a_basic_data_display_object = basic_data_display_mapper(aProteomics_data)
    print(aProteomics_data.id)
    file_data = aProteomics_data.file_data_set.all()
    print(file_data)
    i = 0
    # file_display_array = []
    for _file in file_data:
        print('count ' + str(i))
        i = i + 1
        a_file_display = file_data_display_object()
        a_file_display.id = _file.id
        a_file_display.file_ = _file.attachment
        col_arr = []
        print(a_file_display.id)
        col_data = _file.column_data_set.all()

        for _column in col_data:
            ### if multiple important sheet is present
            col_object = column_data.objects.get(id=_column.id)
            print(col_object)
            if len(col_object.column_names) > 0:
                print('here')
                array = get_csv_file_data(str(_file.attachment),
                                          col_object.column_names.replace("checkbox_", "").split(seperator),
                                          col_object.sheet_index,
                                          col_object.col_index)

                a_file_display.display_data = array
                # print(array)

        a_basic_data_display_object.add_file(a_file_display)

    # print(len(a_basic_data_display_object.file_array[0].display_data))
    template = loader.get_template('details.html')
    context = {
        'prot_data': a_basic_data_display_object,
        'login_context': login_context,
    }
    return HttpResponse(template.render(context, request))


def search(request):
    login_details = set_session_values(request)
    name = request.GET.get('PGAN_name', '')
    results_list = Basic_data.objects.filter(PGAN__icontains=name)
    results_list = results_list.filter(approved=1)
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
                instance_object = form.save(sessionid=request.session['user_id']).id
                messages.success(request, 'Form submitted successfully!')
                form = DataPostForm()
                return redirect('../file_upload/' + str(instance_object))
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
    a_basic_data_display_object = basic_data_display_object()
    if login_details['admin'] == True:
        if request.method == 'GET':
            aProteomics_data = Basic_data.objects.get(pk=id)
            a_basic_data_display_object = basic_data_display_mapper(aProteomics_data)
            file_data = aProteomics_data.file_data_set.all()
            for _file in file_data:
                a_file_display = file_data_display_object()
                a_file_display.id = _file.id
                a_file_display.file_ = _file.attachment
                col_data = _file.column_data_set.all()

                for _column in col_data:
                    col_object = column_data.objects.get(id=_column.id)
                    if len(col_object.column_names) > 0:
                        array = get_csv_file_data(str(_file.attachment),
                                                  col_object.column_names.replace("checkbox_", "").split(seperator),
                                                  col_object.sheet_index,
                                                  col_object.col_index)
                        a_file_display.display_data = array
                a_basic_data_display_object.add_file(a_file_display)
            return render(request, 'update_prot.html',
                          {'prot_data': a_basic_data_display_object, 'login_context': login_details})


        else:
            item = Basic_data.objects.get(id=id)
            print(item)
            form = ProtUpdateForm(instance=item)
            item.approved = 1
            item.save()
            print('../approve_post')
            return redirect('../approve_post')


@csrf_exempt
def preview_csv(request):
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST' and request.FILES.get('attachment'):
        # print(request.POST)
        page = int(request.POST.get('sheet_index').strip()) - 1
        # print(page)
        col_head = int(request.POST.get('col_index').strip()) - 1
        # print(col_head)
        try:
            csv_file = request.FILES['attachment']
            df = pd.read_excel(csv_file, sheet_name=page, header=col_head)
            final_array = df.columns.to_list()
            # print(final_array)
            # print(len(final_array))
            return JsonResponse({'headers': final_array})
        except:
            return JsonResponse({'headers': []})
    return JsonResponse({'headers': []})


def get_processed_options(_dict_option):
    option_str = ''

    for key, value in _dict_option.items():
        print(f"{key}: {value}")
        if key.startswith('checkbox_'):
            if len(option_str) == 0:
                option_str = str(key)
            else:
                option_str = option_str + seperator + str(key)

    return option_str


def file_upload(request, context_id):
    login_details = set_session_values(request)
    if request.method == 'GET':
        return render(request, 'file_upload.html',
                      {'login_context': login_details, 'added': False})
    elif request.method == 'POST':
        post_data = request.POST
        print(post_data.items)
        # for key, value in post_data.items():
        #     print(f"{key}: {value}")

        print('equest.method == POST')
        print(request.POST.get('col_index'))
        print(request.POST.get('checkbox'))

        file_form = FileUploadPostForm(request.POST, request.FILES)

        column_form = ColumnDataPostForm(request.POST)
        if file_form.is_valid() and column_form.is_valid():
            # basic_data = Basic_data.objects.get(id=context_id)

            # a_File_data =  File_Data(basic_data_id=context_id,attachment=request.FILES[''])
            option_str = get_processed_options(post_data)
            print(option_str)
            file_instance = file_form.save(context_id, True)
            column_instance = column_form.save(file_instance, True, option_str)
            return render(request, 'file_upload.html',
                          {'login_context': login_details, 'added': True})
        else:
            return render(request, 'file_upload.html',
                          {'login_context': login_details, 'errors': file_form.errors, 'added': False})


def profile_view(request):
    login_context = set_session_values(request)
    user_data = User.objects.get(pk=login_context['id'])
    display_user_data = user_data_display_mapper(user_data)
    # Basic_data.objects.filter(approved=1)
    all_post = Basic_data.objects.filter(createdBy_id=user_data)
    approved_post =all_post.filter(approved=1)
    unapproved_post = all_post.filter(approved=0)
    display_user_data.approved_posts=approved_post
    display_user_data.unapproved_posts=unapproved_post

    print(len(display_user_data.approved_posts))
    print(len(display_user_data.unapproved_posts))
    template = loader.get_template('profile.html')
    context = {
        'user_data': display_user_data,
        'login_context': login_context,
    }
    return HttpResponse(template.render(context, request))
