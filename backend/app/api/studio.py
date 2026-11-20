from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Studio
from app.schemas.clauses import StudioSettingsUpdate, StudioSettingsResponse

router = APIRouter(prefix="/studio", tags=["Studio & Branding"])

def get_or_create_studio(db: Session) -> Studio:
    studio = db.query(Studio).first()
    if not studio:
        studio = Studio(
            nama_usaha="Studio Arsitektur & Desain",
            alamat="Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan",
            kontak="+62 811-9876-5432 | studio@arsitex.id",
            rekening="BCA 8800-9911-22 a.n Studio Arsitektur",
            npwp="02.891.432.1-013.000",
            warna_utama="#0284c7",
            warna_aksen="#0f172a",
            format_penomoran="{TYPE}/{YEAR}/{MONTH}/{SEQ:03d}"
        )
        db.add(studio)
        db.commit()
        db.refresh(studio)
    return studio

@router.get("", response_model=StudioSettingsResponse)
def get_studio_profile(db: Session = Depends(get_db)):
    """Mengambil profil dan branding studio."""
    return get_or_create_studio(db)

@router.put("", response_model=StudioSettingsResponse)
def update_studio_profile(data: StudioSettingsUpdate, db: Session = Depends(get_db)):
    """Memperbarui informasi dan branding studio (warna utama, rekening, nama, dll)."""
    studio = get_or_create_studio(db)
    for field, val in data.model_dump(exclude_unset=True).items():
        if val is not None:
            setattr(studio, field, val)
    db.commit()
    db.refresh(studio)
    return studio

