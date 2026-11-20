import os
import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import (
    Client,
    Project,
    MaterialItem,
    ScheduleStage,
    PaymentTerm,
    Document,
    Studio
)
from app.schemas.crud import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    DocumentResponse,
    DocumentCreateRequest
)
from app.services.numbering import generate_document_number
from app.services.calculator import calculate_financials, calculate_terms
from app.services.pdf_generator import generate_pdf
from app.core.config import settings

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """Mengambil daftar seluruh proyek beserta nama klien dan jumlah dokumennya."""
    projects = db.query(Project).order_by(Project.dibuat_pada.desc()).all()
    res = []
    for p in projects:
        client = db.query(Client).filter(Client.id == p.client_id).first()
        doc_count = db.query(Document).filter(Document.project_id == p.id).count()
        res.append(ProjectResponse(
            id=p.id,
            client_id=p.client_id,
            nama=p.nama,
            lokasi=p.lokasi or "",
            luas_m2=p.luas_m2 or 0.0,
            jenis=p.jenis or "Rumah Tinggal",
            ruang_lingkup=p.ruang_lingkup or "",
            status=p.status or "draft",
            diskon_rp=p.diskon_rp or 0,
            ppn_persen=p.ppn_persen or 11.0,
            dibuat_pada=p.dibuat_pada,
            client_nama=client.nama if client else "-",
            document_count=doc_count
        ))
    return res

@router.post("", response_model=ProjectDetailResponse, status_code=status.HTTP_201_CREATED)
def create_project(proj_in: ProjectCreate, db: Session = Depends(get_db)):
    """Membuat proyek baru beserta rincian material, jadwal, dan termin pembayaran."""
    client = db.query(Client).filter(Client.id == proj_in.client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client ID tidak valid")

    project = Project(
        client_id=proj_in.client_id,
        nama=proj_in.nama,
        lokasi=proj_in.lokasi,
        luas_m2=proj_in.luas_m2,
        jenis=proj_in.jenis,
        ruang_lingkup=proj_in.ruang_lingkup,
        status=proj_in.status or "draft",
        diskon_rp=proj_in.diskon_rp or 0,
        ppn_persen=proj_in.ppn_persen or 11.0
    )
    db.add(project)
    db.flush()

    for item in proj_in.material_items:
        db.add(MaterialItem(project_id=project.id, **item.model_dump()))

    for stage in proj_in.schedule_stages:
        db.add(ScheduleStage(project_id=project.id, **stage.model_dump()))

    for term in proj_in.payment_terms:
        db.add(PaymentTerm(project_id=project.id, **term.model_dump()))

    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Mengambil rincian lengkap satu proyek."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyek tidak ditemukan")
    return project

