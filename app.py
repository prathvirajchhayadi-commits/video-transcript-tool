from flask import Flask, render_template, request, send_file
import os
import whisper
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Transcript banaya
    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    transcript = result["text"]
    
    # Transcript save kiya
    with open(f"{filepath}_transcript.txt", "w") as f:
        f.write(transcript)
    
    return render_template('result.html', 
                         transcript=transcript,
                         filename=file.filename)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    tts = gTTS(text=text, lang='en')
    audio_file = "output_audio.mp3"
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
