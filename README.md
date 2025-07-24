# 🎙️ VoiceTaskAI — Voice-Driven Task Assignment (Local Demo)

---



## 1. 📛 Project Title & Tagline

> **VoiceTaskAI**  
> A voice-activated internal task manager that turns structured spoken instructions into actionable tasks using local Whisper transcription and Python NLP.

Designed as a local-first prototype, VoiceTaskAI enables managers to assign tasks by saying commands like:

🗣️ *“Assign 'Review Q3 report' to Alex for Project Mercury, deadline Friday.”*

The system extracts all fields from structured speech and saves the task for immediate use, demonstrating the feasibility of voice-driven workflows for internal teams.


---



## 2. 🔍 Overview / Abstract (V1 Demo)

**VoiceTaskAI** is a local-first prototype for a voice-driven internal task management system. It allows managers to assign tasks by speaking clearly structured commands directly into the browser, eliminating the need for typing or manual data entry.

The system is designed around a **command grammar**, where the user speaks instructions like:

🗣️ *“Assign ‘create the landing page’ to Alex for Project Mercury, deadline Friday.”*

This voice input is captured on the frontend, sent to the backend, transcribed locally using OpenAI’s Whisper model, and parsed into structured fields using a lightweight rule-based NLP pipeline built on spaCy. The result is a clean, structured task object ready for display or tracking.

This prototype is:
- **Fully local** — no cloud dependencies, ensuring privacy
- **Cost-free to run** — ideal for early-stage adoption
- **Demo-ready** — built to prove technical feasibility ahead of formal contract signing

While the current version uses deterministic parsing and rigid speech formatting, the system is designed to evolve into a more flexible architecture using ML-based slot-filling models to tolerate slight variations in phrasing — without relying on large LLMs.

VoiceTaskAI demonstrates that voice-activated task assignment is not only possible, but practical and scalable for internal team environments.


---

## 3. 🎯 Use Case / Example Scenario

_TODO: Describe what a manager might say (e.g., "Assign ‘finalize the report’ to Alex by Friday") and how the system turns it into structured data._

---

## 4. 💻 Tech Stack

### 🧠 Machine Learning & NLP
- **Whisper (base model)** – Local automatic speech recognition (ASR) for transcribing voice recordings
- **spaCy** – Rule-based NLP pipeline for extracting structured task components from transcribed text
- **dateparser** – Parses natural language dates (e.g., "Friday", "next week") into standard ISO format

### ⚙️ Backend
- **FastAPI** – Python web framework used to expose a `/record` endpoint that accepts voice files
- **Uvicorn** – ASGI server used for local development and testing

### 🗃️ Task Storage
- **In-memory Python dictionary** – Stores task objects during runtime (no persistence layer)
- **Optional JSON file** – Used to persist tasks between runs for demonstration purposes

### 🛠️ System Tools
- **ffmpeg** – Used to convert incoming `.webm` files to `.wav`, which is the format required by Whisper
- **Python 3.9+** – Required to run all core components

---

> 📌 Note: There is no frontend or UI in this version of the prototype. Voice recordings are provided manually or via Postman/Swagger uploads to the `/record` endpoint.
---



## 5. 🔁 Architecture & Flow

The VoiceTaskAI prototype follows a simple linear pipeline to convert structured voice recordings into task objects.

### 🔄 Data Flow Summary

1. **Voice File Submission**
   - A manager records a voice command (e.g., using any tool) and submits the `.webm` file to the `/record` endpoint via Swagger, Postman, or curl.

2. **Audio Conversion**
   - The backend uses `ffmpeg` to convert the uploaded `.webm` file to `.wav` format, which is required by Whisper.

3. **Speech Transcription**
   - The `.wav` file is transcribed locally using the Whisper model, producing a structured command string like:
     ```
     Assign ‘create landing page’ to Alex for Project Mercury, deadline Friday.
     ```

4. **NLP Parsing**
   - The transcription is processed using a custom rule-based pipeline built with `spaCy` and `regex`.
   - The parser extracts:
     - Task title
     - Assignee
     - Project
     - Deadline

5. **Task Creation**
   - A structured task object is created and stored in memory (or optionally in a JSON file for persistence).

6. **Result Delivery**
   - The backend returns the parsed task as a JSON response to the client.
e._

---



