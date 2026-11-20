import os
import json
import tempfile
from typing import Dict, Any
import typst

from app.services.calculator import calculate_financials, calculate_terms
from app.services.clauses_default import DEFAULT_CLAUSES

class PDFGenerationError(Exception):
    pass

def generate_pdf(doc_type: str, raw_data: Dict[str, Any]) -> bytes:
    """
    Mengompilasi template Typst menjadi byte PDF dengan data JSON yang sudah dihitung.
    doc_type: 'proposal', 'invoice', 'spek', atau 'kontrak'
    """
    template_filename = f"{doc_type}.typ"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "templates", template_filename)

    if not os.path.exists(template_path):
        raise PDFGenerationError(f"Template tidak ditemukan: {template_path}")

    material_items = raw_data.get("material_items", [])
    diskon_rp = raw_data.get("diskon_rp", 0)
    ppn_persen = raw_data.get("ppn_persen", 11.0)
    
    financials = calculate_financials(material_items, diskon_rp=diskon_rp, ppn_persen=ppn_persen)
    payment_terms = raw_data.get("payment_terms", [])
    calculated_terms = calculate_terms(financials["total"], payment_terms)

    # Pastikan branding studio memiliki warna default jika tidak disetel
    studio_info = raw_data.get("studio", {})
    if isinstance(studio_info, dict):
        if not studio_info.get("warna_utama"):
            studio_info["warna_utama"] = "#0284c7"
        if not studio_info.get("warna_aksen"):
            studio_info["warna_aksen"] = "#0f172a"
        raw_data["studio"] = studio_info

    payload = {
        **raw_data,
        "financials": financials,
        "payment_terms": calculated_terms,
        "calculated_items": financials["items"]
    }

    # Untuk kontrak, siapkan pasal-pasal
    if doc_type == "kontrak" and "clauses" not in payload:
        payload["clauses"] = DEFAULT_CLAUSES

    # Jika invoice, siapkan data termin terpilih
    if doc_type == "invoice":
        idx = raw_data.get("termin_terpilih_index", 0)
        if 0 <= idx < len(calculated_terms):
            selected_term = calculated_terms[idx]
        elif calculated_terms:
            selected_term = calculated_terms[0]
        else:
            selected_term = {
                "label": "Tagihan Proyek",
                "nominal": financials["total"],
                "nominal_fmt": financials["total_fmt"],
                "pemicu": "Tagihan Pembayaran",
                "terbilang": financials["terbilang_total"]
            }
        payload["selected_term"] = selected_term

    with tempfile.TemporaryDirectory() as tmpdir:
        json_file_path = os.path.join(tmpdir, "data.json")
        typ_file_path = os.path.join(tmpdir, template_filename)

        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(template_path, "r", encoding="utf-8") as f_src:
            template_content = f_src.read()

        with open(typ_file_path, "w", encoding="utf-8") as f_dst:
            f_dst.write(template_content)

        try:
            pdf_bytes = typst.compile(typ_file_path, root=tmpdir)
            return pdf_bytes
        except Exception as e:
            raise PDFGenerationError(f"Gagal mengompilasi Typst PDF ({doc_type}): {str(e)}")
