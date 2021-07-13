from main_1_class import model
import streamlit as st
import os
import base64
import io
# from PIL import Image
# from pydub import AudioSegment
# st.title('Hello audiophiles')
st.markdown('<p align="center"><img width="200" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Audio_Book_Icon_2.svg/1200px-Audio_Book_Icon_2.svg.png"alt="File:Audio Book Icon 2.svg - Wikimedia Commons"></p>', unsafe_allow_html=True)
st.markdown('<h1 align="center">Hello Audiophiles</h1>',unsafe_allow_html=True)
import base64
st.subheader("Upload PDF here")
PDF_file=st.file_uploader("Upload A PDF",type=['PDF'])
if PDF_file is not None:
    file_details= {"FileName":PDF_file.name,"FileType":PDF_file.type}
    st.write(file_details)
    with open(PDF_file.name,"wb") as f:
        f.write(PDF_file.getbuffer())
    st.success("File Uploaded")
    demo1=model(PDF_file.name)
    demo1.custom_model()
    mp3_file=PDF_file.name.replace(".pdf",".mp3")
    def get_binary_file_downloader_html(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:file/mp3;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download mp3</a>'
        return href
    st.markdown(get_binary_file_downloader_html(mp3_file),unsafe_allow_html=True)
