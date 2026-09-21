import { useEffect, useState } from "react";
import { api, API } from "@/lib/api";
import { toast } from "sonner";
import { Loader2, FileDown, FileSpreadsheet, FileText, FileType } from "lucide-react";

const JENIS = [
  { key: "kasus", label: "Daftar Tindak Lanjut & Sasaran Bermasalah" },
  { key: "kunjungan", label: "Rekap Kunjungan Kader" },
  { key: "keluarga", label: "Daftar Keluarga Terdaftar" },
];

export default function Laporan() {
  const [rekap, setRekap] = useState(null);
  useEffect(() => { api.get("/rekap").then((r) => setRekap(r.data)); }, []);

  const download = async (jenis, fmt) => {
    try {
      const res = await api.get(`/export/${jenis}`, { params: { fmt }, responseType: "blob" });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url; a.download = `laporan_${jenis}.${fmt === "excel" ? "xlsx" : fmt}`; a.click();
      URL.revokeObjectURL(url);
      toast.success(`Laporan ${fmt.toUpperCase()} diunduh`);
    } catch (e) { toast.error("Gagal mengunduh laporan"); }
  };

  return (
    <div className="animate-slide-up space-y-5">
      {/* Rekap otomatis */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5">
        <p className="mb-4 text-sm font-bold text-slate-800">Rekapitulasi Otomatis (Bulan Berjalan)</p>
        {!rekap ? <Loader2 className="h-6 w-6 animate-spin text-teal-600" /> : (
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            {[["Keluarga Dikunjungi", rekap.keluarga_dikunjungi], ["Sasaran Bermasalah", rekap.sasaran_bermasalah], ["Tanda Bahaya", rekap.tanda_bahaya], ["Edukasi Diberikan", rekap.edukasi], ["Dilaporkan ke Nakes", rekap.dilaporkan], ["Kasus Selesai", rekap.kasus_selesai], ["Kasus Belum Selesai", rekap.kasus_belum_selesai]].map(([l, v]) => (
              <div key={l} className="rounded-xl bg-slate-50 p-3"><p className="text-xl font-extrabold text-slate-900">{v}</p><p className="text-xs text-slate-500">{l}</p></div>
            ))}
          </div>
        )}
        {rekap && (
          <div className="mt-4">
            <p className="mb-2 text-xs font-semibold text-slate-500">Sasaran dikunjungi per kelompok</p>
            <div className="flex flex-wrap gap-2">{rekap.per_kelompok.map((p) => <span key={p.kelompok} className="rounded-full bg-teal-50 px-3 py-1 text-xs font-medium text-teal-700">{p.kelompok}: {p.jumlah}</span>)}</div>
          </div>
        )}
      </div>

      {/* Export */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5">
        <p className="mb-4 flex items-center gap-2 text-sm font-bold text-slate-800"><FileDown className="h-5 w-5 text-teal-600" /> Ekspor Laporan</p>
        <div className="space-y-3">
          {JENIS.map((j) => (
            <div key={j.key} className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-slate-100 bg-slate-50 p-3">
              <span className="text-sm font-medium text-slate-700">{j.label}</span>
              <div className="flex gap-2">
                <button data-testid={`export-${j.key}-csv`} onClick={() => download(j.key, "csv")} className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-teal-400"><FileText className="h-4 w-4" /> CSV</button>
                <button data-testid={`export-${j.key}-excel`} onClick={() => download(j.key, "excel")} className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-teal-400"><FileSpreadsheet className="h-4 w-4" /> Excel</button>
                <button data-testid={`export-${j.key}-pdf`} onClick={() => download(j.key, "pdf")} className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-teal-400"><FileType className="h-4 w-4" /> PDF</button>
              </div>
            </div>
          ))}
        </div>
        <p className="mt-3 text-xs text-slate-400">Laporan mencantumkan tanggal cetak & nama pengguna yang mencetak.</p>
      </div>
    </div>
  );
}
