# AC Power Factor Simulator

Laboratorium virtual interaktif untuk mempelajari faktor daya, gelombang tegangan/arus, serta daya aktif, reaktif, dan semu pada rangkaian AC.

## Fitur

- Beban resistif, induktif, dan kapasitif.
- Input tegangan dan arus RMS serta sudut fase.
- Validasi jenis beban dan rentang sudut.
- Grafik gelombang sinus dengan Plotly.
- Diagram skematis rangkaian dan segitiga daya.
- Interpretasi hasil otomatis.
- Pengujian otomatis menggunakan pytest.

## Struktur proyek

```text
ac_power_factor_simulator/
├── app.py
├── calculations.py
├── requirements.txt
├── README.md
└── tests/
    └── test_calculations.py
```

## Prasyarat

Gunakan Python 3.10 atau lebih baru. Instal Python dari https://www.python.org/downloads/ dan saat instalasi Windows, centang **Add Python to PATH**.

## Instalasi dan menjalankan secara lokal

1. Buka terminal atau Command Prompt.
2. Masuk ke folder proyek.
3. Buat lingkungan virtual:

   **Windows**
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Pasang dependensi:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

6. Streamlit biasanya membuka browser otomatis. Jika tidak, buka alamat lokal yang ditampilkan di terminal, umumnya `http://localhost:8501`.

## Menguji beban

Setelah aplikasi terbuka, masukkan nilai berikut di panel kiri dan tekan **Mulai Simulasi** untuk setiap kasus.

| Kasus | Jenis beban | V RMS | I RMS | Sudut fase | PF | P | Q | S |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A | Resistif | 220 V | 5 A | 0° | 1,000 | 1100 W | 0 VAR | 1100 VA |
| B | Induktif | 220 V | 5 A | +30° | 0,866 | 952,63 W | +550 VAR | 1100 VA |
| C | Kapasitif | 220 V | 5 A | −30° | 0,866 | 952,63 W | −550 VAR | 1100 VA |

Untuk menguji validasi, masukkan tegangan atau arus nol/negatif, atau pilih jenis beban dengan tanda sudut yang tidak sesuai. Aplikasi menolak input ketika tombol simulasi ditekan.

## Menjalankan pengujian otomatis

Dari folder proyek dan saat lingkungan virtual aktif:

```bash
pytest -q
```

Tes mencakup tiga kasus perhitungan, validasi input, dan identitas segitiga daya.

## Publikasi gratis melalui GitHub dan Streamlit Community Cloud

1. Buat akun atau masuk ke https://github.com/.
2. Buat repositori baru, misalnya `ac-power-factor-simulator`.
3. Unggah `app.py`, `calculations.py`, `requirements.txt`, `README.md`, dan folder `tests/`. Jangan unggah folder `.venv`.
4. Pastikan perubahan sudah di-commit ke cabang utama (biasanya `main`).
5. Buka https://share.streamlit.io/ dan masuk menggunakan akun GitHub.
6. Pilih **Create app** atau **Deploy an app**.
7. Pilih repositori, cabang `main`, dan berkas utama `app.py`.
8. Mulai deployment dan tunggu proses instalasi dependensi selesai.
9. Setelah berhasil, Streamlit akan memberikan URL publik seperti `https://nama-aplikasi.streamlit.app`. Salin tautan tersebut untuk dikumpulkan kepada dosen.
10. Jika kode diperbarui di GitHub, Streamlit Community Cloud biasanya membangun ulang aplikasi secara otomatis.

Nama tombol atau langkah pada layanan hosting dapat berubah. Ikuti antarmuka Streamlit Community Cloud yang tersedia saat deployment.

## Teori dan batasan model

Dengan nilai RMS dan sudut fase `φ` dalam radian saat perhitungan:

- `PF = |cos(φ)|`
- `S = V × I`
- `P = V × I × cos(φ)`
- `Q = V × I × sin(φ)`
- `S² = P² + Q²`

Sudut positif menandakan beban induktif (arus tertinggal, Q positif), sedangkan sudut negatif menandakan beban kapasitif (arus mendahului, Q negatif). Beban resistif ideal menggunakan sudut 0°.

Sudut fase merupakan input model pembelajaran, bukan hasil estimasi dari nilai komponen R, L, dan C. Grafik gelombang menggunakan frekuensi ilustrasi 50 Hz; frekuensi tidak mengubah perhitungan daya yang menggunakan nilai RMS dan sudut fase. Diagram rangkaian bersifat skematis dan bukan rancangan instalasi fisik.
