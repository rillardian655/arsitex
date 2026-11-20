import os
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Document
from app.schemas.crud import DocumentDetailResponse
from app.services.numbering import generate_document_number
from app.services.pdf_generator import generate_pdf

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/next-number")
def get_next_document_number(
    jenis: str = Query("proposal", pattern="^(proposal|invoice|spek|kontrak)$"),
    db: Session = Depends(get_db)
):
    """Mendapatkan nomor urut dokumen otomatis berikutnya untuk jenis tertentu."""
    number = generate_document_number(db, jenis)
    return {"jenis": jenis, "next_number": number}

@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document_detail(document_id: int, db: Session = Depends(get_db)):
    """Mengambil detail dokumen dan data snapshot-nya."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")
    return DocumentDetailResponse(
        id=doc.id,
        project_id=doc.project_id,
        jenis=doc.jenis,
        nomor=doc.nomor,
        versi=doc.versi,
        dibuat_pada=doc.dibuat_pada,
        pdf_download_url=f"/api/documents/{doc.id}/pdf",
        snapshot_data=doc.snapshot_data
    )

@router.get("/{document_id}/pdf")
def download_document_pdf(document_id: int, db: Session = Depends(get_db)):
    """
    Mengunduh file PDF resmi berdasarkan snapshot data yang terkunci.
    Perubahan data proyek di kemudian hari tidak akan memengaruhi isi PDF ini.
    """
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")

    clean_num = doc.nomor.replace("/", "_")
    filename = f"{clean_num}.pdf"

    if doc.pdf_path and os.path.exists(doc.pdf_path):
        with open(doc.pdf_path, "rb") as f:
            pdf_bytes = f.read()
    else:
        pdf_bytes = generate_pdf(doc.jenis, doc.snapshot_data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{filename}"'
        }
    )
