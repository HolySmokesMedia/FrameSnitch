from flask import Flask, request, render_template_string, redirect, url_for
import os
from PIL import Image
import io
import cv2
import numpy as np

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>FrameSnitch</title>
<h1>Upload an image</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=image>
  <input type=submit value=Upload>
</form>
{% if result %}
<h2>Result:</h2>
<p>{{ result }}</p>
{% endif %}
'''

def is_blurry(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var < 100  # Threshold can be tweaked

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template_string(HTML_TEMPLATE, result="No image file provided.")

        file = request.files['image']
        if file.filename == '':
            return render_template_string(HTML_TEMPLATE, result="No file selected.")

        try:
            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            blurry = is_blurry(cv_img)
            result = "Blurry" if blurry else "Clear"
            return render_template_string(HTML_TEMPLATE, result=result)

        except Exception as e:
            return render_template_string(HTML_TEMPLATE, result=f"Error: {str(e)}")

    return render_template_string(HTML_TEMPLATE, result=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
