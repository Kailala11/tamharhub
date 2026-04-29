"""
ui_helpers.py — Responsive CSS dan komponen UI untuk TamharHub
Redesign: Hijau + Biru, formal dan bersih untuk institusi pendidikan
"""

LOGO_B64 = "data:image/png;base64,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"

# ── Responsive CSS ─────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 15px !important;
}
.stApp { background: #f0f4f8; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { background: #003366 !important; height: 0 !important; }

/* ── Masthead ── */
.masthead {
    background: linear-gradient(135deg, #003366 0%, #1a5c3a 100%);
    padding: 0 20px;
    height: 58px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
    box-shadow: 0 2px 12px rgba(0,51,102,0.25);
}
.mast-left { display: flex; align-items: center; gap: 12px; }
.mast-logo {
    width: 42px; height: 42px;
    background: #fff;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    padding: 2px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    overflow: hidden;
}
.mast-logo img {
    width: 100%; height: 100%; object-fit: contain;
}
.mast-title { 
    font-size: 19px; font-weight: 800; color: #fff; 
    letter-spacing: -.02em; line-height: 1;
}
.mast-title span { color: #7dd3c0; }
.mast-school {
    font-size: 11px; color: rgba(255,255,255,0.65);
    margin-top: 2px; letter-spacing: .01em;
}
.mast-user {
    text-align: right;
}
.mast-user-name {
    font-size: 12px; color: rgba(255,255,255,0.9); font-weight: 600;
}
.mast-user-role {
    font-size: 10px; color: rgba(255,255,255,0.5);
    font-family: 'DM Mono', monospace; margin-top: 2px;
}

/* ── Content ── */
.main-content { padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.kpi-card {
    background: #fff; 
    border-radius: 12px; padding: 16px;
    border: none;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.05);
    border-top: 3px solid #e4e8f0;
    transition: transform .15s;
}
.kpi-card.green { border-top-color: #1a5c3a; }
.kpi-card.red   { border-top-color: #dc2626; }
.kpi-card.blue  { border-top-color: #003366; }
.kpi-card.amber { border-top-color: #d97706; }
.kpi-label {
    font-size: 10px; font-weight: 600; letter-spacing: .1em;
    text-transform: uppercase; color: #94a3b8; margin-bottom: 6px;
    font-family: 'DM Mono', monospace;
}
.kpi-value { font-size: 28px; font-weight: 800; line-height: 1; letter-spacing: -.02em; }
.kpi-value.green { color: #1a5c3a; }
.kpi-value.red   { color: #dc2626; }
.kpi-value.blue  { color: #003366; }
.kpi-value.amber { color: #d97706; }
.kpi-sub { font-size: 11px; color: #94a3b8; margin-top: 4px; }

/* ── Alert boxes ── */
.alrt {
    border-radius: 10px; padding: 12px 16px;
    font-size: 14px; line-height: 1.5;
    border-left: 4px solid; margin-bottom: 6px;
}
.alrt.green { background: #f0fdf4; border-color: #1a5c3a; color: #14532d; }
.alrt.red   { background: #fef2f2; border-color: #dc2626; color: #991b1b; }
.alrt.amber { background: #fffbeb; border-color: #d97706; color: #92400e; }
.alrt.blue  { background: #eff6ff; border-color: #003366; color: #1e3a5f; }

/* ── Cards ── */
.card {
    background: #fff; border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
    overflow: hidden;
}
.card-head {
    background: #f8fafc; border-bottom: 1px solid #e2e8f0;
    padding: 11px 16px;
    display: flex; align-items: center; justify-content: space-between;
}
.card-title {
    font-family: 'DM Mono', monospace;
    font-size: 10px; font-weight: 500; letter-spacing: .1em;
    text-transform: uppercase; color: #94a3b8;
}
.card-body { padding: 14px 16px; }

/* ── Guru row ── */
.guru-row {
    display: flex; align-items: center; gap: 12px;
    padding: 11px 0; border-bottom: 1px solid #f1f5f9;
}
.guru-row:last-child { border-bottom: none; }
.guru-name { font-size: 14px; font-weight: 600; color: #1e293b; }
.guru-kelas { font-size: 11px; color: #94a3b8; margin-top: 1px; }

/* ── Badge ── */
.bdg {
    font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 500;
    padding: 3px 9px; border-radius: 20px;
    display: inline-block; white-space: nowrap;
    letter-spacing: .03em; text-transform: uppercase;
}
.bdg-green { background: #dcfce7; color: #14532d; }
.bdg-red   { background: #fee2e2; color: #991b1b; }
.bdg-amber { background: #fef3c7; color: #92400e; }
.bdg-blue  { background: #dbeafe; color: #1e3a5f; }
.bdg-x     { background: #f1f5f9; color: #94a3b8; }

/* ── Jurnal card ── */
.jurnal-card {
    background: #fff; border-radius: 12px; margin-bottom: 10px; overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.jurnal-head {
    background: linear-gradient(135deg, #003366, #1a5c3a);
    padding: 10px 16px;
    display: flex; align-items: center; justify-content: space-between;
}
.jurnal-tgl { font-size: 12px; font-weight: 600; color: #fff; }
.jurnal-body { padding: 14px 16px; }
.jurnal-topik { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 4px; }
.jurnal-guru { font-size: 11px; color: #94a3b8; margin-bottom: 10px; }
.jurnal-act {
    font-size: 13px; color: #475569; line-height: 1.6;
    background: #f8fafc; border-radius: 8px; padding: 10px 12px;
}

/* ── Agenda card ── */
.agenda-card {
    background: #fff;
    border-left: 3px solid #003366;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px; margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.agenda-card.akademik  { border-left-color: #1a5c3a; }
.agenda-card.libur     { border-left-color: #dc2626; }
.agenda-card.rapat     { border-left-color: #d97706; }
.agenda-card.kegiatan  { border-left-color: #7c3aed; }
.agenda-judul { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 3px; }
.agenda-tgl   { font-family: 'DM Mono', monospace; font-size: 10px; color: #94a3b8; }
.agenda-desk  { font-size: 13px; color: #64748b; margin-top: 6px; line-height: 1.5; }

/* ── Wali murid ── */
.wm-banner {
    background: linear-gradient(135deg, #003366 0%, #1a5c3a 100%);
    border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; color: #fff;
}
.wm-banner h3 { font-size: 17px; font-weight: 700; margin-bottom: 5px; }
.wm-banner p  { font-size: 13px; opacity: .75; }

/* ── Streamlit overrides ── */
div[data-testid="stSelectbox"] > div > div {
    min-height: 48px !important; font-size: 15px !important;
    border-radius: 8px !important;
}
div[data-testid="stSelectbox"] label {
    font-size: 12px !important; font-weight: 600 !important;
    color: #64748b !important; margin-bottom: 4px !important;
    text-transform: uppercase; letter-spacing: .04em;
}
div[data-testid="stTextInput"] input {
    min-height: 48px !important; font-size: 15px !important;
    border-radius: 8px !important;
}
div[data-testid="stTextInput"] label {
    font-size: 12px !important; font-weight: 600 !important;
    color: #64748b !important; text-transform: uppercase; letter-spacing: .04em;
}
div[data-testid="stTextArea"] textarea {
    font-size: 15px !important; border-radius: 8px !important;
}
div[data-testid="stTextArea"] label {
    font-size: 12px !important; font-weight: 600 !important;
    color: #64748b !important; text-transform: uppercase; letter-spacing: .04em;
}
div[data-testid="stNumberInput"] input {
    min-height: 48px !important; font-size: 15px !important;
}
div[data-testid="stRadio"] label {
    font-size: 14px !important; font-weight: 500 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex; flex-wrap: wrap; gap: 8px;
}
div[data-testid="stRadio"] label {
    display: flex !important; align-items: center !important;
    min-height: 46px !important; padding: 8px 16px !important;
    border: 1.5px solid #e2e8f0 !important; border-radius: 8px !important;
    background: #fff !important; cursor: pointer !important;
    flex: 1 !important; min-width: 100px !important; justify-content: center !important;
}

.stButton > button {
    min-height: 48px !important; font-size: 14px !important;
    font-weight: 700 !important; border-radius: 10px !important;
    width: 100% !important; letter-spacing: .02em;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #003366, #1a5c3a) !important;
    border: none !important; color: #fff !important;
    box-shadow: 0 4px 12px rgba(0,51,102,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: .92 !important;
    box-shadow: 0 6px 16px rgba(0,51,102,0.35) !important;
}
.stDownloadButton > button {
    min-height: 48px !important; font-size: 14px !important;
    font-weight: 600 !important; border-radius: 10px !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 12px !important; font-weight: 600 !important;
    min-height: 44px !important; padding: 8px 14px !important;
    letter-spacing: .02em; text-transform: uppercase;
}
.stTabs [aria-selected="true"] {
    color: #003366 !important;
    border-bottom: 3px solid #003366 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important; flex-wrap: nowrap !important;
    background: #fff !important;
    border-bottom: 1px solid #e2e8f0 !important;
}

div[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, #003366, #1a5c3a) !important;
    color: white !important; border: none !important;
    font-size: 14px !important; min-height: 52px !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] { background: #0f172a !important; }
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label { color: #94a3b8 !important; }
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-size: 14px !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: #1e293b !important; border: 1px solid #334155 !important;
    color: #94a3b8 !important; font-size: 13px !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 10px !important; overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}

div[data-testid="stSuccess"] {
    font-size: 14px !important; border-radius: 10px !important;
    padding: 12px 16px !important;
}
div[data-testid="stWarning"] { font-size: 14px !important; border-radius: 10px !important; }
div[data-testid="stInfo"] { font-size: 14px !important; border-radius: 10px !important; }
div[data-testid="stError"] { font-size: 14px !important; border-radius: 10px !important; }

details summary {
    font-size: 13px !important; font-weight: 600 !important;
    padding: 12px 16px !important; min-height: 46px !important;
    color: #1e293b !important;
}

div[data-testid="stMetric"] label { font-size: 11px !important; color: #94a3b8 !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 26px !important; font-weight: 800 !important; color: #1e293b !important;
}

div[data-testid="stDateInput"] input {
    min-height: 48px !important; font-size: 15px !important;
}

hr { border-color: #e2e8f0 !important; }

@media (max-width: 640px) {
    .kpi-grid { grid-template-columns: 1fr 1fr; }
    .kpi-value { font-size: 22px; }
    .main-content { padding: 12px 14px; }
    .masthead { padding: 0 14px; height: 54px; }
    .mast-title { font-size: 16px; }
}
</style>
"""

STATUS_LABEL = {"H": "Hadir", "A": "Tidak Hadir / Alpa", "I": "Izin", "S": "Sakit", "?": "Belum Mengisi"}
STATUS_LABEL_SHORT = {"H": "Hadir", "A": "Alpa", "I": "Izin", "S": "Sakit", "?": "Belum Mengisi"}
STATUS_COLOR = {"H": "green", "A": "red", "I": "amber", "S": "blue", "?": "red"}
KAT_COLOR_MAP = {
    "Umum": "blue", "Akademik": "akademik",
    "Kegiatan Siswa": "kegiatan", "Rapat": "rapat",
    "Libur": "libur", "Pengumuman": "blue"
}

def masthead(user_name: str, role: str) -> str:
    role_label = {"kepsek": "Kepala Sekolah", "guru": "Guru", "walimurid": "Wali Murid"}
    short_name = user_name.split(",")[0] if user_name else ""
    return f"""
    <div class="masthead">
      <div class="mast-left">
        <div class="mast-logo">
          <img src="data:image/png;base64,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" onerror="this.style.display='none'" alt="Logo">
        </div>
        <div>
          <div class="mast-title">Tamhar<span>Hub</span></div>
          <div class="mast-school">SD Taman Harapan 1 Bekasi</div>
        </div>
      </div>
      <div class="mast-user">
        <div class="mast-user-name">{short_name}</div>
        <div class="mast-user-role">{role_label.get(role,'')}</div>
      </div>
    </div>"""

def kpi_card(label: str, value, sub: str = "", color: str = "") -> str:
    return f"""
    <div class="kpi-card {color}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {color}">{value}</div>
      {'<div class="kpi-sub">'+sub+'</div>' if sub else ''}
    </div>"""

def alrt(text: str, color: str = "blue") -> str:
    return f'<div class="alrt {color}">{text}</div>'

def jurnal_card(j) -> str:
    guru_short = str(j.get("guru_nama", j.get("guru", ""))).split(",")[0]
    kelas_short = str(j.get("kelas", ""))
    return f"""
    <div class="jurnal-card">
      <div class="jurnal-head">
        <span class="jurnal-tgl">{j.get('tanggal','')} · {kelas_short}</span>
        <span class="bdg" style="background:rgba(255,255,255,0.2);color:#fff;font-size:9px">{j.get('mapel','')}</span>
      </div>
      <div class="jurnal-body">
        <div class="jurnal-topik">{j.get('topik','')}</div>
        <div class="jurnal-guru">{guru_short}</div>
        <div class="jurnal-act">{j.get('aktivitas','')}</div>
        {'<div style="margin-top:8px;font-size:11px;color:#94a3b8">Media: '+j.get("media","")+"</div>" if j.get("media") else ""}
        {'<div style="font-size:11px;color:#94a3b8">Catatan: '+j.get("catatan","")+"</div>" if j.get("catatan") else ""}
      </div>
    </div>"""

def agenda_card(ag) -> str:
    kat = ag.get("kategori","Umum")
    cls = KAT_COLOR_MAP.get(kat, "blue")
    tgl = ag.get("tanggal","")
    if ag.get("tanggal_end") and ag["tanggal_end"] != ag["tanggal"]:
        tgl += f" s/d {ag['tanggal_end']}"
    return f"""
    <div class="agenda-card {cls}">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px">
        <div class="agenda-judul">{ag.get('judul','')}</div>
        <span class="bdg bdg-blue" style="font-size:9px;flex-shrink:0">{kat}</span>
      </div>
      <div class="agenda-tgl">{tgl}</div>
      {'<div class="agenda-desk">'+ag.get("deskripsi","")+"</div>" if ag.get("deskripsi") else ""}
    </div>"""
