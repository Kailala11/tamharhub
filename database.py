"""
database.py — SQLite layer untuk TamharHub
SD Taman Harapan 1 Bekasi
"""
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import date, datetime

DB_PATH = Path("tamharhub.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS guru (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nama        TEXT NOT NULL UNIQUE,
        kelas       TEXT,
        role        TEXT DEFAULT 'guru',
        status      TEXT DEFAULT 'Aktif',
        created_at  TEXT DEFAULT (date('now'))
    );

    CREATE TABLE IF NOT EXISTS mapel_guru (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        guru_id  INTEGER REFERENCES guru(id) ON DELETE CASCADE,
        mapel    TEXT NOT NULL,
        UNIQUE(guru_id, mapel)
    );

    CREATE TABLE IF NOT EXISTS siswa (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nama     TEXT NOT NULL,
        kelas    TEXT NOT NULL,
        status   TEXT DEFAULT 'Aktif'
    );

    CREATE TABLE IF NOT EXISTS absen_guru (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        guru_id   INTEGER REFERENCES guru(id),
        tanggal   TEXT NOT NULL,
        status    TEXT NOT NULL CHECK(status IN ('H','A','I','S')),
        keterangan TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now','localtime')),
        UNIQUE(guru_id, tanggal)
    );

    CREATE TABLE IF NOT EXISTS absen_siswa (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        siswa_id  INTEGER REFERENCES siswa(id),
        guru_id   INTEGER REFERENCES guru(id),
        tanggal   TEXT NOT NULL,
        status    TEXT NOT NULL CHECK(status IN ('H','A','I','S')),
        keterangan TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now','localtime')),
        UNIQUE(siswa_id, tanggal)
    );

    CREATE TABLE IF NOT EXISTS jurnal (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        guru_id    INTEGER REFERENCES guru(id),
        tanggal    TEXT NOT NULL,
        kelas      TEXT NOT NULL,
        mapel      TEXT NOT NULL,
        topik      TEXT NOT NULL,
        aktivitas  TEXT NOT NULL,
        media      TEXT DEFAULT '',
        catatan    TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    """)

    # Seed guru jika kosong
    if c.execute("SELECT COUNT(*) FROM guru").fetchone()[0] == 0:
        _seed_guru(conn)

    conn.commit()
    conn.close()

# ── DATA GURU ─────────────────────────────────────────────────────
GURU_DATA = [
    # (nama, kelas)
    ("Annisa Rosmiati, S.Pd",       "I Abu Bakar Ash Shidiq"),
    ("Asnah Garlay, S.Pd",          "I Abu Bakar Ash Shidiq"),
    ("Rahmawati, S.Pd",             "I Umar bin Khatab"),
    ("Ainun Fatiyah, S.Pd",         "I Umar bin Khatab"),
    ("Euis Mulyati, S.Pd",          "I Utsman bin Affan"),
    ("Syarkiyah, S.Pd",             "I Ali bin Abi Thalib"),
    ("Winda Atmeiti, S.Pd",         "II Abu Bakar Ash Shidiq"),
    ("Griyana Novita Sari, S.Pd",   "II Abu Bakar Ash Shidiq"),
    ("Yollanda Mega Putri, S.Pd",   "II Umar bin Khatab"),
    ("Widyastuti, S.Pd",            "II Umar bin Khatab"),
    ("Alyuma Oklisia, S.Pd",        "II Utsman bin Affan"),
    ("Siti Ferda Heriati, S.P",     "II Utsman bin Affan"),
    ("Rosenah, S.Pd",               "II Ali bin Abi Thalib"),
    ("Usfatun Juliana, S.Pd",       "III Abu Bakar Ash Shidiq"),
    ("Aa Zamah, S.Pd",              "III Umar bin Khatab"),
    ("Lenia Nadhroh, S.Pd",         "III Utsman bin Affan"),
    ("Dra. Wagiati",                "III Ali bin Abi Thalib"),
    ("Dra. Juniti",                 "III Abdurahman bin Auf"),
    ("M. Haris, S.Pd",              "IV Abu Bakar Ash Shidiq"),
    ("Ii Hilyati, S.Pd",            "IV Umar bin Khatab"),
    ("Diah Handayani, S.Sos",       "IV Utsman bin Affan"),
    ("Yuniati, S.Ag",               "IV Ali bin Abi Thalib"),
    ("Rita Afiati, S.Pd",           "V Abu Bakar Ash Shidiq"),
    ("Fathur, S.Pd",                "V Umar bin Khatab"),
    ("Dian Asih Rahayu, S.Pd",      "V Utsman bin Affan"),
    ("Hj. Wardah, S.Pd",            "VI Abu Bakar Ash Shidiq"),
    ("Yuliana Banjar Susanti, S.Pd","VI Umar bin Khatab"),
    ("Karsim Fahresyi, S.Pd",       "VI Utsman bin Affan"),
    ("Lia Nuriasih, S.Pd",          "VI Ali bin Abi Thalib"),
    # Guru bidang studi
    ("Akim, S.Pd",                  "Semua Tingkat"),
    ("Syirojudin, S.Pd",            "Semua Tingkat"),
    ("Munawir, S.Pd",               "Semua Tingkat"),
    ("H. Mukhlasin, S.Pd",          "Semua Tingkat"),
    ("Ari Rivaldi, S.Pd",           "Semua Tingkat"),
    ("Assadulloh, SE",              "Semua Tingkat"),
    ("Ilhamul Karim, S.Pd",         "Semua Tingkat"),
    ("Fuad Arif, S.Pd",             "Semua Tingkat"),
    ("Ayu Suraya, S.Pd",            "Semua Tingkat"),
]

MAPEL_DEFAULT = {
    "Akim, S.Pd":                  ["PJOK"],
    "Syirojudin, S.Pd":            ["PJOK"],
    "Munawir, S.Pd":               ["PADB"],
    "H. Mukhlasin, S.Pd":          ["PADB"],
    "Ari Rivaldi, S.Pd":           ["TIK"],
    "Assadulloh, SE":              ["TIK"],
    "Ilhamul Karim, S.Pd":         ["B. Arab"],
    "Fuad Arif, S.Pd":             ["B. Inggris"],
    "Ayu Suraya, S.Pd":            ["Tahfidh"],
}

def _seed_guru(conn):
    c = conn.cursor()
    for nama, kelas in GURU_DATA:
        c.execute("INSERT INTO guru (nama, kelas) VALUES (?,?)", (nama, kelas))
        guru_id = c.lastrowid
        # Mapel default
        mapel_list = MAPEL_DEFAULT.get(nama, ["Tematik"])
        for m in mapel_list:
            c.execute("INSERT OR IGNORE INTO mapel_guru (guru_id, mapel) VALUES (?,?)", (guru_id, m))

# ── QUERIES ───────────────────────────────────────────────────────

def get_all_guru():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT g.id, g.nama, g.kelas, g.status,
               GROUP_CONCAT(mg.mapel, ', ') as mapel_list
        FROM guru g
        LEFT JOIN mapel_guru mg ON mg.guru_id = g.id
        WHERE g.status = 'Aktif'
        GROUP BY g.id
        ORDER BY g.id
    """, conn)
    conn.close()
    return df

