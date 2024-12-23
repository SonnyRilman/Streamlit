import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Daftar Prodi dengan kode dan passing grade
prodi_list = {
    "Informatika (5314)": 85,
    "Psikologi (9114)": 75,
    "Farmasi (8114)": 70,
    "PGSD (1134)": 65,
    "Manajemen (2214)": 75,
    "Sastra Inggris (4214)": 70,
    "Pendidikan Bahasa Inggris (PBI) (1214)": 70
}

# Data pengguna dengan nilai rata-rata dan pilihan prodi
data_pengguna = {
    'user_id': [1, 2, 3, 4, 5],
    'nilai_rata_rata': [85, 75, 90, 65, 70],  # Nilai rata-rata raport
    'Informatika (5314)': [1, 1, 1, 0, 0],  # 1 = memilih, 0 = tidak memilih
    'Psikologi (9114)': [1, 0, 1, 1, 0],
    'Farmasi (8114)': [0, 1, 0, 1, 1],
    'PGSD (1134)': [0, 0, 1, 1, 1],
}

df = pd.DataFrame(data_pengguna)

# Fungsi untuk menghitung nilai rata-rata
def hitung_nilai_rata_rata(nilai_ipa):
    return sum(nilai_ipa) / len(nilai_ipa)

# Fungsi untuk memberikan rekomendasi prodi berdasarkan nilai rata-rata dan passing grade
def rekomendasi_prodi(nilai_ipa, jurusan):
    nilai_rata_rata = hitung_nilai_rata_rata(nilai_ipa)
    
    if jurusan == "IPA":
        daftar_prodi = list(prodi_list.keys())
    elif jurusan == "IPS":
        daftar_prodi = list(prodi_list.keys())
    else:
        return "Jurusan tidak valid"
    
    rekomendasi_lain = []
    for prodi in daftar_prodi:
        if nilai_rata_rata >= prodi_list[prodi]:
            rekomendasi_lain.append(prodi)

    return rekomendasi_lain, nilai_rata_rata

# Fungsi untuk menghitung cosine similarity dan memberikan rekomendasi berdasarkan kesamaan
def collaborative_filtering_cosine(nilai_rata_rata_pengguna):
    X = df[['nilai_rata_rata']].values
    target_user = np.array([[nilai_rata_rata_pengguna]])
    similarity_scores = cosine_similarity(target_user, X)
    
    most_similar_user_idx = similarity_scores.argsort()[0][-2]
    
    rekomendasi_prodi = set()
    for prodi in df.columns[2:]:
        if df.iloc[most_similar_user_idx][prodi] == 1:
            rekomendasi_prodi.add(prodi)

    return list(rekomendasi_prodi)

# Fungsi untuk memberikan rekomendasi berdasarkan passing grade dan collaborative filtering
def rekomendansi_terpadu(nilai_ipa, jurusan, nilai_rata_rata_pengguna):
    rekomendasi_passing_grade, nilai_rata_rata = rekomendasi_prodi(nilai_ipa, jurusan)
    rekomendasi_collab = collaborative_filtering_cosine(nilai_rata_rata_pengguna)

    rekomendasi_akhir = set(rekomendasi_passing_grade).intersection(rekomendasi_collab)
    
    return list(rekomendasi_akhir), nilai_rata_rata

# Tampilan Awal dengan Logo
def tampilkan_tampilan_awal():
    st.set_page_config(page_title="Sistem Rekomendasi Prodi", page_icon=":books:", layout="centered")
    
    # Sidebar untuk navigasi
    st.sidebar.image("logo_kampus.png", width=200)  # Ganti dengan logo kampus Anda
    st.sidebar.title("Menu")
    st.sidebar.write("Selamat datang di sistem rekomendasi prodi! Pilih opsi di bawah untuk melanjutkan.")
    
    if "formulir_input" not in st.session_state:
        st.session_state.formulir_input = False
    
    if st.session_state.formulir_input:
        tampilkan_formulir_input()
    else:
        if st.sidebar.button("Mulai"):
            st.session_state.formulir_input = True
            tampilkan_formulir_input()

# Formulir Input untuk Data Mahasiswa
def tampilkan_formulir_input():
    st.title("Formulir Input Data Calon Mahasiswa")

    # Input Jurusan
    jurusan = st.selectbox("Pilih Jurusan", ["IPA", "IPS"], index=0)

    # Input Nilai Raport (Contoh: 5 mata pelajaran)
    nilai_ipa = []
    if jurusan == "IPA":
        st.subheader("Input Nilai Mata Pelajaran IPA")
        nilai_ipa.append(st.number_input("Nilai Bahasa Indonesia", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Bahasa Inggris", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Biologi", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Fisika", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Kimia", min_value=0, max_value=100))
    elif jurusan == "IPS":
        st.subheader("Input Nilai Mata Pelajaran IPS")
        nilai_ipa.append(st.number_input("Nilai Bahasa Indonesia", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Bahasa Inggris", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Ekonomi", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Geografi", min_value=0, max_value=100))
        nilai_ipa.append(st.number_input("Nilai Sosiologi", min_value=0, max_value=100))

    # Pilihan Prodi
    st.subheader("Pilih Program Studi")
    pilihan_1 = "Informatika (5314)"
    st.write(f"Pilihan 1: {pilihan_1}")

    pilihan_prodi_2_3 = ["Psikologi (9114)", "Farmasi (8114)", "PGSD (1134)", "Manajemen (2214)", "Sastra Inggris (4214)", "Pendidikan Bahasa Inggris (PBI) (1214)"] if jurusan == "IPA" else ["Psikologi (9114)", "PGSD (1134)", "Manajemen (2214)", "Sastra Inggris (4214)", "Pendidikan Bahasa Inggris (PBI) (1214)"]

    pilihan_2 = st.selectbox("Pilihan Prodi 2", pilihan_prodi_2_3)
    pilihan_3 = st.selectbox("Pilihan Prodi 3", pilihan_prodi_2_3)

    # Tombol untuk melihat rekomendasi
    if st.button("Lihat Rekomendasi"):
        nilai_rata_rata = hitung_nilai_rata_rata(nilai_ipa)
        rekomendasi_akhir, nilai_rata_rata_pengguna = rekomendansi_terpadu(nilai_ipa, jurusan, nilai_rata_rata)

        st.subheader("Hasil Rekomendasi Prodi")
        st.write(f"Nilai Rata-Rata: {nilai_rata_rata:.2f}")
        if rekomendasi_akhir:
            st.write("Berikut adalah prodi yang direkomendasikan:")
            for prodi in rekomendasi_akhir:
                st.write(f"- {prodi}")
        else:
            st.write("Tidak ada prodi yang dapat direkomendasikan berdasarkan kriteria Anda.")

# Menjalankan aplikasi
if __name__ == "__main__":
    tampilkan_tampilan_awal()
