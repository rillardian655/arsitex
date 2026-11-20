from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Client, Project
from app.schemas.crud import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    """Mengambil daftar seluruh klien beserta jumlah proyek aktifnya."""
    clients = db.query(Client).order_by(Client.nama.asc()).all()
    res = []
    for c in clients:
        proj_count = db.query(Project).filter(Project.client_id == c.id).count()
        res.append(ClientResponse(
            id=c.id,
            nama=c.nama,
            perusahaan=c.perusahaan,
            alamat=c.alamat,
            telepon=c.telepon,
            email=c.email,
            catatan=c.catatan,
            project_count=proj_count
        ))
    return res

@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    """Menambahkan data klien baru."""
    client = Client(**client_in.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return ClientResponse(
        id=client.id,
        nama=client.nama,
        perusahaan=client.perusahaan,
        alamat=client.alamat,
        telepon=client.telepon,
        email=client.email,
        catatan=client.catatan,
        project_count=0
    )

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Mengambil detail satu klien."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klien tidak ditemukan")
    proj_count = db.query(Project).filter(Project.client_id == client.id).count()
    return ClientResponse(
        id=client.id,
        nama=client.nama,
        perusahaan=client.perusahaan,
        alamat=client.alamat,
        telepon=client.telepon,
        email=client.email,
        catatan=client.catatan,
        project_count=proj_count
    )

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_in: ClientUpdate, db: Session = Depends(get_db)):
    """Memperbarui informasi klien."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klien tidak ditemukan")

    update_data = client_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(client, field, val)

    db.commit()
    db.refresh(client)
    proj_count = db.query(Project).filter(Project.client_id == client.id).count()
    return ClientResponse(
        id=client.id,
        nama=client.nama,
        perusahaan=client.perusahaan,
        alamat=client.alamat,
        telepon=client.telepon,
        email=client.email,
        catatan=client.catatan,
        project_count=proj_count
    )

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Menghapus klien (dan seluruh proyeknya secara cascade)."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klien tidak ditemukan")
    db.delete(client)
    db.commit()
    return None

