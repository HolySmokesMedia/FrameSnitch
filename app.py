import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from analyze_image import analyze_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = analyze_image(filepath)
            return render_template(
                'index.html',
                filename=filename,
                risk_score=result['risk_score'],
                ai_score=result.get('ai_score'),
                analysis=result['analysis'],
                ela_image_path=result.get('ela_image_path')
            )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
