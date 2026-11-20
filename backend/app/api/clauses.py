from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import ContractClause
from app.schemas.clauses import ContractClauseResponse, ContractClauseBulkUpdate
from app.services.clauses_default import DEFAULT_CLAUSES

router = APIRouter(prefix="/clauses", tags=["Contract Clauses"])

def ensure_default_clauses(db: Session):
    count = db.query(ContractClause).count()
    if count == 0:
        for c in DEFAULT_CLAUSES:
            db.add(ContractClause(**c))
        db.commit()

@router.get("", response_model=List[ContractClauseResponse])
def get_contract_clauses(db: Session = Depends(get_db)):
    """Mengambil seluruh daftar pasal/klausul kontrak kerja."""
    ensure_default_clauses(db)
    return db.query(ContractClause).order_by(ContractClause.urutan.asc()).all()

@router.put("", response_model=List[ContractClauseResponse])
def update_contract_clauses(data: ContractClauseBulkUpdate, db: Session = Depends(get_db)):
    """Memperbarui pasal/klausul kontrak kerja yang disunting oleh pengguna."""
    for item in data.clauses:
        clause = db.query(ContractClause).filter(ContractClause.kode == item.kode).first()
        if clause:
            clause.judul = item.judul
            clause.isi = item.isi
            clause.urutan = item.urutan
            clause.aktif = item.aktif
        else:
            db.add(ContractClause(**item.model_dump()))
    db.commit()
    return db.query(ContractClause).order_by(ContractClause.urutan.asc()).all()

@router.post("/reset", response_model=List[ContractClauseResponse])
def reset_contract_clauses(db: Session = Depends(get_db)):
    """Mereset seluruh pasal kontrak ke template standar arsitek Indonesia."""
    db.query(ContractClause).delete()
    for c in DEFAULT_CLAUSES:
        db.add(ContractClause(**c))
    db.commit()
    return db.query(ContractClause).order_by(ContractClause.urutan.asc()).all()

