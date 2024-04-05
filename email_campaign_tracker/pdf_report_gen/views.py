from django.shortcuts import redirect, render
from .forms import SpreadsheetUploadForm, DocumentUploadForm
import pandas as pd
from reportlab.pdfgen import canvas
from django.http import FileResponse
from .models import Spreadsheet
from .models import PDFReport
from .models import Document

# Create your views here.


# ========================
def upload_spreadsheet(request):
    if request.method == "POST":
        form = SpreadsheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("some-view")
    else:
        form = SpreadsheetUploadForm()
    return render(request, "upload.html", {"form": form})


# TODO: need to come up wih calculations


# generate the pdf report
def generate_pdf(request, spreadsheet_id):
    # get the spreadsheet
    spreadsheet = Spreadsheet.objects.get(id=spreadsheet_id)

    # read into a pandas dataframe
    df = pd.read_excel(spreadsheet.spreadsheet)

    # create a new PDF file
    c = canvas.Canvas("report.pdf")
    # add some content to the PDF, based on the dataframe
    # this is just a simple example
    for i, row in df.iterrows():
        text = ", ".join(str(x) for x in row)
        c.drawString(100, 800 - i * 100, text)

        # close and save the PDF
    c.save()

    # open the PDF file and return it as a response
    with open("somefile.pdf", "rb") as f:
        pdf = FileResponse(f, content_type="application/pdf")
        pdf["Content-Disposition"] = "inline; filename=somefile.pdf"
        return pdf

# download the pdf
def download_pdf(request, pdf_id):
        pdf = PDFReport.objects.get(id=pdf_id)
        # open the PDF file and return it as a response
        with open(pdf.pdf, "rb") as f:
            response = FileResponse(f, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="{pdf.file.name}"'
            return response


# ========================
# handle form submission and save the file
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("some-view")
    else:
        form = DocumentUploadForm()
    return render(request, "upload.html", {"form": form})


# ========================
# handle file downloads
def download_document(request, document_id):
    document = Document.objects.get(id=document_id)
    with open(document.file, "rb") as f:
        response = FileResponse(f, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{document.file.name}"'
        return response


# ========================
# list documents
def list_documents(request):
    documents = Document.objects.all()
    return render(request, "documents.html", {"documents": documents})
