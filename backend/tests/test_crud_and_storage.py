import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import get_db
from app.models.base import Base

# In-memory SQLite with StaticPool so all threads/sessions share the same DB
TEST_DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

client = TestClient(app)

def test_client_crud():
    # 1. Create client
    res = client.post("/api/clients", json={
        "nama": "Ibu Ratna Dewi",
        "perusahaan": "Dewi Hospitality",
        "alamat": "Jl. Gandaria No. 12, Jakarta",
        "telepon": "08123456789",
        "email": "ratna@dewi.com",
        "catatan": "Klien VIP"
    })
    assert res.status_code == 201
    created = res.json()
    assert created["nama"] == "Ibu Ratna Dewi"
    client_id = created["id"]

    # 2. List clients
    list_res = client.get("/api/clients")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Update client
    up_res = client.put(f"/api/clients/{client_id}", json={
        "telepon": "08999999999"
    })
    assert up_res.status_code == 200
    assert up_res.json()["telepon"] == "08999999999"

    # 4. Get single client
    get_res = client.get(f"/api/clients/{client_id}")
    assert get_res.status_code == 200
    assert get_res.json()["telepon"] == "08999999999"

def test_project_crud_and_duplicate():
    c_res = client.post("/api/clients", json={"nama": "Pak Hendra"})
    c_id = c_res.json()["id"]

    proj_payload = {
        "client_id": c_id,
        "nama": "Rumah Tropis Hendra",
        "lokasi": "Bandung Utara",
        "luas_m2": 250.0,
        "jenis": "Rumah Tinggal",
        "ruang_lingkup": "Desain Arsitektur & Interior",
        "diskon_rp": 500000,
        "ppn_persen": 11.0,
        "material_items": [
            {
                "area": "Fasad",
                "pekerjaan": "Cat Eksterior",
                "material": "Cat Dulux Weathershield",
                "merek": "Dulux",
                "volume": 50.0,
                "satuan": "m²",
                "harga_satuan": 150000,
                "catatan": "Warna cream"
            }
        ],
        "schedule_stages": [
            {
                "tahap": "Skematik Desain",
                "durasi": "2 Minggu",
                "keterangan": "Konsep 2D"
            }
        ],
        "payment_terms": [
            {
                "urutan": 1,
                "label": "DP",
                "persen": 50.0,
                "pemicu": "Mulai kerja"
            },
            {
                "urutan": 2,
                "label": "Pelunasan",
                "persen": 50.0,
                "pemicu": "Serah terima"
            }
        ]
    }
    p_res = client.post("/api/projects", json=proj_payload)
    assert p_res.status_code == 201
    proj_data = p_res.json()
    p_id = proj_data["id"]
    assert proj_data["nama"] == "Rumah Tropis Hendra"
    assert len(proj_data["material_items"]) == 1
    assert len(proj_data["payment_terms"]) == 2

    # Test Duplikasi Proyek
    dup_res = client.post(f"/api/projects/{p_id}/duplicate")
    assert dup_res.status_code == 201
    dup_data = dup_res.json()
    assert dup_data["nama"] == "Rumah Tropis Hendra (Salinan)"
    assert dup_data["id"] != p_id
    assert len(dup_data["material_items"]) == 1
    assert len(dup_data["schedule_stages"]) == 1
    assert len(dup_data["payment_terms"]) == 2

