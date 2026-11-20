from typing import List, Dict

DEFAULT_CLAUSES: List[Dict[str, str | int | bool]] = [
    {
        "kode": "PASAL_1",
        "judul": "Pasal 1: Ruang Lingkup Jasa Perancangan",
        "isi": "PIHAK KEDUA berkewajiban melaksanakan pekerjaan perencanaan dan desain arsitektur/interior sesuai dengan deskripsi ruang lingkup yang disepakati, meliputi perancangan konsep skematik, pengembangan desain 3D, penyusunan Gambar Kerja Detail (DED), serta pendampingan pemilihan spesifikasi material.",
        "urutan": 1,
        "aktif": True
    },
    {
        "kode": "PASAL_2",
        "judul": "Pasal 2: Jangka Waktu & Jadwal Pelaksanaan",
        "isi": "Pekerjaan perancangan dilaksanakan sesuai jadwal tahapan kerja yang disepakati bersama. Jangka waktu pengerjaan tidak mencakup durasi waktu yang dibutuhkan PIHAK PERTAMA untuk memberikan persetujuan (approval) atau revisi melebihi batas wajar.",
        "urutan": 2,
        "aktif": True
    },
    {
        "kode": "PASAL_3",
        "judul": "Pasal 3: Nilai Kontrak & Ketentuan Pembayaran",
        "isi": "Total nilai imbalan jasa dan tahapan pembayaran disepakati sesuai dengan skema termin pembayaran pada dokumen perjanjian ini. Pembayaran dilakukan melalui transfer ke rekening bank resmi PIHAK KEDUA. Keterlambatan pembayaran termin dapat mengakibatkan penghentian sementara pekerjaan perancangan.",
        "urutan": 3,
        "aktif": True
    },
    {
        "kode": "PASAL_4",
        "judul": "Pasal 4: Hak dan Kewajiban Para Pihak",
        "isi": "PIHAK PERTAMA berhak menerima hasil rancangan desain sesuai standar profesional dan berkewajiban memberikan data lahan/lokasi yang akurat serta membayar imbalan jasa tepat waktu. PIHAK KEDUA berhak menerima pembayaran tepat waktu dan berkewajiban menyelesaikan desain dengan keahlian terbaiknya.",
        "urutan": 4,
        "aktif": True
    },
    {
        "kode": "PASAL_5",
        "judul": "Pasal 5: Batasan Revisi Desain",
        "isi": "Revisi desain pada setiap tahapan dibatasi maksimal sebanyak 2 (dua) kali revisi minor tanpa mengubah konsep dasar tata ruang atau luasan secara mendasar. Revisi mayor atau perubahan menyeluruh setelah persetujuan tahapan akan dikenakan biaya tambahan (addendum) sesuai kesepakatan bersama.",
        "urutan": 5,
        "aktif": True
    },
    {
        "kode": "PASAL_6",
        "judul": "Pasal 6: Hak Kekayaan Intelektual (Hak Cipta Desain)",
        "isi": "Hak Cipta dan kepemilikan intelektual atas seluruh konsep desain, gambar kerja, dan model 3D tetap berada pada PIHAK KEDUA (Studio/Arsitek). PIHAK PERTAMA memperoleh hak guna pakai non-eksklusif atas desain tersebut semata-mata untuk pelaksanaan pembangunan pada lokasi proyek yang tercantum.",
        "urutan": 6,
        "aktif": True
    },
    {
        "kode": "PASAL_7",
        "judul": "Pasal 7: Pembatalan dan Pemutusan Perjanjian",
        "isi": "Apabila PIHAK PERTAMA membatalkan perjanjian secara sepihak sebelum pekerjaan selesai, maka seluruh pembayaran uang muka (DP) dan termin yang telah dibayarkan tidak dapat ditarik kembali, dan PIHAK PERTAMA wajib membayar pekerjaan yang telah diselesaikan hingga tanggal pembatalan.",
        "urutan": 7,
        "aktif": True
    },
    {
        "kode": "PASAL_8",
        "judul": "Pasal 8: Keadaan Kahar (Force Majeure)",
        "isi": "Para pihak dibebaskan dari tanggung jawab atas keterlambatan atau kegagalan pemenuhan kewajiban apabila disebabkan oleh keadaan kahar di luar kendali wajar manusia, seperti bencana alam, kebakaran, gempa bumi, huru-hara, atau kebijakan pemerintah terkait darurat sipil.",
        "urutan": 8,
        "aktif": True
    },
    {
        "kode": "PASAL_9",
        "judul": "Pasal 9: Penyelesaian Perselisihan",
        "isi": "Segala perselisihan yang timbul sehubungan dengan penafsiran atau pelaksanaan perjanjian ini akan diselesaikan secara musyawarah untuk mufakat. Apabila tidak tercapai mufakat dalam waktu 30 (tiga puluh) hari kalender, maka akan diselesaikan melalui domisili hukum Pengadilan Negeri setempat.",
        "urutan": 9,
        "aktif": True
    }
]

