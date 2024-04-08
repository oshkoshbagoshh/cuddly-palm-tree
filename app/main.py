# main entry way for app
# from flask import Flask

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import os, traceback


# Flask app setup site
site = Flask(__name__)
site.config["UPLOAD_DIR"] = "uploads"
site.config["OUTPUT_DIR"] = "reports"
site.config["PLOT_DIR"] = "plots"

web_paths_list = ["UPLOAD_DIR", "OUTPUT_DIR", "PLOT_DIR"]

for dir in ["UPLOAD_DIR", "OUTPUT_DIR", "PLOT_DIR"]:
    if not os.path.exists(site.config[dir]):
        os.mkdir(site.config[dir])

ALLOWED_EXTENSIONS = {"xlsx", "xls", "ods"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_spreadsheet(filename):
    # read spreadsheet
    # TODO: change this to fit based off what the file will have
    spradsheet = pd.read_excel(filename, sheet_name=["Sales", "Inventory"])
    sales_data = spradsheet["Sales"]
    inventory_data = spradsheet["Inventory"]

    # processing
    total_sales = sales_data["Amount"].sum()

    # Generate plot
    sales_data["Amount"].plot(kind="bar")
    plt.title("Sales Data")
    plot_path = os.path.join(site.config["PLOT_DIR"], "sales_plots.png")
    plt.savefig(plot_path)
    plt.close()

    # Create a PDF Report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Sales: {total_sales}", ln=True)
    pdf.image(plot_path, x=10, y=20, w=180)
    pdf.output(os.path.join(site.config["OUTPUT_DIR"], "report.pdf"))


@site.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Sales Report Generator</title>
</head>
<body>
    <h1>Upload sales spreadsheet</h1>
    <form action="/process" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Generate report">
    </form>
</body>
</html>
"""


@site.route("/process", methods=["POST"])
def upload_and_process():
    if "file" not in request.files:
        return "Invalid request."

    file = request.files["file"]
    if file.filename == "":
        return "No file selected."

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(site.config["UPLOAD_DIR"],filename)
        file.save(filepath)

        try:
            process_spreadsheet(filepath)
            return send_from_directory(
                directory=site.config["OUTPUT_DIR"],
                path="report.pdf",
                as_attachment=True,
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
            return "An error occurred. Please ensure that your spreadsheet is correctly formatted and try again."


if __name__ == "__main__":
    site.run(host="0.0.0.0", port=8080, debug=True)
    