def get_guru_by_nama(nama):
    conn = get_conn()
    row = conn.execute("SELECT * FROM guru WHERE nama=?", (nama,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_mapel_guru(guru_id):
    conn = get_conn()
    rows = conn.execute("SELECT mapel FROM mapel_guru WHERE guru_id=? ORDER BY mapel", (guru_id,)).fetchall()
    conn.close()
    return [r["mapel"] for r in rows]

def add_mapel_guru(guru_id, mapel):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO mapel_guru (guru_id, mapel) VALUES (?,?)", (guru_id, mapel.strip()))
        conn.commit()
        return True, "Berhasil ditambahkan."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_mapel_guru(guru_id, mapel):
    conn = get_conn()
    conn.execute("DELETE FROM mapel_guru WHERE guru_id=? AND mapel=?", (guru_id, mapel))
    conn.commit()
    conn.close()

def get_siswa_by_kelas(kelas):
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM siswa WHERE kelas=? AND status='Aktif' ORDER BY nama", conn, params=[kelas])
    conn.close()
    return df

def add_siswa_bulk(nama_list, kelas):
    conn = get_conn()
    for nama in nama_list:
        nama = nama.strip()
        if nama:
            conn.execute("INSERT OR IGNORE INTO siswa (nama, kelas) VALUES (?,?)", (nama, kelas))
    conn.commit()
    conn.close()

# ── ABSEN GURU ────────────────────────────────────────────────────

def upsert_absen_guru(guru_id, tanggal, status, keterangan=""):
    conn = get_conn()
    conn.execute("""
        INSERT INTO absen_guru (guru_id, tanggal, status, keterangan)
        VALUES (?,?,?,?)
        ON CONFLICT(guru_id, tanggal) DO UPDATE SET status=excluded.status, keterangan=excluded.keterangan
    """, (guru_id, tanggal, status, keterangan))
    conn.commit()
    conn.close()

def get_absen_guru_hari(tanggal):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT g.id, g.nama, g.kelas,
               COALESCE(a.status, '?') as status,
               COALESCE(a.keterangan, '') as keterangan,
               CASE WHEN a.id IS NULL THEN 0 ELSE 1 END as sudah_isi
        FROM guru g
        LEFT JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal=?
        WHERE g.status='Aktif'
        ORDER BY g.id
    """, conn, params=[tanggal])
    conn.close()
    return df

def get_absen_guru_rekap(bulan, tahun):
    conn = get_conn()
    prefix = f"{tahun}-{str(bulan).zfill(2)}"
    df = pd.read_sql("""
        SELECT g.nama, g.kelas,
               SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END) as hadir,
               SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) as alpa,
               SUM(CASE WHEN a.status='I' THEN 1 ELSE 0 END) as izin,
               SUM(CASE WHEN a.status='S' THEN 1 ELSE 0 END) as sakit,
               COUNT(a.id) as total_hari
        FROM guru g
        LEFT JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal LIKE ?
        WHERE g.status='Aktif'
        GROUP BY g.id
        ORDER BY g.id
    """, conn, params=[prefix+"%"])
    conn.close()
    return df

def get_status_absen_guru(guru_id, tanggal):
    conn = get_conn()
    row = conn.execute("SELECT status, keterangan FROM absen_guru WHERE guru_id=? AND tanggal=?", (guru_id, tanggal)).fetchone()
    conn.close()
    return dict(row) if row else None

# ── ABSEN SISWA ───────────────────────────────────────────────────

def upsert_absen_siswa_bulk(data_list, guru_id, tanggal):
    """data_list: list of (siswa_id, status, keterangan)"""
    conn = get_conn()
    for siswa_id, status, ket in data_list:
        conn.execute("""
            INSERT INTO absen_siswa (siswa_id, guru_id, tanggal, status, keterangan)
            VALUES (?,?,?,?,?)
            ON CONFLICT(siswa_id, tanggal) DO UPDATE SET status=excluded.status, keterangan=excluded.keterangan
        """, (siswa_id, guru_id, tanggal, status, ket))
    conn.commit()
    conn.close()

def get_absen_siswa_hari(kelas, tanggal):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.id, s.nama,
               COALESCE(a.status, 'H') as status,
               COALESCE(a.keterangan,'') as keterangan
        FROM siswa s
        LEFT JOIN absen_siswa a ON a.siswa_id=s.id AND a.tanggal=?
        WHERE s.kelas=? AND s.status='Aktif'
        ORDER BY s.nama
    """, conn, params=[tanggal, kelas])
    conn.close()
    return df

