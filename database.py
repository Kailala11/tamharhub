"""
database.py — TamharHub Database Layer
Arsitektur: Supabase (PostgreSQL) sebagai primary, SQLite sebagai fallback lokal.
Semua fungsi otomatis pakai Supabase kalau credentials tersedia.
"""
import sqlite3
import pandas as pd
from datetime import date

# ── CONFIG ────────────────────────────────────────────────────────
DB_PATH      = "tamharhub.db"
SUPABASE_URL = "https://fodvxtulmrzzwtvirpuc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvZHZ4dHVsbXJ6end0dmlycHVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyNTY4OTIsImV4cCI6MjA5MjgzMjg5Mn0.kGByHoXbJf2VJlROfa6i8VeI1t1BUVySjvp5zRo4AjQ"

DESKRIPSI_SIKAP = {"A": "Sangat Baik", "B": "Baik", "C": "Cukup", "D": "Perlu Bimbingan"}
TP_COLS = ['tp1','tp2','tp3','tp4','tp5','tp6','tp7','tp8','tp9','tp10','asts','asas']

# ── SUPABASE CLIENT ───────────────────────────────────────────────
_sb_client = None

def get_sb():
    global _sb_client
    if _sb_client is not None:
        return _sb_client
    try:
        import streamlit as st
        url = st.secrets.get("supabase", {}).get("url", SUPABASE_URL)
        key = st.secrets.get("supabase", {}).get("key", SUPABASE_KEY)
    except Exception:
        url, key = SUPABASE_URL, SUPABASE_KEY
    try:
        from supabase import create_client
        _sb_client = create_client(url, key)
        return _sb_client
    except Exception:
        return None

def sb_ok():
    return get_sb() is not None

# ── SQLITE FALLBACK ───────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── GENERIC HELPERS ───────────────────────────────────────────────
def _sb_df(table, select="*", filters=None, order=None, limit=None):
    try:
        q = get_sb().table(table).select(select)
        if filters:
            for k, v in filters.items():
                q = q.eq(k, v)
        if order:
            q = q.order(order)
        if limit:
            q = q.limit(limit)
        res = q.execute()
        return pd.DataFrame(res.data or [])
    except Exception:
        return None

def _sb_upsert(table, data, conflict):
    try:
        get_sb().table(table).upsert(data, on_conflict=conflict).execute()
        return True
    except Exception as e:
        print(f"SB upsert {table}: {e}")
        return False

def _sb_one(table, select="*", filters=None):
    try:
        q = get_sb().table(table).select(select)
        if filters:
            for k, v in filters.items():
                q = q.eq(k, v)
        res = q.limit(1).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

# ── DATA GURU ─────────────────────────────────────────────────────
GURU_DATA = [
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
    "Akim, S.Pd":          ["PJOK"],
    "Syirojudin, S.Pd":    ["PJOK"],
    "Munawir, S.Pd":       ["PADB"],
    "H. Mukhlasin, S.Pd":  ["PADB"],
    "Ari Rivaldi, S.Pd":   ["TIK"],
    "Assadulloh, SE":      ["TIK"],
    "Ilhamul Karim, S.Pd": ["B. Arab"],
    "Fuad Arif, S.Pd":     ["B. Inggris"],
    "Ayu Suraya, S.Pd":    ["Tahfidh"],
}

# ── INIT ─────────────────────────────────────────────────────────
def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE, kelas TEXT,
            status TEXT DEFAULT 'Aktif', nuptk TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS mapel_guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER REFERENCES guru(id), mapel TEXT NOT NULL,
            UNIQUE(guru_id, mapel)
        );
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL, kelas TEXT NOT NULL,
            status TEXT DEFAULT 'Aktif',
            nis TEXT DEFAULT '', nisn TEXT DEFAULT '',
            alamat TEXT DEFAULT '', fase TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS absen_guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER REFERENCES guru(id),
            tanggal TEXT NOT NULL, status TEXT NOT NULL,
            keterangan TEXT DEFAULT '',
            UNIQUE(guru_id, tanggal)
        );
        CREATE TABLE IF NOT EXISTS absen_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER, guru_id INTEGER,
            tanggal TEXT NOT NULL, status TEXT NOT NULL,
            keterangan TEXT DEFAULT '',
            UNIQUE(siswa_id, tanggal)
        );
        CREATE TABLE IF NOT EXISTS jurnal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER, tanggal TEXT NOT NULL,
            kelas TEXT NOT NULL, mapel TEXT NOT NULL,
            topik TEXT NOT NULL, aktivitas TEXT NOT NULL,
            media TEXT DEFAULT '', catatan TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER, guru_id INTEGER,
            semester TEXT, tahun_ajar TEXT, mapel TEXT,
            pengetahuan REAL, keterampilan REAL,
            sikap TEXT DEFAULT 'B', capaian TEXT DEFAULT '',
            UNIQUE(siswa_id, semester, tahun_ajar, mapel)
        );
        CREATE TABLE IF NOT EXISTS nilai_tp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER, guru_id INTEGER, kelas TEXT,
            semester TEXT, tahun_ajar TEXT, mapel TEXT,
            tp1 REAL, tp2 REAL, tp3 REAL, tp4 REAL, tp5 REAL,
            tp6 REAL, tp7 REAL, tp8 REAL, tp9 REAL, tp10 REAL,
            asts REAL, asas REAL, nr REAL,
            capaian_maksimal TEXT DEFAULT '',
            updated_at TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(siswa_id, semester, tahun_ajar, mapel)
        );
        CREATE TABLE IF NOT EXISTS ekskul_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER, guru_id INTEGER,
            semester TEXT, tahun_ajar TEXT,
            nama_ekskul TEXT, keterangan TEXT DEFAULT '',
            UNIQUE(siswa_id, semester, tahun_ajar, nama_ekskul)
        );
        CREATE TABLE IF NOT EXISTS catatan_rapor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER, guru_id INTEGER,
            semester TEXT, tahun_ajar TEXT,
            catatan_wali TEXT DEFAULT '', tanggapan_ortu TEXT DEFAULT '',
            UNIQUE(siswa_id, semester, tahun_ajar)
        );
        CREATE TABLE IF NOT EXISTS agenda_sekolah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL, deskripsi TEXT DEFAULT '',
            tanggal TEXT NOT NULL, tanggal_end TEXT DEFAULT '',
            kategori TEXT DEFAULT 'Umum', dibuat_oleh TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS guru_kelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER REFERENCES guru(id) ON DELETE CASCADE,
            kelas TEXT NOT NULL, UNIQUE(guru_id, kelas)
        );
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER, bucket TEXT NOT NULL,
            path TEXT NOT NULL, nama_file TEXT NOT NULL,
            kategori TEXT NOT NULL, ukuran INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            UNIQUE(bucket, path)
        );
    """)
    for nama, kelas in GURU_DATA:
        try:
            conn.execute("INSERT OR IGNORE INTO guru (nama,kelas) VALUES (?,?)", (nama, kelas))
        except: pass
    conn.commit()
    for nama, mapels in MAPEL_DEFAULT.items():
        row = conn.execute("SELECT id FROM guru WHERE nama=?", (nama,)).fetchone()
        if row:
            for mp in mapels:
                try:
                    conn.execute("INSERT OR IGNORE INTO mapel_guru (guru_id,mapel) VALUES (?,?)", (row['id'], mp))
                except: pass
    rows = conn.execute("SELECT id,kelas FROM guru WHERE kelas IS NOT NULL AND kelas!=''").fetchall()
    for r in rows:
        try:
            conn.execute("INSERT OR IGNORE INTO guru_kelas (guru_id,kelas) VALUES (?,?)", (r['id'], r['kelas']))
        except: pass
    conn.commit()
    conn.close()

def init_agenda_table(): pass
def init_nilai_table(): pass
def init_nilai_tp_table(): pass
def init_guru_kelas_table(): pass
def init_file_metadata_table(): pass

def run_migrations():
    conn = get_conn()
    for sql in [
        "ALTER TABLE guru ADD COLUMN nuptk TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN nis TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN nisn TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN alamat TEXT DEFAULT ''",
        "ALTER TABLE siswa ADD COLUMN fase TEXT DEFAULT ''",
        "ALTER TABLE nilai_siswa ADD COLUMN capaian TEXT DEFAULT ''",
    ]:
        try: conn.execute(sql)
        except: pass
    conn.commit()
    conn.close()

# ── GURU ──────────────────────────────────────────────────────────
def get_all_guru():
    if sb_ok():
        df = _sb_df("guru","id,nama,kelas,status,nuptk",{"status":"Aktif"},"nama")
        if df is not None: return df
    conn = get_conn()
    df = pd.read_sql("SELECT id,nama,kelas,status,nuptk FROM guru WHERE status='Aktif' ORDER BY nama", conn)
    conn.close()
    return df

def get_guru_by_nama(nama):
    if sb_ok():
        r = _sb_one("guru","*",{"nama":nama})
        if r is not None: return r
    conn = get_conn()
    row = conn.execute("SELECT * FROM guru WHERE nama=?", (nama,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_mapel_guru(guru_id):
    if sb_ok():
        df = _sb_df("mapel_guru","mapel",{"guru_id":guru_id})
        if df is not None: return df["mapel"].tolist() if not df.empty else []
    conn = get_conn()
    rows = conn.execute("SELECT mapel FROM mapel_guru WHERE guru_id=? ORDER BY mapel", (guru_id,)).fetchall()
    conn.close()
    return [r["mapel"] for r in rows]

def add_mapel_guru(guru_id, mapel):
    if sb_ok():
        try:
            get_sb().table("mapel_guru").insert({"guru_id":guru_id,"mapel":mapel}).execute()
            return True, "OK"
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return False, "Sudah ada"
    try:
        conn = get_conn()
        conn.execute("INSERT OR IGNORE INTO mapel_guru (guru_id,mapel) VALUES (?,?)", (guru_id, mapel))
        conn.commit(); conn.close()
        return True, "OK"
    except Exception as e:
        return False, str(e)

def delete_mapel_guru(guru_id, mapel):
    if sb_ok():
        try:
            get_sb().table("mapel_guru").delete().eq("guru_id",guru_id).eq("mapel",mapel).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("DELETE FROM mapel_guru WHERE guru_id=? AND mapel=?", (guru_id, mapel))
    conn.commit(); conn.close()

def update_nuptk(guru_id, nuptk):
    if sb_ok():
        try:
            get_sb().table("guru").update({"nuptk":nuptk}).eq("id",guru_id).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("UPDATE guru SET nuptk=? WHERE id=?", (nuptk, guru_id))
    conn.commit(); conn.close()

def get_nuptk(guru_id):
    if sb_ok():
        r = _sb_one("guru","nuptk",{"id":guru_id})
        if r is not None: return r.get("nuptk","")
    try:
        conn = get_conn()
        row = conn.execute("SELECT nuptk FROM guru WHERE id=?", (guru_id,)).fetchone()
        conn.close()
        return row["nuptk"] if row and row["nuptk"] else ""
    except: return ""

def get_kelas_guru(guru_id):
    if sb_ok():
        df = _sb_df("guru_kelas","kelas",{"guru_id":guru_id})
        if df is not None and not df.empty: return df["kelas"].tolist()
        if df is not None:
            r = _sb_one("guru","kelas",{"id":guru_id})
            return [r["kelas"]] if r and r.get("kelas") else []
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT DISTINCT COALESCE(gk.kelas, g.kelas) as kelas
            FROM guru g LEFT JOIN guru_kelas gk ON gk.guru_id=g.id
            WHERE g.id=? ORDER BY kelas
        """, (guru_id,)).fetchall()
        conn.close()
        return [r["kelas"] for r in rows if r["kelas"]]
    except: return []

