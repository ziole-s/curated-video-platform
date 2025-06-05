from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_folder='frontend')  # static_folder used for fallback serving

VIDEO_BASE_PATH = os.path.join(os.path.dirname(__file__), 'video_base')

@app.route('/api/videos')
def get_videos():
    category = request.args.get('category', '').lower()
    filename = f"{category}_category.json"
    filepath = os.path.join(VIDEO_BASE_PATH, filename)

    if not os.path.exists(filepath):
        return jsonify([]), 404

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return jsonify([]), 500

    return jsonify(data)

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Serve static assets like JS, CSS, images
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(debug=True)
