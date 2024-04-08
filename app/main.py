# main entry way for app
# from flask import Flask

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from fpdf import FPDF
from flask import Flask,request, send_from_directory
from werkzeug.utils import secure_filename
import os, traceback


# Flask app setup site
site = Flask(__name__)
site.config["UPLOAD_DIR"] = "uploads"
site.config["OUTPUT_DIR"] = "reports"
site.config["PLOT_DIR"] = "plots"

web_paths_list  = ["UPLOAD_DIR", "OUTPUT_DIR", "PLOT_DIR"]


for dir in web_paths_list:
    if not os.path.exists(site.config[id]):
        os.mkdir(site.config[dir])
    
    # spreadsheet style only  
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'ods', 'csv', 'tsv'}

def allowed_file(filename):
    allowed_file(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_spreadsheet(filename):
    # read spreadsheet
    # TODO: change this to fit based off what the file will have
    spradsheet = pd.read_excel(filename,sheet_name=["Sales","Inventory"])
    sales_data = spradsheet["Sales"] 
    inventory_data = spradsheet["Inventory"]
    
    # processing
    total_sales = sales_data['Amount'].sum()
    
    #Generate plot
    sales_data['Amount'].plot(kind='bar')
    plt.title('Sales Data')
    plot_path = os.path.join(site.config["PLOT_DIR"], "sales_plots.png")
    plt.savefig(plot_path)
    plt.close()
    
    
    # Create a PDF Report 
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10 ,f"Total Sales: {total_sales}", ln=True)
    pdf.image(plot_path, x=10, y=20, w=180)
    pdf.output(os.path.join(site.config["OUTPUT_DIR"], "report.pdf"))
    

    
    
    
    
    
    



