# PRD — PWS ILP MELATI

## Problem Statement
Aplikasi digitalisasi ceklis kunjungan rumah oleh kader di wilayah kerja UPT Puskesmas Melati. Dua peran: **Kader** (mobile PWA — data keluarga, wizard kunjungan, ceklis dinamis, tanda bahaya, edukasi, lapor tindak lanjut) dan **Admin/Petugas** (desktop dashboard — pantau cakupan, daftar prioritas, pusat tindak lanjut, notifikasi, rekap otomatis, ekspor laporan, manajemen master, Dashboard Akreditasi simulasi).

## User Choices
- Login sederhana username/password (JWT self-built, token via Bearer/localStorage).
- Fokus MVP: alur Kader + Dashboard/Tindak Lanjut Admin.
- Ceklis & definisi operasional diambil dari Excel "Kartu Ceklis Kunjungan Rumah.xlsx" (120 master questions, 8 kelompok sasaran).
- PWA dasar + simpan draf otomatis (offline penuh menyusul).
- Ekspor laporan (CSV/Excel/PDF) di MVP pertama.

## Architecture
- **Backend**: FastAPI + MongoDB (motor). All routes `/api`. JWT auth (bcrypt). Rule engine `evaluate_answers` → temuan (merah/kuning) driven by admin-editable `master_questions` collection. `create_cases` + notifikasi. Aggregations for dashboard/kpi, charts, rekap. Export CSV/Excel(openpyxl)/PDF(fpdf2). Audit log. Akreditasi CRUD + version history.
- **Frontend**: React (CRA/craco). AuthContext (localStorage `pws_token`). Kader = mobile-first `max-w-md` bottom-nav; Admin = desktop sidebar. Recharts, lucide-react, shadcn/ui, sonner. Design per `/app/design_guidelines.json` (teal/emerald health palette, status colors hijau/kuning/merah/biru with icon+text).

## Core Entities (MongoDB)
users(role kader/admin, wilayah), wilayah, posyandu, master_questions, keluarga, anggota (auto kelompok sasaran by umur+kondisi), kunjungan (per_anggota answers+temuan), kasus (tindak lanjut, 10 status + riwayat audit trail), notifikasi, akreditasi (simulasi + versions), audit_logs.

## Personas
1. Kader kesehatan (kemampuan digital beragam, ponsel Android).
2. Petugas/Admin Puskesmas/Pustu (desktop/tablet).

## Implemented (2026-06)
- Auth username/password + role & region scoping (403 isolation verified).
- Kader: Beranda KPI, daftar/tambah keluarga + anggota (auto kelompok sasaran, NIK 16-digit validation non-blocking untuk draf, deteksi duplikat), Wizard 8-langkah dgn progress bar, ceklis dinamis per kelompok, kartu Ya/Tidak, danger grid, "Apa maksudnya?" definisi operasional, autosave draf (localStorage), ringkasan, edukasi, konfirmasi tanda bahaya wajib sebelum kirim, Tugas/status laporan, Profil.
- Admin: Dashboard KPI + charts + filter, Daftar Prioritas (filter/sort, detail kasus, ubah status, PJ, hasil, alasan wajib utk "tidak dapat ditindaklanjuti"), Keluarga & Sasaran, Laporan (rekap otomatis + ekspor CSV/Excel/PDF), Dashboard Akreditasi (kartu/grafik/narasi/PDCA/RTL editable, versi, mode presentasi, banner SIMULASI), Manajemen Kader, Master Pertanyaan (edit definisi/priority/problem_when), Notifikasi, Audit Log.
- Seed demo data fiktif: 4 kelurahan, 6 posyandu, 10 kader, 34 keluarga, kunjungan hijau/kuning/merah, kasus belum & sudah ditindaklanjuti, 1 dashboard akreditasi dgn data dummy.
- Testing: backend 35/35 (setelah fix PDF), frontend 100% flow.

## Backlog (P1/P2)
- P1: Offline penuh (IndexedDB + antrean sinkronisasi + konflik), peta sebaran RT/RW, foto lampiran + persetujuan, export PowerPoint akreditasi, drag-and-drop dashboard builder.
- P1: Modul detail per kunjungan (K1-K6 tanggal/tempat/petugas, imunisasi granular) — saat ini ringkas ke pertanyaan kunci + danger signs.
- P2: Notifikasi push, penggabungan data duplikat, pemindahan anggota antar keluarga, masa simpan data & soft-delete UI, shadcn DatePicker di filter dashboard.
- P2: Import master pertanyaan penuh dari seluruh sheet Excel (grid K1-K6 dsb).

## Test Credentials
admin/admin123 · kader1..kader10/kader123 (lihat /app/memory/test_credentials.md)
