from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class ContractClauseIn(BaseModel):
    kode: str
    judul: str
    isi: str
    urutan: Optional[int] = 1
    aktif: Optional[bool] = True

class ContractClauseResponse(ContractClauseIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ContractClauseBulkUpdate(BaseModel):
    clauses: List[ContractClauseIn]

class StudioSettingsUpdate(BaseModel):
    nama_usaha: Optional[str] = None
    alamat: Optional[str] = None
    kontak: Optional[str] = None
    logo_path: Optional[str] = None
    rekening: Optional[str] = None
    npwp: Optional[str] = None
    warna_utama: Optional[str] = None
    warna_aksen: Optional[str] = None
    format_penomoran: Optional[str] = None

class StudioSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama_usaha: str
    alamat: Optional[str] = ""
    kontak: Optional[str] = ""
    logo_path: Optional[str] = None
    rekening: Optional[str] = ""
    npwp: Optional[str] = ""
    warna_utama: str
    warna_aksen: str
    format_penomoran: str

