# PRD — PWS ILP Melati (Kunjungan Rumah)

## Original Problem Statement
Import repo `ILP-Melati-kunjunganrumah` (existing full-stack PWA) and get it installed, running, and seeded locally. Two roles: Kader (PWA visit wizard, checklists, offline draft) and Admin/Petugas (KPI dashboard, priority list, follow-up, exports, accreditation, cadre management, audit log).

## Source
- GitHub: https://github.com/tiofansha-bit/ILP-Melati-kunjunganrumah.git
- Branch used: `conflict_210926_1057` (Phase 1 gate: scanned clean — NO conflict markers, so no fallback to `main` needed).

## Architecture (as-is, no rewrite)
- Frontend: React 19 (CRA + craco), Tailwind, shadcn/ui — served on :3000 (supervisor).
- Backend: FastAPI + Motor (async MongoDB), JWT auth, all routes under `/api` — served on 0.0.0.0:8001 (supervisor; external via REACT_APP_BACKEND_URL).
- Database: MongoDB local, DB_NAME=`ilp_melati`.
- Seeding: `backend/seed_demo.py` runs idempotently on startup (count-guards + upsert).

## Env
- backend/.env: MONGO_URL, DB_NAME=ilp_melati, CORS_ORIGINS, JWT_SECRET (required by code), ADMIN_EMAIL, ADMIN_PASSWORD.
- frontend/.env: REACT_APP_BACKEND_URL (platform external URL — replaces localhost:8000 for k8s ingress).

## Dependencies notes
- Removed unused `emergentintegrations==0.2.0` pin (not imported anywhere; conflicted with pre-installed litellm wheel).
- Added `openpyxl` (Excel export) and `fpdf2` (PDF export) — used by server.py but missing from original requirements.

## Personas
- Kader: mobile PWA, records home visits, dynamic per-group checklists, offline draft.
- Admin/Petugas: desktop dashboard, KPI, priority cases, follow-up assignment, exports (CSV/Excel/PDF), accreditation module, cadre management, audit log.

## Implemented / Verified (2026-06)
- Repo imported into /app on clean branch; services running.
- Seed populated: 11 users (1 admin + 10 kader), 4 kelurahan, 6 posyandu, 34 keluarga, 118 anggota, 26 kunjungan, 104 kasus, 135 master questions, 1 akreditasi.
- Verified: admin & kader1 login (JWT), authenticated `/api/dashboard/kpi` returns computed data, `/api/kasus` returns cases, frontend login page renders.

## Test Credentials
- admin / admin123 (role admin), kader1..kader10 / kader123 (role kader). See test_credentials.md.

## Backlog / Not yet exercised
- P1: Full UI flows (8-step kader visit wizard, offline draft, admin follow-up, exports download) not click-tested end-to-end.
- P2: External integrations (email/notification) left as local defaults per user decision.
