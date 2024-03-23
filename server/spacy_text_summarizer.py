class SpacyTextSummarizer:
    def __init__(self, nlp):
        self.nlp = nlp

    def summarize_text(self, text):
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
        print(sentences)
        sorted_sentences = sorted(sentences, key=lambda x: -x[2])
        top_three = sorted(sorted_sentences[:3], key=lambda x: x[0])
        return " ".join([sentence[1] for sentence in top_three])