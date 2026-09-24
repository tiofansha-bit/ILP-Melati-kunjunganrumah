# Prompt Import — PWS ILP Melati (deploy final)

Salin-tempel prompt di bawah untuk meng-import & menjalankan aplikasi PERSIS seperti deploy final saat ini (termasuk data asli).

---

```
Import & jalankan ulang aplikasi PWS ILP Melati (kunjungan rumah) PERSIS seperti deploy final saat ini.

## Sumber
- Repo GitHub: https://github.com/tiofansha-bit/ILP-Melati-kunjunganrumah.git
- Branch: gunakan branch yang berisi versi final (fitur "Impor Keluarga -> tujukan ke kader" + folder backend/snapshot/).
- Safety gate: scan seluruh tree untuk conflict marker (<<<<<<<, =======, >>>>>>>). Kalau bersih -> lanjut. Kalau kotor -> fallback ke main dan laporkan file yang konflik.

## Environment (platform Emergent)
- Backend FastAPI di 0.0.0.0:8001 via supervisor (BUKAN :8000). Semua route prefix /api.
- Frontend React pakai REACT_APP_BACKEND_URL eksternal (jangan localhost:8000/:3000).
- MongoDB lokal.

## File .env
- backend/.env:
  MONGO_URL="mongodb://localhost:27017"
  DB_NAME="ilp_melati"
  CORS_ORIGINS="*"
  JWT_SECRET="ilp-melati-local-dev-secret-change-me"   # WAJIB, kode crash tanpa ini
  ADMIN_EMAIL="tiofansha@gmail.com"
  ADMIN_PASSWORD="admin123"
  FRONTEND_URL="<origin REACT_APP_BACKEND_URL environment ini>"
- frontend/.env: JANGAN ubah REACT_APP_BACKEND_URL bawaan environment.

## Dependencies
- Backend: pip install -r backend/requirements.txt. Pastikan openpyxl (import/export Excel) dan fpdf2 (export PDF) terpasang. Buang/skip pin emergentintegrations kalau bikin konflik litellm (tidak dipakai kode).
- Frontend: yarn install (bukan npm).

## Data — RESTORE DARI SNAPSHOT (data asli, ikut di repo)
Jalankan:
  python backend/snapshot_data.py restore
Ini menghapus koleksi lalu mengimpor data asli dari backend/snapshot/*.json
(31 user, 56 keluarga, 197 anggota, 66 kunjungan, 496 kasus, 135 master pertanyaan, 4 kelurahan, 6 posyandu, 1 akreditasi).
Tidak perlu akses ke situs lama (melati-health-app.emergent.host) lagi.
(Alternatif data demo: biarkan seed_demo.py jalan otomatis saat backend start.)

## Jalankan & verifikasi
- Start via supervisor (restart backend & frontend). JANGAN uvicorn manual / npm.
- Smoke test login: admin/admin123 dan kader1..kader30 / kader123
  (catatan: akun kader1=tio mungkin nonaktif; pakai kader aktif mis. kader11).
- Verifikasi dashboard admin tampil (KPI + menu: Dashboard, Daftar Prioritas, Keluarga & Sasaran,
  Laporan & Rekap, Mode, Manajemen Kader, Rekap per Kader, Import Data, Master Pertanyaan, Audit Log).
- Verifikasi fitur: buka Import Data > Impor Keluarga, pilih "Tujukan ke Kader", unggah 1 file ->
  login sebagai kader itu -> keluarga muncul di daftarnya.

## Aturan
- Conflict branch kotor -> auto-fallback ke main + laporkan file.
- Port 8000/3000 bentrok / tidak sesuai environment -> sesuaikan otomatis.
- Kredensial simpan/update di memory/test_credentials.md.
```

---

## Catatan
- Update snapshot bila data berubah: `python backend/snapshot_data.py dump` lalu push ulang.
- `backend/snapshot/users.json` berisi bcrypt hash password default (admin123/kader123). Ganti password setelah dipakai sungguhan karena repo public.
