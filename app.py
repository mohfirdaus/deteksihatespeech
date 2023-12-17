import streamlit as st
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os

# Gunakan st.cache_data alih-alih st.cache
@st.cache_data
def load_model():
    tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')
    model = BertForSequenceClassification.from_pretrained('sidaus/hatespeech-commentnews',token=st.secrets["token"])
    return tokenizer, model

# Fungsi untuk melakukan analisis teks
def analyze_text(user_input, tokenizer, model):
    test_sample = tokenizer([user_input], padding=True, truncation=True, max_length=512, return_tensors='pt')
    output = model(**test_sample)
    y_pred = np.argmax(output.logits.detach().numpy(), axis=1)
    return output.logits, y_pred[0]

def main():
    st.title("Aplikasi Deteksi Ujaran Kebencian")
    st.sidebar.header("Panduan Pengguna")
    st.sidebar.markdown("1. Masukkan teks yang ingin Anda analisis.")
    st.sidebar.markdown("2. Klik tombol 'Analisis' untuk mendapatkan prediksi.")

    # Muat model menggunakan fungsi load_model
    tokenizer, model = load_model()

    # Input untuk analisis teks
    user_input = st.text_area('Masukkan Teks untuk Dianalisis')

    # Tombol Analisis
    button = st.button("Analisis")

    # Kamus untuk pemetaan label prediksi
    label_mapping = {1: 'Termasuk Ujaran Kebencian', 0: 'Bukan Termasuk Ujaran Kebencian'}

    # Lakukan analisis jika tombol ditekan
    if button and user_input:
        logits, prediction = analyze_text(user_input, tokenizer, model)

        # Tampilkan logits dan label prediksi
        st.subheader("Hasil Analisis")
        st.write("Logits:", logits)
        st.write("Prediksi:", label_mapping[prediction])

if __name__ == "__main__":
    main()