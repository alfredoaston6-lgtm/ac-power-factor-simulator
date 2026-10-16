"""Fungsi validasi dan perhitungan daya AC, terpisah dari antarmuka."""
import math


def validasi_input(jenis: str, tegangan: float, arus: float, sudut: float) -> list[str]:
    """Mengembalikan daftar pesan kesalahan; daftar kosong berarti valid."""
    kesalahan = []
    jenis_valid = {"Resistif", "Induktif", "Kapasitif"}
    if jenis not in jenis_valid:
        kesalahan.append("Pilih jenis beban yang tersedia.")
    if tegangan <= 0:
        kesalahan.append("Tegangan harus lebih besar dari 0 V RMS.")
    if arus <= 0:
        kesalahan.append("Arus harus lebih besar dari 0 A RMS.")
    if not -89.9 <= sudut <= 89.9:
        kesalahan.append("Sudut fase harus berada pada rentang −89,9° sampai +89,9°.")
    if jenis == "Resistif" and not math.isclose(sudut, 0.0, abs_tol=1e-9):
        kesalahan.append("Beban resistif ideal harus memiliki sudut fase 0°.")
    elif jenis == "Induktif" and sudut <= 0:
        kesalahan.append("Beban induktif harus menggunakan sudut fase positif.")
    elif jenis == "Kapasitif" and sudut >= 0:
        kesalahan.append("Beban kapasitif harus menggunakan sudut fase negatif.")
    return kesalahan


def hitung_daya_ac(jenis: str, tegangan: float, arus: float, sudut: float) -> dict:
    """Menghitung besaran daya AC berdasarkan nilai RMS dan sudut fase derajat."""
    kesalahan = validasi_input(jenis, tegangan, arus, sudut)
    if kesalahan:
        raise ValueError(" ".join(kesalahan))

    phi_rad = math.radians(sudut)
    s = tegangan * arus
    p = s * math.cos(phi_rad)
    q = s * math.sin(phi_rad)
    pf = abs(math.cos(phi_rad))

    # Bersihkan residu numerik kecil pada beban resistif ideal.
    if math.isclose(sudut, 0.0, abs_tol=1e-12):
        q = 0.0

    karakter_pf = "unity" if math.isclose(pf, 1.0, abs_tol=1e-12) else (
        "lagging" if jenis == "Induktif" else "leading" if jenis == "Kapasitif" else "unity"
    )
    return {
        "jenis": jenis,
        "tegangan": float(tegangan),
        "arus": float(arus),
        "sudut": float(sudut),
        "phi_rad": phi_rad,
        "pf": pf,
        "p": p,
        "q": q,
        "s": s,
        "karakter_pf": karakter_pf,
    }