def tambah_guru_kelas(guru_id, kelas):
    if sb_ok():
        try:
            get_sb().table("guru_kelas").insert({"guru_id":guru_id,"kelas":kelas}).execute()
            return True
        except: return False
    try:
        conn = get_conn()
        conn.execute("INSERT OR IGNORE INTO guru_kelas (guru_id,kelas) VALUES (?,?)", (guru_id, kelas))
        conn.commit(); conn.close()
        return True
    except: return False

def hapus_guru_kelas(guru_id, kelas):
    if sb_ok():
        try:
            get_sb().table("guru_kelas").delete().eq("guru_id",guru_id).eq("kelas",kelas).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("DELETE FROM guru_kelas WHERE guru_id=? AND kelas=?", (guru_id, kelas))
    conn.commit(); conn.close()

def get_guru_by_kelas(kelas):
    if sb_ok():
        try:
            df = _sb_df("guru_kelas","guru_id",{"kelas":kelas})
            if df is not None and not df.empty:
                ids = df["guru_id"].tolist()
                res = get_sb().table("guru").select("id,nama,kelas").in_("id",ids).execute()
                return res.data or []
        except: pass
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT DISTINCT g.id,g.nama,g.kelas FROM guru g
            LEFT JOIN guru_kelas gk ON gk.guru_id=g.id
            WHERE (g.kelas=? OR gk.kelas=?) AND g.status='Aktif'
        """, (kelas, kelas)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except: return []

# ── SISWA ─────────────────────────────────────────────────────────
def get_siswa_by_kelas(kelas):
    if sb_ok():
        df = _sb_df("siswa","id,nama,kelas,status",{"kelas":kelas,"status":"Aktif"},"nama")
        if df is not None: return df
    conn = get_conn()
    df = pd.read_sql("SELECT id,nama,kelas,status FROM siswa WHERE kelas=? AND status='Aktif' ORDER BY nama", conn, params=[kelas])
    conn.close()
    return df

def get_siswa_by_kelas_lengkap(kelas):
    if sb_ok():
        df = _sb_df("siswa","*",{"kelas":kelas,"status":"Aktif"},"nama")
        if df is not None: return df
    try:
        conn = get_conn()
        df = pd.read_sql("SELECT * FROM siswa WHERE kelas=? AND status='Aktif' ORDER BY nama", conn, params=[kelas])
        conn.close()
        return df
    except: return get_siswa_by_kelas(kelas)

def add_siswa_bulk(names, kelas):
    for nama in names:
        if sb_ok():
            try:
                get_sb().table("siswa").insert({"nama":nama.strip(),"kelas":kelas,"status":"Aktif"}).execute()
                continue
            except: pass
        try:
            conn = get_conn()
            conn.execute("INSERT OR IGNORE INTO siswa (nama,kelas) VALUES (?,?)", (nama.strip(), kelas))
            conn.commit(); conn.close()
        except: pass

def add_siswa_lengkap(nama, kelas, nis="", nisn="", alamat="", fase=""):
    data = {"nama":nama.strip(),"kelas":kelas,"status":"Aktif","nis":nis,"nisn":nisn,"alamat":alamat,"fase":fase}
    if sb_ok():
        try:
            get_sb().table("siswa").insert(data).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO siswa (nama,kelas,nis,nisn,alamat,fase) VALUES (?,?,?,?,?,?)",
                 (nama.strip(),kelas,nis,nisn,alamat,fase))
    conn.commit(); conn.close()

def update_siswa_info(siswa_id, nis="", nisn="", alamat="", fase=""):
    data = {"nis":nis,"nisn":nisn,"alamat":alamat,"fase":fase}
    if sb_ok():
        try:
            get_sb().table("siswa").update(data).eq("id",siswa_id).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("UPDATE siswa SET nis=?,nisn=?,alamat=?,fase=? WHERE id=?", (nis,nisn,alamat,fase,siswa_id))
    conn.commit(); conn.close()

def get_semua_kelas():
    if sb_ok():
        try:
            res = get_sb().table("guru").select("kelas").neq("kelas","Semua Tingkat").execute()
            return sorted(set(r["kelas"] for r in res.data if r.get("kelas")))
        except: pass
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT kelas FROM guru WHERE kelas!='Semua Tingkat' AND kelas IS NOT NULL ORDER BY kelas").fetchall()
    conn.close()
    return [r["kelas"] for r in rows]

# ── ABSENSI GURU ──────────────────────────────────────────────────
def get_absen_guru_hari(tanggal):
    all_g = get_all_guru()
    if sb_ok():
        try:
            res = get_sb().table("absen_guru").select("guru_id,status,keterangan").eq("tanggal",tanggal).execute()
            filled = {r["guru_id"]: r for r in res.data}
            rows = []
            for _, g in all_g.iterrows():
                ab = filled.get(g["id"], {})
                rows.append({"id":g["id"],"nama":g["nama"],"kelas":g["kelas"],
                             "status":ab.get("status","?"),"keterangan":ab.get("keterangan",""),
                             "sudah_isi":1 if ab else 0})
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    df = pd.read_sql("""
        SELECT g.id, g.nama, g.kelas,
               COALESCE(a.status,'?') as status,
               COALESCE(a.keterangan,'') as keterangan,
               CASE WHEN a.id IS NULL THEN 0 ELSE 1 END as sudah_isi
        FROM guru g
        LEFT JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal=?
        WHERE g.status='Aktif' ORDER BY g.kelas,g.nama
    """, conn, params=[tanggal])
    conn.close()
    return df

def upsert_absen_guru(guru_id, tanggal, status, keterangan=""):
    data = {"guru_id":guru_id,"tanggal":tanggal,"status":status,"keterangan":keterangan}
    if sb_ok():
        try:
            get_sb().table("absen_guru").upsert(data, on_conflict="guru_id,tanggal").execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("""INSERT INTO absen_guru (guru_id,tanggal,status,keterangan) VALUES (?,?,?,?)
        ON CONFLICT(guru_id,tanggal) DO UPDATE SET status=excluded.status,keterangan=excluded.keterangan""",
        (guru_id,tanggal,status,keterangan))
    conn.commit(); conn.close()

def get_status_absen_guru(guru_id, tanggal):
    if sb_ok():
        r = _sb_one("absen_guru","status,keterangan",{"guru_id":guru_id,"tanggal":tanggal})
        return r
    conn = get_conn()
    row = conn.execute("SELECT status,keterangan FROM absen_guru WHERE guru_id=? AND tanggal=?",(guru_id,tanggal)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_absen_guru_rekap(bulan, tahun):
    bulan_str = f"{tahun}-{str(bulan).zfill(2)}"
    if sb_ok():
        try:
            from collections import defaultdict
            g_res = get_sb().table("guru").select("id,nama,kelas").eq("status","Aktif").execute()
            a_res = get_sb().table("absen_guru").select("guru_id,status").like("tanggal",f"{bulan_str}%").execute()
            counts = defaultdict(lambda: {"H":0,"A":0,"I":0,"S":0,"total":0})
            for a in a_res.data:
                gid = a["guru_id"]; st = a["status"]
                if st in counts[gid]: counts[gid][st] += 1
                counts[gid]["total"] += 1
            rows = []
            for g in g_res.data:
                c = counts[g["id"]]
                rows.append({"nama":g["nama"],"kelas":g["kelas"],
                    "hadir":c["H"],"alpa":c["A"],"izin":c["I"],"sakit":c["S"],"total_hari":c["total"]})
            return pd.DataFrame(rows).sort_values("nama")
        except: pass
    conn = get_conn()
    df = pd.read_sql("""
        SELECT g.nama, g.kelas,
               SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END) as hadir,
               SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) as alpa,
               SUM(CASE WHEN a.status='I' THEN 1 ELSE 0 END) as izin,
               SUM(CASE WHEN a.status='S' THEN 1 ELSE 0 END) as sakit,
               COUNT(a.id) as total_hari
        FROM guru g LEFT JOIN absen_guru a ON a.guru_id=g.id AND a.tanggal LIKE ?
        WHERE g.status='Aktif' GROUP BY g.id ORDER BY g.nama
    """, conn, params=[f"{bulan_str}%"])
    conn.close()
    return df

def get_guru_tidak_hadir(tanggal):
    df = get_absen_guru_hari(tanggal)
    return df[df["status"] != "H"] if not df.empty else df

def get_summary_hari(tanggal):
    df = get_absen_guru_hari(tanggal)
    total  = len(df)
    hadir  = len(df[df["status"]=="H"])
    jurnal = 0
    if sb_ok():
        try:
            res = get_sb().table("jurnal").select("id",count="exact").eq("tanggal",tanggal).execute()
            jurnal = res.count or 0
        except: pass
    else:
        try:
            conn = get_conn()
            jurnal = conn.execute("SELECT COUNT(*) FROM jurnal WHERE tanggal=?", (tanggal,)).fetchone()[0]
            conn.close()
        except: pass
    return {"total_guru":total,"hadir_guru":hadir,"absen_guru":total-hadir,"jurnal_hari":jurnal}

# ── ABSENSI SISWA ─────────────────────────────────────────────────
def get_absen_siswa_hari(kelas, tanggal):
    df_s = get_siswa_by_kelas(kelas)
    if df_s.empty: return pd.DataFrame(columns=["id","nama","status","keterangan"])
    if sb_ok():
        try:
            sids = df_s["id"].tolist()
            res  = get_sb().table("absen_siswa").select("siswa_id,status,keterangan")\
                .eq("tanggal",tanggal).in_("siswa_id",sids).execute()
            filled = {r["siswa_id"]: r for r in res.data}
            rows = [{"id":int(r["id"]),"nama":r["nama"],
                     "status":filled.get(int(r["id"]),{}).get("status","H"),
                     "keterangan":filled.get(int(r["id"]),{}).get("keterangan","")}
                    for _, r in df_s.iterrows()]
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.id, s.nama, COALESCE(a.status,'H') as status, COALESCE(a.keterangan,'') as keterangan
        FROM siswa s LEFT JOIN absen_siswa a ON a.siswa_id=s.id AND a.tanggal=?
        WHERE s.kelas=? AND s.status='Aktif' ORDER BY s.nama
    """, conn, params=[tanggal, kelas])
    conn.close()
    return df

