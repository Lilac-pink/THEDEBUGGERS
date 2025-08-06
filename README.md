# 🎥 Visual Understanding Chat Assistant

## 📌 Project Overview
This project is a **Flask-based Visual Understanding Chat Assistant** that:
1. Accepts a video upload from the user.
2. Extracts frames from the video.
3. Uses **Google Gemini API** to generate a short summary of the video.
4. Remembers the summary and allows the user to **chat** about the video content.

It is designed as a **lightweight prototype** for hackathons, research, or early-stage projects involving **video understanding + conversational AI**.

---

## 🛠 Code Overview

### 1. **Video Upload & Storage**
- Uses **Flask** to handle file uploads.
- Stores videos in `uploads/` directory temporarily.

### 2. **Frame Extraction**
- Uses **OpenCV** to:
  - Open the uploaded video.
  - Select 3 evenly spaced frames.
  - Convert frames to **Base64-encoded JPEG**.

### 3. **Video Analysis with Gemini**
- Sends extracted frames to **Gemini API** (`gemini-1.5-flash`) for quick, free-tier analysis.
- Receives a **short text summary**.

### 4. **Chatbot Functionality**
- Stores last summary in memory.
- Answers user questions by combining stored summary + simple reasoning.

---

## 🏗 High-Level Architecture

![Architecture Diagram](architecture.png)

**Flow:**
1. User uploads video.
2. Backend extracts frames.
3. Frames sent to Gemini API.
4. Gemini returns video summary.
5. User can chat about the video.
6. Chatbot uses stored summary to answer.

---

## 💻 Tech Stack & Justifications

| Component      | Technology Used        | Why This Choice? |
|----------------|------------------------|------------------|
| Backend        | Flask (Python)         | Lightweight, easy to build REST APIs. |
| Video Processing | OpenCV               | Reliable, widely used for frame extraction. |
| AI Model       | Google Gemini API      | Free tier available, supports multimodal input. |
| File Storage   | Local `uploads/` folder| Simple for prototypes, no cloud setup needed. |
| Frontend       | HTML + Jinja Templates | Fast to implement with Flask for hackathons. |

---

## ⚙ Backend Setup

1. **Clone Repository**
```bash
git clone https://github.com/your-username/video-chat-assistant.git
cd video-chat-assistant
