#let data = json("data.json")

#let primary_hex = if "warna_utama" in data.studio and data.studio.warna_utama != "" { data.studio.warna_utama } else { "#0284c7" }
#let accent_hex = if "warna_aksen" in data.studio and data.studio.warna_aksen != "" { data.studio.warna_aksen } else { "#0f172a" }

#let primary_col = rgb(primary_hex)
#let accent_col = rgb(accent_hex)

#set document(
  title: "Kontrak Kerja Desain - " + data.project.nama,
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
        #text(size: 8pt, fill: rgb("#64748b"))[ | Surat Perjanjian Kerja Sama]
      ],
      align(right)[
        #text(size: 8.5pt, fill: rgb("#64748b"))[No: #if data.nomor_dokumen != "" { data.nomor_dokumen } else { "KTR/DRAFT" }]
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
        #text(size: 7.5pt, fill: rgb("#94a3b8"))[Arsi-TeX Contract System | Perjanjian Resmi Desain Arsitektur]
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

// === JUDUL KONTRAK ===
#align(center)[
  #text(size: 14pt, weight: "bold", fill: accent_col)[SURAT PERJANJIAN KERJA SAMA]
  #v(2pt)
  #text(size: 11pt, weight: "bold", fill: primary_col)[JASA PERANCANGAN DESAIN ARSITEKTUR & INTERIOR]
  #v(2pt)
  #text(size: 9pt, fill: rgb("#64748b"))[Nomor: #if data.nomor_dokumen != "" { data.nomor_dokumen } else { "KTR/2026/11/001" }]
]

#v(14pt)

// === PEMBUKA PERJANJIAN ===
Pada hari ini, tanggal *#if data.tanggal_dokumen != "" { data.tanggal_dokumen } else { "20 November 2026" }*, bertempat di #data.project.lokasi, para pihak yang bertanda tangan di bawah ini:

#v(6pt)

#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt, fill: rgb("#f8fafc"))[
  #grid(
    columns: (90pt, 10pt, 1fr),
    row-gutter: 4pt,
    [*1. Nama*], [:], [#data.client.nama],
    [*Perusahaan*], [:], [#if data.client.perusahaan != "" { data.client.perusahaan } else { "-" }],
    [*Alamat*], [:], [#data.client.alamat],
    [*Kontak*], [:], [#data.client.telepon | #data.client.email],
  )
  #v(4pt)
  #text(size: 8.5pt, style: "italic", fill: rgb("#475569"))[Selanjutnya disebut sebagai *PIHAK PERTAMA* (Pemberi Tugas).]
]

#v(6pt)

#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt, fill: rgb("#f8fafc"))[
  #grid(
    columns: (90pt, 10pt, 1fr),
    row-gutter: 4pt,
    [*2. Nama Usaha*], [:], [#data.studio.nama_usaha],
    [*Alamat*], [:], [#data.studio.alamat],
    [*Kontak*], [:], [#data.studio.kontak],
    [*Rekening*], [:], [#data.studio.rekening],
  )
  #v(4pt)
  #text(size: 8.5pt, style: "italic", fill: rgb("#475569"))[Selanjutnya disebut sebagai *PIHAK KEDUA* (Penyedia Jasa / Arsitek).]
]

#v(8pt)

Kedua belah pihak sepakat mengikatkan diri dalam Perjanjian Kerja Sama Perancangan Desain untuk proyek *#data.project.nama* yang berlokasi di *#data.project.lokasi*, dengan ketentuan dan pasal-pasal sebagai berikut:

#v(10pt)

// === PASAL-PASAL KONTRAK ===
#if "clauses" in data and data.clauses.len() > 0 [
  #for clause in data.clauses [
    #if clause.aktif [
      #block(width: 100%, inset: (y: 4pt))[
        #text(weight: "bold", fill: accent_col)[#clause.judul]
        #v(3pt)
        #text(size: 9pt, fill: rgb("#334155"))[#clause.isi]
      ]
      #v(4pt)
    ]
  ]
] else [
  #block(width: 100%)[
    #text(weight: "bold")[Pasal 1: Ruang Lingkup Pekerjaan]
    #v(2pt)
    #text(size: 9pt)[PIHAK KEDUA melaksanakan pekerjaan perancangan: #data.project.ruang_lingkup.]
  ]
]