def get_absen_siswa_rekap(kelas, bulan, tahun):
    conn = get_conn()
    prefix = f"{tahun}-{str(bulan).zfill(2)}"
    df = pd.read_sql("""
        SELECT s.nama,
               SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END) as hadir,
               SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) as alpa,
               SUM(CASE WHEN a.status='I' THEN 1 ELSE 0 END) as izin,
               SUM(CASE WHEN a.status='S' THEN 1 ELSE 0 END) as sakit,
               COUNT(a.id) as total_hari,
               ROUND(SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END)*100.0/NULLIF(COUNT(a.id),0),1) as pct_hadir
        FROM siswa s
        LEFT JOIN absen_siswa a ON a.siswa_id=s.id AND a.tanggal LIKE ?
        WHERE s.kelas=? AND s.status='Aktif'
        GROUP BY s.id
        ORDER BY s.nama
    """, conn, params=[prefix+"%", kelas])
    conn.close()
    return df

# ── JURNAL ────────────────────────────────────────────────────────

def simpan_jurnal(guru_id, tanggal, kelas, mapel, topik, aktivitas, media, catatan):
    conn = get_conn()
    conn.execute("""
        INSERT INTO jurnal (guru_id, tanggal, kelas, mapel, topik, aktivitas, media, catatan)
        VALUES (?,?,?,?,?,?,?,?)
    """, (guru_id, tanggal, kelas, mapel, topik, aktivitas, media, catatan))
    conn.commit()
    conn.close()

def get_jurnal_guru(guru_id, limit=20):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT j.*, g.nama as guru_nama
        FROM jurnal j JOIN guru g ON g.id=j.guru_id
        WHERE j.guru_id=?
        ORDER BY j.tanggal DESC, j.id DESC
        LIMIT ?
    """, conn, params=[guru_id, limit])
    conn.close()
    return df

def get_jurnal_semua(tanggal=None, limit=50):
    conn = get_conn()
    if tanggal:
        df = pd.read_sql("""
            SELECT j.*, g.nama as guru_nama
            FROM jurnal j JOIN guru g ON g.id=j.guru_id
            WHERE j.tanggal=?
            ORDER BY j.id DESC LIMIT ?
        """, conn, params=[tanggal, limit])
    else:
        df = pd.read_sql("""
            SELECT j.*, g.nama as guru_nama
            FROM jurnal j JOIN guru g ON g.id=j.guru_id
            ORDER BY j.tanggal DESC, j.id DESC LIMIT ?
        """, conn, params=[limit])
    conn.close()
    return df

# ── SUMMARY ───────────────────────────────────────────────────────

def get_summary_hari(tanggal):
    conn = get_conn()
    total_guru = conn.execute("SELECT COUNT(*) FROM guru WHERE status='Aktif'").fetchone()[0]
    hadir_guru = conn.execute("""
        SELECT COUNT(*) FROM (
            SELECT g.id FROM guru g
            INNER JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal=?
            WHERE g.status='Aktif' AND a.status='H'
        )
    """, (tanggal,)).fetchone()[0]
    total_siswa = conn.execute("SELECT COUNT(*) FROM siswa WHERE status='Aktif'").fetchone()[0]
    hadir_siswa = conn.execute("""
        SELECT COUNT(*) FROM absen_siswa WHERE tanggal=? AND status='H'
    """, (tanggal,)).fetchone()[0]
    absen_siswa = conn.execute("""
        SELECT COUNT(*) FROM absen_siswa WHERE tanggal=? AND status='A'
    """, (tanggal,)).fetchone()[0]
    jurnal_hari = conn.execute("SELECT COUNT(*) FROM jurnal WHERE tanggal=?", (tanggal,)).fetchone()[0]
    conn.close()
    return {
        "total_guru": total_guru,
        "hadir_guru": hadir_guru,
        "absen_guru": total_guru - hadir_guru,
        "total_siswa": total_siswa,
        "hadir_siswa": hadir_siswa,
        "absen_siswa_alpa": absen_siswa,
        "jurnal_hari": jurnal_hari,
    }

def get_guru_tidak_hadir(tanggal):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT g.nama, g.kelas, COALESCE(a.status,'?') as status, COALESCE(a.keterangan,'') as keterangan
        FROM guru g
        LEFT JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal=?
        WHERE g.status='Aktif' AND COALESCE(a.status,'?') != 'H'
        ORDER BY g.id
    """, conn, params=[tanggal])
    conn.close()
    return df

def get_siswa_tidak_hadir(tanggal):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.nama, s.kelas, a.status, COALESCE(a.keterangan,'') as keterangan
        FROM absen_siswa a JOIN siswa s ON s.id=a.siswa_id
        WHERE a.tanggal=? AND a.status != 'H'
        ORDER BY s.kelas, s.nama
    """, conn, params=[tanggal])
    conn.close()
    return df


# ── AGENDA SEKOLAH ────────────────────────────────────────────────

def init_agenda_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agenda_sekolah (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            judul       TEXT NOT NULL,
            deskripsi   TEXT DEFAULT '',
            tanggal     TEXT NOT NULL,
            tanggal_end TEXT DEFAULT '',
            kategori    TEXT DEFAULT 'Umum',
            dibuat_oleh TEXT DEFAULT '',
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()

def tambah_agenda(judul, deskripsi, tanggal, tanggal_end, kategori, dibuat_oleh):
    conn = get_conn()
    conn.execute("""
        INSERT INTO agenda_sekolah (judul, deskripsi, tanggal, tanggal_end, kategori, dibuat_oleh)
        VALUES (?,?,?,?,?,?)
    """, (judul, deskripsi, str(tanggal), str(tanggal_end) if tanggal_end else '', kategori, dibuat_oleh))
    conn.commit()
    conn.close()

def hapus_agenda(agenda_id):
    conn = get_conn()
    conn.execute("DELETE FROM agenda_sekolah WHERE id=?", (agenda_id,))
    conn.commit()
    conn.close()

def get_agenda_mendatang(limit=20):
    from datetime import date
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM agenda_sekolah
        WHERE tanggal >= ?
        ORDER BY tanggal ASC LIMIT ?
    """, conn, params=[str(date.today()), limit])
    conn.close()
    return df

