from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import T5Tokenizer, T5ForConditionalGeneration
import spacy
from spacy_text_summarizer import SpacyTextSummarizer
from string import punctuation
from collections import Counter
from heapq import nlargest

# Hugging Face() T5, BART, etc.) Gensim, spaCy, OpenAI, BERT
app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
summarizer = SpacyTextSummarizer(nlp)

def process_transcript(transcripts):
    transcript = ' '.join([item['text'] for item in transcripts])
    summary = summarizer.summarize_text(transcript)
    return { "Summarized Video:": summary }

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