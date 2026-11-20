from app.services.pdf_generator import generate_pdf
from app.api.endpoints import get_sample_data

def test_generate_proposal_pdf():
    data = get_sample_data()
    data["jenis"] = "proposal"
    pdf_bytes = generate_pdf("proposal", data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")

def test_generate_invoice_pdf():
    data = get_sample_data()
    data["jenis"] = "invoice"
    pdf_bytes = generate_pdf("invoice", data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")

def test_generate_spek_pdf():
    data = get_sample_data()
    data["jenis"] = "spek"
    pdf_bytes = generate_pdf("spek", data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")

def test_generate_kontrak_pdf():
    data = get_sample_data()
    data["jenis"] = "kontrak"
    pdf_bytes = generate_pdf("kontrak", data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")

def test_generate_proposal_multipage_table():
    data = get_sample_data()
    data["jenis"] = "proposal"
    lots_of_items = []
    for i in range(1, 60):
        lots_of_items.append({
            "area": f"Lantai {i // 10 + 1}",
            "pekerjaan": f"Pekerjaan Finishing Ruang {i}",
            "material": f"Material Khusus {i}",
            "merek": "Standard Brand",
            "volume": float(i * 2),
            "satuan": "m²",
            "harga_satuan": 150000,
            "catatan": f"Catatan baris {i}"
        })
    data["material_items"] = lots_of_items
    pdf_bytes = generate_pdf("proposal", data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 10000
    assert pdf_bytes.startswith(b"%PDF-")