def get_agenda_semua(limit=50):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM agenda_sekolah
        ORDER BY tanggal DESC LIMIT ?
    """, conn, params=[limit])
    conn.close()
    return df

def get_jurnal_by_kelas(kelas, limit=30):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT j.tanggal, j.mapel, j.topik, j.aktivitas,
               j.media, j.catatan, g.nama as guru_nama
        FROM jurnal j JOIN guru g ON g.id=j.guru_id
        WHERE j.kelas = ?
        ORDER BY j.tanggal DESC, j.id DESC LIMIT ?
    """, conn, params=[kelas, limit])
    conn.close()
    return df

def get_semua_kelas():
    conn = get_conn()
    rows = conn.execute("""
        SELECT DISTINCT kelas FROM guru
        WHERE kelas != 'Semua Tingkat' AND status='Aktif'
        ORDER BY kelas
    """).fetchall()
    conn.close()
    return [r["kelas"] for r in rows]


# ── NILAI SISWA ───────────────────────────────────────────────────

def init_nilai_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id    INTEGER REFERENCES siswa(id),
            guru_id     INTEGER REFERENCES guru(id),
            semester    TEXT NOT NULL,
            tahun_ajar  TEXT NOT NULL,
            mapel       TEXT NOT NULL,
            pengetahuan REAL,
            keterampilan REAL,
            sikap       TEXT DEFAULT 'B',
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            updated_at  TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(siswa_id, semester, tahun_ajar, mapel)
        )
    """)
    conn.commit()
    conn.close()

PREDIKAT_ANGKA = [(90,'A'),(80,'B'),(70,'C'),(0,'D')]
DESKRIPSI_SIKAP = {
    'A': 'Sangat Baik',
    'B': 'Baik',
    'C': 'Cukup',
    'D': 'Perlu Bimbingan',
}

def get_predikat(nilai):
    if nilai is None: return '-'
    for batas, pred in PREDIKAT_ANGKA:
        if nilai >= batas: return pred
    return 'D'

def upsert_nilai(siswa_id, guru_id, semester, tahun_ajar, mapel,
                 pengetahuan, keterampilan, sikap):
    conn = get_conn()
    conn.execute("""
        INSERT INTO nilai_siswa
            (siswa_id, guru_id, semester, tahun_ajar, mapel, pengetahuan, keterampilan, sikap, updated_at)
        VALUES (?,?,?,?,?,?,?,?,datetime('now','localtime'))
        ON CONFLICT(siswa_id, semester, tahun_ajar, mapel)
        DO UPDATE SET
            pengetahuan=excluded.pengetahuan,
            keterampilan=excluded.keterampilan,
            sikap=excluded.sikap,
            guru_id=excluded.guru_id,
            updated_at=datetime('now','localtime')
    """, (siswa_id, guru_id, semester, tahun_ajar, mapel,
          pengetahuan, keterampilan, sikap))
    conn.commit()
    conn.close()

def get_nilai_kelas(kelas, semester, tahun_ajar):
    """Return pivot: siswa x mapel dengan kolom P, K, S per mapel."""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.id as siswa_id, s.nama as siswa,
               n.mapel, n.pengetahuan, n.keterampilan, n.sikap
        FROM siswa s
        LEFT JOIN nilai_siswa n ON n.siswa_id=s.id
            AND n.semester=? AND n.tahun_ajar=?
        WHERE s.kelas=? AND s.status='Aktif'
        ORDER BY s.nama, n.mapel
    """, conn, params=[semester, tahun_ajar, kelas])
    conn.close()
    return df

