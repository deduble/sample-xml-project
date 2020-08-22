from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .tasks import sleepy, sendemailtask, parseXML
from .forms import UploadXMLForm,ChangeTextForm
from django.shortcuts import redirect
# Create your views here.
from .multiforms import MultiFormsView
from django.urls import reverse, reverse_lazy



def multiple_forms(request):
    if request.method == 'POST':
        upload_form = UploadXMLForm(request.POST)
        changetext_form = ChangeTextForm(request.POST)
        if upload_form.is_valid():
            # Do the needful
            return redirect('/' )
        if changetext_form.is_valid():
            # Do the needful
            return redirect('/' )
    else:
        upload_form = UploadXMLForm()
        changetext_form = ChangeTextForm()
            
    return render(request, 'xml_app/xmlapp.html', {
        'upload_form': upload_form,
        'changetext_form': changetext_form,
    })

