from django.db import models

# Create your models here.
class Spreadsheet(models.Model):
    file = models.FileField(upload_to='spreadsheets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name

class PDFReport(models.Model):
    file = models.FileField(upload_to='pdf_reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
    
# upload file 
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    