def get_nilai_siswa(siswa_id, semester, tahun_ajar):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT mapel, pengetahuan, keterampilan, sikap
        FROM nilai_siswa
        WHERE siswa_id=? AND semester=? AND tahun_ajar=?
        ORDER BY mapel
    """, conn, params=[siswa_id, semester, tahun_ajar])
    conn.close()
    return df

def get_nilai_satu_siswa_mapel(siswa_id, semester, tahun_ajar, mapel):
    conn = get_conn()
    row = conn.execute("""
        SELECT pengetahuan, keterampilan, sikap
        FROM nilai_siswa
        WHERE siswa_id=? AND semester=? AND tahun_ajar=? AND mapel=?
    """, (siswa_id, semester, tahun_ajar, mapel)).fetchone()
    conn.close()
    return dict(row) if row else None


# ── NUPTK GURU ────────────────────────────────────────────────────

def update_nuptk(guru_id, nuptk):
    conn = get_conn()
    conn.execute("UPDATE guru SET nuptk=? WHERE id=?", (nuptk.strip(), guru_id))
    conn.commit()
    conn.close()

def get_nuptk(guru_id):
    conn = get_conn()
    try:
        row = conn.execute("SELECT nuptk FROM guru WHERE id=?", (guru_id,)).fetchone()
        conn.close()
        return row["nuptk"] if row and row["nuptk"] else ""
    except Exception:
        conn.close()
        return ""

# ── SISWA LENGKAP (NIS, NISN, Alamat, Fase) ───────────────────────

def add_siswa_lengkap(nama, kelas, nis="", nisn="", alamat="", fase=""):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO siswa (nama,kelas,nis,nisn,alamat,fase) VALUES (?,?,?,?,?,?)",
            (nama.strip(), kelas, nis.strip(), nisn.strip(), alamat.strip(), fase.strip())
        )
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()

def update_siswa_info(siswa_id, nis="", nisn="", alamat="", fase=""):
    conn = get_conn()
    conn.execute(
        "UPDATE siswa SET nis=?, nisn=?, alamat=?, fase=? WHERE id=?",
        (nis, nisn, alamat, fase, siswa_id)
    )
    conn.commit()
    conn.close()

def get_siswa_by_kelas_lengkap(kelas):
    conn = get_conn()
    try:
        df = pd.read_sql(
            "SELECT * FROM siswa WHERE kelas=? AND status='Aktif' ORDER BY nama",
            conn, params=[kelas]
        )
    except Exception:
        df = get_siswa_by_kelas(kelas)
    conn.close()
    return df

# ── EKSKUL ────────────────────────────────────────────────────────

def upsert_ekskul(siswa_id, guru_id, semester, tahun_ajar, nama_ekskul, keterangan):
    conn = get_conn()
    conn.execute("""
        INSERT INTO ekskul_siswa (siswa_id,guru_id,semester,tahun_ajar,nama_ekskul,keterangan)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT(siswa_id,semester,tahun_ajar,nama_ekskul)
        DO UPDATE SET keterangan=excluded.keterangan
    """, (siswa_id, guru_id, semester, tahun_ajar, nama_ekskul, keterangan))
    conn.commit()
    conn.close()

def get_ekskul_siswa(siswa_id, semester, tahun_ajar):
    conn = get_conn()
    df = pd.read_sql(
        "SELECT nama_ekskul, keterangan FROM ekskul_siswa WHERE siswa_id=? AND semester=? AND tahun_ajar=? ORDER BY id",
        conn, params=[siswa_id, semester, tahun_ajar]
    )
    conn.close()
    return df

# ── CATATAN RAPOR ─────────────────────────────────────────────────

def upsert_catatan(siswa_id, guru_id, semester, tahun_ajar, catatan_wali, tanggapan_ortu=""):
    conn = get_conn()
    conn.execute("""
        INSERT INTO catatan_rapor (siswa_id,guru_id,semester,tahun_ajar,catatan_wali,tanggapan_ortu)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT(siswa_id,semester,tahun_ajar)
        DO UPDATE SET catatan_wali=excluded.catatan_wali, tanggapan_ortu=excluded.tanggapan_ortu
    """, (siswa_id, guru_id, semester, tahun_ajar, catatan_wali, tanggapan_ortu))
    conn.commit()
    conn.close()

def get_catatan(siswa_id, semester, tahun_ajar):
    conn = get_conn()
    row = conn.execute(
        "SELECT catatan_wali, tanggapan_ortu FROM catatan_rapor WHERE siswa_id=? AND semester=? AND tahun_ajar=?",
        (siswa_id, semester, tahun_ajar)
    ).fetchone()
    conn.close()
    return dict(row) if row else {"catatan_wali": "", "tanggapan_ortu": ""}

def get_absen_count_siswa(siswa_id, semester, tahun_ajar):
    """Hitung total sakit, izin, alpa dari absen_siswa untuk periode semester."""
    conn = get_conn()
    # Mapping semester ke bulan
    if "Ganjil" in semester:
        bulan_range = [7,8,9,10,11,12]
    else:
        bulan_range = [1,2,3,4,5,6]
    tahun = tahun_ajar.split("/")[0] if "Ganjil" in semester else tahun_ajar.split("/")[1]
    placeholders = ",".join(["?" for _ in bulan_range])
    params = [siswa_id] + [f"{tahun}-{str(b).zfill(2)}%" for b in bulan_range]
    rows = []
    for b in bulan_range:
        r = conn.execute(
            "SELECT status, COUNT(*) as cnt FROM absen_siswa WHERE siswa_id=? AND tanggal LIKE ? GROUP BY status",
            (siswa_id, f"{tahun}-{str(b).zfill(2)}%")
        ).fetchall()
        rows.extend(r)
    conn.close()
    result = {"S":0,"I":0,"A":0}
    for r in rows:
        if r["status"] in result:
            result[r["status"]] += r["cnt"]
    return result


# ── MULTI WALI KELAS ──────────────────────────────────────────────

def init_guru_kelas_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guru_kelas (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER REFERENCES guru(id) ON DELETE CASCADE,
            kelas   TEXT NOT NULL,
            UNIQUE(guru_id, kelas)
        )
    """)
    # Populate dari kolom kelas jika belum ada
    count = conn.execute("SELECT COUNT(*) FROM guru_kelas").fetchone()[0]
    if count == 0:
        rows = conn.execute("SELECT id, kelas FROM guru WHERE kelas IS NOT NULL AND kelas != ''").fetchall()
        for r in rows:
            try:
                conn.execute("INSERT OR IGNORE INTO guru_kelas (guru_id, kelas) VALUES (?,?)", (r['id'], r['kelas']))
            except: pass
    conn.commit()
    conn.close()

