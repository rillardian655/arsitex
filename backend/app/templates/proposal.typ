#let data = json("data.json")

#let primary_hex = if "warna_utama" in data.studio and data.studio.warna_utama != "" { data.studio.warna_utama } else { "#0284c7" }
#let accent_hex = if "warna_aksen" in data.studio and data.studio.warna_aksen != "" { data.studio.warna_aksen } else { "#0f172a" }

#let primary_col = rgb(primary_hex)
#let accent_col = rgb(accent_hex)

#set document(
  title: "Proposal - " + data.project.nama,
  author: data.studio.nama_usaha
)

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm),
  header: [
    #grid(
      columns: (1fr, auto),
      align(left)[
        #text(size: 8.5pt, weight: "bold", fill: primary_col)[#data.studio.nama_usaha]
        #text(size: 8pt, fill: rgb("#64748b"))[ | Proposal Penawaran Desain]
      ],
      align(right)[
        #text(size: 8.5pt, fill: rgb("#64748b"))[No: #if data.nomor_dokumen != "" { data.nomor_dokumen } else { "PROP/DRAFT" }]
      ]
    )
    #v(3pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
  ],
  footer: [
    #line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
    #v(4pt)
    #grid(
      columns: (1fr, auto),
      align(left)[
        #text(size: 8pt, fill: rgb("#94a3b8"))[Arsi-TeX Document Engine | Dokumen Resmi Studio]
      ],
      align(right)[
        #text(size: 8pt, fill: rgb("#64748b"))[Halaman #context counter(page).display()]
      ]
    )
  ]
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Arial"),
  size: 9.5pt,
  fill: rgb("#1e293b"),
  spacing: 120%
)

// === HEADER UTAMA ===
#block(width: 100%, fill: rgb("#f8fafc"), inset: 16pt, radius: 4pt, stroke: 1pt + rgb("#e2e8f0"))[
  #grid(
    columns: (1fr, auto),
    [
      #text(size: 8pt, weight: "bold", fill: primary_col)[DOKUMEN PROPOSAL PENAWARAN]
      #v(2pt)
      #text(size: 16pt, weight: "bold", fill: accent_col)[#data.project.nama]
      #v(3pt)
      #text(size: 9pt, fill: rgb("#475569"))[Jenis Proyek: #data.project.jenis | Luas: #data.project.luas_m2 m²]
    ],
    align(right)[
      #text(size: 8.5pt, fill: rgb("#64748b"))[Tanggal Dokumen:]
      #v(1pt)
      #text(size: 9.5pt, weight: "bold", fill: rgb("#1e293b"))[#if data.tanggal_dokumen != "" { data.tanggal_dokumen } else { "Tanggal Draf" }]
      #v(4pt)
      #text(size: 8.5pt, fill: rgb("#64748b"))[Lokasi:]
      #v(1pt)
      #text(size: 9pt, fill: rgb("#334155"))[#data.project.lokasi]
    ]
  )
]

#v(12pt)

// === INFORMASI PIHAK ===
#grid(
  columns: (1fr, 1fr),
  gutter: 16pt,
  block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
    #text(size: 9pt, weight: "bold", fill: accent_col)[INFORMASI PENGIRIM (STUDIO)]
    #v(4pt)
    #text(size: 10.5pt, weight: "bold", fill: primary_col)[#data.studio.nama_usaha]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[#data.studio.alamat]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Kontak: #data.studio.kontak]
    #if data.studio.npwp != "" [
      #v(2pt)
      #text(size: 8pt, fill: rgb("#64748b"))[NPWP: #data.studio.npwp]
    ]
  ],
  block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
    #text(size: 9pt, weight: "bold", fill: accent_col)[DITUJUKAN KEPADA (KLIEN)]
    #v(4pt)
    #text(size: 10.5pt, weight: "bold", fill: rgb("#1e293b"))[#data.client.nama]
    #if data.client.perusahaan != "" [
      #v(2pt)
      #text(size: 9pt, weight: "medium", fill: rgb("#475569"))[#data.client.perusahaan]
    ]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[#data.client.alamat]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Telepon: #data.client.telepon | Email: #data.client.email]
  ]
)

#v(10pt)

// === RUANG LINGKUP ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
  #text(size: 9.5pt, weight: "bold", fill: accent_col)[1. Ruang Lingkup Pekerjaan]
  #v(4pt)
  #text(size: 9pt, fill: rgb("#334155"))[#data.project.ruang_lingkup]
]

#v(10pt)

// === SPESIFIKASI & RINCIAN BIAYA ===
#text(size: 10pt, weight: "bold", fill: accent_col)[2. Rincian Spesifikasi Material & Estimasi Biaya Pekerjaan]
#v(6pt)

#if data.calculated_items.len() > 0 [
  #table(
    columns: (24pt, 65pt, 1fr, 75pt, 35pt, 30pt, 65pt, 75pt),
    stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
    fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
    table.header(
      align(center)[*No*],
      align(left)[*Area*],
      align(left)[*Uraian Pekerjaan*],
      align(left)[*Material*],
      align(right)[*Vol*],
      align(center)[*Sat*],
      align(right)[*Harga*],
      align(right)[*Total*]
    ),
    for (i, item) in data.calculated_items.enumerate() [
      #align(center)[#(i + 1)]
      #align(left)[#text(size: 8.5pt)[#item.area]]
      #align(left)[#text(size: 8.5pt, weight: "medium")[#item.pekerjaan]]
      #align(left)[#text(size: 8.5pt)[#item.material #if item.merek != "-" and item.merek != "" [(#item.merek)]]]
      #align(right)[#text(size: 8.5pt)[#item.volume]]
      #align(center)[#text(size: 8.5pt)[#item.satuan]]
      #align(right)[#text(size: 8.5pt)[#item.harga_satuan_fmt]]
      #align(right)[#text(size: 8.5pt, weight: "bold")[#item.subtotal_fmt]]
    ]
  )
] else [
  #text(style: "italic", fill: rgb("#64748b"))[Tidak ada rincian item pekerjaan yang ditambahkan.]
]

