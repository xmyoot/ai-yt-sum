import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin

from youtube_transcript_api import YouTubeTranscriptApi
from supabase import create_client, Client
from textblob import TextBlob
# from transformers import T5Tokenizer, T5ForConditionalGeneration
import spacy
from summarizer import Summarizer
from string import punctuation
from collections import Counter
from heapq import nlargest

# Hugging Face() T5, BART, etc.) Gensim, spaCy, OpenAI, BERT
app = Flask(__name__)
CORS(app)
app.debug = True
load_dotenv()

# Supabase setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# data, count = supabase.table('countries').insert({"id": 1, "name": "Denmark"}).execute()
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
            # print(f"Transcript: {transcript}")  # Debugging line

            summary = summarizer.openai_summarize(transcript)
            # print(f"Summary: {summary}")  # Debugging line

            # Sentiment analysis
            blob = TextBlob(summary)
            sentiment = blob.sentiment.polarity

            summaries.append({f"{round(section_start/60)}-{round((section_start + section_length)/60)} minutes": {
                "summary": summary,
                "sentiment": sentiment
            }})
            section_start = item['start']
            section = [item['text']]

    if section:
        transcript = ' '.join(section)
        summary = summarizer.openai_summarize(transcript)
        
        # Sentiment analysis
        blob = TextBlob(summary)
        sentiment = blob.sentiment.polarity
        
        summaries.append({
            f"{round(section_start/60)}-{round((section_start + section_length)/60)} minutes": {
                "summary": summary,
                "sentiment": sentiment
            }
        })

    return { "Summarized Video:": summaries }

@app.route('/api/serverCheck', methods=['GET'])
def get_data():
    data = {"test message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/transcript', methods=['POST'])
@cross_origin()
def get_transcript():
    url = request.json.get('url')
    video_id = url.split('watch?v=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    processed_transcript = process_transcript(transcript)
    return jsonify(processed_transcript)

if __name__ == '__main__':
    app.run(port=5000)