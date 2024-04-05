# forms to handle the input from the user for the pdf report generation
from django import forms
from .models import Spreadsheet, Document

class SpreadsheetUploadForm(forms.ModelForm):
    class Meta:
        model = Spreadsheet
        fields = ('file',)
        
        
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
        
