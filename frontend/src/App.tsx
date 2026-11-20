import { useState, useEffect } from "react";
import { 
  Building2, 
  FileText, 
  User, 
  Plus, 
  Trash2, 
  Download, 
  Calendar, 
  CreditCard, 
  Layers, 
  AlertCircle,
  Sparkles,
  RefreshCw,
  Receipt,
  Save,
  Copy,
  FolderOpen,
  History,
  X,
  ExternalLink,
  ShieldCheck,
  Scale,
  Palette,
  RotateCcw
} from "lucide-react";
import { 
  FormDataState, 
  MaterialItem, 
  ScheduleStage, 
  PaymentTerm, 
  ContractClauseItem,
  CalculationResponse,
  SavedProjectItem,
  PublishedDocumentItem
} from "./types";

const INITIAL_DATA: FormDataState = {
  jenis: "proposal",
  nomor_dokumen: "PROP/2026/11/001",
  tanggal_dokumen: "20 November 2026",
  studio: {
    nama_usaha: "Studio Arsitektur & Desain",
    alamat: "Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan",
    kontak: "+62 811-9876-5432 | studio@arsitex.id",
    rekening: "BCA 8800-9911-22 a.n Studio Arsitektur",
    npwp: "02.891.432.1-013.000",
    warna_utama: "#0284c7",
    warna_aksen: "#0f172a",
  },
  client: {
    nama: "Bapak Arya Pratama",
    perusahaan: "Pratama Hospitality Group",
    alamat: "Cluster Bukit Hijau B-12, Cilandak, Jakarta Selatan",
    telepon: "+62 812-8899-7766",
    email: "arya.pratama@gmail.com",
    catatan: "Konsep Modern Japandi Tropis dengan bukaan cahaya maksimal.",
  },
  project: {
    nama: "Villa Paviliun & Rumah Tinggal Arya",
    lokasi: "Jl. Lembah Pakar Timur No. 8, Bandung",
    luas_m2: 320,
    jenis: "Rumah Tinggal & Paviliun",
    ruang_lingkup: "Perancangan Konsep Arsitektur, Desain Interior Ruang Utama, Gambar Kerja DED, RAB, dan Pengawasan Berkala.",
  },
  material_items: [
    {
      area: "Fasad & Eksterior",
      pekerjaan: "Finishing Dinding Kamprot & Weathercoat",
      material: "Semen Plester Kamprot & Cat Weathercoat",
      merek: "Dulux Weathershield",
      volume: 140,
      satuan: "m²",
      harga_satuan: 185000,
      catatan: "Warna Sand Stone Matt",
    },
    {
      area: "Lantai 1",
      pekerjaan: "Pemasangan Lantai Granit Tile 60x120",
      material: "Granite Tile Glazed Polished",
      merek: "Indogress Travertine",
      volume: 95,
      satuan: "m²",
      harga_satuan: 380000,
      catatan: "Pola random vein",
    },
    {
      area: "Plafon",
      pekerjaan: "Plafon Gypsum 9mm Rangka Hollow",
      material: "Gypsum Board Jaya & Hollow Galvanis",
      merek: "Jayaboard",
      volume: 120,
      satuan: "m²",
      harga_satuan: 145000,
      catatan: "Drop ceiling indirect warm light",
    },
  ],
  schedule_stages: [
    {
      tahap: "Tahap 1: Konsep & Skematik Desain",
      tanggal_mulai: "01 Des 2026",
      tanggal_selesai: "14 Des 2026",
      durasi: "2 Minggu",
      keterangan: "Moodboard, denah 2D, konsep massa 3D",
    },
    {
      tahap: "Tahap 2: Pengembangan Desain & 3D Render",
      tanggal_mulai: "15 Des 2026",
      tanggal_selesai: "05 Jan 2027",
      durasi: "3 Minggu",
      keterangan: "3D Photorealistic render eksterior & interior",
    },
    {
      tahap: "Tahap 3: Gambar Kerja Detail (DED) & RAB",
      tanggal_mulai: "06 Jan 2027",
      tanggal_selesai: "25 Jan 2027",
      durasi: "3 Minggu",
      keterangan: "Bundel gambar arsitektur, MEP, spesifikasi material",
    },
  ],
  payment_terms: [
    {
      urutan: 1,
      label: "Termin 1 (DP Konsep)",
      persen: 30,
      pemicu: "Penandatanganan proposal & persetujuan konsep awal",
    },
    {
      urutan: 2,
      label: "Termin 2 (Pengembangan Desain)",
      persen: 40,
      pemicu: "Persetujuan final 3D render & denah detail",
    },
    {
      urutan: 3,
      label: "Termin 3 (Pelunasan)",
      persen: 30,
      pemicu: "Serah terima dokumen cetak & DED final",
    },
  ],
  diskon_rp: 1000000,
  ppn_persen: 11,
  termin_terpilih_index: 0,
};

