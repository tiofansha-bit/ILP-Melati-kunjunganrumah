# PRD — PWS ILP MELATI (Kunjungan Rumah)

## Problem Statement
Aplikasi digitalisasi ceklis kunjungan rumah oleh kader di wilayah kerja UPT Puskesmas Melati. Dua peran: **Kader** (mobile PWA — data keluarga, wizard kunjungan, ceklis dinamis, tanda bahaya, edukasi, lapor tindak lanjut) dan **Admin/Petugas** (desktop dashboard — pantau cakupan, daftar prioritas, tindak lanjut, notifikasi, rekap, ekspor laporan, manajemen master).

Task saat ini: **Import repo dari GitHub** (`tiofansha-bit/ILP-Melati-kunjunganrumah`), install dependency, jalankan di environment Emergent as-is.

## Architecture
- **Backend**: FastAPI + MongoDB (motor). Semua route `/api`. JWT auth (bcrypt). Seed idempotent di startup (`seed_demo.seed_all`). Export CSV/Excel(openpyxl)/PDF(fpdf2). Audit log. Akreditasi CRUD + version history.
- **Frontend**: React (CRA/craco). AuthContext (localStorage `pws_token`). Kader = mobile-first bottom-nav; Admin = desktop sidebar. Recharts, lucide-react, shadcn/ui, sonner.
- **Env (Emergent)**: backend `MONGO_URL`, `DB_NAME=ilp_melati`, `CORS_ORIGINS`, `JWT_SECRET`. Frontend `REACT_APP_BACKEND_URL`. Backend :8001, frontend :3000 via supervisor.

## Personas
1. Kader kesehatan (ponsel Android, kemampuan digital beragam).
2. Petugas/Admin Puskesmas/Pustu (desktop/tablet).

## Implemented (2026-06)
- **Import & setup selesai**: repo di-clone ke /app, dependency backend (fpdf2, openpyxl, dll) & frontend (yarn) terpasang, `.env` dibuat sesuai konvensi Emergent, `JWT_SECRET` ditambahkan.
- Seed demo berjalan (idempotent di startup): 11 users, 4 kelurahan, 6 posyandu, 135 master questions, 34 keluarga, 118 anggota, 26 kunjungan, 104 kasus, 32 notifikasi, 1 dashboard akreditasi.
- Login terverifikasi: `admin/admin123`, `kader1/kader123`.
- **UI changes**: menu "Mode" (Akreditasi) disembunyikan dari sidebar admin; teks "Data demonstrasi bersifat fiktif" dihapus dari login.
- **Ganti Kata Sandi (baru, 2026-06)**: endpoint `POST /api/auth/change-password` (verifikasi kata sandi lama via bcrypt, min 6 karakter). Modal bersama `ChangePassword.js` di halaman Profil kader (tombol `change-password-btn`) dan header admin (tombol `admin-change-password-btn`). Diverifikasi testing agent 100% (wrong current→error, valid→sukses & re-login OK, kedua role).
- **Ekspor Laporan**: `/export/{jenis}` (kasus/kunjungan/keluarga) format CSV/Excel(openpyxl)/PDF(fpdf2) — 9 kombinasi terverifikasi 200 + content-type benar; tombol di menu Laporan berfungsi (download).
- **Mode Offline Kader**: `offline.js` (antrean sinkron + cache localStorage) + `SyncBar.js` (auto-flush tiap 15s & saat kembali online). Wizard memakai `submitKunjungan`/cache untuk keluarga, detail, & pertanyaan → kader bisa mengisi tanpa sinyal, terkirim otomatis saat online.
- **Ekspor Terfilter (baru)**: `/export/{jenis}` menerima `start`, `end`, `kelurahan`; UI menu Laporan punya filter tanggal + kelurahan + chip filter aktif. Terverifikasi (filter kelurahan hanya baris cocok, rentang tanggal future=0).
- **Reset Sandi Kader (baru)**: `POST /api/admin/kader/{uid}/reset-password` (default kader123, min 6 char) + tombol "Reset Sandi" per baris di Manajemen Kader. Terverifikasi (reset→login baru OK→restore). 

## Belum Dikerjakan
- **Sesuaikan ceklis dengan file kartu ceklis Excel**: DITUNDA — file Excel belum diunggah user. Perlu file `Kartu Ceklis Kunjungan Rumah.xlsx` untuk menyesuaikan `master_questions`.

## Backlog (P1/P2)
- P1: Offline penuh (IndexedDB + antrean sinkronisasi), peta sebaran RT/RW, foto lampiran.
- P2: Notifikasi push, import master pertanyaan penuh dari Excel, silence Recharts ResponsiveContainer warning (non-blocking).

## Test Credentials
admin/admin123 · kader1..kader10/kader123 (lihat /app/memory/test_credentials.md)