def test_auto_numbering_and_snapshot_immutability():
    c_res = client.post("/api/clients", json={"nama": "Klien Penomoran"})
    c_id = c_res.json()["id"]

    p_res = client.post("/api/projects", json={
        "client_id": c_id,
        "nama": "Proyek Penomoran",
        "material_items": [
            {"pekerjaan": "Pekerjaan Asli", "material": "Kayu Jati", "volume": 1, "satuan": "unit", "harga_satuan": 10000000}
        ],
        "payment_terms": [
            {"urutan": 1, "label": "Pelunasan", "persen": 100.0}
        ]
    })
    p_id = p_res.json()["id"]

    # 1. Terbitkan dokumen proposal pertama
    doc1_res = client.post(f"/api/projects/{p_id}/documents", json={
        "jenis": "proposal",
        "tanggal_dokumen": "20 November 2026"
    })
    assert doc1_res.status_code == 201
    doc1_data = doc1_res.json()
    assert "PROP/" in doc1_data["nomor"]
    assert doc1_data["nomor"].endswith("/001")

    # 2. Terbitkan dokumen proposal kedua
    doc2_res = client.post(f"/api/projects/{p_id}/documents", json={
        "jenis": "proposal",
        "tanggal_dokumen": "20 November 2026"
    })
    assert doc2_res.status_code == 201
    doc2_data = doc2_res.json()
    assert doc2_data["nomor"].endswith("/002")

    # 3. Terbitkan dokumen invoice
    inv_res = client.post(f"/api/projects/{p_id}/documents", json={
        "jenis": "invoice",
        "tanggal_dokumen": "20 November 2026"
    })
    assert inv_res.status_code == 201
    assert inv_res.json()["nomor"].startswith("INV/")
    assert inv_res.json()["nomor"].endswith("/001")

    # 4. Buktikan Snapshot Immutability:
    client.put(f"/api/projects/{p_id}", json={
        "nama": "Proyek Diubah Setelah Terbit",
        "material_items": [
            {"pekerjaan": "Pekerjaan Baru", "material": "Baja Ringan", "volume": 1, "satuan": "unit", "harga_satuan": 50000000}
        ]
    })

    # Ambil detail dokumen lama (doc1)
    doc_detail_res = client.get(f"/api/documents/{doc1_data['id']}")
    assert doc_detail_res.status_code == 200
    snapshot = doc_detail_res.json()["snapshot_data"]
    # Nama di snapshot dokumen lama HARUS tetap 'Proyek Penomoran', bukan yang baru
    assert snapshot["project"]["nama"] == "Proyek Penomoran"
    assert snapshot["material_items"][0]["material"] == "Kayu Jati"

    # Unduh PDF dari endpoint /documents/{id}/pdf
    pdf_res = client.get(f"/api/documents/{doc1_data['id']}/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000
    assert pdf_res.content.startswith(b"%PDF-")

def test_studio_branding():
    # 1. Get studio
    res = client.get("/api/studio")
    assert res.status_code == 200
    studio_data = res.json()
    assert "warna_utama" in studio_data
    assert studio_data["warna_utama"] == "#0284c7"

    # 2. Update studio branding
    up_res = client.put("/api/studio", json={
        "nama_usaha": "Atelier Megah Nusantara",
        "warna_utama": "#059669",
        "warna_aksen": "#064e3b"
    })
    assert up_res.status_code == 200
    updated = up_res.json()
    assert updated["nama_usaha"] == "Atelier Megah Nusantara"
    assert updated["warna_utama"] == "#059669"
    assert updated["warna_aksen"] == "#064e3b"

def test_contract_clauses():
    # 1. Get default clauses (auto-seeded)
    res = client.get("/api/clauses")
    assert res.status_code == 200
    clauses = res.json()
    assert len(clauses) >= 8
    assert clauses[0]["kode"] == "PASAL_1"

    # 2. Update a clause
    clauses[0]["judul"] = "Pasal 1: Lingkup Kustom Arsitek"
    up_res = client.put("/api/clauses", json={"clauses": clauses})
    assert up_res.status_code == 200
    up_clauses = up_res.json()
    assert up_clauses[0]["judul"] == "Pasal 1: Lingkup Kustom Arsitek"

    # 3. Reset clauses to default
    rst_res = client.post("/api/clauses/reset")
    assert rst_res.status_code == 200
    rst_clauses = rst_res.json()
    assert rst_clauses[0]["judul"] == "Pasal 1: Ruang Lingkup Jasa Perancangan"

