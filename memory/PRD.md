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
- Seed demo berjalan: 11 users (admin + 10 kader), 4 kelurahan, 6 posyandu, 135 master questions, 34 keluarga, 118 anggota, 26 kunjungan, 104 kasus, 32 notifikasi, 1 dashboard akreditasi.
- Login terverifikasi: `admin/admin123`, `kader1/kader123`. Dashboard KPI, charts, kader beranda semua mengembalikan data (via live URL).
- **UI changes (permintaan user)**: menu "Mode" (Dashboard Simulasi Akreditasi) disembunyikan dari sidebar admin; teks "Data demonstrasi bersifat fiktif" dihapus dari halaman login. Diverifikasi testing agent (frontend 100%).

## Backlog (P1/P2)
- P1: Offline penuh (IndexedDB + antrean sinkronisasi), peta sebaran RT/RW, foto lampiran.
- P2: Notifikasi push, import master pertanyaan penuh dari Excel, silence Recharts ResponsiveContainer warning (non-blocking).

## Test Credentials
admin/admin123 · kader1..kader10/kader123 (lihat /app/memory/test_credentials.md)
