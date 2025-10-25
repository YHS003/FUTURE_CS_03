# app.py - Flask app for secure file upload/download (AES-128 CBC)

import os, json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from io import BytesIO
from crypto import encrypt_bytes, decrypt_bytes  # Custom encryption/decryption functions

# -------------------------------------------------------------
# Load environment variables (.env file)
# -------------------------------------------------------------
load_dotenv()

# Get AES encryption key from environment variable
AES_KEY_HEX = os.getenv('AES_KEY_HEX')
if not AES_KEY_HEX:
    raise SystemExit('AES_KEY_HEX not set in .env')

# Convert hex key to bytes
AES_KEY = bytes.fromhex(AES_KEY_HEX)

# Validate AES key length (16 bytes = 128 bits)
if len(AES_KEY) != 16:
    raise SystemExit('AES_KEY_HEX must be 16 bytes (32 hex chars) for AES-128')

# -------------------------------------------------------------
# Define storage paths
# -------------------------------------------------------------
BASE = Path(__file__).parent
UP_ENC = BASE / 'uploads_encrypted'  # Folder for encrypted files
UP_ENC.mkdir(exist_ok=True)          # Create if not exists
METADATA = BASE / 'metadata.json'    # Metadata file to store info about uploaded files

# -------------------------------------------------------------
# Initialize Flask app
# -------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET') or 'dev-secret'  # Used for session flash messages

# -------------------------------------------------------------
# Helper functions for metadata management
# -------------------------------------------------------------
def load_metadata():
    """Load metadata from JSON file (maps stored filenames to original names and sizes)."""
    if METADATA.exists():
        try:
            return json.loads(METADATA.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}

def save_metadata(d):
    """Save updated metadata back to the JSON file."""
    METADATA.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.route('/')
def home():
    """Redirect root URL to the upload page."""
    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET','POST'])
def upload():
    """Handle file uploads and encryption."""
    if request.method == 'POST':
        # Check if file exists in the request
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        f = request.files['file']

        # Validate filename
        if f.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        filename = secure_filename(f.filename)  # Sanitize filename
        data = f.read()  # Read file bytes

        # Try to encrypt file content
        try:
            blob = encrypt_bytes(AES_KEY, data)
        except Exception as e:
            flash('Encryption failed: ' + str(e), 'error')
            return redirect(request.url)

        # Save encrypted file to uploads_encrypted/
        stored_name = filename + '.enc'
        path = UP_ENC / stored_name
        path.write_bytes(blob)

        # Save file metadata (for download name & size)
        md = load_metadata()
        md[stored_name] = {'original_filename': filename, 'size': len(blob)}
        save_metadata(md)

        flash('File encrypted and saved as ' + stored_name, 'success')
        return redirect(request.url)

    else:
        # On GET request → Show upload page with stored files
        md = load_metadata()
        return render_template('upload.html', files=md)

@app.route('/download/<stored_name>')
def download(stored_name):
    """Handle decryption and file download."""
    stored_name = secure_filename(stored_name)
    path = UP_ENC / stored_name

    # Ensure file exists
    if not path.exists():
        flash('File not found', 'error')
        return redirect(url_for('upload'))

    # Read encrypted file bytes
    blob = path.read_bytes()

    # Try to decrypt file
    try:
        plaintext = decrypt_bytes(AES_KEY, blob)
    except Exception as e:
        flash('Decryption failed: ' + str(e), 'error')
        return redirect(url_for('upload'))

    # Retrieve original filename from metadata
    md = load_metadata()
    orig = md.get(stored_name, {}).get('original_filename', 'download.bin')

    # Prepare decrypted file for sending
    bio = BytesIO(plaintext)
    bio.seek(0)

    # Send file as downloadable attachment
    return send_file(bio, as_attachment=True, download_name=orig)

# -------------------------------------------------------------
# Run the Flask development server
# -------------------------------------------------------------
if __name__ == '__main__':
    # Host 0.0.0.0 allows access from other devices on same network
    app.run(host='0.0.0.0', port=5000, debug=True)
