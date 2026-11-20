import datetime
from typing import List, Optional, Literal, Any, Dict
from pydantic import BaseModel, ConfigDict

# === CLIENT SCHEMAS ===
class ClientBase(BaseModel):
    nama: str
    perusahaan: Optional[str] = ""
    alamat: Optional[str] = ""
    telepon: Optional[str] = ""
    email: Optional[str] = ""
    catatan: Optional[str] = ""

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    nama: Optional[str] = None
    perusahaan: Optional[str] = None
    alamat: Optional[str] = None
    telepon: Optional[str] = None
    email: Optional[str] = None
    catatan: Optional[str] = None

class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_count: Optional[int] = 0

# === SUB-ITEM SCHEMAS ===
class MaterialItemIn(BaseModel):
    area: Optional[str] = "Umum"
    pekerjaan: str
    material: str
    merek: Optional[str] = "-"
    volume: float = 1.0
    satuan: str = "ls"
    harga_satuan: int = 0
    catatan: Optional[str] = ""

class MaterialItemResponse(MaterialItemIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int

class ScheduleStageIn(BaseModel):
    tahap: str
    tanggal_mulai: Optional[str] = ""
    tanggal_selesai: Optional[str] = ""
    durasi: Optional[str] = ""
    keterangan: Optional[str] = ""

class ScheduleStageResponse(ScheduleStageIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int

class PaymentTermIn(BaseModel):
    urutan: int = 1
    label: str
    persen: Optional[float] = None
    nominal: Optional[int] = 0
    pemicu: Optional[str] = ""
    jatuh_tempo: Optional[str] = ""

class PaymentTermResponse(PaymentTermIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int

# === PROJECT SCHEMAS ===
class ProjectBase(BaseModel):
    nama: str
    lokasi: Optional[str] = ""
    luas_m2: Optional[float] = 0.0
    jenis: Optional[str] = "Rumah Tinggal"
    ruang_lingkup: Optional[str] = ""
    status: Optional[str] = "draft"
    diskon_rp: Optional[int] = 0
    ppn_persen: Optional[float] = 11.0

class ProjectCreate(ProjectBase):
    client_id: int
    material_items: List[MaterialItemIn] = []
    schedule_stages: List[ScheduleStageIn] = []
    payment_terms: List[PaymentTermIn] = []

class ProjectUpdate(BaseModel):
    nama: Optional[str] = None
    client_id: Optional[int] = None
    lokasi: Optional[str] = None
    luas_m2: Optional[float] = None
    jenis: Optional[str] = None
    ruang_lingkup: Optional[str] = None
    status: Optional[str] = None
    diskon_rp: Optional[int] = None
    ppn_persen: Optional[float] = None
    material_items: Optional[List[MaterialItemIn]] = None
    schedule_stages: Optional[List[ScheduleStageIn]] = None
    payment_terms: Optional[List[PaymentTermIn]] = None

class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    client_id: int
    dibuat_pada: datetime.datetime
    client_nama: Optional[str] = ""
    document_count: Optional[int] = 0

class ProjectDetailResponse(ProjectResponse):
    model_config = ConfigDict(from_attributes=True)
    client: ClientResponse
    material_items: List[MaterialItemResponse] = []
    schedule_stages: List[ScheduleStageResponse] = []
    payment_terms: List[PaymentTermResponse] = []

# === DOCUMENT SCHEMAS ===
class DocumentCreateRequest(BaseModel):
    jenis: Literal["proposal", "invoice", "spek", "kontrak"]
    termin_terpilih_index: Optional[int] = 0
    tanggal_dokumen: Optional[str] = ""

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    jenis: str
    nomor: str
    versi: int
    dibuat_pada: datetime.datetime
    pdf_download_url: str

class DocumentDetailResponse(DocumentResponse):
    model_config = ConfigDict(from_attributes=True)
    snapshot_data: Dict[str, Any]