def get_kelas_guru(guru_id: int) -> list:
    """Return list kelas yang diajar guru ini (support multi kelas)."""
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT COALESCE(gk.kelas, g.kelas) as kelas
            FROM guru g
            LEFT JOIN guru_kelas gk ON gk.guru_id = g.id
            WHERE g.id = ?
            ORDER BY kelas
        """, (guru_id,)).fetchall()
        conn.close()
        kelas_list = list(dict.fromkeys([r['kelas'] for r in rows if r['kelas']]))
        return kelas_list
    except Exception:
        # Fallback: ambil dari kolom kelas langsung
        try:
            row = conn.execute("SELECT kelas FROM guru WHERE id=?", (guru_id,)).fetchone()
        except Exception:
            row = None
        conn.close()
        return [row['kelas']] if row and row['kelas'] else []

def get_guru_by_kelas(kelas: str) -> list:
    """Return list guru yang mengajar di kelas ini."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT DISTINCT g.id, g.nama, g.kelas
        FROM guru g
        LEFT JOIN guru_kelas gk ON gk.guru_id = g.id
        WHERE g.kelas = ? OR gk.kelas = ?
        AND g.status = 'Aktif'
    """, (kelas, kelas)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def tambah_guru_kelas(guru_id: int, kelas: str):
    conn = get_conn()
    try:
        conn.execute("INSERT OR IGNORE INTO guru_kelas (guru_id, kelas) VALUES (?,?)", (guru_id, kelas))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def hapus_guru_kelas(guru_id: int, kelas: str):
    conn = get_conn()
    conn.execute("DELETE FROM guru_kelas WHERE guru_id=? AND kelas=?", (guru_id, kelas))
    conn.commit()
    conn.close()


# ── NILAI TP (Tujuan Pembelajaran) ────────────────────────────────

def init_nilai_tp_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS nilai_tp (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id   INTEGER REFERENCES siswa(id),
            guru_id    INTEGER REFERENCES guru(id),
            kelas      TEXT NOT NULL,
            semester   TEXT NOT NULL,
            tahun_ajar TEXT NOT NULL,
            mapel      TEXT NOT NULL,
            tp1  REAL, tp2  REAL, tp3  REAL, tp4  REAL, tp5  REAL,
            tp6  REAL, tp7  REAL, tp8  REAL, tp9  REAL, tp10 REAL,
            asts REAL,
            asas REAL,
            nr   REAL,
            capaian_maksimal TEXT DEFAULT '',
            updated_at TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(siswa_id, semester, tahun_ajar, mapel)
        )
    """)
    conn.commit()
    conn.close()

TP_COLS = ['tp1','tp2','tp3','tp4','tp5','tp6','tp7','tp8','tp9','tp10','asts','asas']

def hitung_nr(row_dict: dict) -> float:
    """NR = rata-rata semua TP yang diisi + ASTS + ASAS."""
    vals = [row_dict.get(c) for c in TP_COLS
            if row_dict.get(c) is not None and str(row_dict.get(c)).strip() not in ('','None')]
    nums = [float(v) for v in vals if v not in (None, '') and str(v) not in ('None',)]
    return round(sum(nums)/len(nums), 2) if nums else 0.0

