import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')

url = 'https://economictimes.indiatimes.com/tech/startups/pine-labs-owned-setu-teams-up-with-sarvam-ai-to-build-llm-for-financial-services/articleshow/109926155.cms?from=mdr'

article = Article(url)

article.download()
article.parse()

article.nlp()

print(f'Title : {article.title}')
print(f'Authors : {article.authors}')
print(f'Publication Date : {article.publish_date}')
print(f'Summary = {article.summary}')