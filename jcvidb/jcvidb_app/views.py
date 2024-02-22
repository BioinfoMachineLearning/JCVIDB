# from django.core.checks import messages
import time

from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User, Proteomic, Role
from .details_form import DetailsForm
from .registration_form import RegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
def main(request):
    if request != "POST":


        aProteomics_data_list = Proteomic.objects.all().values()

        paginator = Paginator(aProteomics_data_list, 5)
        page_number =request.GET.get('page')

        # if page_number is None:
        #     page_number=1

        try:
            aProteomics_data = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            aProteomics_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            aProteomics_data = paginator.page(paginator.num_pages)
        print(page_number)
        return render(request, 'main.html', { 'aProteomics_data': aProteomics_data})

        # return HttpResponse(template.render(context, request))
    # else:
    #     print('here')
    #     form = request.POST
    #     print(form.cleaned_data['PGAN'])
    #     print(form.cleaned_data['id'])
    #
    #     aProteomics_data = Proteomic.objects.get(id=id)
    #     print(aProteomics_data)


def details(request, id):
    aProteomics_data = Proteomic.objects.get(id=id)
    print(aProteomics_data.id)
    template = loader.get_template('details.html')
    context = {
        'prot_data': aProteomics_data,
    }
    return HttpResponse(template.render(context, request))


def search(request):
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
    if name =="":
        name= request.GET.get('query')
    return render(request, 'search.html', {'results': results, 'search_query': name})


def create_User(request):
    if request.method == 'POST':
        print("here")
        form = RegistrationForm(request.POST )
        print(form)
        if form.is_valid():
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            form.instance.password = hashed_password
            form.save()
            messages.success(request, 'Form submitted successfully!')
            # time.sleep(2)
            form=RegistrationForm()
            return redirect('../')
        else:
            print(form.errors)
            form = RegistrationForm(form)
            messages.error(request, 'Form is invalid!')
            return render(request, 'registration_form.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration_form.html', {'form': form})

