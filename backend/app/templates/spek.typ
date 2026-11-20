#let data = json("data.json")

#let primary_hex = if "warna_utama" in data.studio and data.studio.warna_utama != "" { data.studio.warna_utama } else { "#0284c7" }
#let accent_hex = if "warna_aksen" in data.studio and data.studio.warna_aksen != "" { data.studio.warna_aksen } else { "#0f172a" }

#let primary_col = rgb(primary_hex)
#let accent_col = rgb(accent_hex)

#set document(
  title: "Spesifikasi Teknis - " + data.project.nama,
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
        #text(size: 8pt, fill: rgb("#64748b"))[ | Spesifikasi Teknis & Daftar Material]
      ],
      align(right)[
        #text(size: 8.5pt, fill: rgb("#64748b"))[No: #if data.nomor_dokumen != "" { data.nomor_dokumen } else { "SPEK/DRAFT" }]
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
        #text(size: 8pt, fill: rgb("#94a3b8"))[Arsi-TeX Material Engine | Dokumen Spesifikasi Resmi]
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

// === HEADER DOKUMEN ===
#block(width: 100%, fill: rgb("#f8fafc"), inset: 16pt, radius: 4pt, stroke: 1pt + rgb("#e2e8f0"))[
  #grid(
    columns: (1fr, auto),
    [
      #text(size: 8pt, weight: "bold", fill: primary_col)[DOKUMEN SPESIFIKASI TEKNIS]
      #v(2pt)
      #text(size: 16pt, weight: "bold", fill: accent_col)[#data.project.nama]
      #v(3pt)
      #text(size: 9pt, fill: rgb("#475569"))[Lokasi: #data.project.lokasi | Luas Area: #data.project.luas_m2 m²]
    ],
    align(right)[
      #text(size: 8.5pt, fill: rgb("#64748b"))[Tanggal Dokumen:]
      #v(1pt)
      #text(size: 9.5pt, weight: "bold", fill: rgb("#1e293b"))[#if data.tanggal_dokumen != "" { data.tanggal_dokumen } else { "Tanggal Draf" }]
      #v(3pt)
      #text(size: 8.5pt, fill: rgb("#64748b"))[Klien:]
      #v(1pt)
      #text(size: 9pt, weight: "bold", fill: rgb("#334155"))[#data.client.nama]
    ]
  )
]

#v(14pt)

// === KETENTUAN UMUM PELAKSANAAN ===
#block(width: 100%, stroke: 0.5pt + rgb("#e2e8f0"), inset: 12pt, radius: 4pt)[
  #text(size: 9.5pt, weight: "bold", fill: accent_col)[1. Ketentuan Umum & Standar Mutu]
  #v(4pt)
  #text(size: 8.5pt, fill: rgb("#334155"))[
    1. Seluruh material yang didatangkan ke lokasi wajib sesuai dengan merek, spesifikasi, dan tipe yang tercantum dalam dokumen ini.
    2. Penggantian material sejenis hanya diperbolehkan apabila disetujui secara tertulis oleh Arsitek / Pengawas Berkala.
    3. Penyedia jasa / kontraktor wajib membuat *mock-up* atau contoh pemasangan untuk disetujui sebelum pekerjaan massal dimulai.
  ]
]

#v(14pt)

// === TABEL SPESIFIKASI PER AREA ===
#text(size: 10pt, weight: "bold", fill: accent_col)[2. Tabel Rincian Spesifikasi Material & Lingkup Pekerjaan]
#v(6pt)

#if data.calculated_items.len() > 0 [
  #table(
    columns: (24pt, 75pt, 110pt, 1fr, 45pt, 35pt, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1.5pt + primary_col) } else { (bottom: 0.5pt + rgb("#e2e8f0")) },
    fill: (col, row) => if row == 0 { rgb("#f1f5f9") } else { none },
    table.header(
      align(center)[*No*],
      align(left)[*Area / Ruang*],
      align(left)[*Item Pekerjaan*],
      align(left)[*Material & Tipe*],
      align(right)[*Vol*],
      align(center)[*Sat*],
      align(left)[*Catatan & Standar Pemasangan*]
    ),
    for (i, item) in data.calculated_items.enumerate() [
      #align(center)[#(i + 1)]
      #align(left)[#text(size: 8.5pt, weight: "medium")[#item.area]]
      #align(left)[#text(size: 8.5pt)[#item.pekerjaan]]
      #align(left)[#text(size: 8.5pt)[#item.material #if item.merek != "-" and item.merek != "" [(#item.merek)]]]
      #align(right)[#text(size: 8.5pt)[#item.volume]]
      #align(center)[#text(size: 8.5pt)[#item.satuan]]
      #align(left)[#text(size: 8pt, fill: rgb("#475569"))[#if item.catatan != "" { item.catatan } else { "-" }]]
    ]
  )
] else [
  #text(style: "italic", fill: rgb("#64748b"))[Belum ada rincian material yang diinput.]
]

#v(25pt)

// === TANDA TANGAN PERSETUJUAN ===
#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  align(center)[
    #text(size: 8.5pt, fill: rgb("#64748b"))[Disusun oleh Perancang,]
    #v(3pt)
    #text(size: 9.5pt, weight: "bold", fill: accent_col)[#data.studio.nama_usaha]
    #v(48pt)
    #line(length: 70%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Arsitek / Desainer Interior]
  ],
  align(center)[
    #text(size: 8.5pt, fill: rgb("#64748b"))[Disetujui oleh Klien,]
    #v(3pt)
    #text(size: 9.5pt, weight: "bold", fill: accent_col)[#data.client.nama]
    #v(48pt)
    #line(length: 70%, stroke: 0.5pt + rgb("#64748b"))
    #v(2pt)
    #text(size: 8.5pt, fill: rgb("#475569"))[Pemberi Tugas / Pemilik Proyek]
  ]
)

