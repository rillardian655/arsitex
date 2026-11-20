from typing import List, Dict, Any

def terbilang(n: int) -> str:
    """Mengubah bilangan integer menjadi teks terbilang dalam bahasa Indonesia."""
    if n == 0:
        return "Nol Rupiah"
    
    if n < 0:
        return "Minus " + terbilang(abs(n))

    angka = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]

    def _terbilang_rek(val: int) -> str:
        if val < 12:
            return angka[val]
        elif val < 20:
            return _terbilang_rek(val - 10) + " Belas"
        elif val < 100:
            sisa = val % 10
            return _terbilang_rek(val // 10) + " Puluh" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 200:
            sisa = val - 100
            return "Seratus" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 1000:
            sisa = val % 100
            return _terbilang_rek(val // 100) + " Ratus" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 2000:
            sisa = val - 1000
            return "Seribu" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 1000000:
            sisa = val % 1000
            return _terbilang_rek(val // 1000) + " Ribu" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 1000000000:
            sisa = val % 1000000
            return _terbilang_rek(val // 1000000) + " Juta" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        elif val < 1000000000000:
            sisa = val % 1000000000
            return _terbilang_rek(val // 1000000000) + " Miliar" + (f" {_terbilang_rek(sisa)}" if sisa else "")
        else:
            sisa = val % 1000000000000
            return _terbilang_rek(val // 1000000000000) + " Triliun" + (f" {_terbilang_rek(sisa)}" if sisa else "")

    hasil = _terbilang_rek(n).strip()
    return f"{hasil} Rupiah"


def format_rupiah(val: int) -> str:
    """Format angka integer ke string mata uang Rupiah Indonesia (contoh: Rp 12.500.000)."""
    return f"Rp {val:,.0f}".replace(",", ".")


def calculate_financials(material_items: List[Any], diskon_rp: int = 0, ppn_persen: float = 11.0) -> Dict[str, Any]:
    """
    Menghitung subtotal, diskon, DPP, PPN, dan total akhir.
    Semua uang disimpan dalam integer Rupiah murni untuk mencegah floating point issue.
    """
    subtotal = 0
    calculated_items = []

    for item in material_items:
        # volume bisa berupa float (misal 12.5 m2)
        vol = getattr(item, "volume", 1.0)
        harga = getattr(item, "harga_satuan", 0)
        item_subtotal = int(round(vol * harga))
        subtotal += item_subtotal

        calculated_items.append({
            "area": getattr(item, "area", "-"),
            "pekerjaan": getattr(item, "pekerjaan", "-"),
            "material": getattr(item, "material", "-"),
            "merek": getattr(item, "merek", "-") or "-",
            "volume": vol,
            "satuan": getattr(item, "satuan", "ls"),
            "harga_satuan": harga,
            "harga_satuan_fmt": format_rupiah(harga),
            "subtotal": item_subtotal,
            "subtotal_fmt": format_rupiah(item_subtotal),
            "catatan": getattr(item, "catatan", "") or ""
        })

    diskon = max(0, int(diskon_rp))
    dpp = max(0, subtotal - diskon)
    ppn_rp = int(round(dpp * (ppn_persen / 100.0))) if ppn_persen > 0 else 0
    total = dpp + ppn_rp

    return {
        "items": calculated_items,
        "subtotal": subtotal,
        "subtotal_fmt": format_rupiah(subtotal),
        "diskon_rp": diskon,
        "diskon_fmt": format_rupiah(diskon),
        "dpp": dpp,
        "dpp_fmt": format_rupiah(dpp),
        "ppn_persen": ppn_persen,
        "ppn_rp": ppn_rp,
        "ppn_fmt": format_rupiah(ppn_rp),
        "total": total,
        "total_fmt": format_rupiah(total),
        "terbilang_total": terbilang(total)
    }


def calculate_terms(total: int, payment_terms: List[Any]) -> List[Dict[str, Any]]:
    """
    Menghitung nominal tiap termin berdasarkan persentase atau nominal langsung.
    Memvalidasi total persentase harus tepat 100% dan menyesuaikan pembulatan agar total sama persis.
    """
    if not payment_terms:
        return [{
            "urutan": 1,
            "label": "Pelunasan 100%",
            "persen": 100.0,
            "nominal": total,
            "nominal_fmt": format_rupiah(total),
            "pemicu": "Saat pekerjaan selesai / serah terima",
            "jatuh_tempo": "-",
            "terbilang": terbilang(total)
        }]

    # Periksa apakah termin menggunakan persen atau nominal
    uses_percentage = any(getattr(t, "persen", None) is not None for t in payment_terms)

    if uses_percentage:
        total_percent = sum(float(getattr(t, "persen", 0.0) or 0.0) for t in payment_terms)
        # toleransi float 0.01%
        if abs(total_percent - 100.0) > 0.05:
            raise ValueError(f"Total persentase termin harus tepat 100%, saat ini: {total_percent:.1f}%")

        calculated = []
        running_sum = 0
        n_terms = len(payment_terms)

        for i, t in enumerate(payment_terms):
            pct = float(getattr(t, "persen", 0.0) or 0.0)
            if i == n_terms - 1:
                # Termin terakhir menyerap selisih pembulatan integer
                nominal = total - running_sum
            else:
                nominal = int(round(total * (pct / 100.0)))
                running_sum += nominal

            calculated.append({
                "urutan": getattr(t, "urutan", i + 1),
                "label": getattr(t, "label", f"Termin {i+1}"),
                "persen": pct,
                "nominal": nominal,
                "nominal_fmt": format_rupiah(nominal),
                "pemicu": getattr(t, "pemicu", "") or "-",
                "jatuh_tempo": getattr(t, "jatuh_tempo", "") or "-",
                "terbilang": terbilang(nominal)
            })

        return calculated
    else:
        # Termin menggunakan nominal tetap
        total_nominal = sum(int(getattr(t, "nominal", 0) or 0) for t in payment_terms)
        if total_nominal != total and total > 0:
            raise ValueError(
                f"Total nominal termin ({format_rupiah(total_nominal)}) harus sama dengan total nilai ({format_rupiah(total)})"
            )

        calculated = []
        for i, t in enumerate(payment_terms):
            nom = int(getattr(t, "nominal", 0) or 0)
            pct = round((nom / total) * 100, 2) if total > 0 else 0.0
            calculated.append({
                "urutan": getattr(t, "urutan", i + 1),
                "label": getattr(t, "label", f"Termin {i+1}"),
                "persen": pct,
                "nominal": nom,
                "nominal_fmt": format_rupiah(nom),
                "pemicu": getattr(t, "pemicu", "") or "-",
                "jatuh_tempo": getattr(t, "jatuh_tempo", "") or "-",
                "terbilang": terbilang(nom)
            })
        return calculated

