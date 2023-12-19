import streamlit as st
import requests
import time

API_URL = "https://api-inference.huggingface.co/models/sidaus/hatespeech-commentnews"
headers = {"Authorization": st.secrets["token"]}

MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

def query_with_retry(payload):
    for _ in range(MAX_RETRY_ATTEMPTS):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e}")
            st.error("Model mungkin sedang memuat atau layanan tidak tersedia. Menunggu beberapa detik sebelum mencoba lagi.")
            time.sleep(RETRY_DELAY_SECONDS)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error("Terjadi kesalahan saat melakukan analisis. Menunggu beberapa detik sebelum mencoba lagi.")
            time.sleep(RETRY_DELAY_SECONDS)

    st.error("Percobaan maksimum telah dicapai. Silakan coba lagi nanti.")
    return None

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
