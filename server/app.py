from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/api/serverCheck', methods=['GET'])
def get_data():
    data = {"test message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    url = request.json.get('url')
    video_id = url.split('watch?v=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return jsonify(transcript)

if __name__ == '__main__':
    app.run(port=5000)