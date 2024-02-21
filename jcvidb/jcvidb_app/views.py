from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User, Proteomic, Role
from .details_form import DetailsForm


def main(request):
    if request != "POST":
        aProteomics_data = Proteomic.objects.all().values()
        template = loader.get_template('main.html')
        context = {
            'prot_data': aProteomics_data,
        }
        return HttpResponse(template.render(context, request))
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
    results = Proteomic.objects.filter(PGAN__icontains=name)
    print(len(results))
    return render(request, 'search.html', {'results': results, 'search_query': name})