def upsert_nilai_tp(siswa_id, guru_id, kelas, semester, tahun_ajar, mapel, tp_dict, capaian=""):
    nr = hitung_nr(tp_dict)
    data = {
        "siswa_id": siswa_id, "guru_id": guru_id, "kelas": kelas,
        "semester": semester, "tahun_ajar": tahun_ajar, "mapel": mapel,
        "tp1": tp_dict.get("tp1"), "tp2": tp_dict.get("tp2"),
        "tp3": tp_dict.get("tp3"), "tp4": tp_dict.get("tp4"),
        "tp5": tp_dict.get("tp5"), "tp6": tp_dict.get("tp6"),
        "tp7": tp_dict.get("tp7"), "tp8": tp_dict.get("tp8"),
        "tp9": tp_dict.get("tp9"), "tp10": tp_dict.get("tp10"),
        "asts": tp_dict.get("asts"), "asas": tp_dict.get("asas"),
        "nr": nr, "capaian_maksimal": capaian
    }
    # Try Supabase first
    sb = get_sb()
    if sb:
        try:
            sb.table("nilai_tp").upsert(data, on_conflict="siswa_id,semester,tahun_ajar,mapel").execute()
            return nr
        except Exception as e:
            print(f"Supabase upsert_nilai_tp error: {e}")
    # Fallback SQLite
    try:
        conn = get_conn()
        conn.execute(f"""
            INSERT INTO nilai_tp
                (siswa_id,guru_id,kelas,semester,tahun_ajar,mapel,
                 tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9,tp10,asts,asas,nr,capaian_maksimal)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(siswa_id,semester,tahun_ajar,mapel)
            DO UPDATE SET
                guru_id=excluded.guru_id, kelas=excluded.kelas,
                tp1=excluded.tp1, tp2=excluded.tp2, tp3=excluded.tp3,
                tp4=excluded.tp4, tp5=excluded.tp5, tp6=excluded.tp6,
                tp7=excluded.tp7, tp8=excluded.tp8, tp9=excluded.tp9,
                tp10=excluded.tp10, asts=excluded.asts, asas=excluded.asas,
                nr=excluded.nr, capaian_maksimal=excluded.capaian_maksimal
        """, (
            siswa_id, guru_id, kelas, semester, tahun_ajar, mapel,
            data["tp1"], data["tp2"], data["tp3"], data["tp4"], data["tp5"],
            data["tp6"], data["tp7"], data["tp8"], data["tp9"], data["tp10"],
            data["asts"], data["asas"], nr, capaian
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"SQLite upsert_nilai_tp error: {e}")
    return nr


def get_nilai_tp_kelas(kelas, semester, tahun_ajar, mapel):
    """Return semua nilai TP siswa di kelas untuk mapel tertentu."""
    sb = get_sb()
    if sb:
        try:
            # Get siswa
            s_res = sb.table("siswa").select("id,nama").eq("kelas", kelas).eq("status","Aktif").execute()
            siswa_list = s_res.data or []
            if not siswa_list:
                return pd.DataFrame()
            sids = [s["id"] for s in siswa_list]
            # Get nilai
            n_res = sb.table("nilai_tp").select("*").in_("siswa_id", sids)                .eq("semester", semester).eq("tahun_ajar", tahun_ajar).eq("mapel", mapel).execute()
            nilai_map = {n["siswa_id"]: n for n in (n_res.data or [])}
            rows = []
            for s in sorted(siswa_list, key=lambda x: x["nama"]):
                n = nilai_map.get(s["id"], {})
                rows.append({"siswa_id": s["id"], "siswa": s["nama"],
                    "tp1":n.get("tp1"), "tp2":n.get("tp2"), "tp3":n.get("tp3"),
                    "tp4":n.get("tp4"), "tp5":n.get("tp5"), "tp6":n.get("tp6"),
                    "tp7":n.get("tp7"), "tp8":n.get("tp8"), "tp9":n.get("tp9"),
                    "tp10":n.get("tp10"), "asts":n.get("asts"), "asas":n.get("asas"),
                    "nr":n.get("nr"), "capaian_maksimal":n.get("capaian_maksimal","")})
            return pd.DataFrame(rows)
        except Exception as e:
            print(f"Supabase get_nilai_tp_kelas error: {e}")
    # Fallback SQLite
    try:
        conn = get_conn()
        df = pd.read_sql("""
            SELECT s.id as siswa_id, s.nama as siswa,
                   n.tp1,n.tp2,n.tp3,n.tp4,n.tp5,
                   n.tp6,n.tp7,n.tp8,n.tp9,n.tp10,
                   n.asts, n.asas, n.nr, n.capaian_maksimal
            FROM siswa s
            LEFT JOIN nilai_tp n ON n.siswa_id=s.id
                AND n.semester=? AND n.tahun_ajar=? AND n.mapel=?
            WHERE s.kelas=? AND s.status='Aktif'
            ORDER BY s.nama
        """, conn, params=[semester, tahun_ajar, mapel, kelas])
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def get_nilai_tp_siswa(siswa_id, semester, tahun_ajar, mapel):
    """Return satu baris nilai TP untuk siswa + mapel tertentu."""
    # Try Supabase first
    sb = get_sb()
    if sb:
        try:
            res = sb.table("nilai_tp").select("*").eq("siswa_id", siswa_id)                .eq("semester", semester).eq("tahun_ajar", tahun_ajar)                .eq("mapel", mapel).limit(1).execute()
            return res.data[0] if res.data else {}
        except Exception:
            pass
    # Fallback SQLite
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9,tp10,asts,asas,nr,capaian_maksimal
            FROM nilai_tp
            WHERE siswa_id=? AND semester=? AND tahun_ajar=? AND mapel=?
        """, (siswa_id, semester, tahun_ajar, mapel)).fetchone()
        conn.close()
        return dict(row) if row else {}
    except Exception:
        return {}

def get_nr_semua_mapel_siswa(siswa_id, semester, tahun_ajar):
    """Return NR per mapel untuk satu siswa — untuk rapor."""
    sb = get_sb()
    if sb:
        try:
            res = sb.table("nilai_tp").select("mapel,nr,capaian_maksimal")                .eq("siswa_id", siswa_id).eq("semester", semester).eq("tahun_ajar", tahun_ajar).execute()
            return pd.DataFrame(res.data or [])
        except Exception as e:
            print(f"Supabase get_nr_semua_mapel_siswa error: {e}")
    try:
        conn = get_conn()
        df = pd.read_sql("""
            SELECT mapel, nr, capaian_maksimal
            FROM nilai_tp
            WHERE siswa_id=? AND semester=? AND tahun_ajar=?
            ORDER BY mapel
        """, conn, params=[siswa_id, semester, tahun_ajar])
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def get_rekap_nr_kelas(kelas, semester, tahun_ajar):
    """Return pivot NR semua siswa x semua mapel — untuk rekap Excel."""
    sb = get_sb()
    if sb:
        try:
            s_res = sb.table("siswa").select("id,nama").eq("kelas", kelas).eq("status","Aktif").execute()
            siswa_list = s_res.data or []
            if not siswa_list:
                return pd.DataFrame()
            sids = [s["id"] for s in siswa_list]
            n_res = sb.table("nilai_tp").select("siswa_id,mapel,nr,capaian_maksimal")                .in_("siswa_id", sids).eq("semester", semester).eq("tahun_ajar", tahun_ajar).execute()
            siswa_map = {s["id"]: s["nama"] for s in siswa_list}
            rows = []
            for n in (n_res.data or []):
                rows.append({"siswa_id": n["siswa_id"], "siswa": siswa_map.get(n["siswa_id"],""),
                             "mapel": n["mapel"], "nr": n["nr"], "capaian_maksimal": n.get("capaian_maksimal","")})
            return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["siswa_id","siswa","mapel","nr","capaian_maksimal"])
        except Exception as e:
            print(f"Supabase get_rekap_nr_kelas error: {e}")
    try:
        conn = get_conn()
        df = pd.read_sql("""
            SELECT s.id as siswa_id, s.nama as siswa, n.mapel, n.nr, n.capaian_maksimal
            FROM siswa s
            LEFT JOIN nilai_tp n ON n.siswa_id=s.id
                AND n.semester=? AND n.tahun_ajar=?
            WHERE s.kelas=? AND s.status='Aktif'
            ORDER BY s.nama, n.mapel
        """, conn, params=[semester, tahun_ajar, kelas])
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


# ── MIGRATIONS ────────────────────────────────────────────────────

def run_migrations():
    """Jalankan semua schema migrations secara aman — idempotent."""
    conn = get_conn()
    migrations = [
        "ALTER TABLE guru ADD COLUMN nuptk TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN nis TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN nisn TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN alamat TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN fase TEXT DEFAULT ''",
        "ALTER TABLE nilai_siswa ADD COLUMN capaian TEXT DEFAULT ''",
        """CREATE TABLE IF NOT EXISTS ekskul_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER REFERENCES siswa(id),
            guru_id INTEGER REFERENCES guru(id),
            semester TEXT NOT NULL, tahun_ajar TEXT NOT NULL,
            nama_ekskul TEXT NOT NULL, keterangan TEXT DEFAULT '',
            UNIQUE(siswa_id, semester, tahun_ajar, nama_ekskul))""",
        """CREATE TABLE IF NOT EXISTS catatan_rapor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER REFERENCES siswa(id),
            guru_id INTEGER REFERENCES guru(id),
            semester TEXT NOT NULL, tahun_ajar TEXT NOT NULL,
            catatan_wali TEXT DEFAULT '', tanggapan_ortu TEXT DEFAULT '',
            UNIQUE(siswa_id, semester, tahun_ajar))""",
        """CREATE TABLE IF NOT EXISTS nilai_tp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER REFERENCES siswa(id),
            guru_id INTEGER REFERENCES guru(id),
            kelas TEXT NOT NULL, semester TEXT NOT NULL,
            tahun_ajar TEXT NOT NULL, mapel TEXT NOT NULL,
            tp1 REAL, tp2 REAL, tp3 REAL, tp4 REAL, tp5 REAL,
            tp6 REAL, tp7 REAL, tp8 REAL, tp9 REAL, tp10 REAL,
            asts REAL, asas REAL, nr REAL,
            capaian_maksimal TEXT DEFAULT '',
            updated_at TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(siswa_id, semester, tahun_ajar, mapel))""",
        """CREATE TABLE IF NOT EXISTS guru_kelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER REFERENCES guru(id) ON DELETE CASCADE,
            kelas TEXT NOT NULL,
            UNIQUE(guru_id, kelas))""",
        """CREATE TABLE IF NOT EXISTS agenda_sekolah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL, deskripsi TEXT DEFAULT '',
            tanggal TEXT NOT NULL, tanggal_end TEXT DEFAULT '',
            kategori TEXT DEFAULT 'Umum', dibuat_oleh TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime')))""",
    ]
    for sql in migrations:
        try:
            conn.execute(sql)
        except Exception:
            pass
    # Populate guru_kelas dari kolom kelas jika kosong
    try:
        count = conn.execute("SELECT COUNT(*) FROM guru_kelas").fetchone()[0]
        if count == 0:
            rows = conn.execute("SELECT id, kelas FROM guru WHERE kelas IS NOT NULL AND kelas != ''").fetchall()
            for r in rows:
                try:
                    conn.execute("INSERT OR IGNORE INTO guru_kelas (guru_id, kelas) VALUES (?,?)", (r['id'], r['kelas']))
                except Exception:
                    pass
    except Exception:
        pass
    conn.commit()
    conn.close()