def upsert_absen_siswa_bulk(data, guru_id, tanggal):
    for siswa_id, status, keterangan in data:
        d = {"siswa_id":siswa_id,"guru_id":guru_id,"tanggal":tanggal,"status":status,"keterangan":keterangan}
        if sb_ok():
            try:
                get_sb().table("absen_siswa").upsert(d, on_conflict="siswa_id,tanggal").execute()
                continue
            except: pass
        try:
            conn = get_conn()
            conn.execute("""INSERT INTO absen_siswa (siswa_id,guru_id,tanggal,status,keterangan) VALUES (?,?,?,?,?)
                ON CONFLICT(siswa_id,tanggal) DO UPDATE SET status=excluded.status,keterangan=excluded.keterangan""",
                (siswa_id,guru_id,tanggal,status,keterangan))
            conn.commit(); conn.close()
        except: pass

def get_absen_siswa_rekap(kelas, bulan, tahun):
    bulan_str = f"{tahun}-{str(bulan).zfill(2)}"
    df_s = get_siswa_by_kelas(kelas)
    if df_s.empty: return pd.DataFrame()
    if sb_ok():
        try:
            from collections import defaultdict
            sids = df_s["id"].tolist()
            res  = get_sb().table("absen_siswa").select("siswa_id,status")\
                .in_("siswa_id",sids).like("tanggal",f"{bulan_str}%").execute()
            counts = defaultdict(lambda: {"H":0,"A":0,"I":0,"S":0,"total":0})
            for a in res.data:
                sid = a["siswa_id"]; st = a["status"]
                if st in counts[sid]: counts[sid][st] += 1
                counts[sid]["total"] += 1
            rows = []
            for _, s in df_s.iterrows():
                c = counts[s["id"]]; total = c["total"] or 0; h = c["H"]
                rows.append({"nama":s["nama"],"hadir":h,"alpa":c["A"],"izin":c["I"],
                             "sakit":c["S"],"total_hari":total,
                             "pct_hadir":round(h/total*100,1) if total else 0})
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.nama,
               SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END) as hadir,
               SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) as alpa,
               SUM(CASE WHEN a.status='I' THEN 1 ELSE 0 END) as izin,
               SUM(CASE WHEN a.status='S' THEN 1 ELSE 0 END) as sakit,
               COUNT(a.id) as total_hari
        FROM siswa s LEFT JOIN absen_siswa a ON a.siswa_id=s.id AND a.tanggal LIKE ?
        WHERE s.kelas=? AND s.status='Aktif' GROUP BY s.id ORDER BY s.nama
    """, conn, params=[f"{bulan_str}%", kelas])
    conn.close()
    if not df.empty:
        df["pct_hadir"] = df.apply(lambda r: round(r["hadir"]/r["total_hari"]*100,1) if r["total_hari"] else 0, axis=1)
    return df

def get_siswa_tidak_hadir(tanggal):
    if sb_ok():
        try:
            res = get_sb().table("absen_siswa").select("siswa_id,status").eq("tanggal",tanggal).neq("status","H").execute()
            if not res.data: return pd.DataFrame()
            sids  = [r["siswa_id"] for r in res.data]
            s_res = get_sb().table("siswa").select("id,nama,kelas").in_("id",sids).execute()
            s_map = {s["id"]: s for s in s_res.data}
            st_map= {r["siswa_id"]: r["status"] for r in res.data}
            rows  = [{"nama":s_map[sid]["nama"],"kelas":s_map[sid]["kelas"],"status":st_map[sid]}
                     for sid in sids if sid in s_map]
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    df = pd.read_sql("""
        SELECT s.nama, s.kelas, a.status FROM absen_siswa a
        JOIN siswa s ON s.id=a.siswa_id WHERE a.tanggal=? AND a.status!='H'
    """, conn, params=[tanggal])
    conn.close()
    return df

# ── JURNAL ────────────────────────────────────────────────────────
def simpan_jurnal(guru_id, tanggal, kelas, mapel, topik, aktivitas, media="", catatan=""):
    data = {"guru_id":guru_id,"tanggal":tanggal,"kelas":kelas,"mapel":mapel,
            "topik":topik,"aktivitas":aktivitas,"media":media,"catatan":catatan}
    if sb_ok():
        try:
            get_sb().table("jurnal").insert(data).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("INSERT INTO jurnal (guru_id,tanggal,kelas,mapel,topik,aktivitas,media,catatan) VALUES (?,?,?,?,?,?,?,?)",
        (guru_id,tanggal,kelas,mapel,topik,aktivitas,media,catatan))
    conn.commit(); conn.close()

def get_jurnal_guru(guru_id, limit=20):
    if sb_ok():
        try:
            res = get_sb().table("jurnal").select("*").eq("guru_id",guru_id)\
                .order("tanggal",desc=True).limit(limit).execute()
            return pd.DataFrame(res.data or [])
        except: pass
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM jurnal WHERE guru_id=? ORDER BY tanggal DESC LIMIT ?", conn, params=[guru_id,limit])
    conn.close()
    return df

def get_jurnal_semua(tanggal=None, limit=50):
    if sb_ok():
        try:
            q = get_sb().table("jurnal").select("*, guru:guru_id(nama)")
            if tanggal: q = q.eq("tanggal",tanggal)
            res = q.order("tanggal",desc=True).limit(limit).execute()
            rows = []
            for r in res.data or []:
                r["guru_nama"] = r.get("guru",{}).get("nama","") if isinstance(r.get("guru"),dict) else ""
                rows.append(r)
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    sql    = "SELECT j.*, g.nama as guru_nama FROM jurnal j JOIN guru g ON g.id=j.guru_id"
    params = []
    if tanggal:
        sql += " WHERE j.tanggal=?"
        params.append(tanggal)
    sql += f" ORDER BY j.tanggal DESC LIMIT {limit}"
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df

def get_jurnal_by_kelas(kelas, limit=100):
    if sb_ok():
        try:
            res = get_sb().table("jurnal").select("*, guru:guru_id(nama)")\
                .eq("kelas",kelas).order("tanggal",desc=True).limit(limit).execute()
            rows = []
            for r in res.data or []:
                r["guru_nama"] = r.get("guru",{}).get("nama","") if isinstance(r.get("guru"),dict) else ""
                rows.append(r)
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    df = pd.read_sql("""SELECT j.*,g.nama as guru_nama FROM jurnal j
        JOIN guru g ON g.id=j.guru_id WHERE j.kelas=? ORDER BY j.tanggal DESC LIMIT ?""",
        conn, params=[kelas, limit])
    conn.close()
    return df

# ── AGENDA ────────────────────────────────────────────────────────
def tambah_agenda(judul, deskripsi, tanggal, tanggal_end, kategori, dibuat_oleh):
    tgl = str(tanggal); tgl_end = str(tanggal_end) if tanggal_end else ""
    data = {"judul":judul,"deskripsi":deskripsi,"tanggal":tgl,"tanggal_end":tgl_end,
            "kategori":kategori,"dibuat_oleh":dibuat_oleh}
    if sb_ok():
        try:
            get_sb().table("agenda_sekolah").insert(data).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("INSERT INTO agenda_sekolah (judul,deskripsi,tanggal,tanggal_end,kategori,dibuat_oleh) VALUES (?,?,?,?,?,?)",
        (judul,deskripsi,tgl,tgl_end,kategori,dibuat_oleh))
    conn.commit(); conn.close()

def hapus_agenda(agenda_id):
    if sb_ok():
        try:
            get_sb().table("agenda_sekolah").delete().eq("id",agenda_id).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("DELETE FROM agenda_sekolah WHERE id=?", (agenda_id,))
    conn.commit(); conn.close()

def get_agenda_mendatang():
    today = str(date.today())
    if sb_ok():
        try:
            res = get_sb().table("agenda_sekolah").select("*").gte("tanggal",today).order("tanggal").execute()
            return pd.DataFrame(res.data or [])
        except: pass
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM agenda_sekolah WHERE tanggal>=? ORDER BY tanggal", conn, params=[today])
    conn.close()
    return df

def get_agenda_semua(limit=200):
    if sb_ok():
        try:
            res = get_sb().table("agenda_sekolah").select("*").order("tanggal",desc=True).limit(limit).execute()
            return pd.DataFrame(res.data or [])
        except: pass
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM agenda_sekolah ORDER BY tanggal DESC LIMIT {limit}", conn)
    conn.close()
    return df

# ── NILAI (legacy) ────────────────────────────────────────────────
def upsert_nilai(siswa_id, guru_id, semester, tahun_ajar, mapel, p, k, s):
    data = {"siswa_id":siswa_id,"guru_id":guru_id,"semester":semester,"tahun_ajar":tahun_ajar,
            "mapel":mapel,"pengetahuan":p,"keterampilan":k,"sikap":s}
    if sb_ok():
        try:
            get_sb().table("nilai_siswa").upsert(data, on_conflict="siswa_id,semester,tahun_ajar,mapel").execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("""INSERT INTO nilai_siswa (siswa_id,guru_id,semester,tahun_ajar,mapel,pengetahuan,keterampilan,sikap)
        VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(siswa_id,semester,tahun_ajar,mapel)
        DO UPDATE SET pengetahuan=excluded.pengetahuan,keterampilan=excluded.keterampilan,sikap=excluded.sikap""",
        (siswa_id,guru_id,semester,tahun_ajar,mapel,p,k,s))
    conn.commit(); conn.close()

def get_nilai_kelas(kelas, semester, tahun_ajar):
    df_s = get_siswa_by_kelas(kelas)
    if df_s.empty: return pd.DataFrame()
    if sb_ok():
        try:
            sids = df_s["id"].tolist()
            res  = get_sb().table("nilai_siswa").select("siswa_id,mapel,pengetahuan,keterampilan,sikap")\
                .in_("siswa_id",sids).eq("semester",semester).eq("tahun_ajar",tahun_ajar).execute()
            s_map = {int(s["id"]):s["nama"] for _,s in df_s.iterrows()}
            rows  = [{"siswa_id":r["siswa_id"],"siswa":s_map.get(r["siswa_id"],""),
                      "mapel":r["mapel"],"pengetahuan":r["pengetahuan"],
                      "keterampilan":r["keterampilan"],"sikap":r["sikap"]} for r in res.data]
            return pd.DataFrame(rows)
        except: pass
    conn = get_conn()
    sids = df_s["id"].tolist()
    ph   = ",".join(["?"]*len(sids))
    df   = pd.read_sql(f"""SELECT n.siswa_id, s.nama as siswa, n.mapel,n.pengetahuan,n.keterampilan,n.sikap
        FROM nilai_siswa n JOIN siswa s ON s.id=n.siswa_id
        WHERE n.siswa_id IN ({ph}) AND n.semester=? AND n.tahun_ajar=?""",
        conn, params=sids+[semester,tahun_ajar])
    conn.close()
    return df

def get_nilai_siswa(siswa_id, semester, tahun_ajar):
    if sb_ok():
        try:
            res = get_sb().table("nilai_siswa").select("mapel,pengetahuan,keterampilan,sikap,capaian")\
                .eq("siswa_id",siswa_id).eq("semester",semester).eq("tahun_ajar",tahun_ajar).execute()
            return pd.DataFrame(res.data or [])
        except: pass
    conn = get_conn()
    df = pd.read_sql("SELECT mapel,pengetahuan,keterampilan,sikap,capaian FROM nilai_siswa WHERE siswa_id=? AND semester=? AND tahun_ajar=?",
        conn, params=[siswa_id,semester,tahun_ajar])
    conn.close()
    return df

def get_nilai_satu_siswa_mapel(siswa_id, semester, tahun_ajar, mapel):
    if sb_ok():
        r = _sb_one("nilai_siswa","pengetahuan,keterampilan,sikap",
                    {"siswa_id":siswa_id,"semester":semester,"tahun_ajar":tahun_ajar,"mapel":mapel})
        return r
    conn = get_conn()
    row = conn.execute("SELECT pengetahuan,keterampilan,sikap FROM nilai_siswa WHERE siswa_id=? AND semester=? AND tahun_ajar=? AND mapel=?",
        (siswa_id,semester,tahun_ajar,mapel)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_predikat(nilai):
    if nilai is None: return "-"
    if nilai >= 90: return "A"
    if nilai >= 80: return "B"
    if nilai >= 70: return "C"
    return "D"

# ── NILAI TP ──────────────────────────────────────────────────────
def hitung_nr(tp_dict):
    """NR = rata-rata TP (50%) + ASTS (25%) + ASAS (25%)."""
    tp_vals = []
    for c in ['tp1','tp2','tp3','tp4','tp5','tp6','tp7','tp8','tp9','tp10']:
        v = tp_dict.get(c)
        if v is not None and str(v).strip() not in ('','None','nan'):
            try: tp_vals.append(float(v))
            except: pass
    rata_tp = sum(tp_vals)/len(tp_vals) if tp_vals else None

    def safe_float(val):
        try:
            return float(val) if val is not None and str(val).strip() not in ('','None','nan') else None
        except: return None

    asts = safe_float(tp_dict.get('asts'))
    asas = safe_float(tp_dict.get('asas'))

    if rata_tp is not None and asts is not None and asas is not None:
        return round((rata_tp * 0.5) + (asts * 0.25) + (asas * 0.25), 2)
    elif rata_tp is not None and asts is not None:
        return round((rata_tp * 0.667) + (asts * 0.333), 2)
    elif rata_tp is not None and asas is not None:
        return round((rata_tp * 0.667) + (asas * 0.333), 2)
    elif rata_tp is not None:
        return round(rata_tp, 2)
    elif asts is not None and asas is not None:
        return round((asts + asas) / 2, 2)
    return 0.0

def upsert_nilai_tp(siswa_id, guru_id, kelas, semester, tahun_ajar, mapel, tp_dict, capaian=""):
    nr   = hitung_nr(tp_dict)
    data = {"siswa_id":siswa_id,"guru_id":guru_id,"kelas":kelas,"semester":semester,
            "tahun_ajar":tahun_ajar,"mapel":mapel,"nr":nr,"capaian_maksimal":capaian}
    for c in TP_COLS:
        data[c] = tp_dict.get(c)
    if sb_ok():
        try:
            get_sb().table("nilai_tp").upsert(data, on_conflict="siswa_id,semester,tahun_ajar,mapel").execute()
            return nr
        except Exception as e:
            print(f"upsert_nilai_tp sb: {e}")
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO nilai_tp
            (siswa_id,guru_id,kelas,semester,tahun_ajar,mapel,
             tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9,tp10,asts,asas,nr,capaian_maksimal)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(siswa_id,semester,tahun_ajar,mapel) DO UPDATE SET
            guru_id=excluded.guru_id,kelas=excluded.kelas,
            tp1=excluded.tp1,tp2=excluded.tp2,tp3=excluded.tp3,tp4=excluded.tp4,tp5=excluded.tp5,
            tp6=excluded.tp6,tp7=excluded.tp7,tp8=excluded.tp8,tp9=excluded.tp9,tp10=excluded.tp10,
            asts=excluded.asts,asas=excluded.asas,nr=excluded.nr,capaian_maksimal=excluded.capaian_maksimal""",
            (siswa_id,guru_id,kelas,semester,tahun_ajar,mapel,
             data.get("tp1"),data.get("tp2"),data.get("tp3"),data.get("tp4"),data.get("tp5"),
             data.get("tp6"),data.get("tp7"),data.get("tp8"),data.get("tp9"),data.get("tp10"),
             data.get("asts"),data.get("asas"),nr,capaian))
        conn.commit(); conn.close()
    except Exception as e:
        print(f"upsert_nilai_tp sqlite: {e}")
    return nr

