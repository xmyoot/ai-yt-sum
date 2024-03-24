# Importing dependencies from transformers
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()
import os
client = OpenAI()

from transformers import PegasusForConditionalGeneration, PegasusTokenizer
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

class Summarizer:
    def __init__(self, nlp):
        self.nlp = nlp
    def abstract_summarize(self, text):
        # Create tokens - number representation of our text
        tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        # Summarize 
        summary = model.generate(**tokens)
        # Decode the summary
        return tokenizer.batch_decode(summary, skip_special_tokens=True)
   
    def openai_summarize(self, text):
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a youtube summarizing tool which will be given a section of a youtube video transcript"},
            {"role": "user", "content": f"Compose a summary of this -- {text} -- and return it following the format, This section is about ..."}
        ]
        )
        return completion.choices[0].message.content
    
    def extract_summarize(self, text):
        doc = self.nlp(text=text)
        # determine word count
        word_dict = {}
        for word in doc:
            word = word.text.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        # Score each sentence
        sentences = []
        sentence_score = 0
        for i, sentence in enumerate(doc.sents):
            for word in sentence:
                word = word.text.lower()
                sentence_score += word_dict[word]
            sentences.append((i, sentence.text.replace("\n", " "), sentence_score/len(sentence)))
        sorted_sentences = sorted(sentences, key=lambda x: -x[2])
        top_three = sorted(sorted_sentences[:3], key=lambda x: x[0])
        return " ".join([sentence[1] for sentence in top_three])