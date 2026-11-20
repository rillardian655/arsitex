from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class StudioData(BaseModel):
    nama_usaha: str = Field(default="Studio Arsitektur & Desain")
    alamat: Optional[str] = Field(default="Jl. Arsitektur No. 10, Jakarta Selatan")
    kontak: Optional[str] = Field(default="+62 812-3456-7890 | studio@arsitex.id")
    logo_path: Optional[str] = None
    rekening: Optional[str] = Field(default="BCA 1234567890 a.n Studio Arsitektur")
    npwp: Optional[str] = Field(default="01.234.567.8-901.000")

class ClientData(BaseModel):
    nama: str
    perusahaan: Optional[str] = ""
    alamat: Optional[str] = ""
    telepon: Optional[str] = ""
    email: Optional[str] = ""
    catatan: Optional[str] = ""

class MaterialItemData(BaseModel):
    area: Optional[str] = "Umum"
    pekerjaan: str
    material: str
    merek: Optional[str] = "-"
    volume: float = 1.0
    satuan: str = "ls"
    harga_satuan: int = 0
    catatan: Optional[str] = ""

class ScheduleStageData(BaseModel):
    tahap: str
    tanggal_mulai: Optional[str] = ""
    tanggal_selesai: Optional[str] = ""
    durasi: Optional[str] = ""
    keterangan: Optional[str] = ""

class PaymentTermData(BaseModel):
    urutan: int = 1
    label: str
    persen: Optional[float] = None
    nominal: Optional[int] = 0
    pemicu: Optional[str] = ""
    jatuh_tempo: Optional[str] = ""

class ProjectData(BaseModel):
    nama: str
    lokasi: Optional[str] = ""
    luas_m2: Optional[float] = 0.0
    jenis: Optional[str] = "Rumah Tinggal"
    ruang_lingkup: Optional[str] = "Perancangan Arsitektur & Desain Interior"

class DocumentGenerationRequest(BaseModel):
    jenis: Literal["proposal", "invoice", "spek", "kontrak"]
    nomor_dokumen: Optional[str] = ""
    tanggal_dokumen: Optional[str] = ""
    studio: StudioData
    client: ClientData
    project: ProjectData
    material_items: List[MaterialItemData] = []
    schedule_stages: List[ScheduleStageData] = []
    payment_terms: List[PaymentTermData] = []
    diskon_rp: int = 0
    ppn_persen: float = 11.0 # 0 jika non-PPN
    termin_terpilih_index: Optional[int] = 0 # khusus invoice: termin ke berapa yang ditagihkan

class CalculationResponse(BaseModel):
    subtotal: int
    diskon_rp: int
    dpp: int
    ppn_persen: float
    ppn_rp: int
    total: int
    terbilang_total: str
    calculated_terms: List[dict]