#v(8pt)

// === TABEL NILAI KONTRAK & TERMIN ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 10pt, radius: 4pt, fill: rgb("#f8fafc"))[
  #text(weight: "bold", fill: accent_col)[Rincian Nilai & Termin Pembayaran:]
  #v(4pt)
  #grid(
    columns: (120pt, 1fr),
    row-gutter: 4pt,
    [Total Nilai Kontrak:], [#text(weight: "bold", fill: primary_col)[#data.financials.total_fmt]],
    [Terbilang:], [#text(style: "italic")[#data.financials.terbilang_total]],
  )
  #v(6pt)
  #table(
    columns: (24pt, 110pt, 45pt, 85pt, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
    fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
    table.header(
      align(center)[*No*],
      align(left)[*Termin*],
      align(center)[*Persen*],
      align(right)[*Nominal*],
      align(left)[*Pemicu Pembayaran*]
    ),
    for (i, term) in data.payment_terms.enumerate() [
      #align(center)[#(i + 1)]
      #align(left)[#text(size: 8.5pt, weight: "medium")[#term.label]]
      #align(center)[#text(size: 8.5pt)[#term.persen%]]
      #align(right)[#text(size: 8.5pt, weight: "bold")[#term.nominal_fmt]]
      #align(left)[#text(size: 8.5pt)[#term.pemicu]]
    ]
  )
]

#v(14pt)

Demikian Perjanjian ini dibuat dalam 2 (dua) rangkap bermaterai cukup dan memiliki kekuatan hukum yang sama bagi kedua belah pihak.

#v(20pt)

// === TANDA TANGAN DENGAN KOTAK MATERAI ===
#grid(
  columns: (1fr, 1fr),
  gutter: 24pt,
  align(center)[
    #text(size: 9pt, fill: rgb("#475569"))[PIHAK PERTAMA (Klien)]
    #v(3pt)
    #text(size: 10pt, weight: "bold", fill: accent_col)[#data.client.nama]
    #v(10pt)
    #rect(width: 80pt, height: 42pt, stroke: (paint: rgb("#94a3b8"), dash: "dashed", thickness: 0.5pt), radius: 2pt)[
      #align(center + horizon)[#text(size: 7pt, fill: rgb("#94a3b8"))[MATERAI\ Rp 10.000]]
    ]
    #v(10pt)
    #line(length: 75%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Pemberi Tugas]
  ],
  align(center)[
    #text(size: 9pt, fill: rgb("#475569"))[PIHAK KEDUA (Penyedia Jasa)]
    #v(3pt)
    #text(size: 10pt, weight: "bold", fill: accent_col)[#data.studio.nama_usaha]
    #v(10pt)
    #rect(width: 80pt, height: 42pt, stroke: (paint: rgb("#94a3b8"), dash: "dashed", thickness: 0.5pt), radius: 2pt)[
      #align(center + horizon)[#text(size: 7pt, fill: rgb("#94a3b8"))[MATERAI\ Rp 10.000]]
    ]
    #v(10pt)
    #line(length: 75%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Arsitek Penanggung Jawab]
  ]
)

#v(16pt)

// === DISCLAIMER HUKUM WAJIB ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 8pt, radius: 3pt, fill: rgb("#fef2f2"))[
  #text(size: 7.5pt, fill: rgb("#991b1b"))[
    *Pemberitahuan Hukum (Legal Disclaimer):* Surat perjanjian ini merupakan template perancangan arsitektur dan desain interior standar yang dihasilkan secara otomatis oleh sistem Arsi-TeX, dan bukan merupakan nasihat hukum resmi. Para pihak disarankan untuk menelaah kembali klausul dan pasal yang disepakati sesuai dengan regulasi dan kesepakatan masing-masing.
  ]
]
