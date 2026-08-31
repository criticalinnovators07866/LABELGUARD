from flask import Flask, render_template, request
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import os
from complaince import check_compliance
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")
TabError



@app.route("/check", methods=["POST"])
def check():

    if "product_image" not in request.files:
        return "No image uploaded"

    file = request.files["product_image"]

    if file.filename == "":
        return "Please select an image"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # OCR
    image = Image.open(filepath)
    extracted_text = pytesseract.image_to_string(image)

    text = extracted_text.lower()

    # Basic compliance checks
    checks, score = check_compliance(extracted_text)
    return render_template(
        "result.html",
        text=extracted_text,
        checks=checks,
        score=score
    )


if __name__ == "__main__":
    app.run(debug=True)