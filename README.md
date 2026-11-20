# Arsi-TeX: Automated Architecture & Interior Document Generator

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Typst](https://img.shields.io/badge/PDF_Engine-Typst-239dad.svg)](https://typst.app)
[![React](https://img.shields.io/badge/Frontend-React_19_TypeScript-61dafb.svg?logo=react&logoColor=black)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind_CSS_v4-38bdf8.svg?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Container-Docker_Compose-2496ed.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Pytest](https://img.shields.io/badge/Tests-17_Passed-brightgreen.svg)](https://pytest.org)

**Arsi-TeX** adalah sistem otomasi dokumen profesional (Proposal Penawaran Jasa, Spesifikasi Teknis Material, Invoice Termin Pembayaran, dan Kontrak Kerja Desain Arsitektur) yang dirancang khusus untuk arsitek, desainer interior, dan kontraktor kecil di Indonesia.

Aplikasi ini menggabungkan kecepatan pengisian form web intuitif dengan mesin typesetting modern **Typst**, menghasilkan dokumen PDF dengan tipografi tajam, margin presisi, repeating table header, dan penomoran otomatis tanpa pengguna perlu mempelajari sintaks kode apa pun.

---

## 📑 4 Jenis Dokumen Resmi yang Dihasilkan

| Jenis Dokumen | Kode Nomor | Deskripsi & Komponen Utama |
| :--- | :--- | :--- |
| **Proposal Desain** | `PROP/YYYY/MM/xxx` | Cover elegan, profil studio & klien, ringkasan data proyek, ruang lingkup jasa, tabel rincian biaya dengan repeating header, tahapan jadwal kerja, skema termin pembayaran, syarat & ketentuan, dan kolom tanda tangan. |
| **Spesifikasi Teknis** | `SPEK/YYYY/MM/xxx` | Dokumen spesifikasi material terorganisasi per area/ruang (item pekerjaan, jenis material, merek/tipe, volume, satuan, dan standar mutu pengerjaan) serta lembar persetujuan pemilik proyek. |
| **Invoice Tagihan** | `INV/YYYY/MM/xxx` | Kop surat resmi studio, nomor invoice, tanggal jatuh tempo, rincian termin tertagih, subtotal, diskon, PPN (11% / kustom), total, teks Terbilang Rupiah otomatis, instruksi rekening bank, dan catatan pembayaran. |
| **Kontrak Kerja Desain** | `KTR/YYYY/MM/xxx` | Perjanjian kerja formal antara Studio dan Klien yang memuat 9 pasal standar (Ruang Lingkup, Jangka Waktu, Nilai & Pembayaran, Hak & Kewajiban, Revisi & Approval, Hak Cipta Desain, Pembatalan, Force Majeure, Penyelesaian Sengketa) disertai kotak materai Rp 10.000 dan legal disclaimer. |

---

## ✨ Fitur Utama

### 1. Mesin PDF Berbasis Typst (Bukan Canvas / Screenshot Hack)
- Dokumen PDF dikompilasi langsung dari template Typst berkecepatan tinggi.
- Teks dokumen dapat disorot (searchable & selectable text), tajam untuk dicetak dalam ukuran A4.
- Tabel material panjang secara otomatis terpecah ke halaman baru dengan header tabel yang berulang (*repeating header*).

### 2. Logika Finansial Presisi & Terbilang Bahasa Indonesia
- **Integer Rupiah Penuh**: Seluruh perhitungan uang disimpan sebagai bilangan bulat Rupiah tanpa pembulatan *float* desimal yang rawan selisih.
- **Validasi 100% Termin**: Sistem memvalidasi akumulasi persentase termin harus tepat 100%. Sisa pembulatan Rupiah dialokasikan secara matematis ke termin terakhir agar totalnya klop.
- **Terbilang Otomatis**: Konversi angka Rupiah ke kata-kata berbahasa Indonesia formal (misal: `Rp 247.500.000` → *"Dua Ratus Empat Puluh Tujuh Juta Lima Ratus Ribu Rupiah"*).

### 3. Manajemen Klien & Proyek (CRUD & Duplikasi 1-Klik)
- **Database Penyimpanan**: Tersimpan rapi di SQLite (lokal/docker) dan siap bermigrasi ke PostgreSQL.
- **Duplikasi Proyek 1-Klik**: Duplikasi proyek lama beserta seluruh rincian spesifikasi material, jadwal kerja, dan termin pembayaran menjadi draf baru dalam hitungan detik.
- **Penomoran Dokumen Otomatis**: Penomoran terstandardisasi dan otomatis bertambah per bulan (misal `PROP/2026/11/001`, `PROP/2026/11/002`).

### 4. Immutabilitas Snapshot Dokumen
- Setiap dokumen yang diterbitkan secara resmi (`POST /api/projects/{id}/documents`) akan **mengunci seluruh data saat itu ke dalam JSON snapshot**.
- Perubahan data klien atau rincian proyek di kemudian hari **tidak akan merusak atau mengubah isi dokumen lama** yang telah diterbitkan sebelumnya. File PDF arsip dapat diunduh ulang kapan saja melalui tab Riwayat Dokumen.

### 5. Fleksibilitas Klausul Kontrak & Legal Disclaimer
- Memuat 9 klausul baku praktik arsitek & interior Indonesia yang dapat diaktifkan, dinonaktifkan, atau disunting langsung dari antarmuka web.
- Dilengkapi tombol reset ke klausul baku bawaan.
- Menampilkan *legal disclaimer* jelas bahwa draf kontrak merupakan panduan standar dan disarankan untuk ditinjau oleh konsultan hukum.

### 6. Branding Studio & Kustomisasi Warna
- Studio dapat mengatur nama usaha, alamat, kontak, nomor rekening, NPWP, serta memilih **Warna Utama** dan **Warna Aksen** brand.
- Warna brand otomatis disuntikkan ke dalam palet PDF Typst (garis aksen, badge nomor dokumen, header tabel, dan footer).

### 7. Pengalaman Pengguna (UI/UX)
- Stepper navigasi 7 tahap: **Studio & Klien → Data Proyek → Material & Biaya → Jadwal Kerja → Termin Pembayaran → Klausul Kontrak → Riwayat Dokumen**.
- **Autosave Draft**: Draf pengisian form otomatis tersimpan ke `localStorage` sehingga data tidak hilang saat tab tertutup tanpa sengaja.
- **Live PDF Preview**: Pratinjau dokumen langsung di samping form sebelum diterbitkan atau diunduh.

---

## 🛠️ Arsitektur & Stack Teknologi

```
Arsitex/
├── docker-compose.yml       # Orkestrasi Docker (Backend + Frontend)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── api/             # FastAPI Endpoints (clients, projects, documents, clauses, studio)
│   │   ├── core/            # Config & environment settings
│   │   ├── db/              # SQLAlchemy session & connection
│   │   ├── models/          # SQLAlchemy ORM Entities
│   │   ├── schemas/         # Pydantic v2 schemas
│   │   ├── services/
│   │   │   ├── calculator.py    # Integer math, Terbilang ID, PPN, termin
│   │   │   ├── numbering.py     # Sequential auto-numbering
│   │   │   ├── pdf_generator.py # Typst compiler wrapper
│   │   │   └── clauses_default.py # 9 pasal standar kontrak
│   │   ├── templates/       # Template Typst (.typ)
│   │   │   ├── proposal.typ
│   │   │   ├── spek.typ
│   │   │   ├── invoice.typ
│   │   │   └── kontrak.typ
│   │   └── main.py          # FastAPI application entrypoint
│   └── tests/               # 17 automated Pytest suites
└── frontend/
    ├── Dockerfile           # Multi-stage build (Node 22 -> Nginx Alpine)
    ├── nginx.conf           # Reverse proxy /api/ to backend:8000
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── App.tsx          # Main Stepper UI, Preview, Autosave & Project Drawer
        └── types.ts         # TypeScript strict interfaces
```

---

## 🚀 Cara Menjalankan

### Opsi A: Menggunakan Docker Compose (Direkomendasikan untuk Produksi)

Cukup satu perintah dari direktori root:

```bash
docker compose up --build -d
```

- **Aplikasi Web**: Buka [http://localhost:5173](http://localhost:5173) atau [http://localhost](http://localhost)
- **Backend API Docs (Swagger)**: Buka [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database & PDF Storage**: Terpasang otomatis di volume `./storage/`

Untuk menghentikan kontainer:
```bash
docker compose down
```

---

### Opsi B: Menjalankan Secara Lokal (Development Mode)

#### 1. Persiapan Backend
Pastikan Python 3.12+ telah terpasang:

```bash
cd backend

# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate

# Pasang dependensi
pip install -r requirements.txt

# Jalankan server FastAPI
uvicorn app.main:app --reload --port 8000
```
API akan aktif di `http://localhost:8000`.

#### 2. Persiapan Frontend
Buka terminal baru di folder `frontend`:

```bash
cd frontend

# Pasang paket node
npm install

# Jalankan Vite dev server
npm run dev
```
Aplikasi frontend akan aktif di `http://localhost:5173`.

---

## 🧪 Pengujian Otomatis (Automated Testing)

Arsi-TeX dilengkapi dengan pengujian komprehensif menggunakan Pytest yang menguji seluruh logika finansial, database, penomoran urut, hingga kompilasi PDF asli:

```bash
PYTHONPATH=backend backend/venv/bin/pytest backend/tests -v
```

Hasil uji: **17 passed** tanpa kegagalan:
1. `test_terbilang_dasar`: Validasi angka nol, belasan, puluhan, ratusan.
2. `test_terbilang_ribuan_jutaan`: Validasi jutaan, miliaran, triliunan.
3. `test_format_rupiah`: Validasi pemformatan `Rp 12.500.000`.
4. `test_calculate_financials`: Validasi subtotal, diskon, PPN 11%, dan total.
5. `test_calculate_terms_persen`: Validasi distribusi termin pembayaran normal.
6. `test_calculate_terms_persen_ganjil_dan_pembulatan`: Validasi pembagian 33.33% tanpa selisih 1 rupiah pun.
7. `test_calculate_terms_invalid_persen`: Menolak skema termin yang total persentasenya tidak 100%.
8. `test_client_crud`: Pengujian pembuatan, pembacaan, dan update klien.
9. `test_project_crud_and_duplicate`: Pengujian proyek dan duplikasi 1-klik beserta sub-item.
10. `test_auto_numbering_and_snapshot_immutability`: Pengujian nomor urut berulang dan isolasi snapshot dokumen lama.
11. `test_studio_branding`: Pengujian kustomisasi profil dan warna brand studio.
12. `test_contract_clauses`: Pengujian modifikasi klausul kontrak dan reset ke pasal baku.
13. `test_generate_proposal_pdf`: Kompilasi dokumen Proposal Typst menjadi byte PDF valid.
14. `test_generate_invoice_pdf`: Kompilasi dokumen Invoice Typst menjadi byte PDF valid.
15. `test_generate_spek_pdf`: Kompilasi dokumen Spesifikasi Teknis Typst menjadi byte PDF valid.
16. `test_generate_kontrak_pdf`: Kompilasi dokumen Kontrak Kerja Typst menjadi byte PDF valid.
17. `test_generate_proposal_multipage_table`: Pengujian tabel material lebih dari 40 baris agar otomatis memicu page break dan repeating header.

---

## 📡 Ringkasan Endpoint API

| Method | Endpoint | Deskripsi |
| :--- | :--- | :--- |
| `POST` | `/api/calculate` | Kalkulasi finansial instan (subtotal, diskon, PPN, termin, terbilang) |
| `POST` | `/api/documents/preview` | Preview instan PDF tanpa menyimpan ke database (mengembalikan stream PDF) |
| `POST` | `/api/documents/download` | Unduh langsung PDF draf sekali pakai |
| `GET` | `/api/documents/next-number?jenis={proposal\|spek\|invoice\|kontrak}` | Prediksi nomor dokumen urut berikutnya |
| `GET` | `/api/documents/{id}/pdf` | Unduh file PDF resmi berdasarkan snapshot yang terkunci |
| `GET` | `/api/clients` / `POST /api/clients` | Daftar & tambah data klien |
| `GET` | `/api/projects` / `POST /api/projects` | Daftar & simpan data proyek |
| `POST` | `/api/projects/{id}/duplicate` | Duplikasi proyek secara utuh (1-klik clone) |
| `POST` | `/api/projects/{id}/documents` | Terbitkan dokumen resmi, kunci snapshot, buat file arsip PDF |
| `GET` | `/api/projects/{id}/documents` | Ambil riwayat dokumen yang pernah diterbitkan untuk proyek ini |
| `GET` | `/api/clauses` / `PUT /api/clauses/{id}` | Ambil & perbarui klausul pasal kontrak |
| `POST` | `/api/clauses/reset` | Reset seluruh klausul kontrak ke standar baku 9 pasal |
| `GET` | `/api/studio` / `PUT /api/studio` | Profil studio & pengaturan warna branding (`warna_utama`, `warna_aksen`) |

---

## ⚖️ Lisensi & Catatan Hukum

- Template kontrak kerja arsitektur yang disediakan adalah draf panduan standar dan bukan merupakan nasihat hukum formal. Pengguna dianjurkan untuk meninjau kembali klausul kontrak bersama konsultan hukum sebelum ditandatangani para pihak.
