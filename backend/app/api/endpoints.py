import datetime
from fastapi import APIRouter, HTTPException, Response
from app.schemas.document import DocumentGenerationRequest, CalculationResponse
from app.services.calculator import calculate_financials, calculate_terms, terbilang
from app.services.pdf_generator import generate_pdf, PDFGenerationError

router = APIRouter()

@router.post("/calculate", response_model=CalculationResponse)
def calculate_data(req: DocumentGenerationRequest):
    """Menghitung total, diskon, PPN, dan distribusi nominal termin."""
    try:
        financials = calculate_financials(
            req.material_items,
            diskon_rp=req.diskon_rp,
            ppn_persen=req.ppn_persen
        )
        calculated_terms = calculate_terms(financials["total"], req.payment_terms)

        return CalculationResponse(
            subtotal=financials["subtotal"],
            diskon_rp=financials["diskon_rp"],
            dpp=financials["dpp"],
            ppn_persen=financials["ppn_persen"],
            ppn_rp=financials["ppn_rp"],
            total=financials["total"],
            terbilang_total=financials["terbilang_total"],
            calculated_terms=calculated_terms
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan kalkulasi: {str(e)}")


@router.post("/documents/preview")
def preview_document_pdf(req: DocumentGenerationRequest):
    """Mengompilasi dan mengembalikan pratinjau dokumen PDF secara inline."""
    try:
        data_dict = req.model_dump()
        pdf_bytes = generate_pdf(req.jenis, data_dict)
        
        filename = f"{req.jenis}_{datetime.date.today().strftime('%Y%m%d')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"'
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except PDFGenerationError as pge:
        raise HTTPException(status_code=500, detail=str(pge))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses PDF: {str(e)}")


@router.post("/documents/download")
def download_document_pdf(req: DocumentGenerationRequest):
    """Mengompilasi dan mengembalikan dokumen PDF sebagai attachment (unduhan)."""
    try:
        data_dict = req.model_dump()
        pdf_bytes = generate_pdf(req.jenis, data_dict)
        
        clean_num = (req.nomor_dokumen or "DOK").replace("/", "_")
        filename = f"{req.jenis.upper()}_{clean_num}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except PDFGenerationError as pge:
        raise HTTPException(status_code=500, detail=str(pge))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses PDF: {str(e)}")


@router.get("/sample-data")
def get_sample_data():
    """Mengembalikan data contoh proyek arsitektur Indonesia yang realistis."""
    return {
        "jenis": "proposal",
        "nomor_dokumen": "PROP/2026/11/008",
        "tanggal_dokumen": "20 November 2026",
        "studio": {
            "nama_usaha": "Atelier Runa Studio Arsitektur",
            "alamat": "Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan",
            "kontak": "+62 811-9876-5432 | halo@runastudio.id",
            "rekening": "BCA 8800-9911-22 a.n Atelier Runa Desain Studio",
            "npwp": "02.891.432.1-013.000"
        },
        "client": {
            "nama": "Bapak Arya Pratama & Ibu Sarah",
            "perusahaan": "Pratama Hospitality Group",
            "alamat": "Cluster Bukit Hijau B-12, Cilandak, Jakarta Selatan",
            "telepon": "+62 812-8899-7766",
            "email": "arya.pratama@gmail.com",
            "catatan": "Klien menghendaki konsep Modern Japandi Tropis dengan bukaan cahaya maksimal."
        },
        "project": {
            "nama": "Villa Paviliun & Rumah Tinggal Arya",
            "lokasi": "Jl. Lembah Pakar Timur No. 8, Bandung",
            "luas_m2": 320.0,
            "jenis": "Rumah Tinggal & Paviliun",
            "ruang_lingkup": "Perancangan Konsep Arsitektur, Desain Interior Ruang Utama, Gambar Kerja DED, Rencana Anggaran Biaya (RAB), dan Pengawasan Berkala."
        },
        "material_items": [
            {
                "area": "Fasad & Eksterior",
                "pekerjaan": "Finishing Dinding Bata Ringan & Kamprot",
                "material": "Semen Plester Kamprot & Cat Weathercoat",
                "merek": "Dulux Weathershield",
                "volume": 140.0,
                "satuan": "m²",
                "harga_satuan": 185000,
                "catatan": "Warna Sand Stone Matt"
            },
            {
                "area": "Fasad & Pintu",
                "pekerjaan": "Kusen dan Pintu Kayu Kisi-Kisi",
                "material": "Kayu Ulin Solid Oven Grade A",
                "merek": "Custom Carpenter",
                "volume": 1.0,
                "satuan": "unit",
                "harga_satuan": 18500000,
                "catatan": "Finishing polyurethane outdoor"
            },
            {
                "area": "Lantai 1 (Living & Dining)",
                "pekerjaan": "Pemasangan Lantai Granit Tile 60x120",
                "material": "Granite Tile Glazed Polished",
                "merek": "Indogress Travertine Series",
                "volume": 95.0,
                "satuan": "m²",
                "harga_satuan": 380000,
                "catatan": "Pola random vein"
            },
            {
                "area": "Plafon",
                "pekerjaan": "Plafon Gypsum 9mm Rangka Hollow Galvanis",
                "material": "Gypsum Board Jaya & Hollow 4x4",
                "merek": "Jayaboard",
                "volume": 120.0,
                "satuan": "m²",
                "harga_satuan": 145000,
                "catatan": "Drop ceiling untuk indirect warm lighting"
            },
            {
                "area": "Master Bedroom",
                "pekerjaan": "Lantai Parket Kayu Engineered",
                "material": "Engineered White Oak Flooring",
                "merek": "QuickStep Wood Series",
                "volume": 35.0,
                "satuan": "m²",
                "harga_satuan": 520000,
                "catatan": "Underlayer foam antibakteri"
            },
            {
                "area": "Master Bathroom",
                "pekerjaan": "Sanitary & Faucet Kamar Mandi",
                "material": "Monoblok Gantung & Rain Shower Mixer",
                "merek": "Toto Matt Black Edition",
                "volume": 1.0,
                "satuan": "set",
                "harga_satuan": 14500000,
                "catatan": "Garansi resmi distributor"
            }
        ],
        "schedule_stages": [
            {
                "tahap": "Tahap 1: Pengumpulan Data & Skematik Desain",
                "tanggal_mulai": "01 Des 2026",
                "tanggal_selesai": "14 Des 2026",
                "durasi": "2 Minggu",
                "keterangan": "Moodboard, denah tata ruang 2D, konsep massa bangunan 3D"
            },
            {
                "tahap": "Tahap 2: Pengembangan Desain & 3D Render",
                "tanggal_mulai": "15 Des 2026",
                "tanggal_selesai": "05 Jan 2027",
                "durasi": "3 Minggu",
                "keterangan": "Visualisasi 3D Photorealistic eksterior & interior utama"
            },
            {
                "tahap": "Tahap 3: Gambar Kerja Detail (DED) & RAB",
                "tanggal_mulai": "06 Jan 2027",
                "tanggal_selesai": "25 Jan 2027",
                "durasi": "3 Minggu",
                "keterangan": "Gambar arsitektur, struktur, MEP, dan spesifikasi material final"
            },
            {
                "tahap": "Tahap 4: Pengawasan Berkala & Serah Terima",
                "tanggal_mulai": "Februari 2027",
                "tanggal_selesai": "Sesuai Proyek",
                "durasi": "Fleksibel",
                "keterangan": "Inspeksi mingguan dan pendampingan pemilihan material"
            }
        ],
        "payment_terms": [
            {
                "urutan": 1,
                "label": "Termin 1 (DP Konsep)",
                "persen": 30.0,
                "pemicu": "Penandatanganan kontrak proposal & persetujuan skematik",
                "jatuh_tempo": "H+3 penandatanganan"
            },
            {
                "urutan": 2,
                "label": "Termin 2 (Pengembangan Desain)",
                "persen": 40.0,
                "pemicu": "Persetujuan final 3D render & tata ruang",
                "jatuh_tempo": "Sebelum pengerjaan gambar kerja detail"
            },
            {
                "urutan": 3,
                "label": "Termin 3 (Pelunasan Dokumen)",
                "persen": 30.0,
                "pemicu": "Penyerahan bundel Gambar Kerja DED, RAB & spesifikasi final",
                "jatuh_tempo": "Saat serah terima bundel dokumen cetak & PDF"
            }
        ],
        "diskon_rp": 2500000,
        "ppn_persen": 11.0,
        "termin_terpilih_index": 0
    }

