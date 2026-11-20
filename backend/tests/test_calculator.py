import pytest
from app.services.calculator import terbilang, format_rupiah, calculate_financials, calculate_terms

def test_terbilang_dasar():
    assert terbilang(0) == "Nol Rupiah"
    assert terbilang(1) == "Satu Rupiah"
    assert terbilang(11) == "Sebelas Rupiah"
    assert terbilang(15) == "Lima Belas Rupiah"
    assert terbilang(20) == "Dua Puluh Rupiah"
    assert terbilang(99) == "Sembilan Puluh Sembilan Rupiah"
    assert terbilang(100) == "Seratus Rupiah"
    assert terbilang(101) == "Seratus Satu Rupiah"
    assert terbilang(115) == "Seratus Lima Belas Rupiah"
    assert terbilang(250) == "Dua Ratus Lima Puluh Rupiah"

def test_terbilang_ribuan_jutaan():
    assert terbilang(1000) == "Seribu Rupiah"
    assert terbilang(1500) == "Seribu Lima Ratus Rupiah"
    assert terbilang(10000) == "Sepuluh Ribu Rupiah"
    assert terbilang(100000) == "Seratus Ribu Rupiah"
    assert terbilang(1000000) == "Satu Juta Rupiah"
    assert terbilang(12500000) == "Dua Belas Juta Lima Ratus Ribu Rupiah"
    assert terbilang(1000000000) == "Satu Miliar Rupiah"
    assert terbilang(2500000000) == "Dua Miliar Lima Ratus Juta Rupiah"

def test_format_rupiah():
    assert format_rupiah(0) == "Rp 0"
    assert format_rupiah(12500000) == "Rp 12.500.000"
    assert format_rupiah(500) == "Rp 500"

class DummyItem:
    def __init__(self, pekerjaan, volume, satuan, harga_satuan, area="Umum", material="Bahan", merek="-"):
        self.pekerjaan = pekerjaan
        self.volume = volume
        self.satuan = satuan
        self.harga_satuan = harga_satuan
        self.area = area
        self.material = material
        self.merek = merek
        self.catatan = ""

def test_calculate_financials():
    items = [
        DummyItem("Plester Dinding", 10.0, "m2", 100000), # 1.000.000
        DummyItem("Lantai Granit", 20.5, "m2", 200000),   # 4.100.000
    ]
    # Subtotal: 5.100.000
    # Diskon: 100.000 -> DPP: 5.000.000
    # PPN 11%: 550.000 -> Total: 5.550.000
    res = calculate_financials(items, diskon_rp=100000, ppn_persen=11.0)
    assert res["subtotal"] == 5100000
    assert res["diskon_rp"] == 100000
    assert res["dpp"] == 5000000
    assert res["ppn_rp"] == 550000
    assert res["total"] == 5550000
    assert "Lima Juta Lima Ratus Lima Puluh Ribu Rupiah" in res["terbilang_total"]

class DummyTerm:
    def __init__(self, label, persen=None, nominal=0, pemicu=""):
        self.label = label
        self.persen = persen
        self.nominal = nominal
        self.pemicu = pemicu
        self.urutan = 1
        self.jatuh_tempo = "-"

def test_calculate_terms_persen():
    total = 10000000 # 10 juta
    terms = [
        DummyTerm("DP 30%", persen=30.0),
        DummyTerm("Termin 2 40%", persen=40.0),
        DummyTerm("Pelunasan 30%", persen=30.0),
    ]
    calc = calculate_terms(total, terms)
    assert len(calc) == 3
    assert calc[0]["nominal"] == 3000000
    assert calc[1]["nominal"] == 4000000
    assert calc[2]["nominal"] == 3000000
    # Sum of nominals must equal total exactly
    assert sum(t["nominal"] for t in calc) == total

def test_calculate_terms_persen_ganjil_dan_pembulatan():
    # 10.000.001 dibagi 33.33%, 33.33%, 33.34%
    total = 10000001
    terms = [
        DummyTerm("T1", persen=33.33),
        DummyTerm("T2", persen=33.33),
        DummyTerm("T3", persen=33.34),
    ]
    calc = calculate_terms(total, terms)
    assert sum(t["nominal"] for t in calc) == total

def test_calculate_terms_invalid_persen():
    terms = [
        DummyTerm("DP", persen=40.0),
        DummyTerm("Pelunasan", persen=50.0), # Total 90%, bukan 100%
    ]
    with pytest.raises(ValueError) as exc:
        calculate_terms(1000000, terms)
    assert "100%" in str(exc.value)


