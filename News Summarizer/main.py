import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')

url = 'https://www.cloudflare.com/learning/ai/what-is-large-language-model/'

article = Article(url)

article.download()
article.parse()

article.nlp()

print(f'Title : {article.title}')
print(f'Authors : {article.authors}')
print(f'Publication Date : {article.publish_date}')
print(f'Summary = {article.summary}')
try:
    with open(r'News Summarizer\output.txt', 'w') as file:
        file.write(f'Title : {article.title}\n')
        file.write(f'Authors : {article.authors}\n')
        file.write(f'Publication Date : {article.publish_date}\n')
        file.write(f'Summary = {article.summary}\n')
except:
    print("Did not work")