def get_nilai_tp_siswa(siswa_id, semester, tahun_ajar, mapel):
    if sb_ok():
        r = _sb_one("nilai_tp","*",{"siswa_id":siswa_id,"semester":semester,"tahun_ajar":tahun_ajar,"mapel":mapel})
        if r is not None: return r
    try:
        conn = get_conn()
        row  = conn.execute("""SELECT tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9,tp10,asts,asas,nr,capaian_maksimal
            FROM nilai_tp WHERE siswa_id=? AND semester=? AND tahun_ajar=? AND mapel=?""",
            (siswa_id,semester,tahun_ajar,mapel)).fetchone()
        conn.close()
        return dict(row) if row else {}
    except: return {}

def get_nilai_tp_kelas(kelas, semester, tahun_ajar, mapel):
    df_s = get_siswa_by_kelas(kelas)
    if df_s.empty: return pd.DataFrame()
    if sb_ok():
        try:
            sids = df_s["id"].tolist()
            res  = get_sb().table("nilai_tp").select("*").in_("siswa_id",sids)\
                .eq("semester",semester).eq("tahun_ajar",tahun_ajar).eq("mapel",mapel).execute()
            n_map = {r["siswa_id"]:r for r in res.data}
            rows  = []
            for _, s in df_s.sort_values("nama").iterrows():
                n = n_map.get(s["id"],{})
                rows.append({"siswa_id":s["id"],"siswa":s["nama"],
                    **{c:n.get(c) for c in TP_COLS},
                    "nr":n.get("nr"),"capaian_maksimal":n.get("capaian_maksimal","")})
            return pd.DataFrame(rows)
        except: pass
    try:
        conn = get_conn()
        sids = df_s["id"].tolist()
        ph   = ",".join(["?"]*len(sids))
        df   = pd.read_sql(f"""SELECT s.id as siswa_id,s.nama as siswa,
            n.tp1,n.tp2,n.tp3,n.tp4,n.tp5,n.tp6,n.tp7,n.tp8,n.tp9,n.tp10,n.asts,n.asas,n.nr,n.capaian_maksimal
            FROM siswa s LEFT JOIN nilai_tp n ON n.siswa_id=s.id
            AND n.semester=? AND n.tahun_ajar=? AND n.mapel=?
            WHERE s.id IN ({ph}) AND s.status='Aktif' ORDER BY s.nama""",
            conn, params=[semester,tahun_ajar,mapel]+sids)
        conn.close()
        return df
    except: return pd.DataFrame()

