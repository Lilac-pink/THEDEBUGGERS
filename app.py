from flask import Flask, render_template, request, jsonify
import os
import cv2
import base64
import numpy as np
from werkzeug.utils import secure_filename
import google.generativeai as genai

# ------------------ CONFIG ------------------ #
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Replace with your Gemini API key (free from https://aistudio.google.com/app/apikey)
genai.configure(api_key="AIzaSyADTeHFIcsrGWYMF7ywduAvN12MGvgOXyM")

# Gemini model (fast + free tier)
model = genai.GenerativeModel("gemini-1.5-flash")

# Memory for last summary
last_summary = None

# ------------------ FRAME EXTRACTION ------------------ #
def extract_frames(video_path, num_frames=3):
    frames_base64 = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video file.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, frame = cap.read()
        if success:
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            frames_base64.append(img_base64)

    cap.release()
    return frames_base64

# ------------------ GEMINI ANALYSIS ------------------ #
def analyze_video(video_path):
    global last_summary
    try:
        frames = extract_frames(video_path, num_frames=3)
        if not frames:
            return "Error: Could not extract any frames from the video."

        # Prepare Gemini input
        parts = [{"mime_type": "image/jpeg", "data": base64.b64decode(frame)} for frame in frames]

        response = model.generate_content(
            contents=[
                "Analyze these images from a video and give a short summary.",
                *parts
            ]
        )

        last_summary = response.text.strip() if response.text else "No summary generated."
        return last_summary

    except Exception as e:
        print("Error analyzing video:", e)
        return f"Error processing video: {str(e)}"

# ------------------ SIMPLE CHATBOT ------------------ #
@app.route('/chat', methods=['POST'])
def chat():
    global last_summary
    data = request.json
    question = data.get("question", "")

    if not last_summary:
        return jsonify({"answer": "No video analyzed yet. Please upload a video first."})

    # Simple answer logic: combine summary + question
    answer = f"Based on the video summary: {last_summary}\n\nMy answer: {question} likely relates to the main content shown."
    return jsonify({"answer": answer})

# ------------------ FLASK ROUTES ------------------ #
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST' and 'video' in request.files:
        file = request.files['video']
        if file.filename:
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(video_path)
            summary = analyze_video(video_path)
            try:
                os.remove(video_path)
            except:
                pass
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