#v(8pt)

// === TOTAL FINANSIAL ===
#align(right)[
  #block(width: 55%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt, fill: rgb("#f8fafc"))[
    #table(
      columns: (1fr, auto),
      stroke: none,
      inset: (x: 0pt, y: 3pt),
      [#text(size: 8.5pt, fill: rgb("#475569"))[Subtotal Biaya:]],
      [#text(size: 8.5pt, weight: "bold")[#data.financials.subtotal_fmt]],

      ..if data.financials.diskon_rp > 0 {
        (
          [#text(size: 8.5pt, fill: rgb("#dc2626"))[Potongan Diskon:]],
          [#text(size: 8.5pt, fill: rgb("#dc2626"), weight: "bold")[- #data.financials.diskon_fmt]]
        )
      } else { () },

      ..if data.financials.ppn_persen > 0 {
        (
          [#text(size: 8.5pt, fill: rgb("#475569"))[PPN (#data.financials.ppn_persen%):]],
          [#text(size: 8.5pt, weight: "bold")[#data.financials.ppn_fmt]]
        )
      } else { () },

      table.hline(stroke: 1pt + rgb("#cbd5e1")),

      [#text(size: 10.5pt, weight: "bold", fill: accent_col)[Total Penawaran:]],
      [#text(size: 11pt, weight: "bold", fill: primary_col)[#data.financials.total_fmt]]
    )
  ]
]

#v(4pt)
#block(width: 100%, fill: rgb("#eff6ff"), stroke: 0.5pt + rgb("#bfdbfe"), inset: 8pt, radius: 3pt)[
  #text(size: 8.5pt, fill: primary_col)[*Terbilang:* #data.financials.terbilang_total]
]

#v(12pt)

// === JADWAL TAHAPAN KERJA ===
#if data.schedule_stages.len() > 0 [
  #text(size: 10pt, weight: "bold", fill: accent_col)[3. Rencana Tahapan Pelaksanaan Kerja]
  #v(4pt)
  #table(
    columns: (30pt, 1fr, 80pt, 120pt),
    stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
    fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
    table.header(
      align(center)[*No*],
      align(left)[*Tahapan Kegiatan*],
      align(center)[*Durasi / Periode*],
      align(left)[*Keterangan Output*]
    ),
    for (i, stage) in data.schedule_stages.enumerate() [
      #align(center)[#(i + 1)]
      #align(left)[#text(size: 8.5pt, weight: "medium")[#stage.tahap]]
      #align(center)[#text(size: 8.5pt)[#if stage.durasi != "" { stage.durasi } else { stage.tanggal_mulai + " s/d " + stage.tanggal_selesai }]]
      #align(left)[#text(size: 8.5pt)[#stage.keterangan]]
    ]
  )
  #v(10pt)
]

// === TERMIN PEMBAYARAN ===
#text(size: 10pt, weight: "bold", fill: accent_col)[4. Skema & Termin Pembayaran]
#v(4pt)
#table(
  columns: (30pt, 120pt, 50pt, 90pt, 1fr),
  stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
  fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
  table.header(
    align(center)[*No*],
    align(left)[*Termin / Tahap*],
    align(center)[*Persen*],
    align(right)[*Nominal*],
    align(left)[*Pemicu / Syarat Pembayaran*]
  ),
  for (i, term) in data.payment_terms.enumerate() [
    #align(center)[#(i + 1)]
    #align(left)[#text(size: 8.5pt, weight: "medium")[#term.label]]
    #align(center)[#text(size: 8.5pt)[#term.persen%]]
    #align(right)[#text(size: 8.5pt, weight: "bold")[#term.nominal_fmt]]
    #align(left)[#text(size: 8.5pt)[#term.pemicu]]
  ]
)

#v(12pt)

// === REKENING PEMBAYARAN ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt)[
  #text(size: 8.5pt, weight: "bold", fill: accent_col)[Rekening Resmi Pembayaran:]
  #v(2pt)
  #text(size: 9pt, fill: primary_col, weight: "bold")[#data.studio.rekening]
]

#v(20pt)

// === TANDA TANGAN PERSETUJUAN ===
#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  align(center)[
    #text(size: 9pt, fill: rgb("#64748b"))[Diajukan oleh,]
    #v(3pt)
    #text(size: 9.5pt, weight: "bold", fill: accent_col)[#data.studio.nama_usaha]
    #v(48pt)
    #line(length: 70%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Penyedia Jasa / Arsitek]
  ],
  align(center)[
    #text(size: 9pt, fill: rgb("#64748b"))[Disetujui oleh,]
    #v(3pt)
    #text(size: 9.5pt, weight: "bold", fill: accent_col)[#data.client.nama]
    #v(48pt)
    #line(length: 70%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Klien / Pemberi Tugas]
  ]
)
