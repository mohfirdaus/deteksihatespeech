# Aplikasi Deteksi Ujaran Kebencian

Selamat datang di Aplikasi Deteksi Ujaran Kebencian! Aplikasi ini menggunakan model NLP (Natural Language Processing) IndoBERT Base Phase 2 untuk menganalisis teks dan menentukan apakah teks tersebut mengandung ujaran kebencian atau tidak. Model ini telah dilatih menggunakan dataset komentar berita dari Kompas, yang mencakup beragam bahasa dan konteks untuk memberikan hasil yang lebih akurat.

Aplikasi ini diharapkan dapat membantu dalam mendeteksi dan memitigasi ujaran kebencian dalam komentar berita. Terima kasih telah menggunakan [Aplikasi Deteksi Ujaran Kebencian](https://deteksihate-speech.streamlit.app/)!

## Cara Penggunaan

1. **Masukkan Teks:** Pada aplikasi, terdapat area teks masukan. Silakan masukkan teks yang ingin Anda analisis.

2. **Klik Tombol Analisis:** Setelah memasukkan teks, klik tombol "Analisis" untuk memulai proses analisis.

3. **Hasil Analisis:** Hasil analisis akan ditampilkan di bawah tombol "Analisis". Anda akan melihat prediksi apakah teks termasuk dalam ujaran kebencian beserta skor kepercayaan.

## Keterangan

- Jika teks termasuk dalam ujaran kebencian, label akan ditampilkan sebagai "Termasuk Hatespeech".
- Jika teks tidak mengandung ujaran kebencian, label akan ditampilkan sebagai "Bukan Termasuk Hatespeech".

## Kontribusi

Jika Anda menemui bug atau ingin melakukan perbaikan, silakan buat *issue* atau *pull request*. Kami sangat menghargai kontribusi dari para pengguna.

## Referensi

Bryan Wilie, Karissa Vincentio, Genta Indra Winata, Samuel Cahyawijaya, X. Li, Zhi Yuan Lim, S. Soleman, R. Mahendra, Pascale Fung, Syafri Bahar, A. Purwarianti. (2020). **IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding**. In *Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing*.

Kompas. (2023). **Indeks Berita Kompas**. Kompas. URL: [https://indeks.kompas.com/](https://indeks.kompas.com/).

