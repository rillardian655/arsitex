import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True, index=True)
    nama_usaha = Column(String(255), nullable=False)
    alamat = Column(Text, nullable=True)
    kontak = Column(String(100), nullable=True)
    logo_path = Column(String(255), nullable=True)
    rekening = Column(Text, nullable=True)
    npwp = Column(String(100), nullable=True)
    warna_utama = Column(String(50), default="#0284c7")
    warna_aksen = Column(String(50), default="#0f172a")
    format_penomoran = Column(String(100), default="{TYPE}/{YEAR}/{MONTH}/{SEQ:03d}")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(255), nullable=False)
    perusahaan = Column(String(255), nullable=True)
    alamat = Column(Text, nullable=True)
    telepon = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    catatan = Column(Text, nullable=True)

    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    nama = Column(String(255), nullable=False)
    lokasi = Column(String(255), nullable=True)
    luas_m2 = Column(Float, nullable=True)
    jenis = Column(String(100), nullable=True)
    ruang_lingkup = Column(Text, nullable=True)
    status = Column(String(50), default="draft")
    diskon_rp = Column(Integer, default=0)
    ppn_persen = Column(Float, default=11.0)
    dibuat_pada = Column(DateTime, default=utc_now)

    client = relationship("Client", back_populates="projects")
    material_items = relationship("MaterialItem", back_populates="project", cascade="all, delete-orphan")
    schedule_stages = relationship("ScheduleStage", back_populates="project", cascade="all, delete-orphan")
    payment_terms = relationship("PaymentTerm", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")

class MaterialItem(Base):
    __tablename__ = "material_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    area = Column(String(100), nullable=True)
    pekerjaan = Column(String(255), nullable=False)
    material = Column(String(255), nullable=False)
    merek = Column(String(100), nullable=True)
    volume = Column(Float, nullable=False, default=1.0)
    satuan = Column(String(50), nullable=False, default="ls")
    harga_satuan = Column(Integer, nullable=False, default=0)
    catatan = Column(Text, nullable=True)

    project = relationship("Project", back_populates="material_items")

class ScheduleStage(Base):
    __tablename__ = "schedule_stages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    tahap = Column(String(100), nullable=False)
    tanggal_mulai = Column(String(50), nullable=True)
    tanggal_selesai = Column(String(50), nullable=True)
    durasi = Column(String(50), nullable=True)
    keterangan = Column(Text, nullable=True)

    project = relationship("Project", back_populates="schedule_stages")

class PaymentTerm(Base):
    __tablename__ = "payment_terms"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    urutan = Column(Integer, nullable=False, default=1)
    label = Column(String(100), nullable=False)
    persen = Column(Float, nullable=True)
    nominal = Column(Integer, nullable=False, default=0)
    pemicu = Column(String(255), nullable=True)
    jatuh_tempo = Column(String(50), nullable=True)

    project = relationship("Project", back_populates="payment_terms")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    jenis = Column(String(50), nullable=False) # proposal, invoice, spek, kontrak
    nomor = Column(String(100), nullable=False)
    versi = Column(Integer, default=1)
    snapshot_data = Column(JSON, nullable=False)
    pdf_path = Column(String(255), nullable=True)
    dibuat_pada = Column(DateTime, default=utc_now)

    project = relationship("Project", back_populates="documents")

class ContractClause(Base):
    __tablename__ = "contract_clauses"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(50), unique=True, index=True, nullable=False)
    judul = Column(String(255), nullable=False)
    isi = Column(Text, nullable=False)
    urutan = Column(Integer, default=1)
    aktif = Column(Boolean, default=True)
