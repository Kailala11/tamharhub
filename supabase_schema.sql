-- ============================================================
-- TamharHub — Supabase Schema
-- Jalankan seluruh file ini di Supabase SQL Editor
-- Project: SD Taman Harapan 1 Bekasi
-- ============================================================

-- Aktifkan UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── GURU ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS guru (
    id         SERIAL PRIMARY KEY,
    nama       TEXT NOT NULL UNIQUE,
    kelas      TEXT,
    status     TEXT DEFAULT 'Aktif',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── MAPEL GURU ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS mapel_guru (
    id      SERIAL PRIMARY KEY,
    guru_id INTEGER REFERENCES guru(id) ON DELETE CASCADE,
    mapel   TEXT NOT NULL,
    UNIQUE(guru_id, mapel)
);

-- ── SISWA ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS siswa (
    id         SERIAL PRIMARY KEY,
    nama       TEXT NOT NULL,
    kelas      TEXT NOT NULL,
    status     TEXT DEFAULT 'Aktif',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── ABSEN GURU ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS absen_guru (
    id         SERIAL PRIMARY KEY,
    guru_id    INTEGER REFERENCES guru(id),
    tanggal    DATE NOT NULL,
    status     TEXT NOT NULL CHECK(status IN ('H','A','I','S')),
    keterangan TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(guru_id, tanggal)
);

-- ── ABSEN SISWA ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS absen_siswa (
    id         SERIAL PRIMARY KEY,
    siswa_id   INTEGER REFERENCES siswa(id),
    guru_id    INTEGER REFERENCES guru(id),
    tanggal    DATE NOT NULL,
    status     TEXT NOT NULL CHECK(status IN ('H','A','I','S')),
    keterangan TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(siswa_id, tanggal)
);

-- ── JURNAL ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jurnal (
    id         SERIAL PRIMARY KEY,
    guru_id    INTEGER REFERENCES guru(id),
    tanggal    DATE NOT NULL,
    kelas      TEXT NOT NULL,
    mapel      TEXT NOT NULL,
    topik      TEXT NOT NULL,
    aktivitas  TEXT NOT NULL,
    media      TEXT DEFAULT '',
    catatan    TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── NILAI SISWA ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id           SERIAL PRIMARY KEY,
    siswa_id     INTEGER REFERENCES siswa(id),
    guru_id      INTEGER REFERENCES guru(id),
    semester     TEXT NOT NULL,
    tahun_ajar   TEXT NOT NULL,
    mapel        TEXT NOT NULL,
    pengetahuan  NUMERIC(5,2),
    keterampilan NUMERIC(5,2),
    sikap        TEXT DEFAULT 'B',
    updated_at   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(siswa_id, semester, tahun_ajar, mapel)
);

-- ── AGENDA SEKOLAH ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agenda_sekolah (
    id          SERIAL PRIMARY KEY,
    judul       TEXT NOT NULL,
    deskripsi   TEXT DEFAULT '',
    tanggal     DATE NOT NULL,
    tanggal_end DATE,
    kategori    TEXT DEFAULT 'Umum',
    dibuat_oleh TEXT DEFAULT '',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── ROW LEVEL SECURITY (opsional, untuk keamanan tambahan) ───
-- Aktifkan RLS agar data hanya bisa diakses via service key
ALTER TABLE guru          ENABLE ROW LEVEL SECURITY;
ALTER TABLE mapel_guru    ENABLE ROW LEVEL SECURITY;
ALTER TABLE siswa         ENABLE ROW LEVEL SECURITY;
ALTER TABLE absen_guru    ENABLE ROW LEVEL SECURITY;
ALTER TABLE absen_siswa   ENABLE ROW LEVEL SECURITY;
ALTER TABLE jurnal        ENABLE ROW LEVEL SECURITY;
ALTER TABLE nilai_siswa   ENABLE ROW LEVEL SECURITY;
ALTER TABLE agenda_sekolah ENABLE ROW LEVEL SECURITY;

-- Policy: izinkan semua operasi dari service role (aplikasi)
DO $$
DECLARE
    t TEXT;
BEGIN
    FOR t IN SELECT unnest(ARRAY[
        'guru','mapel_guru','siswa','absen_guru',
        'absen_siswa','jurnal','nilai_siswa','agenda_sekolah'
    ]) LOOP
        EXECUTE format('
            CREATE POLICY "service_full_access" ON %I
            FOR ALL USING (true) WITH CHECK (true);', t);
    END LOOP;
END $$;

-- ── SEED DATA GURU ────────────────────────────────────────────
-- (38 guru SD Taman Harapan 1 Bekasi)
INSERT INTO guru (nama, kelas) VALUES
-- Kelas I
('Annisa Rosmiati, S.Pd',       'I Abu Bakar Ash Shidiq'),
('Asnah Garlay, S.Pd',          'I Abu Bakar Ash Shidiq'),
('Rahmawati, S.Pd',             'I Umar bin Khatab'),
('Ainun Fatiyah, S.Pd',         'I Umar bin Khatab'),
('Euis Mulyati, S.Pd',          'I Utsman bin Affan'),
('Syarkiyah, S.Pd',             'I Ali bin Abi Thalib'),
-- Kelas II
('Winda Atmeiti, S.Pd',         'II Abu Bakar Ash Shidiq'),
('Griyana Novita Sari, S.Pd',   'II Abu Bakar Ash Shidiq'),
('Yollanda Mega Putri, S.Pd',   'II Umar bin Khatab'),
('Widyastuti, S.Pd',            'II Umar bin Khatab'),
('Alyuma Oklisia, S.Pd',        'II Utsman bin Affan'),
('Siti Ferda Heriati, S.P',     'II Utsman bin Affan'),
('Rosenah, S.Pd',               'II Ali bin Abi Thalib'),
-- Kelas III
('Usfatun Juliana, S.Pd',       'III Abu Bakar Ash Shidiq'),
('Aa Zamah, S.Pd',              'III Umar bin Khatab'),
('Lenia Nadhroh, S.Pd',         'III Utsman bin Affan'),
('Dra. Wagiati',                'III Ali bin Abi Thalib'),
('Dra. Juniti',                 'III Abdurahman bin Auf'),
-- Kelas IV
('M. Haris, S.Pd',              'IV Abu Bakar Ash Shidiq'),
('Ii Hilyati, S.Pd',            'IV Umar bin Khatab'),
('Diah Handayani, S.Sos',       'IV Utsman bin Affan'),
('Yuniati, S.Ag',               'IV Ali bin Abi Thalib'),
-- Kelas V
('Rita Afiati, S.Pd',           'V Abu Bakar Ash Shidiq'),
('Fathur, S.Pd',                'V Umar bin Khatab'),
('Dian Asih Rahayu, S.Pd',      'V Utsman bin Affan'),
-- Kelas VI
('Hj. Wardah, S.Pd',            'VI Abu Bakar Ash Shidiq'),
('Yuliana Banjar Susanti, S.Pd','VI Umar bin Khatab'),
('Karsim Fahresyi, S.Pd',       'VI Utsman bin Affan'),
('Lia Nuriasih, S.Pd',          'VI Ali bin Abi Thalib'),
-- Guru Bidang Studi
('Akim, S.Pd',                  'Semua Tingkat'),
('Syirojudin, S.Pd',            'Semua Tingkat'),
('Munawir, S.Pd',               'Semua Tingkat'),
('H. Mukhlasin, S.Pd',          'Semua Tingkat'),
('Ari Rivaldi, S.Pd',           'Semua Tingkat'),
('Assadulloh, SE',              'Semua Tingkat'),
('Ilhamul Karim, S.Pd',         'Semua Tingkat'),
('Fuad Arif, S.Pd',             'Semua Tingkat'),
('Ayu Suraya, S.Pd',            'Semua Tingkat')
ON CONFLICT (nama) DO NOTHING;

-- Mapel default guru bidang studi
INSERT INTO mapel_guru (guru_id, mapel)
SELECT g.id, m.mapel FROM guru g
JOIN (VALUES
    ('Akim, S.Pd',         'PJOK'),
    ('Syirojudin, S.Pd',   'PJOK'),
    ('Munawir, S.Pd',      'PADB'),
    ('H. Mukhlasin, S.Pd', 'PADB'),
    ('Ari Rivaldi, S.Pd',  'TIK'),
    ('Assadulloh, SE',     'TIK'),
    ('Ilhamul Karim, S.Pd','B. Arab'),
    ('Fuad Arif, S.Pd',    'B. Inggris'),
    ('Ayu Suraya, S.Pd',   'Tahfidh')
) AS m(nama, mapel) ON g.nama = m.nama
ON CONFLICT (guru_id, mapel) DO NOTHING;

-- Mapel default wali kelas (Tematik)
INSERT INTO mapel_guru (guru_id, mapel)
SELECT id, 'Tematik' FROM guru
WHERE kelas != 'Semua Tingkat'
ON CONFLICT (guru_id, mapel) DO NOTHING;