def get_nr_semua_mapel_siswa(siswa_id, semester, tahun_ajar):
    if sb_ok():
        try:
            res = get_sb().table("nilai_tp").select("mapel,nr,capaian_maksimal")\
                .eq("siswa_id",siswa_id).eq("semester",semester).eq("tahun_ajar",tahun_ajar).execute()
            return pd.DataFrame(res.data or [])
        except: pass
    try:
        conn = get_conn()
        df   = pd.read_sql("SELECT mapel,nr,capaian_maksimal FROM nilai_tp WHERE siswa_id=? AND semester=? AND tahun_ajar=? ORDER BY mapel",
            conn, params=[siswa_id,semester,tahun_ajar])
        conn.close()
        return df
    except: return pd.DataFrame()

def get_rekap_nr_kelas(kelas, semester, tahun_ajar):
    df_s = get_siswa_by_kelas(kelas)
    if df_s.empty: return pd.DataFrame()
    if sb_ok():
        try:
            sids = df_s["id"].tolist()
            res  = get_sb().table("nilai_tp").select("siswa_id,mapel,nr,capaian_maksimal")\
                .in_("siswa_id",sids).eq("semester",semester).eq("tahun_ajar",tahun_ajar).execute()
            s_map = {int(s["id"]):s["nama"] for _,s in df_s.iterrows()}
            rows  = [{"siswa_id":r["siswa_id"],"siswa":s_map.get(r["siswa_id"],""),
                      "mapel":r["mapel"],"nr":r["nr"],"capaian_maksimal":r.get("capaian_maksimal","")}
                     for r in res.data]
            return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["siswa_id","siswa","mapel","nr","capaian_maksimal"])
        except: pass
    try:
        conn = get_conn()
        sids = df_s["id"].tolist()
        ph   = ",".join(["?"]*len(sids))
        df   = pd.read_sql(f"""SELECT s.id as siswa_id,s.nama as siswa,n.mapel,n.nr,n.capaian_maksimal
            FROM siswa s LEFT JOIN nilai_tp n ON n.siswa_id=s.id AND n.semester=? AND n.tahun_ajar=?
            WHERE s.id IN ({ph}) AND s.status='Aktif' ORDER BY s.nama,n.mapel""",
            conn, params=[semester,tahun_ajar]+sids)
        conn.close()
        return df
    except: return pd.DataFrame()

