# Arsi-TeX

> Automated Architecture & Interior Document Generator Powered by FastAPI, Typst, and React.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Typst](https://img.shields.io/badge/PDF_Engine-Typst-239dad.svg)](https://typst.app)
[![React](https://img.shields.io/badge/Frontend-React_19_TypeScript-61dafb.svg?logo=react&logoColor=black)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind_CSS_v4-38bdf8.svg?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Container-Docker_Compose-2496ed.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Tests-17_Passed-2ea44f.svg)](https://pytest.org)

Arsi-TeX adalah sistem otomatisasi dokumen terpadu yang dirancang untuk arsitek, desainer interior, dan kontraktor skala menengah ke bawah di Indonesia. Sistem ini mengeliminasi pekerjaan administratif manual dalam penyusunan proposal penawaran, rincian spesifikasi teknis, invoice penagihan termin, dan kontrak kerja formal.

Berbeda dengan solusi generator dokumen berbasis HTML canvas atau screenshot DOM yang menghasilkan teks buram dan pagination tidak presisi, Arsi-TeX mengintegrasikan mesin typesetting **Typst** secara native di sisi backend. Hasil akhir berupa file PDF berstandar cetak dengan tipografi presisi, teks yang dapat diseleksi (searchable vector text), penomoran halaman otomatis, dan pemecahan tabel dinamis (*repeating table header*).

---

## Dokumen yang Dihasilkan

Sistem menyediakan 4 template dokumen terstandardisasi:

| Jenis Dokumen | Format Penomoran | Komponen Utama |
| :--- | :--- | :--- |
| Proposal Desain | `PROP/YYYY/MM/xxx` | Cover resmi studio, profil klien, parameter proyek (luas, lokasi, tipologi), ruang lingkup jasa terstruktur, tabel rincian biaya dengan repeating header, jadwal tahapan kerja, skema termin, dan kolom tanda tangan kedua pihak. |
| Spesifikasi Teknis | `SPEK/YYYY/MM/xxx` | Matriks spesifikasi material per area/ruang pekerjaan, volume, satuan, merek/tipe material, instruksi teknis instalasi, standar mutu pengerjaan, dan lembar persetujuan owner. |
| Invoice Tagihan | `INV/YYYY/MM/xxx` | Kop surat studio, nomor faktur urut, jatuh tempo, pemetaan termin tertagih, subtotal, diskon, PPN (11% atau kustom), total Rupiah, konversi teks Terbilang otomatis, dan instruksi rekening transfer. |
| Kontrak Kerja Desain | `KTR/YYYY/MM/xxx` | Perjanjian kerja formal 9 pasal standar praktik arsitektur (Ruang Lingkup, Jangka Waktu, Nilai Kontrak & Termin, Hak & Kewajiban, Revisi & Approval, Hak Cipta Desain, Pembatalan, Force Majeure, Penyelesaian Sengketa), kotak materai Rp 10.000, dan klausul disclaimer. |

---

## Fitur Utama

### 1. Mesin Kompilasi PDF Typst
- Kompilasi dokumen native tanpa dependensi headless browser yang berat.
- Tipografi tajam berbasis format A4 dengan margin yang konsisten.
- Penanganan tabel panjang otomatis (*multi-page table break*) dengan header kolom yang berulang pada setiap halaman baru.

### 2. Akurasi Finansial dan Terbilang Otomatis
- **Aritmatika Integer Rupiah**: Seluruh kalkulasi finansial dihitung dalam representasi bilangan bulat untuk menghindari *floating-point rounding error*.
- **Distribusi Sisa Pembulatan**: Pembagian termin persentase divalidasi ketat (harus tepat 100%). Sisa pembulatan Rupiah dialokasikan secara otomatis ke termin akhir sehingga akumulasi nominal termin tepat bernilai sama dengan total proyek.
- **Konversi Terbilang Bahasa Indonesia**: Parser bilangan otomatis yang menghasilkan kalimat baku terbilang bahasa Indonesia (contoh: Rp 247.500.000 dikonversi menjadi "Dua Ratus Empat Puluh Tujuh Juta Lima Ratus Ribu Rupiah").

### 3. Manajemen Klien, Proyek, dan Duplikasi Instan
- Database terstruktur untuk entitas studio, klien, proyek, rincian material, tahapan kerja, dan termin pembayaran.
- **Duplikasi Proyek 1-Klik**: Kemampuan kloning proyek lama beserta seluruh rincian spesifikasi dan skema pembayarannya menjadi draf proyek baru dalam hitungan detik.
- **Penomoran Urut Otomatis**: Generator nomor dokumen berurutan per kategori dokumen dan per periode bulan (contoh: `PROP/2026/11/001`, `PROP/2026/11/002`).

### 4. Immutabilitas Snapshot Dokumen
- Setiap penerbitan dokumen resmi mengunci salinan data proyek saat itu (*immutable JSON snapshot*) ke database.
- Perubahan atau pembaruan pada data proyek di masa mendatang tidak akan memengaruhi dokumen historis yang sudah diterbitkan.
- File PDF yang telah diterbitkan dapat diunduh ulang kapan saja melalui tab Riwayat Dokumen.

### 5. Kustomisasi Branding dan Fleksibilitas Klausul
- Pengaturan identitas studio mencakup logo, kontak resmi, rekening perbankan, NPWP, serta penyesuaian **Warna Utama** dan **Warna Aksen** brand yang langsung terintegrasi ke palet dokumen PDF.
- Editor pasal kontrak interaktif: setiap pasal dapat diedit, diaktifkan, dinonaktifkan, atau dikembalikan ke format baku bawaan (*factory reset*).
- Penyimpanan draf otomatis (*local storage autosave*) untuk mencegah kehilangan data saat form tertutup.

---

## Arsitektur Sistem

```
Arsitex/
├── docker-compose.yml              # Orkestrasi multi-container
├── backend/
│   ├── Dockerfile                  # Container backend (Python 3.12-slim + font liberation)
│   ├── requirements.txt            # Dependensi backend
│   ├── app/
│   │   ├── api/                    # Router endpoint REST API
│   │   │   ├── clients.py          # CRUD data klien
│   │   │   ├── projects.py         # CRUD proyek, duplikasi, penerbitan dokumen
│   │   │   ├── documents.py        # Pengunduhan PDF snapshot dan auto-numbering
│   │   │   ├── clauses.py          # Manajemen pasal kontrak
│   │   │   ├── studio.py           # Konfigurasi profil & warna studio
│   │   │   └── endpoints.py        # Utilitas kalkulasi dan preview instan
│   │   ├── core/                   # Konfigurasi aplikasi & environment
│   │   ├── db/                     # Sesi SQLAlchemy & koneksi database
│   │   ├── models/                 # Definisi skema ORM SQLAlchemy
│   │   ├── schemas/                # Skema validasi Pydantic v2
│   │   ├── services/
│   │   │   ├── calculator.py       # Aritmatika finansial, PPN, termin, terbilang
│   │   │   ├── numbering.py        # Generator nomor urut dokumen
│   │   │   ├── pdf_generator.py    # Wrapper kompilasi Typst ke PDF stream
│   │   │   └── clauses_default.py  # 9 pasal standar kontrak arsitektur
│   │   ├── templates/              # File template typesetting Typst (.typ)
│   │   │   ├── proposal.typ
│   │   │   ├── spek.typ
│   │   │   ├── invoice.typ
│   │   │   └── kontrak.typ
│   │   └── main.py                 # Titik masuk aplikasi FastAPI
│   └── tests/                      # Rangkaian pengujian unit Pytest
└── frontend/
    ├── Dockerfile                  # Multi-stage container build (Node 22 -> Nginx Alpine)
    ├── nginx.conf                  # Konfigurasi reverse proxy Nginx
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── App.tsx                 # Form stepper, live preview, drawer, dan riwayat
        ├── types.ts                # Deklarasi tipe TypeScript ketat
        ├── main.tsx                # Entry point React
        └── index.css               # Setup Tailwind CSS v4
```

---

## Panduan Instalasi dan Menjalankan

### Opsi 1: Menggunakan Docker Compose (Direkomendasikan)

Prasyarat: Docker Engine dan Docker Compose telah terpasang.

Jalankan perintah berikut pada direktori utama:

```bash
docker compose up --build -d
```

Akses layanan:
- Frontend Web App: `http://localhost:5173` atau `http://localhost`
- Dokumentasi API Interaktif (Swagger UI): `http://localhost:8000/docs`
- Redoc API: `http://localhost:8000/redoc`

Untuk menghentikan kontainer:
```bash
docker compose down
```

---

### Opsi 2: Menjalankan Secara Lokal (Development)

#### Backend (FastAPI)
Prasyarat: Python 3.12 atau yang lebih baru.

```bash
cd backend

# Membuat dan mengaktifkan virtual environment
python3 -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate

# Menginstal dependensi
pip install -r requirements.txt

# Menjalankan server pengembangan
uvicorn app.main:app --reload --port 8000
```

#### Frontend (React + Vite)
Prasyarat: Node.js 20 atau yang lebih baru.

```bash
cd frontend

# Menginstal paket dependensi
npm install

# Menjalankan server pengembangan Vite
npm run dev
```

Aplikasi frontend dapat diakses melalui browser pada alamat `http://localhost:5173`.

---

## Konfigurasi Environment

Aplikasi dapat dikonfigurasi melalui environment variable atau file `.env`:

| Variabel | Default | Keterangan |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./arsitex.db` | URL koneksi database (SQLite atau PostgreSQL) |
| `STORAGE_DIR` | `storage` | Direktori penyimpanan file PDF arsip |
| `TEMPLATES_DIR` | `app/templates` | Direktori penyimpanan template Typst |

---

## Pengujian Otomatis

Rangkaian unit test komprehensif memvalidasi integritas logika finansial, database, nomor urut dokumen, dan kompilasi PDF.

Jalankan seluruh test suite menggunakan perintah:

```bash
PYTHONPATH=backend backend/venv/bin/pytest backend/tests -v
```

Cakupan pengujian (17 skenario lulus):
- `test_terbilang_dasar`: Validasi bilangan nol, satuan, belasan, dan puluhan.
- `test_terbilang_ribuan_jutaan`: Validasi bilangan jutaan, miliaran, dan triliunan.
- `test_format_rupiah`: Format mata uang standar Indonesia (`Rp 12.500.000`).
- `test_calculate_financials`: Perhitungan subtotal material, diskon, DPP, PPN 11%, dan total akhir.
- `test_calculate_terms_persen`: Distribusi nominal termin berbasis persentase.
- `test_calculate_terms_persen_ganjil_dan_pembulatan`: Distribusi presisi persentase ganjil (33.33%) dengan alokasi sisa pembulatan pada termin akhir.
- `test_calculate_terms_invalid_persen`: Penolakan skema termin apabila total persentase tidak tepat 100%.
- `test_client_crud`: Siklus hidup pembuatan, pembacaan, dan pembaharuan profil klien.
- `test_project_crud_and_duplicate`: Pembuatan proyek dan duplikasi instan beserta seluruh relasi sub-item.
- `test_auto_numbering_and_snapshot_immutability`: Generator nomor berurutan dan penguncian snapshot data dokumen lama.
- `test_studio_branding`: Penyimpanan profil studio dan warna kustom.
- `test_contract_clauses`: Penyesuaian isi klausul kontrak dan fungsionalitas reset ke pasal baku.
- `test_generate_proposal_pdf`: Kompilasi template Proposal ke dalam byte PDF valid.
- `test_generate_invoice_pdf`: Kompilasi template Invoice ke dalam byte PDF valid.
- `test_generate_spek_pdf`: Kompilasi template Spesifikasi Teknis ke dalam byte PDF valid.
- `test_generate_kontrak_pdf`: Kompilasi template Kontrak Kerja Desain ke dalam byte PDF valid.
- `test_generate_proposal_multipage_table`: Pengujian tabel volume besar untuk memastikan page break dan header berulang berjalan sempurna.

---

## Dokumentasi Endpoint REST API

| Method | Endpoint | Fungsi |
| :--- | :--- | :--- |
| `POST` | `/api/calculate` | Kalkulasi finansial cepat (subtotal, diskon, PPN, termin, terbilang). |
| `POST` | `/api/documents/preview` | Render preview stream PDF langsung tanpa menyimpan ke database. |
| `POST` | `/api/documents/download` | Unduh file PDF draf instan. |
| `GET` | `/api/documents/next-number` | Ambil nomor dokumen urut berikutnya berdasarkan jenis dokumen (`proposal`, `spek`, `invoice`, `kontrak`). |
| `GET` | `/api/documents/{id}/pdf` | Unduh file PDF resmi berdasarkan snapshot data yang terkunci. |
| `GET` | `/api/clients` | Mengambil seluruh daftar klien terdaftar. |
| `POST` | `/api/clients` | Menambahkan profil klien baru. |
| `GET` | `/api/projects` | Mengambil seluruh daftar proyek aktif. |
| `POST` | `/api/projects` | Menyimpan proyek baru beserta seluruh rincian spesifikasi, jadwal, dan termin. |
| `POST` | `/api/projects/{id}/duplicate` | Duplikasi proyek 1-klik menjadi draf baru. |
| `POST` | `/api/projects/{id}/documents` | Terbitkan dokumen resmi, kunci snapshot data, dan buat arsip file PDF fisik. |
| `GET` | `/api/projects/{id}/documents` | Riwayat seluruh dokumen yang pernah diterbitkan untuk proyek terkait. |
| `GET` | `/api/clauses` | Mengambil daftar klausul pasal kontrak kerja. |
| `PUT` | `/api/clauses/{id}` | Memperbarui isi klausul kontrak kerja. |
| `POST` | `/api/clauses/reset` | Mengembalikan seluruh klausul kontrak ke standar baku 9 pasal. |
| `GET` | `/api/studio` | Mengambil data profil dan pengaturan warna branding studio. |
| `PUT` | `/api/studio` | Memperbarui profil dan warna branding studio. |

---

## Ketentuan Hukum dan Batasan

Template dokumen perjanjian kerja arsitektur yang disediakan sistem adalah draf panduan standar berdasarkan praktik umum di Indonesia dan tidak dimaksudkan sebagai nasihat hukum formal. Pengguna disarankan untuk meninjau kembali klausul kontrak bersama konsultan hukum sebelum ditandatangani oleh para pihak.
