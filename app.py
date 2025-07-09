from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from utils.metadata import analyze_metadata
from utils.ela import generate_ela_image, calculate_ela_difference
from utils.frequency import calculate_high_freq_ratio
from utils.ai_detector import estimate_ai_likelihood
from utils.scan_db import has_been_scanned, record_scan

UPLOAD_FOLDER = 'uploads'
ELA_FOLDER = 'static/ela'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            result = {'error': 'No file part in the request'}
        file = request.files['file']
        if file.filename == '':
            result = {'error': 'No selected file'}
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if has_been_scanned(filename):
                result = {'cached': True, 'filename': filename}
            else:
                metadata = analyze_metadata(filepath)
                ela_path, ela_max_diff = generate_ela_image(filepath)
                high_freq_ratio = calculate_high_freq_ratio(filepath)
                ai_score, ai_flags = estimate_ai_likelihood(filepath)

                record_scan(filename)

                result = {
                    'metadata': metadata,
                    'ela_max_diff': ela_max_diff,
                    'high_freq_ratio': high_freq_ratio,
                    'ai_score': ai_score,
                    'ai_flags': ai_flags,
                    'ela_path': ela_path,
                    'filename': filename
                }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