# ── EKSKUL & CATATAN ──────────────────────────────────────────────
def upsert_ekskul(siswa_id, guru_id, semester, tahun_ajar, nama_ekskul, keterangan):
    data = {"siswa_id":siswa_id,"guru_id":guru_id,"semester":semester,"tahun_ajar":tahun_ajar,
            "nama_ekskul":nama_ekskul,"keterangan":keterangan}
    if sb_ok():
        try:
            get_sb().table("ekskul_siswa").upsert(data, on_conflict="siswa_id,semester,tahun_ajar,nama_ekskul").execute()
            return
        except: pass
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO ekskul_siswa (siswa_id,guru_id,semester,tahun_ajar,nama_ekskul,keterangan)
            VALUES (?,?,?,?,?,?) ON CONFLICT(siswa_id,semester,tahun_ajar,nama_ekskul)
            DO UPDATE SET keterangan=excluded.keterangan""",
            (siswa_id,guru_id,semester,tahun_ajar,nama_ekskul,keterangan))
        conn.commit(); conn.close()
    except: pass

def get_ekskul_siswa(siswa_id, semester, tahun_ajar):
    if sb_ok():
        try:
            res = get_sb().table("ekskul_siswa").select("nama_ekskul,keterangan")\
                .eq("siswa_id",siswa_id).eq("semester",semester).eq("tahun_ajar",tahun_ajar).execute()
            return pd.DataFrame(res.data or [])
        except: pass
    try:
        conn = get_conn()
        df   = pd.read_sql("SELECT nama_ekskul,keterangan FROM ekskul_siswa WHERE siswa_id=? AND semester=? AND tahun_ajar=? ORDER BY id",
            conn, params=[siswa_id,semester,tahun_ajar])
        conn.close()
        return df
    except: return pd.DataFrame()

def upsert_catatan(siswa_id, guru_id, semester, tahun_ajar, catatan_wali, tanggapan_ortu=""):
    data = {"siswa_id":siswa_id,"guru_id":guru_id,"semester":semester,"tahun_ajar":tahun_ajar,
            "catatan_wali":catatan_wali,"tanggapan_ortu":tanggapan_ortu}
    if sb_ok():
        try:
            get_sb().table("catatan_rapor").upsert(data, on_conflict="siswa_id,semester,tahun_ajar").execute()
            return
        except: pass
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO catatan_rapor (siswa_id,guru_id,semester,tahun_ajar,catatan_wali,tanggapan_ortu)
            VALUES (?,?,?,?,?,?) ON CONFLICT(siswa_id,semester,tahun_ajar)
            DO UPDATE SET catatan_wali=excluded.catatan_wali,tanggapan_ortu=excluded.tanggapan_ortu""",
            (siswa_id,guru_id,semester,tahun_ajar,catatan_wali,tanggapan_ortu))
        conn.commit(); conn.close()
    except: pass

def get_catatan(siswa_id, semester, tahun_ajar):
    if sb_ok():
        r = _sb_one("catatan_rapor","catatan_wali,tanggapan_ortu",
                    {"siswa_id":siswa_id,"semester":semester,"tahun_ajar":tahun_ajar})
        return r if r else {"catatan_wali":"","tanggapan_ortu":""}
    try:
        conn = get_conn()
        row  = conn.execute("SELECT catatan_wali,tanggapan_ortu FROM catatan_rapor WHERE siswa_id=? AND semester=? AND tahun_ajar=?",
            (siswa_id,semester,tahun_ajar)).fetchone()
        conn.close()
        return dict(row) if row else {"catatan_wali":"","tanggapan_ortu":""}
    except: return {"catatan_wali":"","tanggapan_ortu":""}

def get_absen_count_siswa(siswa_id, semester, tahun_ajar):
    try:
        bulan_range = [7,8,9,10,11,12] if "Ganjil" in semester else [1,2,3,4,5,6]
        tahun = tahun_ajar.split("/")[0] if "Ganjil" in semester else tahun_ajar.split("/")[1]
        result = {"S":0,"I":0,"A":0}
        if sb_ok():
            try:
                for b in bulan_range:
                    res = get_sb().table("absen_siswa").select("status")\
                        .eq("siswa_id",siswa_id).like("tanggal",f"{tahun}-{str(b).zfill(2)}%").execute()
                    for r in res.data:
                        if r["status"] in result: result[r["status"]] += 1
                return result
            except: pass
        conn = get_conn()
        for b in bulan_range:
            rows = conn.execute("SELECT status,COUNT(*) as cnt FROM absen_siswa WHERE siswa_id=? AND tanggal LIKE ? GROUP BY status",
                (siswa_id, f"{tahun}-{str(b).zfill(2)}%")).fetchall()
            for r in rows:
                if r["status"] in result: result[r["status"]] += r["cnt"]
        conn.close()
        return result
    except: return {"S":0,"I":0,"A":0}

# ── FILE METADATA ─────────────────────────────────────────────────
def simpan_metadata_file(guru_id, bucket, path, nama_file, kategori, ukuran=0):
    data = {"guru_id":guru_id,"bucket":bucket,"path":path,"nama_file":nama_file,"kategori":kategori,"ukuran":ukuran}
    if sb_ok():
        try:
            get_sb().table("file_metadata").upsert(data, on_conflict="bucket,path").execute()
            return
        except: pass
    try:
        conn = get_conn()
        conn.execute("INSERT OR REPLACE INTO file_metadata (guru_id,bucket,path,nama_file,kategori,ukuran) VALUES (?,?,?,?,?,?)",
            (guru_id,bucket,path,nama_file,kategori,ukuran))
        conn.commit(); conn.close()
    except: pass

def get_files_guru(guru_id, kategori=None):
    filters = {"guru_id":guru_id}
    if kategori: filters["kategori"] = kategori
    if sb_ok():
        df = _sb_df("file_metadata","*",filters,"created_at")
        if df is not None: return df
    try:
        conn = get_conn()
        sql  = "SELECT * FROM file_metadata WHERE guru_id=?"
        params = [guru_id]
        if kategori:
            sql += " AND kategori=?"
            params.append(kategori)
        df = pd.read_sql(sql+" ORDER BY kategori,created_at DESC", conn, params=params)
        conn.close()
        return df
    except: return pd.DataFrame()

