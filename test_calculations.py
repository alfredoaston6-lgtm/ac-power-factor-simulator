import math
import pytest

from calculations import hitung_daya_ac, validasi_input


def test_beban_resistif():
    hasil = hitung_daya_ac("Resistif", 220, 5, 0)
    assert hasil["pf"] == pytest.approx(1.0)
    assert hasil["p"] == pytest.approx(1100.0)
    assert hasil["q"] == pytest.approx(0.0)
    assert hasil["s"] == pytest.approx(1100.0)


def test_beban_induktif():
    hasil = hitung_daya_ac("Induktif", 220, 5, 30)
    assert hasil["pf"] == pytest.approx(0.8660254, rel=1e-6)
    assert hasil["p"] == pytest.approx(952.6279, rel=1e-5)
    assert hasil["q"] == pytest.approx(550.0)
    assert hasil["s"] == pytest.approx(1100.0)
    assert hasil["karakter_pf"] == "lagging"


def test_beban_kapasitif():
    hasil = hitung_daya_ac("Kapasitif", 220, 5, -30)
    assert hasil["pf"] == pytest.approx(0.8660254, rel=1e-6)
    assert hasil["p"] == pytest.approx(952.6279, rel=1e-5)
    assert hasil["q"] == pytest.approx(-550.0)
    assert hasil["s"] == pytest.approx(1100.0)
    assert hasil["karakter_pf"] == "leading"


@pytest.mark.parametrize("tegangan,arus", [(0, 5), (-220, 5), (220, 0), (220, -5)])
def test_tegangan_atau_arus_tidak_valid(tegangan, arus):
    assert validasi_input("Resistif", tegangan, arus, 0)


@pytest.mark.parametrize(
    "jenis,sudut",
    [("Resistif", 10), ("Induktif", 0), ("Induktif", -30),
     ("Kapasitif", 0), ("Kapasitif", 30), ("Induktif", 90), ("Kapasitif", -90)]
)
def test_kombinasi_jenis_dan_sudut_tidak_valid(jenis, sudut):
    assert validasi_input(jenis, 220, 5, sudut)


def test_identitas_segitiga_daya():
    hasil = hitung_daya_ac("Induktif", 220, 5, 30)
    assert hasil["s"] ** 2 == pytest.approx(hasil["p"] ** 2 + hasil["q"] ** 2)
