"""Generate master_questions.json seed from parsed operational definitions.
Combines checklist coverage questions (yellow when negative) and danger signs
(red when present) per target group. Run once to (re)build the seed file."""
import json, os

BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, 'definitions.json'), encoding='utf-8') as f:
    DEFS = json.load(f)


def find_def(group, *keywords):
    for d in DEFS.get(group, []):
        t = d['title'].lower()
        if all(k.lower() in t for k in keywords):
            return d['definisi']
    return 'Jelas'


# section: data_awal | ceklis | tanda_bahaya
# jenis: yesno | single | multi | number | date | text
# problem_when: value(s) that flag a problem -> priority
GROUPS = {
    'ibu_hamil': {
        'label': 'Ibu Hamil', 'icon': 'HeartHandshake',
        'ceklis': [
            ('BUMIL_SUHU', 'Suhu tubuh ibu', 'number', '°C', None, None, False),
            ('BUMIL_KIA', 'Apakah ibu memiliki Buku KIA?', 'single', None,
             ['Ya, dapat ditunjukkan', 'Ada, tidak dapat ditunjukkan', 'Tidak memiliki', 'Tidak tahu'],
             ['Tidak memiliki', 'Tidak tahu'], 'kuning'),
            ('BUMIL_ANC', 'Apakah ibu sudah memeriksakan kehamilan (K1-K6) sesuai usia kehamilan?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BUMIL_PIRINGKU', 'Apakah ibu makan sesuai Isi Piringku Ibu Hamil?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BUMIL_TTD_ADA', 'Apakah ibu memiliki Tablet Tambah Darah (TTD)?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BUMIL_TTD_MINUM', 'Apakah ibu minum TTD dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BUMIL_LILA', 'Hasil pengukuran LiLA', 'number', 'cm', None, None, None),
            ('BUMIL_LILA_KEK', 'Apakah LiLA kurang dari 23,5 cm?', 'yesno', None, None, 'Ya', 'kuning'),
            ('BUMIL_KELAS', 'Apakah ibu mengikuti Kelas Ibu Hamil?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BUMIL_JIWA', 'Apakah ibu sudah menjalani skrining kesehatan jiwa?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [
            'Demam lebih dari dua hari', 'Pusing/sakit kepala berat', 'Sulit tidur/cemas berlebih',
            'Diare Berulang', 'Resiko TBC', 'Tidak ada gerakan janin',
            'Jantung berdebar-debar atau nyeri di dada', 'Keluar cairan dari jalan lahir',
            'Sakit saat kencing', 'Nyeri perut hebat',
        ],
    },
    'nifas': {
        'label': 'Ibu Bersalin & Nifas', 'icon': 'Baby',
        'ceklis': [
            ('NIFAS_SUHU', 'Suhu tubuh ibu', 'number', '°C', None, None, None),
            ('NIFAS_KIA', 'Apakah ibu memiliki Buku KIA?', 'single', None,
             ['Ya, dapat ditunjukkan', 'Ada, tidak dapat ditunjukkan', 'Tidak memiliki'], ['Tidak memiliki'], 'kuning'),
            ('NIFAS_KF', 'Apakah kunjungan nifas (KF1-KF4) sudah sesuai jadwal?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('NIFAS_VITA', 'Apakah ibu sudah minum kapsul Vitamin A nifas?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('NIFAS_ASI', 'Apakah ibu memberikan ASI kepada bayi?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('NIFAS_KB', 'Apakah ibu menggunakan KB pascapersalinan?', 'yesno', None, None, None, None),
            ('NIFAS_JIWA', 'Apakah ibu sudah menjalani skrining kesehatan jiwa?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [
            'Demam', 'Ada perasaan bersalah, mudah menangis, kehilangan minat, gelisah, gangguan tidur, gangguan konsentrasi',
            'Tidak bisa BAK, BAK sedikit tapi sering, terasa panas, nyeri panggul, urin keluar tanpa disadari',
            'Nafas pendek dan terengah-engah, nafas dangkal disertai nyeri dada, nafas berat, batuk lebih dari 2 minggu',
            'Sakit kepala', 'Perdarahan (pembalut basah dalam 5 menit)',
            'Area sekitar kelamin bengkak atau nyeri atau ada luka terbuka', 'Keluar cairan  dari jalan lahir',
            'Nyeri ulu hati', 'Pandangan kabur',
            'Payudara bengkak kemerahan disertai nyeri, benjolan disertai nyeri ada keluhan dalam menyusui',
            'Darah nifas berbau atau mengalir atau ada nyeri pada perut bawah',
            'Keputihan berlebih, berwarna dan berbau', 'Jantung berdebar',
        ],
    },
    'bayi': {
        'label': 'Bayi 0-6 Bulan', 'icon': 'Smile',
        'ceklis': [
            ('BAYI_SUHU', 'Suhu tubuh bayi', 'number', '°C', None, None, None),
            ('BAYI_KIA', 'Apakah ada Buku KIA bayi?', 'single', None,
             ['Ya, dapat ditunjukkan', 'Ada, tidak dapat ditunjukkan', 'Tidak memiliki'], ['Tidak memiliki'], 'kuning'),
            ('BAYI_ASI', 'Apakah bayi mendapat ASI Eksklusif?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BAYI_BB', 'Berat badan bayi', 'number', 'kg', None, None, None),
            ('BAYI_PB', 'Panjang badan bayi', 'number', 'cm', None, None, None),
            ('BAYI_LK', 'Lingkar kepala bayi', 'number', 'cm', None, None, None),
            ('BAYI_KN', 'Apakah kunjungan neonatal (KN1-KN3) sudah lengkap sesuai umur?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BAYI_IMUN', 'Apakah imunisasi bayi sudah lengkap sesuai umur?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [
            'Napas: sesak/napas cepat/dada tertarik ke dalam',
            'Aktivitas: tampak lemah/tidak bergerak/menangis atau merintih',
            'Warna kulit: biru/pucat/seperti marmer/memar',
            'Hisapan: tidak mau/lemah menghisap, muntah susu/hijau',
            'Kejang', 'Suhu tubuh terlalu tinggi atau terlalu rendah',
            'BAB tidak normal / belum BAB >48 jam', 'Tidak kencing 6 jam / warna urine tidak normal',
            'Tali pusat merah/bernanah/berbau', 'Mata merah atau bernanah',
            'Kelainan kulit', 'Belum mendapat imunisasi awal (HB0/BCG)',
        ],
    },
    'balita': {
        'label': 'Balita & Anak Prasekolah', 'icon': 'Activity',
        'ceklis': [
            ('BALITA_SUHU', 'Suhu tubuh anak', 'number', '°C', None, None, None),
            ('BALITA_KIA', 'Apakah ada Buku KIA anak?', 'single', None,
             ['Ya, dapat ditunjukkan', 'Ada, tidak dapat ditunjukkan', 'Tidak memiliki'], ['Tidak memiliki'], 'kuning'),
            ('BALITA_BB', 'Berat badan anak', 'number', 'kg', None, None, None),
            ('BALITA_TB', 'Tinggi/panjang badan anak', 'number', 'cm', None, None, None),
            ('BALITA_LK', 'Lingkar kepala anak', 'number', 'cm', None, None, None),
            ('BALITA_IMUN', 'Apakah imunisasi anak sudah lengkap sesuai umur?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BALITA_CACING', 'Apakah anak sudah mendapat obat cacing (usia >1 th)?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BALITA_VITA', 'Apakah anak sudah mendapat kapsul Vitamin A?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('BALITA_GIZI', 'Apakah pemberian makan anak sudah beragam (protein hewani, nabati, sayur, buah)?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [
            'Napas: sesak/napas cepat/dada tertarik ke dalam', 'Batuk dengan bunyi napas tidak normal',
            'Demam dengan kejang atau tanda perdarahan', 'Diare dengan mata cekung/haus terus/darah',
            'Air kencing sedikit atau warna tidak normal', 'Warna kulit biru/pucat/marmer/memar',
            'Aktivitas: lemah atau tidak bergerak', 'Tidak mau makan atau minum',
            'Berat badan tidak naik sesuai pertumbuhan',
        ],
    },
    'remaja': {
        'label': 'Usia Sekolah & Remaja', 'icon': 'UserCheck',
        'ceklis': [
            ('REMAJA_SUHU', 'Suhu tubuh', 'number', '°C', None, None, None),
            ('REMAJA_BB', 'Berat badan', 'number', 'kg', None, None, None),
            ('REMAJA_TB', 'Tinggi badan', 'number', 'cm', None, None, None),
            ('REMAJA_PIRINGKU', 'Apakah makan sesuai Isi Piringku?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('REMAJA_ROKOK', 'Perilaku merokok', 'single', None, ['Tidak', 'Pasif', 'Aktif'], ['Aktif'], 'kuning'),
            ('REMAJA_JIWA', 'Apakah sudah menjalani skrining kesehatan jiwa?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('REMAJA_TTD', 'Khusus remaja putri: apakah minum TTD dalam 1 minggu terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('REMAJA_ANEMIA', 'Khusus remaja putri: apakah sudah periksa anemia (Hb) 1 tahun terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('REMAJA_TD', 'Khusus usia ≥15 th: apakah periksa tekanan darah 1 tahun terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('REMAJA_GD', 'Khusus usia ≥15 th: apakah periksa gula darah 1 tahun terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [],
    },
    'dewasa': {
        'label': 'Usia Dewasa', 'icon': 'ShieldCheck',
        'ceklis': [
            ('DEWASA_SUHU', 'Suhu tubuh', 'number', '°C', None, None, None),
            ('DEWASA_PIRINGKU', 'Apakah makan sesuai Isi Piringku?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('DEWASA_TD', 'Apakah periksa tekanan darah 1 tahun terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('DEWASA_HT', 'Apakah terdiagnosis hipertensi?', 'yesno', None, None, None, None),
            ('DEWASA_HT_OBAT_ADA', 'Jika hipertensi: apakah memiliki obat hipertensi?', 'yesno', None, None, None, None),
            ('DEWASA_HT_OBAT_MINUM', 'Jika hipertensi: apakah minum obat dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('DEWASA_GD', 'Apakah periksa gula darah 1 tahun terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('DEWASA_DM', 'Apakah terdiagnosis diabetes melitus?', 'yesno', None, None, None, None),
            ('DEWASA_DM_OBAT_ADA', 'Jika DM: apakah memiliki obat diabetes?', 'yesno', None, None, None, None),
            ('DEWASA_DM_OBAT_MINUM', 'Jika DM: apakah minum obat dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('DEWASA_ROKOK', 'Perilaku merokok', 'single', None, ['Tidak', 'Pasif', 'Aktif'], ['Aktif'], 'kuning'),
            ('DEWASA_JIWA', 'Apakah sudah menjalani skrining kesehatan jiwa?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [],
    },
    'lansia': {
        'label': 'Lansia', 'icon': 'HeartPulse',
        'ceklis': [
            ('LANSIA_SUHU', 'Suhu tubuh', 'number', '°C', None, None, None),
            ('LANSIA_TD', 'Apakah periksa tekanan darah 1 bulan terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_HT', 'Apakah terdiagnosis hipertensi?', 'yesno', None, None, None, None),
            ('LANSIA_HT_OBAT_MINUM', 'Jika hipertensi: apakah minum obat dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_GD', 'Apakah periksa gula darah 1 bulan terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_DM', 'Apakah terdiagnosis diabetes melitus?', 'yesno', None, None, None, None),
            ('LANSIA_DM_OBAT_MINUM', 'Jika DM: apakah minum obat dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_AKS', 'Apakah sudah skrining Aktivitas Kehidupan Sehari-hari (AKS)?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_SKILAS', 'Apakah sudah skrining SKILAS?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('LANSIA_ROKOK', 'Perilaku merokok', 'single', None, ['Tidak', 'Pasif', 'Aktif'], ['Aktif'], 'kuning'),
            ('LANSIA_JIWA', 'Apakah sudah menjalani skrining kesehatan jiwa?', 'yesno', None, None, 'Tidak', 'kuning'),
        ],
        'tanda_bahaya': [],
    },
    'tbc': {
        'label': 'Skrining TBC', 'icon': 'Stethoscope',
        'ceklis': [
            ('TBC_BATUK', 'Batuk terus-menerus', 'yesno', None, None, 'Ya', 'kuning'),
            ('TBC_DEMAM', 'Demam ≥2 minggu atau berulang tanpa sebab jelas', 'yesno', None, None, 'Ya', 'kuning'),
            ('TBC_BB', 'BB tidak naik/turun dalam 2 bulan berturut-turut', 'yesno', None, None, 'Ya', 'kuning'),
            ('TBC_KONTAK', 'Kontak erat dengan pasien TBC', 'yesno', None, None, 'Ya', 'kuning'),
            ('TBC_DIAG', 'Sudah terdiagnosis TBC', 'yesno', None, None, None, None),
            ('TBC_OBAT_ADA', 'Jika pasien TBC: memiliki obat TBC?', 'yesno', None, None, None, None),
            ('TBC_OBAT_MINUM', 'Jika pasien TBC: minum obat dalam 24 jam terakhir?', 'yesno', None, None, 'Tidak', 'kuning'),
            ('TBC_ROKOK', 'Perilaku merokok', 'single', None, ['Tidak', 'Pasif', 'Aktif'], ['Aktif'], 'kuning'),
        ],
        'tanda_bahaya': [],
    },
}


def build():
    questions = []
    for gcode, g in GROUPS.items():
        order = 0
        for q in g['ceklis']:
            code, text, jenis, satuan, opsi, problem_when, priority = q
            order += 1
            questions.append({
                'kode': code, 'group': gcode, 'section': 'ceklis', 'text': text,
                'definisi': find_def(gcode, text.split('?')[0].split()[0]) if False else _defmatch(gcode, text),
                'jenis': jenis, 'satuan': satuan, 'opsi': opsi or ([] if jenis != 'yesno' else ['Ya', 'Tidak']),
                'wajib': jenis in ('yesno', 'single'),
                'problem_when': problem_when if isinstance(problem_when, list) else ([problem_when] if problem_when else []),
                'priority': priority, 'report_required': False, 'urutan': order,
            })
        for db in g['tanda_bahaya']:
            order += 1
            questions.append({
                'kode': f'{gcode.upper()}_TB_{order}', 'group': gcode, 'section': 'tanda_bahaya',
                'text': db, 'definisi': _defmatch(gcode, db), 'jenis': 'danger',
                'satuan': None, 'opsi': ['Ya', 'Tidak'], 'wajib': True,
                'problem_when': ['Ya'], 'priority': 'merah', 'report_required': True, 'urutan': order,
            })
    return questions


def _defmatch(group, text):
    words = [w for w in text.replace('/', ' ').replace('?', ' ').split() if len(w) > 4][:2]
    for d in DEFS.get(group, []):
        t = d['title'].lower()
        if any(w.lower() in t for w in words) and d['definisi'] not in ('Jelas', ''):
            return d['definisi']
    return text


if __name__ == '__main__':
    qs = build()
    with open(os.path.join(BASE, 'master_questions.json'), 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=1)
    print(f'Built {len(qs)} master questions across {len(GROUPS)} groups')
    from collections import Counter
    print(Counter(q['group'] for q in qs))