@router.put("/{project_id}", response_model=ProjectDetailResponse)
def update_project(project_id: int, proj_in: ProjectUpdate, db: Session = Depends(get_db)):
    """Memperbarui informasi proyek dan menyelaraskan baris material, jadwal, dan termin."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyek tidak ditemukan")

    data = proj_in.model_dump(exclude_unset=True)

    # Update relasi material_items jika disediakan
    if "material_items" in data and data["material_items"] is not None:
        db.query(MaterialItem).filter(MaterialItem.project_id == project.id).delete()
        for item in data["material_items"]:
            db.add(MaterialItem(project_id=project.id, **item))
        del data["material_items"]

    # Update relasi schedule_stages jika disediakan
    if "schedule_stages" in data and data["schedule_stages"] is not None:
        db.query(ScheduleStage).filter(ScheduleStage.project_id == project.id).delete()
        for stage in data["schedule_stages"]:
            db.add(ScheduleStage(project_id=project.id, **stage))
        del data["schedule_stages"]

    # Update relasi payment_terms jika disediakan
    if "payment_terms" in data and data["payment_terms"] is not None:
        db.query(PaymentTerm).filter(PaymentTerm.project_id == project.id).delete()
        for term in data["payment_terms"]:
            db.add(PaymentTerm(project_id=project.id, **term))
        del data["payment_terms"]

    for field, val in data.items():
        setattr(project, field, val)

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Menghapus proyek beserta seluruh dokumen dan rinciannya."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyek tidak ditemukan")
    db.delete(project)
    db.commit()
    return None

@router.post("/{project_id}/duplicate", response_model=ProjectDetailResponse, status_code=status.HTTP_201_CREATED)
def duplicate_project(project_id: int, db: Session = Depends(get_db)):
    """
    Menduplikasi proyek beserta seluruh spesifikasi material, jadwal, dan termin pembayarannya.
    Nama proyek baru akan diberi akhiran '(Salinan)'.
    """
    orig = db.query(Project).filter(Project.id == project_id).first()
    if not orig:
        raise HTTPException(status_code=404, detail="Proyek asal tidak ditemukan")

    new_project = Project(
        client_id=orig.client_id,
        nama=f"{orig.nama} (Salinan)",
        lokasi=orig.lokasi,
        luas_m2=orig.luas_m2,
        jenis=orig.jenis,
        ruang_lingkup=orig.ruang_lingkup,
        status="draft",
        diskon_rp=orig.diskon_rp,
        ppn_persen=orig.ppn_persen
    )
    db.add(new_project)
    db.flush()

    for item in orig.material_items:
        db.add(MaterialItem(
            project_id=new_project.id,
            area=item.area,
            pekerjaan=item.pekerjaan,
            material=item.material,
            merek=item.merek,
            volume=item.volume,
            satuan=item.satuan,
            harga_satuan=item.harga_satuan,
            catatan=item.catatan
        ))

    for stage in orig.schedule_stages:
        db.add(ScheduleStage(
            project_id=new_project.id,
            tahap=stage.tahap,
            tanggal_mulai=stage.tanggal_mulai,
            tanggal_selesai=stage.tanggal_selesai,
            durasi=stage.durasi,
            keterangan=stage.keterangan
        ))

    for term in orig.payment_terms:
        db.add(PaymentTerm(
            project_id=new_project.id,
            urutan=term.urutan,
            label=term.label,
            persen=term.persen,
            nominal=term.nominal,
            pemicu=term.pemicu,
            jatuh_tempo=term.jatuh_tempo
        ))

    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/{project_id}/documents", response_model=List[DocumentResponse])
def get_project_documents(project_id: int, db: Session = Depends(get_db)):
    """Mengambil daftar riwayat dokumen yang sudah diterbitkan untuk proyek ini."""
    docs = db.query(Document).filter(Document.project_id == project_id).order_by(Document.dibuat_pada.desc()).all()
    res = []
    for d in docs:
        res.append(DocumentResponse(
            id=d.id,
            project_id=d.project_id,
            jenis=d.jenis,
            nomor=d.nomor,
            versi=d.versi,
            dibuat_pada=d.dibuat_pada,
            pdf_download_url=f"/api/documents/{d.id}/pdf"
        ))
    return res

@router.post("/{project_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def generate_and_save_project_document(project_id: int, req: DocumentCreateRequest, db: Session = Depends(get_db)):
    """
    Menerbitkan dokumen baru untuk proyek:
    1. Menghasilkan nomor dokumen berurutan otomatis
    2. Mengunci snapshot data (proyek, klien, studio, material, termin, finansial)
    3. Mengompilasi PDF via Typst dan menyimpan file PDF fisik
    4. Menyimpan record dokumen ke database
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyek tidak ditemukan")

    client = project.client
    studio = db.query(Studio).first()

    studio_data = {
        "nama_usaha": studio.nama_usaha if studio else "Studio Arsitektur & Desain",
        "alamat": studio.alamat if studio else "Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan",
        "kontak": studio.kontak if studio else "+62 811-9876-5432 | studio@arsitex.id",
        "rekening": studio.rekening if studio else "BCA 8800-9911-22 a.n Studio Arsitektur",
        "npwp": studio.npwp if studio else "02.891.432.1-013.000",
        "warna_utama": studio.warna_utama if studio and studio.warna_utama else "#0284c7",
        "warna_aksen": studio.warna_aksen if studio and studio.warna_aksen else "#0f172a",
    }

    doc_number = generate_document_number(db, req.jenis)
    doc_date = req.tanggal_dokumen or datetime.date.today().strftime("%d %B %Y")

    # Ambil klausul kontrak jika jenis kontrak
    clauses_data = []
    if req.jenis == "kontrak":
        from app.models.entities import ContractClause
        from app.services.clauses_default import DEFAULT_CLAUSES
        db_clauses = db.query(ContractClause).order_by(ContractClause.urutan.asc()).all()
        if db_clauses:
            clauses_data = [
                {"kode": c.kode, "judul": c.judul, "isi": c.isi, "urutan": c.urutan, "aktif": c.aktif}
                for c in db_clauses
            ]
        else:
            clauses_data = DEFAULT_CLAUSES

    # Siapkan data snapshot
    snapshot = {
        "jenis": req.jenis,
        "nomor_dokumen": doc_number,
        "tanggal_dokumen": doc_date,
        "studio": studio_data,
        "client": {
            "nama": client.nama,
            "perusahaan": client.perusahaan or "",
            "alamat": client.alamat or "",
            "telepon": client.telepon or "",
            "email": client.email or "",
            "catatan": client.catatan or "",
        },
        "project": {
            "nama": project.nama,
            "lokasi": project.lokasi or "",
            "luas_m2": project.luas_m2 or 0.0,
            "jenis": project.jenis or "Rumah Tinggal",
            "ruang_lingkup": project.ruang_lingkup or "",
        },
        "material_items": [
            {
                "area": item.area,
                "pekerjaan": item.pekerjaan,
                "material": item.material,
                "merek": item.merek,
                "volume": item.volume,
                "satuan": item.satuan,
                "harga_satuan": item.harga_satuan,
                "catatan": item.catatan,
            }
            for item in project.material_items
        ],
        "schedule_stages": [
            {
                "tahap": stage.tahap,
                "tanggal_mulai": stage.tanggal_mulai or "",
                "tanggal_selesai": stage.tanggal_selesai or "",
                "durasi": stage.durasi or "",
                "keterangan": stage.keterangan or "",
            }
            for stage in project.schedule_stages
        ],
        "payment_terms": [
            {
                "urutan": term.urutan,
                "label": term.label,
                "persen": term.persen,
                "nominal": term.nominal,
                "pemicu": term.pemicu or "",
                "jatuh_tempo": term.jatuh_tempo or "",
            }
            for term in project.payment_terms
        ],
        "diskon_rp": project.diskon_rp or 0,
        "ppn_persen": project.ppn_persen or 11.0,
        "termin_terpilih_index": req.termin_terpilih_index or 0,
        "clauses": clauses_data
    }

    # Generate PDF
    pdf_bytes = generate_pdf(req.jenis, snapshot)

    # Simpan file PDF ke storage
    base_storage = settings.STORAGE_DIR if os.path.isabs(settings.STORAGE_DIR) else os.path.join(os.getcwd(), settings.STORAGE_DIR)
    storage_dir = os.path.join(base_storage, "documents")
    os.makedirs(storage_dir, exist_ok=True)
    clean_num = doc_number.replace("/", "_")
    pdf_filename = f"{clean_num}.pdf"
    pdf_file_path = os.path.join(storage_dir, pdf_filename)

    with open(pdf_file_path, "wb") as f:
        f.write(pdf_bytes)

    # Simpan ke tabel documents
    doc = Document(
        project_id=project.id,
        jenis=req.jenis,
        nomor=doc_number,
        versi=1,
        snapshot_data=snapshot,
        pdf_path=pdf_file_path,
        dibuat_pada=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        project_id=doc.project_id,
        jenis=doc.jenis,
        nomor=doc.nomor,
        versi=doc.versi,
        dibuat_pada=doc.dibuat_pada,
        pdf_download_url=f"/api/documents/{doc.id}/pdf"
    )
