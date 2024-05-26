import streamlit as st
from pathlib import Path
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent
css = BASE_DIR / 'static' / 'css' / 'main.css'
img = BASE_DIR / "static" / 'img' / 'logo.png'

with open(css) as css_file:
    st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
  

articles_dir = (BASE_DIR / 'articles')
articles = articles_dir.glob("*.md")

def load_markdown(posts):
    for post in posts:
        with open(post, 'r', encoding='utf-8') as file:
            post = file.read()
            return post

def list_markdown_files(posts):
    post_list = []
    for post in posts:
        post_list.append(post.stem)
    return post_list

# posts = load_markdown(articles)
# st.markdown(posts)

article_list = list_markdown_files(articles)

for article in article_list:
    st.page_link("Home.py", label=article)
