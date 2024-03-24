from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import T5Tokenizer, T5ForConditionalGeneration
import spacy
from summarizer import Summarizer
from string import punctuation
from collections import Counter
from heapq import nlargest

# Hugging Face() T5, BART, etc.) Gensim, spaCy, OpenAI, BERT
app = Flask(__name__)
app.debug = True
nlp = spacy.load("en_core_web_sm")
summarizer = Summarizer(nlp)

def process_transcript(transcripts, section_length=300):
    summaries = []
    section_start = 0
    section = []

    for item in transcripts:
        item_end_time = item['start'] + item['duration']
        if item_end_time <= section_start + section_length:
            section.append(item['text'])
        else:
            transcript = ' '.join(section)
            print(f"Transcript: {transcript}")  # Debugging line

            summary = summarizer.openai_summarize(transcript)
            print(f"Summary: {summary}")  # Debugging line

            summaries.append({f"{round(section_start/60)}-{round((section_start + section_length)/60)} minutes": summary})
            section_start = item['start']
            section = [item['text']]

    if section:
        transcript = ' '.join(section)
        summary = summarizer.openai_summarize(transcript)
        summaries.append({f"{round(section_start/60)}-{round((section_start + section_length)/60)} minutes": summary})

    return { "Summarized Video:": summaries }

@app.route('/api/serverCheck', methods=['GET'])
def get_data():
    data = {"test message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    url = request.json.get('url')
    video_id = url.split('watch?v=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    processed_transcript = process_transcript(transcript)
    return jsonify(processed_transcript)

if __name__ == '__main__':
    app.run(port=5000)