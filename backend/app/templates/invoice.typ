#let data = json("data.json")

#let primary_hex = if "warna_utama" in data.studio and data.studio.warna_utama != "" { data.studio.warna_utama } else { "#0284c7" }
#let accent_hex = if "warna_aksen" in data.studio and data.studio.warna_aksen != "" { data.studio.warna_aksen } else { "#0f172a" }

#let primary_col = rgb(primary_hex)
#let accent_col = rgb(accent_hex)

#set document(
  title: "Invoice - " + data.nomor_dokumen,
  author: data.studio.nama_usaha
)

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.2cm, right: 2.2cm),
  header: [
    #grid(
      columns: (1fr, auto),
      align(left)[
        #text(size: 8.5pt, weight: "bold", fill: primary_col)[#data.studio.nama_usaha]
      ],
      align(right)[
        #text(size: 8.5pt, fill: rgb("#64748b"))[Dokumen Penagihan Resmi]
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
        #text(size: 8pt, fill: rgb("#94a3b8"))[Arsi-TeX Invoice System | Harap simpan bukti pembayaran ini]
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

// === HEADER INVOICE ===
#grid(
  columns: (1fr, 1fr),
  [
    #text(size: 14pt, weight: "bold", fill: primary_col)[#data.studio.nama_usaha]
    #v(3pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[#data.studio.alamat]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Kontak: #data.studio.kontak]
    #if data.studio.npwp != "" [
      #v(2pt)
      #text(size: 8pt, fill: rgb("#64748b"))[NPWP: #data.studio.npwp]
    ]
  ],
  align(right)[
    #text(size: 20pt, weight: "bold", fill: accent_col)[INVOICE]
    #v(4pt)
    #text(size: 9pt, fill: rgb("#64748b"))[Nomor:]
    #v(1pt)
    #text(size: 10pt, weight: "bold", fill: primary_col)[#if data.nomor_dokumen != "" { data.nomor_dokumen } else { "INV/2026/001" }]
    #v(3pt)
    #text(size: 8.5pt, fill: rgb("#64748b"))[Tanggal: #if data.tanggal_dokumen != "" { data.tanggal_dokumen } else { "20 November 2026" }]
  ]
)

#v(16pt)
#line(length: 100%, stroke: 1.5pt + primary_col)
#v(14pt)

// === KEPADA & PROYEK ===
#grid(
  columns: (1.1fr, 0.9fr),
  gutter: 16pt,
  block(width: 100%, fill: rgb("#f8fafc"), stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
    #text(size: 8.5pt, weight: "bold", fill: rgb("#64748b"))[DITAGIHKAN KEPADA:]
    #v(4pt)
    #text(size: 11pt, weight: "bold", fill: accent_col)[#data.client.nama]
    #if data.client.perusahaan != "" [
      #v(2pt)
      #text(size: 9pt, weight: "medium", fill: rgb("#334155"))[#data.client.perusahaan]
    ]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[#data.client.alamat]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Telepon: #data.client.telepon | Email: #data.client.email]
  ],
  block(width: 100%, fill: rgb("#f8fafc"), stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
    #text(size: 8.5pt, weight: "bold", fill: rgb("#64748b"))[DATA PROYEK:]
    #v(4pt)
    #text(size: 10pt, weight: "bold", fill: accent_col)[#data.project.nama]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Lokasi: #data.project.lokasi]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Jenis: #data.project.jenis (#data.project.luas_m2 m²)]
  ]
)

#v(14pt)

// === TABEL RINCIAN TAGIHAN ===
#text(size: 10pt, weight: "bold", fill: accent_col)[Rincian Tagihan]
#v(6pt)

#table(
  columns: (30pt, 1fr, 60pt, 100pt),
  stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
  fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
  table.header(
    align(center)[*No*],
    align(left)[*Deskripsi / Uraian Termin*],
    align(center)[*Persen*],
    align(right)[*Jumlah Tagihan*]
  ),
  align(center)[1],
  align(left)[
    #text(weight: "bold")[#data.selected_term.label]
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[#data.selected_term.pemicu]
  ],
  align(center)[#data.selected_term.persen%],
  align(right)[#text(weight: "bold")[#data.selected_term.nominal_fmt]]
)

#v(10pt)

// === TOTAL FINANSIAL ===
#align(right)[
  #block(width: 50%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt, fill: rgb("#f8fafc"))[
    #grid(
      columns: (1fr, auto),
      row-gutter: 6pt,
      [#text(size: 8.5pt, fill: rgb("#475569"))[Total Tagihan Termin:]],
      [#text(size: 9pt, weight: "bold")[#data.selected_term.nominal_fmt]],

      grid.cell(colspan: 2)[#line(length: 100%, stroke: 1pt + rgb("#cbd5e1"))],

      [#text(size: 10pt, weight: "bold", fill: accent_col)[Total Yang Harus Dibayar:]],
      [#text(size: 11pt, weight: "bold", fill: primary_col)[#data.selected_term.nominal_fmt]]
    )
  ]
]

#v(6pt)
#block(width: 100%, fill: rgb("#eff6ff"), stroke: 0.5pt + rgb("#bfdbfe"), inset: 10pt, radius: 4pt)[
  #text(size: 8.5pt, fill: primary_col)[*Terbilang:* #data.selected_term.terbilang]
]

#v(14pt)

// === INSTRUKSI PEMBAYARAN ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
  #text(size: 9pt, weight: "bold", fill: accent_col)[Instruksi & Rekening Pembayaran:]
  #v(4pt)
  #text(size: 9.5pt, weight: "bold", fill: primary_col)[#data.studio.rekening]
  #v(3pt)
  #text(size: 8.5pt, fill: rgb("#475569"))[1. Mohon sertakan nomor invoice pada berita transfer bank.]
  #v(2pt)
  #text(size: 8.5pt, fill: rgb("#475569"))[2. Konfirmasi bukti pembayaran dapat dikirimkan ke kontak WhatsApp/Email studio di atas.]
]

#v(25pt)

// === TANDA TANGAN ===
#align(right)[
  #block(width: 40%)[
    #align(center)[
      #text(size: 8.5pt, fill: rgb("#64748b"))[Hormat kami,]
      #v(3pt)
      #text(size: 9.5pt, weight: "bold", fill: accent_col)[#data.studio.nama_usaha]
      #v(45pt)
      #line(length: 80%, stroke: 0.5pt + rgb("#64748b"))
      #v(2pt)
      #text(size: 8.5pt, fill: rgb("#475569"))[Finance / Arsitek Penanggung Jawab]
    ]
  ]
]
