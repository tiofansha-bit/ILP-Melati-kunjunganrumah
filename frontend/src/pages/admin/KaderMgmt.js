import { useEffect, useState } from "react";
import { api, errMsg } from "@/lib/api";
import { toast } from "sonner";
import { Loader2, Plus, UserCog, X } from "lucide-react";

const KELURAHAN = ["Selat Tengah", "Selat Hulu", "Selat Dalam", "Selat Utara"];

export default function KaderMgmt() {
  const [rows, setRows] = useState(null);
  const [modal, setModal] = useState(null);
  const load = () => api.get("/admin/kader").then((r) => setRows(r.data));
  useEffect(() => { load(); }, []);

  return (
    <div className="animate-slide-up space-y-4">
      <button data-testid="add-kader-btn" onClick={() => setModal({ wilayah: [KELURAHAN[0]], target_keluarga: 30, aktif: true })} className="flex items-center gap-2 rounded-xl bg-teal-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-teal-700"><Plus className="h-4 w-4" /> Tambah Kader</button>
      {!rows ? <div className="flex h-40 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-teal-600" /></div> : (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold text-slate-500"><tr>{["Nama", "Username", "Wilayah", "Posyandu", "Target", "Status", ""].map((h) => <th key={h} className="px-4 py-3">{h}</th>)}</tr></thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((k) => (
                <tr key={k.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-700">{k.nama}</td>
                  <td className="px-4 py-3 text-slate-500">{k.username}</td>
                  <td className="px-4 py-3 text-slate-500">{(k.wilayah || []).join(", ")}</td>
                  <td className="px-4 py-3 text-slate-500">{k.posyandu}</td>
                  <td className="px-4 py-3 text-slate-500">{k.target_keluarga}</td>
                  <td className="px-4 py-3">{k.aktif ? <span className="rounded-lg bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-700">Aktif</span> : <span className="rounded-lg bg-rose-100 px-2 py-1 text-xs font-semibold text-rose-700">Nonaktif</span>}</td>
                  <td className="px-4 py-3"><button data-testid={`edit-kader-${k.id}`} onClick={() => setModal(k)} className="text-sm font-semibold text-teal-600">Edit</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {modal && <KaderModal k={modal} onClose={() => setModal(null)} onSaved={() => { setModal(null); load(); }} />}
    </div>
  );
}

function KaderModal({ k, onClose, onSaved }) {
  const [f, setF] = useState({ nama: k.nama || "", username: k.username || "", password: "", posyandu: k.posyandu || "", wilayah: k.wilayah || [KELURAHAN[0]], target_keluarga: k.target_keluarga || 30, aktif: k.aktif ?? true });
  const [saving, setSaving] = useState(false);
  const save = async () => {
    if (!f.nama || (!k.id && !f.username)) return toast.error("Nama & username wajib");
    setSaving(true);
    try { k.id ? await api.put(`/admin/kader/${k.id}`, f) : await api.post("/admin/kader", f); toast.success("Kader tersimpan"); onSaved(); }
    catch (e) { toast.error(errMsg(e)); } finally { setSaving(false); }
  };
  const cls = "w-full rounded-lg border border-slate-200 px-3 py-2 text-sm";
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div className="w-full max-w-md rounded-2xl bg-white p-5" onClick={(e) => e.stopPropagation()}>
        <div className="mb-3 flex items-center justify-between"><h3 className="text-lg font-bold text-slate-900 flex items-center gap-2"><UserCog className="h-5 w-5 text-teal-600" />{k.id ? "Edit" : "Tambah"} Kader</h3><button onClick={onClose}><X className="h-5 w-5 text-slate-400" /></button></div>
        <div className="space-y-3">
          <div><label className="mb-1 block text-xs font-semibold text-slate-500">Nama</label><input className={cls} value={f.nama} onChange={(e) => setF({ ...f, nama: e.target.value })} /></div>
          {!k.id && <div><label className="mb-1 block text-xs font-semibold text-slate-500">Username</label><input data-testid="kader-username" className={cls} value={f.username} onChange={(e) => setF({ ...f, username: e.target.value })} /></div>}
          <div><label className="mb-1 block text-xs font-semibold text-slate-500">Kata Sandi {k.id && "(kosongkan jika tidak diubah)"}</label><input className={cls} value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} placeholder={k.id ? "••••" : "kader123"} /></div>
          <div className="grid grid-cols-2 gap-3">
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Wilayah</label><select className={cls} value={f.wilayah[0]} onChange={(e) => setF({ ...f, wilayah: [e.target.value] })}>{KELURAHAN.map((w) => <option key={w}>{w}</option>)}</select></div>
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Posyandu</label><input className={cls} value={f.posyandu} onChange={(e) => setF({ ...f, posyandu: e.target.value })} /></div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Target KK</label><input type="number" className={cls} value={f.target_keluarga} onChange={(e) => setF({ ...f, target_keluarga: Number(e.target.value) })} /></div>
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Status</label><select className={cls} value={f.aktif ? "1" : "0"} onChange={(e) => setF({ ...f, aktif: e.target.value === "1" })}><option value="1">Aktif</option><option value="0">Nonaktif</option></select></div>
          </div>
        </div>
        <button data-testid="save-kader" onClick={save} disabled={saving} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 py-2.5 font-semibold text-white disabled:opacity-60">{saving ? <Loader2 className="h-5 w-5 animate-spin" /> : "Simpan"}</button>
      </div>
    </div>
  );
}
