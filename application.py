from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
BACKGROUND_FOLDER = "static/backgrounds"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKGROUND_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-backgrounds')
def get_backgrounds():
    """Return a list of available background images."""
    images = [img for img in os.listdir(BACKGROUND_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return jsonify(images)

@app.route('/background/<filename>')
def serve_background(filename):
    """Serve background images from the directory."""
    return send_from_directory(BACKGROUND_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload():
    """Handle object image upload & remove background."""
    object_img = request.files.get("object")
    if object_img:
        obj_path = os.path.join(UPLOAD_FOLDER, "object.png")
        input_img = Image.open(object_img).convert("RGBA")
        output_img = remove(input_img)  # Remove background
        output_img.save(obj_path, format="PNG")
        return jsonify({"object": f"/{obj_path}"})
    return jsonify({"error": "No file provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
