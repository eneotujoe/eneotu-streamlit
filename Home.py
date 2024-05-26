import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import time
import string
from pathlib import Path
from PIL import Image


st.set_page_config(
    page_title='Eneotu',
    page_icon=':material/thumb_up:',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items={}
)

style_sheet = """
    <style>
        .st-emotion-cache-183lzff {
            font-weight: bold;
            font-family: Helvetica, sans-serif !important;
            
        }
        .st-emotion-cache-4d1onx p {
            font-weight: bold;
            
        }
        .st-emotion-cache-j7qwjs {
            display: flex !important;
            # align-items: center !important;
            
        }
        .st-emotion-cache-1xw8zd0 {
            background-color: #0000ff !important;
            # display: flex;
        }

        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 80px 20px;
        }

        .st-emotion-cache-1kyxreq {
            display: block !important;
        }
    </style>
"""
st.html(style_sheet)

BASE_DIR = Path(__file__).resolve().parent
img = BASE_DIR / "static" / 'img' / 'eneotujoe.png'


img_col, title_col = st.columns(2)

with img_col:
    eneotu = Image.open(img)
    st.image(eneotu)

with title_col:
    st.write('#')
    st.write('#')
    st.title('Eneotu Joe')
    st.text('I Am Artificial Intelligence Researcher')
    # button = st.button("Contact Me", type="primary")
    container = st.container(border=True)
    container.page_link('https://eneotu.com', label='Contact Me', icon="🌎")