def get_all_files_by_kategori(kategori):
    if sb_ok():
        try:
            res = get_sb().table("file_metadata").select("*, guru:guru_id(nama,kelas)")\
                .eq("kategori",kategori).order("created_at",desc=True).execute()
            rows = []
            for r in res.data or []:
                r["guru_nama"] = r.get("guru",{}).get("nama","") if isinstance(r.get("guru"),dict) else ""
                r["kelas"]     = r.get("guru",{}).get("kelas","") if isinstance(r.get("guru"),dict) else ""
                rows.append(r)
            return pd.DataFrame(rows)
        except: pass
    try:
        conn = get_conn()
        df   = pd.read_sql("""SELECT f.*,g.nama as guru_nama,g.kelas FROM file_metadata f
            JOIN guru g ON g.id=f.guru_id WHERE f.kategori=? ORDER BY f.created_at DESC""",
            conn, params=[kategori])
        conn.close()
        return df
    except: return pd.DataFrame()

def hapus_metadata_file(file_id):
    if sb_ok():
        try:
            get_sb().table("file_metadata").delete().eq("id",file_id).execute()
            return
        except: pass
    conn = get_conn()
    conn.execute("DELETE FROM file_metadata WHERE id=?", (file_id,))
    conn.commit(); conn.close()

# ── SUPABASE STORAGE ──────────────────────────────────────────────
def upload_file_storage(bucket, path, file_bytes, content_type="application/octet-stream"):
    sb = get_sb()
    if not sb: return False
    try:
        sb.storage.from_(bucket).upload(path, file_bytes, {"content-type":content_type,"upsert":"true"})
        return True
    except Exception as e:
        print(f"upload_file_storage: {e}")
        return False

def list_files_storage(bucket, folder=""):
    sb = get_sb()
    if not sb: return []
    try:
        return sb.storage.from_(bucket).list(folder) or []
    except: return []

def download_file_storage(bucket, path):
    sb = get_sb()
    if not sb: return b""
    try:
        return sb.storage.from_(bucket).download(path)
    except: return b""

def delete_file_storage(bucket, path):
    sb = get_sb()
    if not sb: return False
    try:
        sb.storage.from_(bucket).remove([path])
        return True
    except: return False


# ── TOPIK TP ──────────────────────────────────────────────────────

def init_topik_tp_table():
    conn = get_conn()
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS topik_tp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guru_id INTEGER, kelas TEXT NOT NULL,
            semester TEXT NOT NULL, tahun_ajar TEXT NOT NULL,
            mapel TEXT NOT NULL, tp_nomor INTEGER NOT NULL,
            nama_topik TEXT DEFAULT '',
            UNIQUE(guru_id,kelas,semester,tahun_ajar,mapel,tp_nomor))""")
        conn.commit()
    except Exception: pass
    conn.close()

def upsert_topik_tp(guru_id, kelas, semester, tahun_ajar, mapel, tp_nomor, nama_topik):
    data = {"guru_id":guru_id,"kelas":kelas,"semester":semester,
            "tahun_ajar":tahun_ajar,"mapel":mapel,"tp_nomor":tp_nomor,"nama_topik":nama_topik}
    sb = get_sb()
    if sb:
        try:
            sb.table("topik_tp").upsert(data, on_conflict="guru_id,kelas,semester,tahun_ajar,mapel,tp_nomor").execute()
            return
        except Exception as e: print(f"upsert_topik_tp: {e}")
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO topik_tp (guru_id,kelas,semester,tahun_ajar,mapel,tp_nomor,nama_topik)
            VALUES (?,?,?,?,?,?,?) ON CONFLICT(guru_id,kelas,semester,tahun_ajar,mapel,tp_nomor)
            DO UPDATE SET nama_topik=excluded.nama_topik""",
            (guru_id,kelas,semester,tahun_ajar,mapel,tp_nomor,nama_topik))
        conn.commit(); conn.close()
    except Exception: pass

def get_topik_tp(guru_id, kelas, semester, tahun_ajar, mapel):
    """Return dict {tp_nomor: nama_topik}."""
    sb = get_sb()
    if sb:
        try:
            res = sb.table("topik_tp").select("tp_nomor,nama_topik")                .eq("guru_id",guru_id).eq("kelas",kelas).eq("semester",semester)                .eq("tahun_ajar",tahun_ajar).eq("mapel",mapel).execute()
            return {r["tp_nomor"]: r["nama_topik"] for r in (res.data or [])}
        except Exception: pass
    try:
        conn = get_conn()
        rows = conn.execute("""SELECT tp_nomor, nama_topik FROM topik_tp
            WHERE guru_id=? AND kelas=? AND semester=? AND tahun_ajar=? AND mapel=?""",
            (guru_id,kelas,semester,tahun_ajar,mapel)).fetchall()
        conn.close()
        return {r["tp_nomor"]: r["nama_topik"] for r in rows}
    except Exception:
        return {}


# ── STAFF (TU, OB, SECURITY) ──────────────────────────────────────

STAFF_LIST = [
    {"nama": "Hadi Broto",          "jabatan": "TU"},
    {"nama": "Rudi Kurniawan, ST",  "jabatan": "TU"},
    {"nama": "Sri Suhartono",       "jabatan": "TU"},
    {"nama": "Suwarto",             "jabatan": "OB"},
    {"nama": "Hambali",             "jabatan": "OB"},
    {"nama": "Suratman",            "jabatan": "OB"},
    {"nama": "Nurhasanah",          "jabatan": "OB"},
    {"nama": "Mustakim",            "jabatan": "Security"},
]

CHECKLIST_DEFAULT = [
    "Menyapu kelas dan teras",
    "Mengepel kelas dan teras",
    "Membersihkan kamar mandi dan kloset",
    "Membersihkan wastafel",
    "Menyalakan lampu dan AC pagi/sebelum kegiatan belajar",
    "Mematikan lampu dan AC setelah kegiatan belajar",
    "Mencuci tempat/bak sampah",
    "Membersihkan saluran air",
    "Merapikan taman",
]

