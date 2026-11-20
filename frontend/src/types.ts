export interface Studio {
  nama_usaha: string;
  alamat: string;
  kontak: string;
  rekening: string;
  npwp: string;
  warna_utama?: string;
  warna_aksen?: string;
}

export interface Client {
  id?: number;
  nama: string;
  perusahaan: string;
  alamat: string;
  telepon: string;
  email: string;
  catatan: string;
}

export interface Project {
  id?: number;
  client_id?: number;
  nama: string;
  lokasi: string;
  luas_m2: number;
  jenis: string;
  ruang_lingkup: string;
  status?: string;
  diskon_rp?: number;
  ppn_persen?: number;
}

export interface MaterialItem {
  id?: number;
  area: string;
  pekerjaan: string;
  material: string;
  merek: string;
  volume: number;
  satuan: string;
  harga_satuan: number;
  catatan: string;
}

export interface ScheduleStage {
  id?: number;
  tahap: string;
  tanggal_mulai: string;
  tanggal_selesai: string;
  durasi: string;
  keterangan: string;
}

export interface PaymentTerm {
  id?: number;
  urutan: number;
  label: string;
  persen: number;
  nominal?: number;
  pemicu: string;
  jatuh_tempo?: string;
}

export interface ContractClauseItem {
  id?: number;
  kode: string;
  judul: string;
  isi: string;
  urutan: number;
  aktif: boolean;
}

export interface FormDataState {
  jenis: "proposal" | "invoice" | "spek" | "kontrak";
  nomor_dokumen: string;
  tanggal_dokumen: string;
  studio: Studio;
  client: Client;
  project: Project;
  material_items: MaterialItem[];
  schedule_stages: ScheduleStage[];
  payment_terms: PaymentTerm[];
  diskon_rp: number;
  ppn_persen: number;
  termin_terpilih_index: number;
  clauses?: ContractClauseItem[];
}

export interface CalculationResponse {
  subtotal: number;
  diskon_rp: number;
  dpp: number;
  ppn_persen: number;
  ppn_rp: number;
  total: number;
  terbilang_total: string;
  calculated_terms: Array<{
    urutan: number;
    label: string;
    persen: number;
    nominal: number;
    nominal_fmt: string;
    pemicu: string;
    terbilang: string;
  }>;
}

export interface SavedProjectItem {
  id: number;
  client_id: number;
  nama: string;
  lokasi: string;
  luas_m2: number;
  jenis: string;
  status: string;
  dibuat_pada: string;
  client_nama: string;
  document_count: number;
}

export interface PublishedDocumentItem {
  id: number;
  project_id: number;
  jenis: string;
  nomor: string;
  versi: number;
  dibuat_pada: string;
  pdf_download_url: string;
}
