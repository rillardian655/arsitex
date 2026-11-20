import datetime
import re
from sqlalchemy.orm import Session
from app.models.entities import Document

PREFIX_MAP = {
    "proposal": "PROP",
    "invoice": "INV",
    "spek": "SPEK",
    "kontrak": "KTR"
}

def generate_document_number(db: Session, doc_type: str, date: datetime.date = None) -> str:
    """
    Menghasilkan nomor dokumen otomatis yang unik dan berurutan per jenis dokumen dan per periode.
    Format default: {TYPE}/{YEAR}/{MONTH:02d}/{SEQ:03d}
    Contoh: PROP/2026/11/001, INV/2026/11/001
    """
    if date is None:
        date = datetime.date.today()

    prefix = PREFIX_MAP.get(doc_type.lower(), doc_type.upper()[:4])
    year_str = f"{date.year}"
    month_str = f"{date.month:02d}"
    prefix_pattern = f"{prefix}/{year_str}/{month_str}/"

    # Cari semua dokumen dengan pola prefix bulan ini
    existing_docs = db.query(Document.nomor).filter(
        Document.nomor.like(f"{prefix_pattern}%")
    ).all()

    max_seq = 0
    seq_regex = re.compile(rf"^{re.escape(prefix_pattern)}(\d+)$")

    for (nomor,) in existing_docs:
        match = seq_regex.match(nomor)
        if match:
            try:
                seq_val = int(match.group(1))
                if seq_val > max_seq:
                    max_seq = seq_val
            except ValueError:
                pass

    next_seq = max_seq + 1
    new_number = f"{prefix_pattern}{next_seq:03d}"

    # Pastikan nomor benar-benar unik
    while db.query(Document).filter(Document.nomor == new_number).first() is not None:
        next_seq += 1
        new_number = f"{prefix_pattern}{next_seq:03d}"

    return new_number