def init_staff_tables():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE,
            jabatan TEXT NOT NULL,
            status TEXT DEFAULT 'Aktif'
        );
        CREATE TABLE IF NOT EXISTS absen_staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER REFERENCES staff(id),
            tanggal TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT '?',
            keterangan TEXT DEFAULT '',
            UNIQUE(staff_id, tanggal)
        );
        CREATE TABLE IF NOT EXISTS checklist_ob (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER REFERENCES staff(id),
            tanggal TEXT NOT NULL,
            item TEXT NOT NULL,
            selesai INTEGER DEFAULT 0,
            urutan INTEGER DEFAULT 0,
            UNIQUE(staff_id, tanggal, item)
        );
        CREATE TABLE IF NOT EXISTS agenda_staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER REFERENCES staff(id),
            tanggal TEXT NOT NULL,
            tugas TEXT NOT NULL,
            selesai INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
    """)
    conn.commit()
    conn.close()

def seed_staff():
    sb = get_sb()
    if sb:
        try:
            res = sb.table("staff").select("id").limit(1).execute()
            if not res.data:
                for s in STAFF_LIST:
                    sb.table("staff").insert(s).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        count = conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
        if count == 0:
            for s in STAFF_LIST:
                conn.execute("INSERT OR IGNORE INTO staff (nama, jabatan) VALUES (?,?)", (s["nama"], s["jabatan"]))
            conn.commit()
        conn.close()
    except Exception: pass

def get_all_staff():
    sb = get_sb()
    if sb:
        try:
            res = sb.table("staff").select("*").eq("status","Aktif").order("jabatan").execute()
            return pd.DataFrame(res.data or [])
        except Exception: pass
    try:
        conn = get_conn()
        df = pd.read_sql("SELECT * FROM staff WHERE status='Aktif' ORDER BY jabatan, nama", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def get_staff_by_nama(nama):
    sb = get_sb()
    if sb:
        try:
            res = sb.table("staff").select("*").eq("nama", nama).limit(1).execute()
            return res.data[0] if res.data else None
        except Exception: pass
    try:
        conn = get_conn()
        row = conn.execute("SELECT * FROM staff WHERE nama=?", (nama,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None

def upsert_absen_staff(staff_id, tanggal, status, keterangan=""):
    data = {"staff_id":staff_id,"tanggal":str(tanggal),"status":status,"keterangan":keterangan}
    sb = get_sb()
    if sb:
        try:
            sb.table("absen_staff").upsert(data, on_conflict="staff_id,tanggal").execute()
            return
        except Exception as e: print(f"upsert_absen_staff: {e}")
    try:
        conn = get_conn()
        conn.execute("INSERT INTO absen_staff (staff_id,tanggal,status,keterangan) VALUES (?,?,?,?) ON CONFLICT(staff_id,tanggal) DO UPDATE SET status=excluded.status, keterangan=excluded.keterangan",
            (staff_id, str(tanggal), status, keterangan))
        conn.commit(); conn.close()
    except Exception: pass

def get_absen_staff_hari(staff_id, tanggal):
    sb = get_sb()
    if sb:
        try:
            res = sb.table("absen_staff").select("status,keterangan").eq("staff_id",staff_id).eq("tanggal",str(tanggal)).limit(1).execute()
            return res.data[0] if res.data else None
        except Exception: pass
    try:
        conn = get_conn()
        row = conn.execute("SELECT status, keterangan FROM absen_staff WHERE staff_id=? AND tanggal=?", (staff_id, str(tanggal))).fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None

def get_absen_staff_rekap(bulan, tahun):
    bulan_str = f"{tahun}-{str(bulan).zfill(2)}"
    sb = get_sb()
    if sb:
        try:
            s_res = sb.table("staff").select("id,nama,jabatan").eq("status","Aktif").execute()
            staff_list = s_res.data or []
            a_res = sb.table("absen_staff").select("staff_id,status").like("tanggal", f"{bulan_str}%").execute()
            absen_map = {}
            for a in (a_res.data or []):
                sid = a["staff_id"]
                if sid not in absen_map:
                    absen_map[sid] = {"H":0,"A":0,"I":0,"S":0,"total":0}
                if a["status"] in absen_map[sid]:
                    absen_map[sid][a["status"]] += 1
                absen_map[sid]["total"] += 1
            rows = []
            for s in staff_list:
                m = absen_map.get(s["id"], {"H":0,"A":0,"I":0,"S":0,"total":0})
                rows.append({"nama":s["nama"],"jabatan":s["jabatan"],"hadir":m["H"],"alpa":m["A"],"izin":m["I"],"sakit":m["S"],"total_hari":m["total"]})
            return pd.DataFrame(rows)
        except Exception: pass
    try:
        conn = get_conn()
        df = pd.read_sql("""
            SELECT s.nama, s.jabatan,
                SUM(CASE WHEN a.status='H' THEN 1 ELSE 0 END) as hadir,
                SUM(CASE WHEN a.status='A' THEN 1 ELSE 0 END) as alpa,
                SUM(CASE WHEN a.status='I' THEN 1 ELSE 0 END) as izin,
                SUM(CASE WHEN a.status='S' THEN 1 ELSE 0 END) as sakit,
                COUNT(a.id) as total_hari
            FROM staff s LEFT JOIN absen_staff a ON a.staff_id=s.id AND a.tanggal LIKE ?
            WHERE s.status='Aktif' GROUP BY s.id ORDER BY s.jabatan, s.nama
        """, conn, params=[f"{bulan_str}%"])
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def get_checklist_ob(staff_id, tanggal):
    sb = get_sb()
    if sb:
        try:
            res = sb.table("checklist_ob").select("*").eq("staff_id",staff_id).eq("tanggal",str(tanggal)).order("urutan").execute()
            return res.data or []
        except Exception: pass
    try:
        conn = get_conn()
        rows = conn.execute("SELECT * FROM checklist_ob WHERE staff_id=? AND tanggal=? ORDER BY urutan", (staff_id, str(tanggal))).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []

def init_checklist_hari(staff_id, tanggal):
    """Inisialisasi checklist default untuk hari ini jika belum ada."""
    existing = get_checklist_ob(staff_id, tanggal)
    if existing:
        return
    sb = get_sb()
    if sb:
        try:
            for i, item in enumerate(CHECKLIST_DEFAULT):
                sb.table("checklist_ob").insert({"staff_id":staff_id,"tanggal":str(tanggal),"item":item,"selesai":0,"urutan":i}).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        for i, item in enumerate(CHECKLIST_DEFAULT):
            conn.execute("INSERT OR IGNORE INTO checklist_ob (staff_id,tanggal,item,selesai,urutan) VALUES (?,?,?,0,?)",
                (staff_id, str(tanggal), item, i))
        conn.commit(); conn.close()
    except Exception: pass

def update_checklist_item(checklist_id, selesai):
    sb = get_sb()
    if sb:
        try:
            sb.table("checklist_ob").update({"selesai": 1 if selesai else 0}).eq("id", checklist_id).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        conn.execute("UPDATE checklist_ob SET selesai=? WHERE id=?", (1 if selesai else 0, checklist_id))
        conn.commit(); conn.close()
    except Exception: pass

def tambah_checklist_item(staff_id, tanggal, item):
    existing = get_checklist_ob(staff_id, tanggal)
    urutan = len(existing)
    sb = get_sb()
    if sb:
        try:
            sb.table("checklist_ob").insert({"staff_id":staff_id,"tanggal":str(tanggal),"item":item,"selesai":0,"urutan":urutan}).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        conn.execute("INSERT OR IGNORE INTO checklist_ob (staff_id,tanggal,item,selesai,urutan) VALUES (?,?,?,0,?)",
            (staff_id, str(tanggal), item, urutan))
        conn.commit(); conn.close()
    except Exception: pass

def get_agenda_staff(staff_id, tanggal):
    sb = get_sb()
    if sb:
        try:
            res = sb.table("agenda_staff").select("*").eq("staff_id",staff_id).eq("tanggal",str(tanggal)).order("created_at").execute()
            return res.data or []
        except Exception: pass
    try:
        conn = get_conn()
        rows = conn.execute("SELECT * FROM agenda_staff WHERE staff_id=? AND tanggal=? ORDER BY created_at", (staff_id, str(tanggal))).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []

def tambah_agenda_staff(staff_id, tanggal, tugas):
    sb = get_sb()
    if sb:
        try:
            sb.table("agenda_staff").insert({"staff_id":staff_id,"tanggal":str(tanggal),"tugas":tugas,"selesai":0}).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        conn.execute("INSERT INTO agenda_staff (staff_id,tanggal,tugas,selesai) VALUES (?,?,?,0)",
            (staff_id, str(tanggal), tugas))
        conn.commit(); conn.close()
    except Exception: pass

def update_agenda_staff(agenda_id, selesai):
    sb = get_sb()
    if sb:
        try:
            sb.table("agenda_staff").update({"selesai": 1 if selesai else 0}).eq("id", agenda_id).execute()
            return
        except Exception: pass
    try:
        conn = get_conn()
        conn.execute("UPDATE agenda_staff SET selesai=? WHERE id=?", (1 if selesai else 0, agenda_id))
        conn.commit(); conn.close()
    except Exception: pass

def get_checklist_summary_hari(tanggal):
    """Summary checklist semua OB untuk kepsek."""
    sb = get_sb()
    if sb:
        try:
            s_res = sb.table("staff").select("id,nama,jabatan").eq("jabatan","OB").eq("status","Aktif").execute()
            rows = []
            for s in (s_res.data or []):
                c_res = sb.table("checklist_ob").select("selesai").eq("staff_id",s["id"]).eq("tanggal",str(tanggal)).execute()
                items = c_res.data or []
                total = len(items)
                done  = sum(1 for i in items if i["selesai"])
                rows.append({"nama":s["nama"],"total":total,"selesai":done,"pct":f"{int(done/total*100)}%" if total else "0%"})
            return rows
        except Exception: pass
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT s.nama, COUNT(c.id) as total, SUM(c.selesai) as selesai
            FROM staff s LEFT JOIN checklist_ob c ON c.staff_id=s.id AND c.tanggal=?
            WHERE s.jabatan='OB' AND s.status='Aktif' GROUP BY s.id
        """, (str(tanggal),)).fetchall()
        conn.close()
        return [{"nama":r["nama"],"total":r["total"],"selesai":r["selesai"] or 0,
                 "pct":f"{int((r['selesai'] or 0)/r['total']*100)}%" if r["total"] else "0%"} for r in rows]
    except Exception:
        return []