export default function App() {
  const [data, setData] = useState<FormDataState>(() => {
    const saved = localStorage.getItem("arsitex_draft");
    if (saved) {
      try { return JSON.parse(saved); } catch { return INITIAL_DATA; }
    }
    return INITIAL_DATA;
  });

  const [activeTab, setActiveTab] = useState<"klien" | "proyek" | "material" | "jadwal" | "termin" | "kontrak" | "riwayat">("material");
  const [clauses, setClauses] = useState<ContractClauseItem[]>([]);
  const [calcResult, setCalcResult] = useState<CalculationResponse | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // State database proyek & riwayat dokumen
  const [activeProjectId, setActiveProjectId] = useState<number | null>(null);
  const [savedProjects, setSavedProjects] = useState<SavedProjectItem[]>([]);
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [projectDocuments, setProjectDocuments] = useState<PublishedDocumentItem[]>([]);
  const [isSavingProject, setIsSavingProject] = useState(false);

  // Autosave ke localStorage
  useEffect(() => {
    localStorage.setItem("arsitex_draft", JSON.stringify(data));
  }, [data]);

  // Ambil daftar proyek tersimpan
  const fetchSavedProjects = async () => {
    try {
      const res = await fetch("/api/projects");
      if (res.ok) {
        const json: SavedProjectItem[] = await res.json();
        setSavedProjects(json);
      }
    } catch {
      // ignore
    }
  };

  // Ambil riwayat dokumen untuk proyek aktif
  const fetchProjectDocuments = async (projId: number) => {
    try {
      const res = await fetch(`/api/projects/${projId}/documents`);
      if (res.ok) {
        const json: PublishedDocumentItem[] = await res.json();
        setProjectDocuments(json);
      }
    } catch {
      // ignore
    }
  };

  // Ambil klausul kontrak
  const fetchClauses = async () => {
    try {
      const res = await fetch("/api/clauses");
      if (res.ok) {
        const json: ContractClauseItem[] = await res.json();
        setClauses(json);
        setData((prev) => ({ ...prev, clauses: json }));
      }
    } catch {
      // ignore
    }
  };

  // Fetch kalkulasi keuangan dari backend
  const fetchCalculation = async (currentData: FormDataState) => {
    setIsCalculating(true);
    setErrorMsg(null);
    try {
      const res = await fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(currentData),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Gagal melakukan kalkulasi");
      }
      const json: CalculationResponse = await res.json();
      setCalcResult(json);
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsCalculating(false);
    }
  };

  // Fetch nomor urut otomatis berikutnya
  const fetchNextDocNumber = async (docType: "proposal" | "invoice" | "spek" | "kontrak") => {
    try {
      const res = await fetch(`/api/documents/next-number?jenis=${docType}`);
      if (res.ok) {
        const json = await res.json();
        setData((prev) => ({ ...prev, nomor_dokumen: json.next_number, jenis: docType }));
      }
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    fetchCalculation(data);
  }, [
    data.material_items, 
    data.payment_terms, 
    data.diskon_rp, 
    data.ppn_persen
  ]);

  useEffect(() => {
    fetchSavedProjects();
    fetchClauses();
  }, []);

  useEffect(() => {
    if (activeProjectId) {
      fetchProjectDocuments(activeProjectId);
    } else {
      setProjectDocuments([]);
    }
  }, [activeProjectId]);

  // Handle Pratinjau PDF
  const handlePreviewPdf = async (docType: "proposal" | "invoice" | "spek" | "kontrak") => {
    setIsGeneratingPdf(true);
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      const payload = { ...data, jenis: docType, clauses };
      const res = await fetch("/api/documents/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || `Gagal menghasilkan pratinjau ${docType}`);
      }

      const blob = await res.blob();
      const objectUrl = URL.createObjectURL(blob);
      setPdfUrl(objectUrl);
      setData((prev) => ({ ...prev, jenis: docType }));
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  // Handle Unduh Draf PDF
  const handleDownloadPdf = async (docType: "proposal" | "invoice" | "spek" | "kontrak") => {
    setIsGeneratingPdf(true);
    setErrorMsg(null);
    try {
      const payload = { ...data, jenis: docType, clauses };
      const res = await fetch("/api/documents/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Gagal mengunduh PDF");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${docType.toUpperCase()}_${data.nomor_dokumen.replace(/[\/\\]/g, "_")}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  // Handle Simpan Proyek ke Database
  const handleSaveProject = async () => {
    setIsSavingProject(true);
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      let clientId = data.client.id;
      if (!clientId) {
        const cRes = await fetch("/api/clients", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data.client),
        });
        if (!cRes.ok) throw new Error("Gagal menyimpan data klien");
        const cJson = await cRes.json();
        clientId = cJson.id;
        setData((prev) => ({ ...prev, client: { ...prev.client, id: clientId } }));
      } else {
        await fetch(`/api/clients/${clientId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data.client),
        });
      }

      const projectPayload = {
        client_id: clientId,
        nama: data.project.nama,
        lokasi: data.project.lokasi,
        luas_m2: data.project.luas_m2,
        jenis: data.project.jenis,
        ruang_lingkup: data.project.ruang_lingkup,
        status: "aktif",
        diskon_rp: data.diskon_rp,
        ppn_persen: data.ppn_persen,
        material_items: data.material_items,
        schedule_stages: data.schedule_stages,
        payment_terms: data.payment_terms,
      };

      if (activeProjectId) {
        const pRes = await fetch(`/api/projects/${activeProjectId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(projectPayload),
        });
        if (!pRes.ok) throw new Error("Gagal memperbarui proyek");
        setSuccessMsg("Proyek berhasil diperbarui di database!");
      } else {
        const pRes = await fetch("/api/projects", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(projectPayload),
        });
        if (!pRes.ok) throw new Error("Gagal membuat proyek baru");
        const pJson = await pRes.json();
        setActiveProjectId(pJson.id);
        setData((prev) => ({ ...prev, project: { ...prev.project, id: pJson.id } }));
        setSuccessMsg("Proyek baru berhasil disimpan ke database!");
      }

      fetchSavedProjects();
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsSavingProject(false);
    }
  };

  // Handle Buka Proyek
  const handleOpenProject = async (id: number) => {
    try {
      const res = await fetch(`/api/projects/${id}`);
      if (!res.ok) throw new Error("Gagal membuka proyek");
      const proj = await res.json();

      setActiveProjectId(proj.id);
      setData((prev) => ({
        ...prev,
        client: {
          id: proj.client.id,
          nama: proj.client.nama,
          perusahaan: proj.client.perusahaan || "",
          alamat: proj.client.alamat || "",
          telepon: proj.client.telepon || "",
          email: proj.client.email || "",
          catatan: proj.client.catatan || "",
        },
        project: {
          id: proj.id,
          client_id: proj.client_id,
          nama: proj.nama,
          lokasi: proj.lokasi || "",
          luas_m2: proj.luas_m2 || 0,
          jenis: proj.jenis || "Rumah Tinggal",
          ruang_lingkup: proj.ruang_lingkup || "",
          status: proj.status,
          diskon_rp: proj.diskon_rp || 0,
          ppn_persen: proj.ppn_persen || 11.0,
        },
        material_items: proj.material_items.map((m: any) => ({
          id: m.id,
          area: m.area || "Umum",
          pekerjaan: m.pekerjaan,
          material: m.material,
          merek: m.merek || "-",
          volume: m.volume,
          satuan: m.satuan,
          harga_satuan: m.harga_satuan,
          catatan: m.catatan || "",
        })),
        schedule_stages: proj.schedule_stages.map((s: any) => ({
          id: s.id,
          tahap: s.tahap,
          tanggal_mulai: s.tanggal_mulai || "",
          tanggal_selesai: s.tanggal_selesai || "",
          durasi: s.durasi || "",
          keterangan: s.keterangan || "",
        })),
        payment_terms: proj.payment_terms.map((t: any) => ({
          id: t.id,
          urutan: t.urutan,
          label: t.label,
          persen: t.persen,
          nominal: t.nominal,
          pemicu: t.pemicu || "",
          jatuh_tempo: t.jatuh_tempo || "",
        })),
        diskon_rp: proj.diskon_rp || 0,
        ppn_persen: proj.ppn_persen || 11.0,
      }));

      setShowProjectModal(false);
      setSuccessMsg(`Proyek "${proj.nama}" berhasil dimuat.`);
      fetchProjectDocuments(proj.id);
    } catch (err: any) {
      setErrorMsg(err.message);
    }
  };

  // Handle Duplikasi Proyek
  const handleDuplicateProject = async (id: number) => {
    try {
      const res = await fetch(`/api/projects/${id}/duplicate`, { method: "POST" });
      if (!res.ok) throw new Error("Gagal menduplikasi proyek");
      const dup = await res.json();
      setSuccessMsg(`Proyek berhasil diduplikasi menjadi "${dup.nama}".`);
      fetchSavedProjects();
      handleOpenProject(dup.id);
    } catch (err: any) {
      setErrorMsg(err.message);
    }
  };

  // Handle Terbitkan & Kunci Dokumen
  const handlePublishDocument = async (docType: "proposal" | "invoice" | "spek" | "kontrak") => {
    if (!activeProjectId) {
      setErrorMsg("Harap simpan proyek ke database terlebih dahulu sebelum menerbitkan dokumen resmi.");
      return;
    }
    setIsGeneratingPdf(true);
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      const res = await fetch(`/api/projects/${activeProjectId}/documents`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          jenis: docType,
          termin_terpilih_index: data.termin_terpilih_index,
          tanggal_dokumen: data.tanggal_dokumen,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Gagal menerbitkan dokumen");
      }

      const docRes = await res.json();
      setSuccessMsg(`Dokumen ${docType.toUpperCase()} nomor ${docRes.nomor} berhasil diterbitkan & snapshot dikunci!`);
      fetchProjectDocuments(activeProjectId);
      setActiveTab("riwayat");
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  // Reset Klausul Kontrak
  const handleResetClauses = async () => {
    try {
      const res = await fetch("/api/clauses/reset", { method: "POST" });
      if (res.ok) {
        const json = await res.json();
        setClauses(json);
        setSuccessMsg("Klausul kontrak berhasil direset ke standar arsitek.");
      }
    } catch {
      setErrorMsg("Gagal mereset pasal kontrak.");
    }
  };

  // Update Satu Klausul
  const handleUpdateClause = (index: number, field: keyof ContractClauseItem, val: any) => {
    const updated = [...clauses];
    updated[index] = { ...updated[index], [field]: val };
    setClauses(updated);
  };

  // Simpan Klausul ke Backend
  const handleSaveClauses = async () => {
    try {
      const res = await fetch("/api/clauses", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ clauses }),
      });
      if (res.ok) {
        setSuccessMsg("Klausul kontrak berhasil disimpan.");
      }
    } catch {
      setErrorMsg("Gagal menyimpan perubahan pasal kontrak.");
    }
  };

  // Reset ke Proyek Baru
  const handleNewProject = () => {
    setActiveProjectId(null);
    localStorage.removeItem("arsitex_draft");
    setData({
      ...INITIAL_DATA,
      project: {
        nama: "Proyek Baru",
        lokasi: "",
        luas_m2: 100,
        jenis: "Rumah Tinggal",
        ruang_lingkup: "",
      },
      client: {
        nama: "Nama Klien Baru",
        perusahaan: "",
        alamat: "",
        telepon: "",
        email: "",
        catatan: "",
      },
      material_items: [],
      schedule_stages: [],
      payment_terms: [
        { urutan: 1, label: "DP 50%", persen: 50, pemicu: "Penandatanganan kontrak" },
        { urutan: 2, label: "Pelunasan 50%", persen: 50, pemicu: "Serah terima dokumen" },
      ],
    });
    setSuccessMsg("Formulir telah direset untuk proyek baru.");
  };

  // Muat data sampel
  const handleLoadSample = async () => {
    try {
      const res = await fetch("/api/sample-data");
      if (res.ok) {
        const sample = await res.json();
        setData(sample);
        setActiveProjectId(null);
        setSuccessMsg("Contoh data arsitektur berhasil dimuat.");
      }
    } catch {
      setData(INITIAL_DATA);
    }
  };

  // Material Item Handlers
  const handleAddMaterial = () => {
    const newItem: MaterialItem = {
      area: "Area Baru",
      pekerjaan: "Pekerjaan Spesifikasi",
      material: "Material Standar",
      merek: "-",
      volume: 1,
      satuan: "unit",
      harga_satuan: 100000,
      catatan: "",
    };
    setData({ ...data, material_items: [...data.material_items, newItem] });
  };

  const handleUpdateMaterial = (index: number, field: keyof MaterialItem, val: any) => {
    const updated = [...data.material_items];
    updated[index] = { ...updated[index], [field]: val };
    setData({ ...data, material_items: updated });
  };

  const handleDeleteMaterial = (index: number) => {
    const updated = data.material_items.filter((_, i) => i !== index);
    setData({ ...data, material_items: updated });
  };

  // Schedule Handlers
  const handleAddSchedule = () => {
    const newStage: ScheduleStage = {
      tahap: `Tahap ${data.schedule_stages.length + 1}: Pekerjaan Baru`,
      tanggal_mulai: "",
      tanggal_selesai: "",
      durasi: "2 Minggu",
      keterangan: "Deskripsi hasil tahapan",
    };
    setData({ ...data, schedule_stages: [...data.schedule_stages, newStage] });
  };

  const handleUpdateSchedule = (index: number, field: keyof ScheduleStage, val: string) => {
    const updated = [...data.schedule_stages];
    updated[index] = { ...updated[index], [field]: val };
    setData({ ...data, schedule_stages: updated });
  };

  const handleDeleteSchedule = (index: number) => {
    const updated = data.schedule_stages.filter((_, i) => i !== index);
    setData({ ...data, schedule_stages: updated });
  };

  // Payment Term Handlers
  const handleAddPaymentTerm = () => {
    const newTerm: PaymentTerm = {
      urutan: data.payment_terms.length + 1,
      label: `Termin ${data.payment_terms.length + 1}`,
      persen: 0,
      pemicu: "Keterangan termin",
    };
    setData({ ...data, payment_terms: [...data.payment_terms, newTerm] });
  };

  const handleUpdateTerm = (index: number, field: keyof PaymentTerm, val: any) => {
    const updated = [...data.payment_terms];
    updated[index] = { ...updated[index], [field]: val };
    setData({ ...data, payment_terms: updated });
  };

  const handleDeleteTerm = (index: number) => {
    const updated = data.payment_terms.filter((_, i) => i !== index);
    setData({ ...data, payment_terms: updated });
  };

  const formatRupiah = (val: number) => `Rp ${val.toLocaleString("id-ID")}`;
  const totalTermPercent = data.payment_terms.reduce((acc, t) => acc + (Number(t.persen) || 0), 0);
  const isTermValid = Math.abs(totalTermPercent - 100) < 0.05;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-sky-500 selection:text-white">
      {/* Top Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div 
              style={{ backgroundColor: data.studio.warna_utama || "#0284c7" }}
              className="w-9 h-9 rounded-lg flex items-center justify-center shadow-lg shadow-sky-500/20"
            >
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white tracking-tight flex items-center gap-2">
                Arsi-TeX <span className="text-xs px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30 font-medium">Full Stack Edition</span>
              </h1>
              <p className="text-xs text-slate-400">
                {activeProjectId ? (
                  <span className="text-sky-300 font-medium">Proyek Aktif: #{activeProjectId} - {data.project.nama}</span>
                ) : (
                  <span className="text-slate-500">Draf Lokal (Tersimpan otomatis)</span>
                )}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowProjectModal(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
              title="Daftar Proyek Tersimpan"
            >
              <FolderOpen className="w-3.5 h-3.5 text-sky-400" />
              Proyek Saya ({savedProjects.length})
            </button>
            <button
              onClick={handleSaveProject}
              disabled={isSavingProject}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white shadow-md shadow-emerald-600/20 transition disabled:opacity-50"
              title="Simpan proyek dan seluruh rinciannya ke database"
            >
              <Save className="w-3.5 h-3.5" />
              {isSavingProject ? "Menyimpan..." : activeProjectId ? "Perbarui DB" : "Simpan DB"}
            </button>
            <button
              onClick={handleLoadSample}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
              title="Muat data sampel arsitektur"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Contoh Data
            </button>
          </div>
        </div>
      </header>

      {/* Sub-Header: Document Type Switcher */}
      <div className="border-b border-slate-800/80 bg-slate-900/40">
        <div className="max-w-7xl mx-auto px-4 py-2 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className="text-slate-400 font-medium">Jenis Dokumen:</span>
            <div className="inline-flex p-1 bg-slate-950 rounded-xl border border-slate-800 gap-1">
              <button
                onClick={() => handlePreviewPdf("proposal")}
                className={`px-3 py-1 rounded-lg font-medium transition ${
                  data.jenis === "proposal" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                1. Proposal Desain
              </button>
              <button
                onClick={() => handlePreviewPdf("spek")}
                className={`px-3 py-1 rounded-lg font-medium transition ${
                  data.jenis === "spek" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                2. Spesifikasi Teknis
              </button>
              <button
                onClick={() => handlePreviewPdf("invoice")}
                className={`px-3 py-1 rounded-lg font-medium transition ${
                  data.jenis === "invoice" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                3. Invoice Termin
              </button>
              <button
                onClick={() => handlePreviewPdf("kontrak")}
                className={`px-3 py-1 rounded-lg font-medium transition ${
                  data.jenis === "kontrak" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                4. Kontrak Kerja
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] text-emerald-400 flex items-center gap-1 font-mono">
              <ShieldCheck className="w-3.5 h-3.5" /> Draf Otomatis Tersimpan
            </span>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form Section (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Navigation Tabs */}
          <div className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 overflow-x-auto text-xs">
            <button
              onClick={() => setActiveTab("klien")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "klien" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <User className="w-3.5 h-3.5" /> Klien & Studio
            </button>
            <button
              onClick={() => setActiveTab("proyek")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "proyek" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Building2 className="w-3.5 h-3.5" /> Data Proyek
            </button>
            <button
              onClick={() => setActiveTab("material")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "material" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Layers className="w-3.5 h-3.5" /> Material ({data.material_items.length})
            </button>
            <button
              onClick={() => setActiveTab("jadwal")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "jadwal" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Calendar className="w-3.5 h-3.5" /> Jadwal ({data.schedule_stages.length})
            </button>
            <button
              onClick={() => setActiveTab("termin")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "termin" ? "bg-sky-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <CreditCard className="w-3.5 h-3.5" /> Termin ({totalTermPercent}%)
            </button>
            <button
              onClick={() => setActiveTab("kontrak")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "kontrak" ? "bg-amber-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Scale className="w-3.5 h-3.5" /> Klausul Kontrak
            </button>
            <button
              onClick={() => setActiveTab("riwayat")}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                activeTab === "riwayat" ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <History className="w-3.5 h-3.5" /> Riwayat ({projectDocuments.length})
            </button>
          </div>

          {/* Feedback Banners */}
          {errorMsg && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-xl flex items-start gap-2.5 text-xs">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}
          {successMsg && (
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-xl flex items-start gap-2.5 text-xs">
              <ShieldCheck className="w-4 h-4 shrink-0 text-emerald-400 mt-0.5" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* Form Content Cards */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-5">
            {/* TAB: KLIEN & STUDIO */}
            {activeTab === "klien" && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-semibold text-sky-400 uppercase tracking-wider mb-3">Informasi Klien</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div>
                      <label className="block text-slate-400 mb-1">Nama Klien / Pemilik *</label>
                      <input
                        type="text"
                        value={data.client.nama}
                        onChange={(e) => setData({ ...data, client: { ...data.client, nama: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Perusahaan / Instansi (Opsional)</label>
                      <input
                        type="text"
                        value={data.client.perusahaan}
                        onChange={(e) => setData({ ...data, client: { ...data.client, perusahaan: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Nomor WhatsApp / Telepon</label>
                      <input
                        type="text"
                        value={data.client.telepon}
                        onChange={(e) => setData({ ...data, client: { ...data.client, telepon: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Email Klien</label>
                      <input
                        type="text"
                        value={data.client.email}
                        onChange={(e) => setData({ ...data, client: { ...data.client, email: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-slate-400 mb-1">Alamat Klien</label>
                      <input
                        type="text"
                        value={data.client.alamat}
                        onChange={(e) => setData({ ...data, client: { ...data.client, alamat: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-sky-400 uppercase tracking-wider">Profil & Branding Studio</h3>
                    <div className="flex items-center gap-3 text-xs">
                      <label className="flex items-center gap-1.5 text-slate-400">
                        <Palette className="w-3.5 h-3.5 text-sky-400" /> Warna Tema:
                        <input
                          type="color"
                          value={data.studio.warna_utama || "#0284c7"}
                          onChange={(e) => setData({ ...data, studio: { ...data.studio, warna_utama: e.target.value } })}
                          className="w-6 h-6 rounded cursor-pointer border border-slate-700 bg-transparent"
                        />
                      </label>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div>
                      <label className="block text-slate-400 mb-1">Nama Usaha / Studio</label>
                      <input
                        type="text"
                        value={data.studio.nama_usaha}
                        onChange={(e) => setData({ ...data, studio: { ...data.studio, nama_usaha: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Kontak Resmi (Telp / Email)</label>
                      <input
                        type="text"
                        value={data.studio.kontak}
                        onChange={(e) => setData({ ...data, studio: { ...data.studio, kontak: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-slate-400 mb-1">Alamat Kantor Studio</label>
                      <input
                        type="text"
                        value={data.studio.alamat}
                        onChange={(e) => setData({ ...data, studio: { ...data.studio, alamat: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">Rekening Pembayaran Bank</label>
                      <input
                        type="text"
                        value={data.studio.rekening}
                        onChange={(e) => setData({ ...data, studio: { ...data.studio, rekening: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-400 mb-1">NPWP Studio (Opsional)</label>
                      <input
                        type="text"
                        value={data.studio.npwp}
                        onChange={(e) => setData({ ...data, studio: { ...data.studio, npwp: e.target.value } })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* TAB: DATA PROYEK */}
            {activeTab === "proyek" && (
              <div className="space-y-4 text-xs">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-400 mb-1">Nama Proyek *</label>
                    <input
                      type="text"
                      value={data.project.nama}
                      onChange={(e) => setData({ ...data, project: { ...data.project, nama: e.target.value } })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Lokasi Proyek</label>
                    <input
                      type="text"
                      value={data.project.lokasi}
                      onChange={(e) => setData({ ...data, project: { ...data.project, lokasi: e.target.value } })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Jenis Proyek (Rumah, Kafe, Kantor, dll.)</label>
                    <input
                      type="text"
                      value={data.project.jenis}
                      onChange={(e) => setData({ ...data, project: { ...data.project, jenis: e.target.value } })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Luas Bangunan / Area (m²)</label>
                    <input
                      type="number"
                      value={data.project.luas_m2}
                      onChange={(e) => setData({ ...data, project: { ...data.project, luas_m2: parseFloat(e.target.value) || 0 } })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-slate-400 mb-1">Ruang Lingkup Jasa Desain</label>
                    <textarea
                      rows={3}
                      value={data.project.ruang_lingkup}
                      onChange={(e) => setData({ ...data, project: { ...data.project, ruang_lingkup: e.target.value } })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1 flex items-center justify-between">
                      <span>Nomor Dokumen</span>
                      <button
                        type="button"
                        onClick={() => fetchNextDocNumber(data.jenis)}
                        className="text-[10px] text-sky-400 hover:underline"
                      >
                        Auto-Generate
                      </button>
                    </label>
                    <input
                      type="text"
                      value={data.nomor_dokumen}
                      onChange={(e) => setData({ ...data, nomor_dokumen: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500 font-mono text-[11px]"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Tanggal Dokumen</label>
                    <input
                      type="text"
                      value={data.tanggal_dokumen}
                      onChange={(e) => setData({ ...data, tanggal_dokumen: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-sky-500"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* TAB: MATERIAL & RINCIAN BIAYA */}
            {activeTab === "material" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Daftar Pekerjaan & Spesifikasi Material
                  </h3>
                  <button
                    onClick={handleAddMaterial}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-sky-600/20 text-sky-400 hover:bg-sky-600/30 border border-sky-500/30 text-xs font-medium transition"
                  >
                    <Plus className="w-3.5 h-3.5" /> Tambah Baris
                  </button>
                </div>

                <div className="space-y-3">
                  {data.material_items.map((item, idx) => (
                    <div key={idx} className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-sky-400">#{idx + 1}</span>
                        <button
                          onClick={() => handleDeleteMaterial(idx)}
                          className="text-slate-500 hover:text-rose-400 transition"
                          title="Hapus Baris"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Area / Ruang</label>
                          <input
                            type="text"
                            value={item.area}
                            onChange={(e) => handleUpdateMaterial(idx, "area", e.target.value)}
                            placeholder="Fasad / Living"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div className="md:col-span-2">
                          <label className="block text-slate-500 text-[10px] mb-0.5">Uraian Pekerjaan</label>
                          <input
                            type="text"
                            value={item.pekerjaan}
                            onChange={(e) => handleUpdateMaterial(idx, "pekerjaan", e.target.value)}
                            placeholder="Finishing Dinding Kamprot"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Material & Merek</label>
                          <input
                            type="text"
                            value={item.material}
                            onChange={(e) => handleUpdateMaterial(idx, "material", e.target.value)}
                            placeholder="Granit Indogress"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Volume</label>
                          <input
                            type="number"
                            step="any"
                            value={item.volume}
                            onChange={(e) => handleUpdateMaterial(idx, "volume", parseFloat(e.target.value) || 0)}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Satuan</label>
                          <input
                            type="text"
                            value={item.satuan}
                            onChange={(e) => handleUpdateMaterial(idx, "satuan", e.target.value)}
                            placeholder="m², unit, ls"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Harga Satuan (Rp)</label>
                          <input
                            type="number"
                            value={item.harga_satuan}
                            onChange={(e) => handleUpdateMaterial(idx, "harga_satuan", parseInt(e.target.value) || 0)}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Subtotal Baris</label>
                          <div className="px-2 py-1 bg-slate-900/50 rounded font-semibold text-emerald-400">
                            {formatRupiah(Math.round(item.volume * item.harga_satuan))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB: JADWAL KERJA */}
            {activeTab === "jadwal" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Tahapan & Timeline Pelaksanaan
                  </h3>
                  <button
                    onClick={handleAddSchedule}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-sky-600/20 text-sky-400 hover:bg-sky-600/30 border border-sky-500/30 text-xs font-medium transition"
                  >
                    <Plus className="w-3.5 h-3.5" /> Tambah Tahap
                  </button>
                </div>

                <div className="space-y-3">
                  {data.schedule_stages.map((stage, idx) => (
                    <div key={idx} className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-sky-400">Tahap #{idx + 1}</span>
                        <button
                          onClick={() => handleDeleteSchedule(idx)}
                          className="text-slate-500 hover:text-rose-400 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                        <div className="md:col-span-2">
                          <label className="block text-slate-500 text-[10px] mb-0.5">Nama Tahap</label>
                          <input
                            type="text"
                            value={stage.tahap}
                            onChange={(e) => handleUpdateSchedule(idx, "tahap", e.target.value)}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Durasi / Periode</label>
                          <input
                            type="text"
                            value={stage.durasi}
                            onChange={(e) => handleUpdateSchedule(idx, "durasi", e.target.value)}
                            placeholder="Contoh: 3 Minggu"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div className="md:col-span-3">
                          <label className="block text-slate-500 text-[10px] mb-0.5">Keterangan Output</label>
                          <input
                            type="text"
                            value={stage.keterangan}
                            onChange={(e) => handleUpdateSchedule(idx, "keterangan", e.target.value)}
                            placeholder="Moodboard, gambar 3D, dokumen DED, dll."
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB: TERMIN PEMBAYARAN */}
            {activeTab === "termin" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Termin Pembayaran (Total Harus 100%)
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Saat ini: <span className={`font-bold ${isTermValid ? "text-emerald-400" : "text-rose-400"}`}>{totalTermPercent}%</span>
                    </p>
                  </div>
                  <button
                    onClick={handleAddPaymentTerm}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-sky-600/20 text-sky-400 hover:bg-sky-600/30 border border-sky-500/30 text-xs font-medium transition"
                  >
                    <Plus className="w-3.5 h-3.5" /> Tambah Termin
                  </button>
                </div>

                <div className="space-y-3">
                  {data.payment_terms.map((term, idx) => (
                    <div key={idx} className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-sky-400">Termin #{idx + 1}</span>
                        <button
                          onClick={() => handleDeleteTerm(idx)}
                          className="text-slate-500 hover:text-rose-400 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                        <div className="md:col-span-2">
                          <label className="block text-slate-500 text-[10px] mb-0.5">Label Termin</label>
                          <input
                            type="text"
                            value={term.label}
                            onChange={(e) => handleUpdateTerm(idx, "label", e.target.value)}
                            placeholder="DP 30% Saat Kontrak"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Persen (%)</label>
                          <input
                            type="number"
                            value={term.persen}
                            onChange={(e) => handleUpdateTerm(idx, "persen", parseFloat(e.target.value) || 0)}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-500 text-[10px] mb-0.5">Estimasi Nominal</label>
                          <div className="px-2 py-1 bg-slate-900/50 rounded font-semibold text-sky-400 truncate">
                            {calcResult?.calculated_terms?.[idx]?.nominal_fmt || "Rp -"}
                          </div>
                        </div>
                        <div className="md:col-span-4">
                          <label className="block text-slate-500 text-[10px] mb-0.5">Syarat Pemicu Pembayaran</label>
                          <input
                            type="text"
                            value={term.pemicu}
                            onChange={(e) => handleUpdateTerm(idx, "pemicu", e.target.value)}
                            placeholder="Misal: Penandatanganan kontrak / Selesai Gambar Kerja"
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1 text-slate-200"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="p-3 bg-indigo-950/30 border border-indigo-900/40 rounded-xl text-xs space-y-1">
                  <label className="block text-indigo-300 font-medium">Pilih Termin yang Ditagihkan pada Invoice:</label>
                  <select
                    value={data.termin_terpilih_index}
                    onChange={(e) => setData({ ...data, termin_terpilih_index: parseInt(e.target.value) || 0 })}
                    className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    {data.payment_terms.map((t, idx) => (
                      <option key={idx} value={idx}>
                        {t.label} ({t.persen}%) - {calcResult?.calculated_terms?.[idx]?.nominal_fmt || ""}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* TAB: KLAUSUL KONTRAK (TAHAP 3) */}
            {activeTab === "kontrak" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xs font-semibold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Scale className="w-3.5 h-3.5" />
                      Klausul & Pasal Perjanjian Kontrak
                    </h3>
                    <p className="text-[11px] text-slate-400">
                      Seluruh pasal di bawah ini dapat disesuaikan dan akan otomatis disematkan ke PDF Kontrak Kerja.
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleResetClauses}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition"
                      title="Kembalikan ke pasal default arsitek"
                    >
                      <RotateCcw className="w-3 h-3 text-amber-400" /> Reset Default
                    </button>
                    <button
                      onClick={handleSaveClauses}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition"
                    >
                      <Save className="w-3 h-3" /> Simpan Klausul
                    </button>
                  </div>
                </div>

                {/* Legal Disclaimer Box */}
                <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-200 text-xs flex items-start gap-2.5">
                  <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <b>Pemberitahuan Hukum:</b> Template kontrak kerja desain ini disediakan sebagai format standar praktik studio arsitektur dan <u>bukan nasihat hukum resmi</u>. Anda disarankan untuk menelaah klausul bersama konsultan hukum sebelum ditandatangani oleh klien.
                  </div>
                </div>

                <div className="space-y-3">
                  {clauses.map((clause, idx) => (
                    <div key={clause.kode} className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <input
                          type="text"
                          value={clause.judul}
                          onChange={(e) => handleUpdateClause(idx, "judul", e.target.value)}
                          className="font-bold text-slate-200 bg-transparent border-b border-slate-800 hover:border-slate-700 focus:outline-none focus:border-amber-400 w-3/4 py-0.5"
                        />
                        <label className="flex items-center gap-1.5 text-slate-400 text-[11px] cursor-pointer">
                          <input
                            type="checkbox"
                            checked={clause.aktif}
                            onChange={(e) => handleUpdateClause(idx, "aktif", e.target.checked)}
                            className="rounded bg-slate-900 border-slate-700 text-amber-500 focus:ring-0"
                          />
                          Sertakan
                        </label>
                      </div>
                      <textarea
                        rows={3}
                        value={clause.isi}
                        onChange={(e) => handleUpdateClause(idx, "isi", e.target.value)}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-slate-300 leading-relaxed focus:outline-none focus:border-amber-500"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB: RIWAYAT DOKUMEN RESMI (TAHAP 2) */}
            {activeTab === "riwayat" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                    <History className="w-3.5 h-3.5" />
                    Riwayat Dokumen Resmi Terbit
                  </h3>
                  {activeProjectId && (
                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => handlePublishDocument("proposal")}
                        disabled={isGeneratingPdf}
                        className="px-2 py-1 rounded bg-sky-600/20 text-sky-400 hover:bg-sky-600/30 border border-sky-500/30 text-xs font-medium transition"
                      >
                        + Proposal
                      </button>
                      <button
                        onClick={() => handlePublishDocument("spek")}
                        disabled={isGeneratingPdf}
                        className="px-2 py-1 rounded bg-sky-600/20 text-sky-400 hover:bg-sky-600/30 border border-sky-500/30 text-xs font-medium transition"
                      >
                        + Spek
                      </button>
                      <button
                        onClick={() => handlePublishDocument("invoice")}
                        disabled={isGeneratingPdf}
                        className="px-2 py-1 rounded bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600/30 border border-indigo-500/30 text-xs font-medium transition"
                      >
                        + Invoice
                      </button>
                      <button
                        onClick={() => handlePublishDocument("kontrak")}
                        disabled={isGeneratingPdf}
                        className="px-2 py-1 rounded bg-amber-600/20 text-amber-400 hover:bg-amber-600/30 border border-amber-500/30 text-xs font-medium transition"
                      >
                        + Kontrak
                      </button>
                    </div>
                  )}
                </div>

                {!activeProjectId ? (
                  <div className="p-8 text-center text-slate-500 text-xs border border-dashed border-slate-800 rounded-xl">
                    <FolderOpen className="w-8 h-8 mx-auto mb-2 text-slate-600" />
                    <p className="font-medium text-slate-400">Proyek belum disimpan</p>
                    <p className="mt-1">Klik tombol <b>"Simpan DB"</b> di navbar atas untuk mengaktifkan riwayat dokumen resmi.</p>
                  </div>
                ) : projectDocuments.length === 0 ? (
                  <div className="p-8 text-center text-slate-500 text-xs border border-dashed border-slate-800 rounded-xl">
                    <History className="w-8 h-8 mx-auto mb-2 text-slate-600" />
                    <p className="font-medium text-slate-400">Belum ada dokumen yang diterbitkan</p>
                    <p className="mt-1">
                      Pilih tombol <b>+ Proposal / Spek / Invoice / Kontrak</b> di atas untuk mengunci snapshot dan mengarsipkan PDF.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {projectDocuments.map((doc) => (
                      <div
                        key={doc.id}
                        className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs hover:border-slate-700 transition"
                      >
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                              doc.jenis === "proposal" 
                                ? "bg-sky-500/20 text-sky-400 border border-sky-500/30" 
                                : doc.jenis === "invoice"
                                ? "bg-indigo-500/20 text-indigo-400 border border-indigo-500/30"
                                : doc.jenis === "spek"
                                ? "bg-teal-500/20 text-teal-400 border border-teal-500/30"
                                : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                            }`}>
                              {doc.jenis}
                            </span>
                            <span className="font-mono font-semibold text-slate-200">{doc.nomor}</span>
                          </div>
                          <p className="text-[11px] text-slate-500">
                            Diterbitkan: {new Date(doc.dibuat_pada).toLocaleDateString("id-ID", { dateStyle: "medium" })} | Versi {doc.versi}
                          </p>
                        </div>

                        <a
                          href={doc.pdf_download_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 font-medium transition"
                        >
                          <Download className="w-3.5 h-3.5" />
                          Unduh Asli
                        </a>
                      </div>
                    ))}
                    <div className="p-2.5 bg-slate-900/60 rounded-lg text-[11px] text-slate-400 border border-slate-800">
                      💡 <b>Keamanan Snapshot:</b> Seluruh dokumen di riwayat ini tidak akan berubah meskipun di masa depan kamu mengubah spesifikasi atau harga proyek.
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Section: Financial Summary & PDF Preview (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Card Kalkulasi Keuangan */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-semibold text-sm text-slate-200 flex items-center gap-2">
                <Receipt className="w-4 h-4 text-sky-400" />
                Ringkasan Finansial Proyek
              </h3>
              {isCalculating && <RefreshCw className="w-3.5 h-3.5 animate-spin text-sky-400" />}
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Subtotal ({data.material_items.length} item):</span>
                <span className="font-medium text-slate-200">
                  {calcResult ? formatRupiah(calcResult.subtotal) : "Rp 0"}
                </span>
              </div>

              <div className="flex items-center justify-between gap-2">
                <span className="text-slate-400">Diskon (Rp):</span>
                <input
                  type="number"
                  value={data.diskon_rp}
                  onChange={(e) => setData({ ...data, diskon_rp: parseInt(e.target.value) || 0 })}
                  className="w-32 text-right bg-slate-950 border border-slate-800 rounded px-2 py-1 text-slate-100"
                />
              </div>

              <div className="flex items-center justify-between gap-2">
                <span className="text-slate-400">PPN (%):</span>
                <input
                  type="number"
                  step="0.5"
                  value={data.ppn_persen}
                  onChange={(e) => setData({ ...data, ppn_persen: parseFloat(e.target.value) || 0 })}
                  className="w-20 text-right bg-slate-950 border border-slate-800 rounded px-2 py-1 text-slate-100"
                />
              </div>

              {data.ppn_persen > 0 && (
                <div className="flex justify-between text-slate-400">
                  <span>Nominal PPN:</span>
                  <span className="font-medium text-slate-200">
                    {calcResult ? formatRupiah(calcResult.ppn_rp) : "Rp 0"}
                  </span>
                </div>
              )}

              <div className="pt-2 border-t border-slate-800 flex justify-between items-baseline">
                <span className="text-sm font-semibold text-slate-100">Total Keseluruhan:</span>
                <span className="text-lg font-bold text-sky-400">
                  {calcResult ? formatRupiah(calcResult.total) : "Rp 0"}
                </span>
              </div>

              <div className="p-2.5 bg-sky-950/40 border border-sky-900/40 rounded-lg text-[11px] text-sky-300 italic">
                "{calcResult?.terbilang_total || "-"}"
              </div>
            </div>

            {/* Tombol Unduh Draf Dokumen */}
            <div className="pt-3 border-t border-slate-800 grid grid-cols-2 gap-2 text-xs">
              <button
                onClick={() => handleDownloadPdf("proposal")}
                disabled={isGeneratingPdf}
                className="w-full inline-flex items-center justify-center gap-1.5 py-2 rounded-xl font-medium bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 transition"
              >
                <Download className="w-3.5 h-3.5" /> Draf Proposal
              </button>
              <button
                onClick={() => handleDownloadPdf("spek")}
                disabled={isGeneratingPdf}
                className="w-full inline-flex items-center justify-center gap-1.5 py-2 rounded-xl font-medium bg-slate-800 hover:bg-slate-700 text-teal-400 border border-slate-700 transition"
              >
                <Download className="w-3.5 h-3.5" /> Draf Spek
              </button>
              <button
                onClick={() => handleDownloadPdf("invoice")}
                disabled={isGeneratingPdf}
                className="w-full inline-flex items-center justify-center gap-1.5 py-2 rounded-xl font-medium bg-slate-800 hover:bg-slate-700 text-indigo-400 border border-slate-700 transition"
              >
                <Download className="w-3.5 h-3.5" /> Draf Invoice
              </button>
              <button
                onClick={() => handleDownloadPdf("kontrak")}
                disabled={isGeneratingPdf}
                className="w-full inline-flex items-center justify-center gap-1.5 py-2 rounded-xl font-medium bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 transition"
              >
                <Download className="w-3.5 h-3.5" /> Draf Kontrak
              </button>
            </div>
          </div>

          {/* Panel Pratinjau PDF */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-xl flex-1 flex flex-col min-h-[460px]">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-sky-400" />
                <h4 className="text-xs font-semibold text-slate-200">
                  Pratinjau PDF: <span className="uppercase text-sky-400 font-bold">{data.jenis}</span>
                </h4>
              </div>
              {pdfUrl && (
                <a
                  href={pdfUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="text-[11px] text-sky-400 hover:underline flex items-center gap-1"
                >
                  Buka Tab Baru <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>

            <div className="flex-1 mt-3 rounded-xl overflow-hidden bg-slate-950 border border-slate-800/80 flex items-center justify-center relative min-h-[400px]">
              {isGeneratingPdf ? (
                <div className="flex flex-col items-center gap-2 text-xs text-slate-400">
                  <RefreshCw className="w-6 h-6 animate-spin text-sky-400" />
                  <span>Mengompilasi Typst menjadi PDF...</span>
                </div>
              ) : pdfUrl ? (
                <iframe
                  src={pdfUrl}
                  title="PDF Preview"
                  className="w-full h-full min-h-[420px] rounded-lg border-0"
                />
              ) : (
                <div className="flex flex-col items-center gap-3 p-6 text-center text-slate-500 text-xs">
                  <div className="w-12 h-12 rounded-full bg-slate-900 flex items-center justify-center border border-slate-800">
                    <FileText className="w-6 h-6 text-slate-600" />
                  </div>
                  <div>
                    <p className="font-medium text-slate-400">Belum ada pratinjau yang aktif</p>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Pilih jenis dokumen di bilah atas (Proposal, Spesifikasi, Invoice, atau Kontrak) untuk pratinjau real-time.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Modal Daftar Proyek Tersimpan */}
      {showProjectModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-5 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <FolderOpen className="w-5 h-5 text-sky-400" />
                <h3 className="font-bold text-sm text-slate-100">Daftar Proyek Tersimpan</h3>
              </div>
              <button
                onClick={() => setShowProjectModal(false)}
                className="text-slate-400 hover:text-white transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Total Proyek: {savedProjects.length}</span>
              <button
                onClick={() => {
                  setShowProjectModal(false);
                  handleNewProject();
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-600 hover:bg-sky-500 text-white transition"
              >
                <Plus className="w-3.5 h-3.5" /> Buat Proyek Baru
              </button>
            </div>

            <div className="max-h-[360px] overflow-y-auto space-y-2 pr-1">
              {savedProjects.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-xs">
                  Belum ada proyek yang disimpan di database.
                </div>
              ) : (
                savedProjects.map((p) => (
                  <div
                    key={p.id}
                    className={`p-3 rounded-xl border transition flex items-center justify-between text-xs ${
                      activeProjectId === p.id
                        ? "bg-sky-950/40 border-sky-500/50"
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700"
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-100">{p.nama}</span>
                        <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 border border-slate-700">
                          {p.jenis}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        Klien: <span className="text-slate-200">{p.client_nama}</span> • Luas: {p.luas_m2} m² • Dokumen: {p.document_count}
                      </p>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => handleDuplicateProject(p.id)}
                        className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                        title="Duplikasi Proyek"
                      >
                        <Copy className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleOpenProject(p.id)}
                        className="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-medium transition"
                      >
                        Buka Proyek
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
