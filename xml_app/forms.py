from .models import FileXML
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit, Field




class UploadXMLForm(forms.Form):
    name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'File Name'}))
    newText     = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'URL'}))

    def __init__(self, *args, **kwargs):
        super(UploadXMLForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'newText',
            Submit('submit','Submit',css_class='btn-success')
        )


class ChangeTextForm(forms.Form):
    name = forms.ModelChoiceField(label='' , required=False, queryset=FileXML.objects.all())
    oldText    = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Old Text'}))
    newText     = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'New Text'}))

    def __init__(self, *args, **kwargs):
        super(ChangeTextForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'oldText',
            'newText',
            Submit('submit','Submit',css_class='btn-success')
        )