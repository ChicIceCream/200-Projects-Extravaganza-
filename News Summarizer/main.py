import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')

url = 'https://arxiv.org/pdf/1502.03044'

article = Article(url)

article.download()
article.parse()

article.nlp()

print(f'Title : {article.title}')
print(f'Authors : {article.authors}')
print(f'Publication Date : {article.publish_date}')
print(f'Summary = {article.summary}')