# ── SUPABASE STORAGE ──────────────────────────────────────────────

SUPABASE_URL = "https://fodvxtulmrzzwtvirpuc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvZHZ4dHVsbXJ6end0dmlycHVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyNTY4OTIsImV4cCI6MjA5MjgzMjg5Mn0.kGByHoXbJf2VJlROfa6i8VeI1t1BUVySjvp5zRo4AjQ"

def get_sb():
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

def upload_file_storage(bucket: str, path: str, file_bytes: bytes, content_type: str = "application/octet-stream") -> bool:
    """Upload file ke Supabase Storage."""
    sb = get_sb()
    if not sb:
        return False
    try:
        sb.storage.from_(bucket).upload(
            path, file_bytes,
            {"content-type": content_type, "upsert": "true"}
        )
        return True
    except Exception as e:
        print(f"Upload error: {e}")
        return False

def list_files_storage(bucket: str, folder: str = "") -> list:
    """List files di bucket/folder."""
    sb = get_sb()
    if not sb:
        return []
    try:
        res = sb.storage.from_(bucket).list(folder)
        return res or []
    except Exception:
        return []

def download_file_storage(bucket: str, path: str) -> bytes:
    """Download file dari Supabase Storage."""
    sb = get_sb()
    if not sb:
        return b""
    try:
        res = sb.storage.from_(bucket).download(path)
        return res
    except Exception:
        return b""

def delete_file_storage(bucket: str, path: str) -> bool:
    """Hapus file dari Supabase Storage."""
    sb = get_sb()
    if not sb:
        return False
    try:
        sb.storage.from_(bucket).remove([path])
        return True
    except Exception:
        return False

def get_public_url(bucket: str, path: str) -> str:
    """Dapatkan URL publik file (hanya untuk public bucket)."""
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}"

# ── FILE METADATA DI DATABASE ─────────────────────────────────────

def init_file_metadata_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_metadata (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id     INTEGER REFERENCES guru(id),
            bucket      TEXT NOT NULL,
            path        TEXT NOT NULL,
            nama_file   TEXT NOT NULL,
            kategori    TEXT NOT NULL,
            ukuran      INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(bucket, path)
        )
    """)
    conn.commit()
    conn.close()

def simpan_metadata_file(guru_id, bucket, path, nama_file, kategori, ukuran=0):
    conn = get_conn()
    conn.execute("""
        INSERT OR REPLACE INTO file_metadata
            (guru_id, bucket, path, nama_file, kategori, ukuran)
        VALUES (?,?,?,?,?,?)
    """, (guru_id, bucket, path, nama_file, kategori, ukuran))
    conn.commit()
    conn.close()

def get_files_guru(guru_id, kategori=None):
    conn = get_conn()
    if kategori:
        df = pd.read_sql("""
            SELECT f.*, g.nama as guru_nama FROM file_metadata f
            JOIN guru g ON g.id=f.guru_id
            WHERE f.guru_id=? AND f.kategori=?
            ORDER BY f.created_at DESC
        """, conn, params=[guru_id, kategori])
    else:
        df = pd.read_sql("""
            SELECT f.*, g.nama as guru_nama FROM file_metadata f
            JOIN guru g ON g.id=f.guru_id
            WHERE f.guru_id=?
            ORDER BY f.kategori, f.created_at DESC
        """, conn, params=[guru_id])
    conn.close()
    return df

def get_all_files_by_kategori(kategori):
    conn = get_conn()
    df = pd.read_sql("""
        SELECT f.*, g.nama as guru_nama, g.kelas FROM file_metadata f
        JOIN guru g ON g.id=f.guru_id
        WHERE f.kategori=?
        ORDER BY g.kelas, g.nama, f.created_at DESC
    """, conn, params=[kategori])
    conn.close()
    return df

def hapus_metadata_file(file_id):
    conn = get_conn()
    conn.execute("DELETE FROM file_metadata WHERE id=?", (file_id,))
    conn.commit()
    conn.close()
