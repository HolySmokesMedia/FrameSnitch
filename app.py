from flask import Flask, request, render_template, send_from_directory
import os
from utils import ela, metadata, frequency, ai_detector
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
ELA_FOLDER = 'static/ela'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ELA_FOLDER'] = ELA_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ELA_FOLDER, exist_ok=True)

def generate_filename(filename):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    name, ext = os.path.splitext(filename)
    safe_name = secure_filename(f"{timestamp}-{name}{ext}")
    return safe_name

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    ela_path = None
    filename = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = generate_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            ela_image_path = ela.create_ela_image(filepath, filename)
            ela_path = os.path.join(app.config["ELA_FOLDER"], ela_image_path)
            ela_result = ela.analyze_ela_image(ela_path)
            metadata_result = metadata.extract_metadata(filepath)
            freq_result = frequency.analyze_frequency(filepath)
            ai_prediction = ai_detector.predict_image(filepath)

            result = {
                "ela_result": ela_result,
                "metadata": metadata_result,
                "frequency": freq_result,
                "ai_prediction": ai_prediction,
            }

    return render_template("index.html", result=result, ela_path=ela_path, filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/static/ela/<filename>")
def static_ela_file(filename):
    return send_from_directory(app.config["ELA_FOLDER"], filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
