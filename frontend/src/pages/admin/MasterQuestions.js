import { useEffect, useState } from "react";
import { api, errMsg } from "@/lib/api";
import { toast } from "sonner";
import { Loader2, ListChecks, Edit2, X, ShieldAlert, Eye } from "lucide-react";

const GROUPS = [
  ["ibu_hamil", "Ibu Hamil"], ["nifas", "Ibu Nifas"], ["bayi", "Bayi 0-6 bln"], ["balita", "Balita & Apras"],
  ["remaja", "Usia Sekolah & Remaja"], ["dewasa", "Usia Dewasa"], ["lansia", "Lansia"], ["tbc", "Skrining TBC"],
];

export default function MasterQuestions() {
  const [group, setGroup] = useState("ibu_hamil");
  const [rows, setRows] = useState(null);
  const [edit, setEdit] = useState(null);
  const load = () => { setRows(null); api.get("/master/questions", { params: { group } }).then((r) => setRows(r.data)); };
  useEffect(load, [group]); // eslint-disable-line

  return (
    <div className="animate-slide-up space-y-4">
      <div className="rounded-2xl border border-sky-200 bg-sky-50 p-3 text-sm text-sky-800">Master pertanyaan & definisi operasional dapat dikelola tanpa mengubah kode. Ubah teks, definisi, jawaban bermasalah, dan prioritas.</div>
      <div className="flex flex-wrap gap-2">
        {GROUPS.map(([k, l]) => <button key={k} data-testid={`mq-group-${k}`} onClick={() => setGroup(k)} className={`rounded-full px-3.5 py-1.5 text-sm font-medium ${group === k ? "bg-teal-600 text-white" : "border border-slate-200 bg-white text-slate-600"}`}>{l}</button>)}
      </div>
      {!rows ? <div className="flex h-40 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-teal-600" /></div> : (
        <div className="space-y-2">
          {rows.map((q) => (
            <div key={q.kode} className="flex items-start gap-3 rounded-xl border border-slate-200 bg-white p-3.5">
              <div className={`mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-lg ${q.section === "tanda_bahaya" ? "bg-rose-50 text-rose-600" : "bg-slate-100 text-slate-500"}`}>{q.section === "tanda_bahaya" ? <ShieldAlert className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-slate-800">{q.text}</p>
                <p className="text-xs text-slate-400">{q.kode} · {q.jenis}{q.satuan ? ` (${q.satuan})` : ""} {q.priority && <span className={`ml-1 rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${q.priority === "merah" ? "bg-rose-100 text-rose-700" : "bg-amber-100 text-amber-700"}`}>{q.priority}</span>}</p>
                {q.definisi && <p className="mt-1 line-clamp-2 text-xs text-slate-500">{q.definisi}</p>}
              </div>
              <button data-testid={`mq-edit-${q.kode}`} onClick={() => setEdit(q)} className="shrink-0 rounded-lg border border-slate-200 p-1.5 text-slate-500 hover:text-teal-600"><Edit2 className="h-4 w-4" /></button>
            </div>
          ))}
        </div>
      )}
      {edit && <EditModal q={edit} onClose={() => setEdit(null)} onSaved={() => { setEdit(null); load(); }} />}
    </div>
  );
}

function EditModal({ q, onClose, onSaved }) {
  const [f, setF] = useState({ text: q.text, definisi: q.definisi || "", priority: q.priority || "", wajib: q.wajib, problem_when: (q.problem_when || []).join(", ") });
  const [saving, setSaving] = useState(false);
  const save = async () => {
    setSaving(true);
    try { await api.put(`/master/questions/${q.kode}`, { text: f.text, definisi: f.definisi, priority: f.priority || null, wajib: f.wajib, problem_when: f.problem_when.split(",").map((s) => s.trim()).filter(Boolean) }); toast.success("Pertanyaan diperbarui"); onSaved(); }
    catch (e) { toast.error(errMsg(e)); } finally { setSaving(false); }
  };
  const cls = "w-full rounded-lg border border-slate-200 px-3 py-2 text-sm";
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div className="w-full max-w-md rounded-2xl bg-white p-5" onClick={(e) => e.stopPropagation()}>
        <div className="mb-3 flex items-center justify-between"><h3 className="flex items-center gap-2 text-lg font-bold text-slate-900"><ListChecks className="h-5 w-5 text-teal-600" /> Edit Pertanyaan</h3><button onClick={onClose}><X className="h-5 w-5 text-slate-400" /></button></div>
        <div className="space-y-3">
          <div><label className="mb-1 block text-xs font-semibold text-slate-500">Teks Pertanyaan</label><input className={cls} value={f.text} onChange={(e) => setF({ ...f, text: e.target.value })} /></div>
          <div><label className="mb-1 block text-xs font-semibold text-slate-500">Definisi Operasional</label><textarea rows={3} className={cls} value={f.definisi} onChange={(e) => setF({ ...f, definisi: e.target.value })} /></div>
          <div className="grid grid-cols-2 gap-3">
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Prioritas jika bermasalah</label><select className={cls} value={f.priority} onChange={(e) => setF({ ...f, priority: e.target.value })}><option value="">- tidak ada -</option><option value="kuning">Kuning</option><option value="merah">Merah</option></select></div>
            <div><label className="mb-1 block text-xs font-semibold text-slate-500">Wajib?</label><select className={cls} value={f.wajib ? "1" : "0"} onChange={(e) => setF({ ...f, wajib: e.target.value === "1" })}><option value="1">Wajib</option><option value="0">Opsional</option></select></div>
          </div>
          <div><label className="mb-1 block text-xs font-semibold text-slate-500">Jawaban penanda masalah (pisah koma)</label><input className={cls} value={f.problem_when} onChange={(e) => setF({ ...f, problem_when: e.target.value })} placeholder="Tidak, Ya" /></div>
        </div>
        <button data-testid="mq-save" onClick={save} disabled={saving} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 py-2.5 font-semibold text-white disabled:opacity-60">{saving ? <Loader2 className="h-5 w-5 animate-spin" /> : "Simpan"}</button>
      </div>
    </div>
  );
}
