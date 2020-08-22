from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .tasks import sleepy, sendemailtask, parseXML, changeText
from .forms import UploadXMLForm,ChangeTextForm
from django.shortcuts import redirect
from xml_app.models import (
    Element,
    Parentship,
    Attribute,
    FileXML
)
# Create your views here.



def multiple_forms(request):
    if request.method == 'POST':
        upload_form = UploadXMLForm(request.POST)
        changetext_form = ChangeTextForm(request.POST)
        print(request.POST)
        if upload_form.is_valid() and 'oldText' not in request.POST:
            print("girdim")
            parseXML.delay(request.user.email , upload_form.cleaned_data['name'],upload_form.cleaned_data['newText'])
            return redirect('/' )
        elif changetext_form.is_valid():
            
            changeText.delay(
                request.user.email,
                changetext_form.cleaned_data['name'].id,
                changetext_form.cleaned_data['oldText'],
                changetext_form.cleaned_data['newText']
                )
            
            return redirect('/' )
    else:
        upload_form = UploadXMLForm()
        changetext_form = ChangeTextForm()
    return render(request, 'xml_app/xmlapp.html', {
        'upload_form': upload_form,
        'changetext_form': changetext_form,
    })

