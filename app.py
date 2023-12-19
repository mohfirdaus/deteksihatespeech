import os
import subprocess
import sys

# Mendapatkan jalur ke direktori saat ini
current_directory = os.path.dirname(os.path.abspath(__file__))

# Menentukan jalur ke file requirements.txt
requirements_file = os.path.join(current_directory, "requirements.txt")

# Mengeksekusi perintah pip install -r requirements.txt
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
except subprocess.CalledProcessError as e:
    print(f"Error during installation: {e}")
    sys.exit(1)
    
import streamlit as st
import requests
from retrying import retry

API_URL = "https://api-inference.huggingface.co/models/sidaus/hatespeech-commentnews"
headers = {"Authorization": st.secrets["token"]}

@retry(stop_max_attempt_number=3, wait_fixed=5000)  # Retry 3 kali, setiap retry setelah 5 detik
def query_with_retry(payload):
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()  # Raise HTTPError for bad responses
    return response.json()

# Set page title and favicon
st.set_page_config(
    page_title="Aplikasi Deteksi Ujaran Kebencian",
    page_icon=":angry:",  # Anda dapat menggantinya dengan emoji pilihan Anda
)

# Menambahkan header dengan judul dan deskripsi
st.title("Aplikasi Deteksi Ujaran Kebencian")
st.markdown(
    "Selamat datang di Aplikasi Deteksi Ujaran Kebencian. Masukkan teks di bawah untuk menganalisis apakah mengandung ujaran kebencian atau tidak."
)

# Area teks masukan
input_text = st.text_area("Masukkan teks")

# Tombol untuk memicu analisis
if st.button("Analisis"):
    if not input_text:
        st.warning("Mohon masukkan teks sebelum melakukan analisis.")
    else:
        with st.spinner("Menganalisis..."):  # Menggunakan st.spinner sebagai pengelola konteks
            try:
                # Melakukan analisis dengan mekanisme pengulangan dan waktu tunggu
                result = query_with_retry({"inputs": input_text})

                # Memeriksa apakah hasilnya adalah list dengan setidaknya satu elemen
                if isinstance(result, list) and result and isinstance(result[0], list):
                    # Memeriksa apakah list dalamnya memiliki setidaknya satu kamus
                    if result[0] and isinstance(result[0][0], dict) and "label" in result[0][0]:
                        prediction = result[0][0]["label"]
                        score = result[0][0]["score"]

                        # Mengganti label
                        if prediction == "LABEL_0":
                            prediction = "Bukan Termasuk Hatespeech"
                        elif prediction == "LABEL_1":
                            prediction = "Termasuk Hatespeech"

                        st.success(f"**Prediksi:** {prediction} dengan skor kepercayaan: {score:.4f}")
                    else:
                        st.error("Kesalahan: Tidak dapat mendapatkan prediksi dari model. Harap periksa respons API.")
                else:
                    st.error("Kesalahan: Tidak dapat mendapatkan prediksi dari model. Harap periksa respons API.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Kesalahan HTTP: {e}")
                st.error("Model mungkin sedang memuat atau layanan tidak tersedia. Silakan coba lagi nanti.")
            except Exception as e:
                st.error(f"Kesalahan: {e}")
                st.error("Terjadi kesalahan saat melakukan analisis. Silakan coba lagi.")
