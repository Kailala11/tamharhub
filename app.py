"""
TamharHub — Platform Administrasi SD Taman Harapan 1 Bekasi
Dioptimasi untuk HP dan laptop, ramah pengguna semua usia.
"""
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import calendar
from rapor import generate_rapor_pdf, generate_rekap_excel, generate_rekap_tp_excel
from ui_helpers import (
    CSS, masthead, kpi_card, alrt, jurnal_card, agenda_card,
    STATUS_LABEL, STATUS_LABEL_SHORT, STATUS_COLOR,
)
from database import (
    init_db, init_agenda_table, init_nilai_table,
    get_all_guru, get_guru_by_nama, get_mapel_guru,
    add_mapel_guru, delete_mapel_guru,
    get_siswa_by_kelas, add_siswa_bulk,
    upsert_absen_guru, get_absen_guru_hari, get_absen_guru_rekap,
    get_status_absen_guru,
    upsert_absen_siswa_bulk, get_absen_siswa_hari, get_absen_siswa_rekap,
    simpan_jurnal, get_jurnal_guru, get_jurnal_semua,
    get_summary_hari, get_guru_tidak_hadir, get_siswa_tidak_hadir,
    tambah_agenda, hapus_agenda,
    get_agenda_mendatang, get_agenda_semua,
    get_jurnal_by_kelas, get_semua_kelas,
    upsert_nilai, get_nilai_kelas, get_nilai_siswa,
    get_nilai_satu_siswa_mapel, get_predikat, DESKRIPSI_SIKAP,
    update_nuptk, get_nuptk,
    get_siswa_by_kelas_lengkap, update_siswa_info,
    upsert_ekskul, get_ekskul_siswa,
    upsert_catatan, get_catatan, get_absen_count_siswa,
    init_guru_kelas_table, get_kelas_guru, tambah_guru_kelas, hapus_guru_kelas,
)

# ── Init ───────────────────────────────────────────────────────────
init_db()
init_agenda_table()
init_nilai_table()
init_guru_kelas_table()

st.set_page_config(
    page_title="TamharHub",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────
for k, v in [("logged_in",False),("role",None),("guru_nama",None),("guru_id",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
# HALAMAN LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("""
        <div style="text-align:center;margin:32px 0 28px">
          <div style="width:90px;height:90px;background:#fff;border-radius:18px;
               border:2px solid #e4e8f0;display:flex;align-items:center;
               justify-content:center;margin:0 auto 14px;padding:6px">
            <img src="data:image/png;base64,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" style="width:100%;height:100%;object-fit:contain">
          </div>
          <h2 style="font-size:26px;font-weight:700;color:#1a1d2e;margin:0">TamharHub</h2>
          <p style="font-size:14px;color:#9aa0b8;margin-top:6px">SD Taman Harapan 1 Bekasi</p>
        </div>""", unsafe_allow_html=True)

        role = st.selectbox("Saya adalah:", ["Kepala Sekolah", "Guru", "Wali Murid"], key="_ukey1")

        guru_nama = None
        if role == "Guru":
            all_guru = get_all_guru()
            guru_nama = st.selectbox("Pilih nama Anda:", all_guru["nama"].tolist(), key="_ukey2")

        if role == "Wali Murid":
            st.markdown('<div class="alrt blue">Wali Murid tidak perlu password. Langsung tekan Masuk.</div>', unsafe_allow_html=True)
            if st.button("Masuk sebagai Wali Murid", type="primary", use_container_width=True):
                st.session_state.update(logged_in=True, role="walimurid", guru_nama="Wali Murid", guru_id=None)
                st.rerun()
        else:
            pw = st.text_input("Password:", type="password", placeholder="Masukkan password Anda")
            if st.button("Masuk", type="primary", use_container_width=True):
                role_key = "kepsek" if role == "Kepala Sekolah" else "guru"
                try:
                    pw_kepsek = st.secrets["passwords"]["kepsek"]
                    pw_guru   = st.secrets["passwords"]["guru"]
                except Exception:
                    pw_kepsek = "kepsek123"   # fallback lokal
                    pw_guru   = "guru2025"
                ok = (role_key=="kepsek" and pw==pw_kepsek) or (role_key=="guru" and pw==pw_guru)
                if ok:
                    gid = None
                    if role_key == "guru":
                        g = get_guru_by_nama(guru_nama)
                        gid = g["id"] if g else None
                    st.session_state.update(
                        logged_in=True, role=role_key,
                        guru_nama=guru_nama if role_key=="guru" else "Rahmat Hidayat, S.Psi., M.M.",
                        guru_id=gid
                    )
                    st.rerun()
                else:
                    st.error("Password salah. Coba lagi.")
    st.stop()

# ── Shared ────────────────────────────────────────────────────────
role    = st.session_state.role
user    = st.session_state.guru_nama
guru_id = st.session_state.guru_id

st.markdown(masthead(user, role), unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### {user}")
    st.markdown("---")
    tgl_dipilih = st.date_input("Pilih tanggal", value=date.today(), key="_ukey3")
    st.markdown("---")
    if st.button("Keluar", use_container_width=True):
        st.session_state.update(logged_in=False, role=None, guru_nama=None, guru_id=None)
        st.rerun()

today_str = str(tgl_dipilih)
tgl_fmt   = tgl_dipilih.strftime("%A, %d %B %Y")

KATEGORI  = ["Umum","Akademik","Kegiatan Siswa","Rapat","Libur","Pengumuman"]
THN_LIST  = ["2024/2025","2025/2026","2026/2027"]

# ══════════════════════════════════════════════════════════════════
# KEPALA SEKOLAH
# ══════════════════════════════════════════════════════════════════
if role == "kepsek":
    tab_ring, tab_absen, tab_jurnal, tab_agenda_ks, tab_nilai_ks, tab_rekap, tab_data = st.tabs([
        "Ringkasan", "Kehadiran", "Jurnal Guru", "Agenda", "Nilai Siswa", "Rekap Bulanan", "Data Sekolah"
    ])

    with tab_ring:
        summ   = get_summary_hari(today_str)
        df_th  = get_guru_tidak_hadir(today_str)
        df_ts  = get_siswa_tidak_hadir(today_str)
        df_jh  = get_jurnal_semua(tanggal=today_str, limit=10)

        st.markdown(f"""
        <div style="padding:16px 20px">
          <div style="font-size:14px;color:#9aa0b8;margin-bottom:10px">{tgl_fmt}</div>
          <div class="kpi-grid">
            {kpi_card("Total Guru",      summ["total_guru"],   "Guru aktif",               "")}
            {kpi_card("Sudah Absen",     summ["hadir_guru"],   "Hadir hari ini",            "green")}
            {kpi_card("Belum/Tdk Hadir", summ["absen_guru"],   "Belum isi / Alpa / Izin",  "red" if summ["absen_guru"]>0 else "")}
            {kpi_card("Jurnal Masuk",    summ["jurnal_hari"],  "Entri hari ini",            "blue")}
          </div>
        </div>""", unsafe_allow_html=True)

        with st.container():
            if df_th.empty:
                st.markdown(alrt("Semua guru hadir hari ini.", "green"), unsafe_allow_html=True)
            else:
                for _, r in df_th.iterrows():
                    lbl = STATUS_LABEL_SHORT.get(r["status"], r["status"])
                    ket = f" · {r['keterangan']}" if r.get("keterangan") else ""
                    st.markdown(alrt(f"<b>{r['nama'].split(',')[0]}</b> ({r['kelas']}) — {lbl}{ket}", "red"), unsafe_allow_html=True)

            if not df_ts.empty:
                for kls, grp in df_ts.groupby("kelas"):
                    names = ", ".join(grp["nama"].tolist())
                    st.markdown(alrt(f"<b>{kls}</b> — {len(grp)} siswa tidak hadir: {names[:70]}{'...' if len(names)>70 else ''}", "amber"), unsafe_allow_html=True)

            if not df_jh.empty:
                st.markdown('<div style="font-weight:600;font-size:15px;margin-top:16px;margin-bottom:8px">Jurnal masuk hari ini</div>', unsafe_allow_html=True)
                for _, j in df_jh.iterrows():
                    st.markdown(jurnal_card(j), unsafe_allow_html=True)

    with tab_absen:
        st.markdown(f'<div style="padding:10px 20px 0;font-size:14px;color:#9aa0b8">{tgl_fmt}</div>', unsafe_allow_html=True)
        tingkat = st.radio("Filter kelas:", ["Semua","Kelas I","Kelas II","Kelas III","Kelas IV","Kelas V","Kelas VI","Bidang Studi"], horizontal=True, label_visibility="collapsed", key="_ukey4")
        df_absen = get_absen_guru_hari(today_str)
        changes = {}
        for _, row in df_absen.iterrows():
            kls = str(row["kelas"])
            if tingkat != "Semua":
                if tingkat == "Bidang Studi":
                    if "Semua" not in kls: continue
                else:
                    num = tingkat.replace("Kelas ","")
                    if not kls.startswith(num+" "): continue

            belum = row["status"] == "?"
            b_color = "#fdf0ef" if belum else "#fff"
            b_border = "#c0281e" if belum else "#e4e8f0"
            b_tag = ' <span style="font-size:10px;background:#fdf0ef;color:#c0281e;border:1px solid #f5bab6;border-radius:3px;padding:1px 6px;font-family:monospace">Belum Mengisi</span>' if belum else ""
            st.markdown(f"""
            <div style="background:{b_color};border:1px solid {b_border};border-radius:10px;
                 padding:12px 16px;margin-bottom:8px">
              <div style="font-size:15px;font-weight:600;color:#1a1d2e">{row['nama']}{b_tag}</div>
              <div style="font-size:12px;color:#9aa0b8">{kls}</div>
            </div>""", unsafe_allow_html=True)
            c1, c2 = st.columns([1.5, 2])
            with c1:
                sv = st.selectbox("", ["H","A","I","S"], index=["H","A","I","S"].index(row["status"] if row["status"] in ["H","A","I","S"] else "H"),
                                  key=f"ks_{row['id']}", format_func=lambda x: STATUS_LABEL_SHORT[x],
                                  label_visibility="collapsed")
            with c2:
                kv = st.text_input("", value=row.get("keterangan",""), key=f"kk_{row['id']}",
                                   placeholder="Keterangan (opsional)", label_visibility="collapsed")
            changes[int(row["id"])] = (sv, kv)

        if st.button("Simpan Kehadiran Guru", type="primary", use_container_width=True):
            for gid2, (sv2, kv2) in changes.items():
                upsert_absen_guru(gid2, today_str, sv2, kv2)
            st.success(f"Kehadiran {len(changes)} guru berhasil disimpan.")
            st.rerun()

    with tab_jurnal:
        c1, c2 = st.columns(2)
        with c1: fg = st.selectbox("Filter guru:", ["Semua"]+get_all_guru()["nama"].tolist(), key="fg_jurnal")
        with c2: ft = st.selectbox("Filter tanggal:", ["Hari ini","Semua"], key="ft_jurnal")
        df_jf = get_jurnal_semua(tanggal=today_str if ft=="Hari ini" else None)
        if fg != "Semua": df_jf = df_jf[df_jf["guru_nama"]==fg]
        if df_jf.empty: st.info("Belum ada jurnal untuk filter ini.")
        else:
            for _, j in df_jf.iterrows():
                st.markdown(jurnal_card(j), unsafe_allow_html=True)

    with tab_agenda_ks:
        with st.expander("Tambah agenda baru", expanded=False):
            with st.form("form_ag_ks"):
                judul = st.text_input("Judul agenda:", placeholder="Contoh: Upacara Bendera")
                c1, c2 = st.columns(2)
                with c1: kat_ks = st.selectbox("Kategori:", KATEGORI, key="kat_agenda_ks")
                with c2: tgl_ag = st.date_input("Tanggal mulai:", value=date.today(), key="_ukey5")
                tgl_end = st.date_input("Tanggal selesai (kosongkan jika 1 hari):", value=date.today(), key="_ukey6")
                desk = st.text_area("Keterangan / detail:", placeholder="Informasi untuk wali murid dan guru...")
                if st.form_submit_button("Simpan Agenda", use_container_width=True):
                    if not judul: st.error("Judul wajib diisi.")
                    else:
                        tambah_agenda(judul, desk, tgl_ag, tgl_end if tgl_end!=tgl_ag else "", kat, "Rahmat Hidayat, S.Psi., M.M.")
                        st.success("Agenda berhasil ditambahkan.")
                        st.rerun()

        df_ag = get_agenda_semua()
        if df_ag.empty: st.info("Belum ada agenda.")
        else:
            for _, ag in df_ag.iterrows():
                c1, c2 = st.columns([10,1])
                with c1: st.markdown(agenda_card(ag), unsafe_allow_html=True)
                with c2:
                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                    if st.button("✕", key=f"del_{ag['id']}", help="Hapus agenda ini"):
                        st.session_state[f"confirm_del_{ag['id']}"] = True
                        st.rerun()
                if st.session_state.get(f"confirm_del_{ag['id']}"):
                    st.warning(f"Yakin hapus agenda **{ag['judul']}**? Tindakan ini tidak bisa dibatalkan.")
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        if st.button("Ya, hapus", key=f"ya_{ag['id']}", type="primary"):
                            hapus_agenda(int(ag["id"]))
                            st.session_state.pop(f"confirm_del_{ag['id']}", None)
                            st.rerun()
                    with cc2:
                        if st.button("Batal", key=f"batal_{ag['id']}"):
                            st.session_state.pop(f"confirm_del_{ag['id']}", None)
                            st.rerun()

    with tab_nilai_ks:
        all_kls = sorted(set(get_all_guru()["kelas"].dropna().unique())-{"Semua Tingkat"})
        c1, c2, c3 = st.columns(3)
        with c1: kls_nv = st.selectbox("Kelas:", all_kls, key="_ukey7")
        with c2: sem_nv = st.selectbox("Semester:", ["Ganjil","Genap"], key="sem_nv_ks")
        with c3: thn_nv = st.selectbox("Tahun Ajaran:", THN_LIST, index=1, key="thn_nv_ks")
        df_nv = get_nilai_kelas(kls_nv, sem_nv, thn_nv)
        df_snv = get_siswa_by_kelas(kls_nv)
        if df_nv.empty or df_nv["mapel"].isna().all():
            st.info(f"Belum ada data nilai untuk {kls_nv} periode ini.")
        else:
            st.dataframe(df_nv[["siswa","mapel","pengetahuan","keterampilan","sikap"]], use_container_width=True, hide_index=True)
        st.markdown("---")
        if not df_snv.empty and st.button("Download Excel Rekap Nilai", type="primary", use_container_width=True):
            sl = [(int(r["id"]),r["nama"]) for _,r in df_snv.iterrows()]
            xl = generate_rekap_excel(kls_nv, sem_nv, thn_nv, df_nv, sl)
            st.download_button("Unduh Sekarang", data=xl,
                file_name=f"rekap_nilai_{kls_nv.replace(' ','_')}_{sem_nv}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)

    with tab_rekap:
        c1, c2 = st.columns(2)
        with c1: bln = st.selectbox("Bulan:", list(range(1,13)), index=date.today().month-1, format_func=lambda m: calendar.month_name[m], key="bln_rekap")
        with c2: thn = st.selectbox("Tahun:", [2024,2025,2026], index=1, key="thn_rekap")
        tab_rg, tab_rs = st.tabs(["Kehadiran Guru","Kehadiran Siswa"])
        with tab_rg:
            df_rg = get_absen_guru_rekap(bln, thn)
            if df_rg.empty or df_rg["total_hari"].sum()==0: st.info("Belum ada data.")
            else:
                st.dataframe(df_rg, use_container_width=True, hide_index=True)
                st.download_button("Download CSV", data=df_rg.to_csv(index=False,encoding="utf-8-sig").encode("utf-8-sig"),
                    file_name=f"rekap_guru_{bln}_{thn}.csv", mime="text/csv", use_container_width=True)
        with tab_rs:
            all_kls_rs = sorted(set(get_all_guru()["kelas"].dropna().unique())-{"Semua Tingkat"})
            kls_rs = st.selectbox("Pilih kelas:", all_kls_rs, key="kls_rs_rekap")
            df_rs  = get_absen_siswa_rekap(kls_rs, bln, thn)
            if df_rs.empty or df_rs["total_hari"].sum()==0: st.info("Belum ada data.")
            else:
                st.dataframe(df_rs, use_container_width=True, hide_index=True,
                    column_config={"pct_hadir": st.column_config.ProgressColumn("Kehadiran %", min_value=0, max_value=100)})
                st.download_button("Download CSV", data=df_rs.to_csv(index=False,encoding="utf-8-sig").encode("utf-8-sig"),
                    file_name=f"rekap_siswa_{kls_rs.replace(' ','_')}_{bln}_{thn}.csv",
                    mime="text/csv", use_container_width=True)

    with tab_data:
        st.markdown('<div class="alrt blue">Guru wali kelas bisa menambah siswa sendiri melalui tab <b>Absen Siswa</b>.</div>', unsafe_allow_html=True)
        all_kls_d = sorted(set(get_all_guru()["kelas"].dropna().unique())-{"Semua Tingkat"})
        kls_d = st.selectbox("Pilih kelas:", all_kls_d, key="kls_d_data")
        df_ex = get_siswa_by_kelas(kls_d)
        st.caption(f"{len(df_ex)} siswa terdaftar di {kls_d}")
        names_in = st.text_area("Nama siswa (satu nama per baris):", placeholder="Ahmad Fauzan\nBunga Ramadhani", height=140)
        if st.button("Tambah Siswa", type="primary", use_container_width=True):
            names = [n.strip() for n in names_in.split("\n") if n.strip()]
            if names: add_siswa_bulk(names, kls_d); st.success(f"{len(names)} siswa ditambahkan."); st.rerun()
            else: st.error("Masukkan minimal satu nama.")
        if not df_ex.empty:
            st.dataframe(df_ex[["nama"]], use_container_width=True, hide_index=True,
                column_config={"nama": st.column_config.TextColumn("Nama Siswa")})

        # ── Backup semua data ─────────────────────────────────
        st.markdown("---")
        st.markdown("**Backup semua data sekolah**")
        st.caption("Download semua data ke Excel sebagai cadangan. Lakukan secara berkala.")
        if st.button("Download Backup Excel", use_container_width=True):
            from io import BytesIO
            buf = BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                # Sheet guru
                df_guru_bk = get_all_guru()
                df_guru_bk.to_excel(writer, sheet_name="Guru", index=False)

                # Sheet siswa semua kelas
                all_kls_bk = sorted(set(get_all_guru()["kelas"].dropna().unique())-{"Semua Tingkat"})
                df_siswa_all = pd.concat(
                    [get_siswa_by_kelas(k) for k in all_kls_bk],
                    ignore_index=True
                ) if all_kls_bk else pd.DataFrame()
                if not df_siswa_all.empty:
                    df_siswa_all.to_excel(writer, sheet_name="Siswa", index=False)

                # Sheet jurnal
                df_jurnal_bk = get_jurnal_semua(limit=1000)
                if not df_jurnal_bk.empty:
                    df_jurnal_bk.to_excel(writer, sheet_name="Jurnal", index=False)

                # Sheet agenda
                df_ag_bk = get_agenda_semua(limit=200)
                if not df_ag_bk.empty:
                    df_ag_bk.to_excel(writer, sheet_name="Agenda", index=False)

                # Sheet absen guru bulan ini
                from datetime import date as dt
                df_absen_bk = get_absen_guru_rekap(dt.today().month, dt.today().year)
                if not df_absen_bk.empty:
                    df_absen_bk.to_excel(writer, sheet_name="Absen Guru", index=False)

            from datetime import date as dt
            st.download_button(
                "Unduh Backup",
                data=buf.getvalue(),
                file_name=f"backup_tamharhub_{dt.today().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════════════
# GURU
# ══════════════════════════════════════════════════════════════════
elif role == "guru":
    guru_info = get_guru_by_nama(user)
    if not guru_info:
        st.error("Data guru tidak ditemukan. Hubungi administrator.")
        st.stop()

    kelas_list = get_kelas_guru(guru_id)   # support multi wali kelas
    kelas_guru = kelas_list[0] if kelas_list else guru_info["kelas"]
    mapel_list = get_mapel_guru(guru_id)

    # ── Onboarding: cek apakah guru sudah setup mapel ──────────
    if not mapel_list:
        st.markdown("""
        <div style="background:#fff;border:2px solid #1a5c3a;border-radius:14px;padding:24px;margin-bottom:16px">
          <div style="font-size:18px;font-weight:700;color:#1a5c3a;margin-bottom:8px">
            Selamat datang, {nama}!
          </div>
          <div style="font-size:14px;color:#5a6080;line-height:1.8;margin-bottom:16px">
            Sebelum mulai, ada <b>3 langkah awal</b> yang perlu dilakukan:<br><br>
            <b>1.</b> Buka tab <b>Profil & Mapel</b> → tambahkan mata pelajaran yang Anda ajar<br>
            <b>2.</b> Buka tab <b>Absen Siswa</b> → tambahkan daftar nama siswa kelas Anda<br>
            <b>3.</b> Mulai isi <b>Absensi Saya</b> setiap hari masuk sekolah
          </div>
          <div style="font-size:13px;color:#9aa0b8">
            Butuh bantuan? Hubungi operator sekolah.
          </div>
        </div>""".format(nama=guru_info["nama"].split(",")[0]), unsafe_allow_html=True)

    tab_ag, tab_as, tab_nv, tab_jg, tab_agnd, tab_profil = st.tabs([
        "Absensi Saya", "Absen Siswa", "Nilai & Rapor", "Jurnal Harian", "Agenda", "Profil & Mapel"
    ])

    with tab_ag:
        existing   = get_status_absen_guru(guru_id, today_str)
        cur_status = existing["status"] if existing else None
        cur_ket    = existing["keterangan"] if existing else ""

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e4e8f0;border-radius:14px;
             padding:20px;margin-bottom:14px">
          <div style="font-size:17px;font-weight:700;color:#1a1d2e">{guru_info['nama']}</div>
          <div style="font-size:13px;color:#9aa0b8;margin-top:3px">{_kls_label}</div>
          <div style="font-size:12px;color:#9aa0b8;margin-top:6px;font-family:'DM Mono',monospace">
            {', '.join(mapel_list) if mapel_list else 'Belum ada mata pelajaran — tambah di tab Profil'}
          </div>
        </div>
        <div style="font-size:14px;color:#9aa0b8;margin-bottom:10px">{tgl_fmt}</div>""", unsafe_allow_html=True)

        if cur_status:
            st.markdown(alrt(f"Status hari ini sudah tercatat: <b>{STATUS_LABEL_SHORT[cur_status]}</b>. Anda bisa mengubahnya di bawah.", STATUS_COLOR[cur_status]), unsafe_allow_html=True)

        st.markdown("**Pilih status kehadiran Anda:**")
        status_baru = st.radio("", ["H","A","I","S"],
            index=["H","A","I","S"].index(cur_status) if cur_status and cur_status in ["H","A","I","S"] else 0,
            format_func=lambda x: STATUS_LABEL[x], horizontal=True, label_visibility="collapsed")
        ket = st.text_input("Keterangan (opsional):", value=cur_ket,
                            placeholder="Contoh: Sakit demam, izin keperluan keluarga...")
        if st.button("Simpan Kehadiran", type="primary", use_container_width=True):
            upsert_absen_guru(guru_id, today_str, status_baru, ket)
            st.success(f"Kehadiran berhasil disimpan: {STATUS_LABEL[status_baru]}")
            st.rerun()

        st.markdown("---")
        st.markdown("**Riwayat 7 hari terakhir:**")
        rows_html = ""
        for i in range(6, -1, -1):
            d   = tgl_dipilih - timedelta(days=i)
            rec = get_status_absen_guru(guru_id, str(d))
            st_str = rec["status"] if rec else "—"
            lbl    = STATUS_LABEL_SHORT.get(st_str, "Belum diisi")
            color  = {"H":"#1a5c3a","A":"#c0281e","I":"#d97706","S":"#1a4a9a","—":"#9aa0b8"}[st_str]
            hari   = d.strftime("%A, %d %b")
            mark   = " <b>(hari ini)</b>" if d == tgl_dipilih else ""
            rows_html += f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                 padding:13px 0;border-bottom:1px solid #f4f6fa">
              <span style="font-size:14px;color:#1a1d2e">{hari}{mark}</span>
              <span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:600;color:{color}">{lbl}</span>
            </div>"""
        st.markdown(f'<div style="background:#fff;border:1px solid #e4e8f0;border-radius:12px;padding:8px 16px">{rows_html}</div>', unsafe_allow_html=True)

    if tab_as is not None:
     with tab_as:
        if len(kelas_list) > 1:
            kelas_aktif = st.selectbox("Pilih kelas:", kelas_list, key="sel_kelas_absen")
        else:
            kelas_aktif = kelas_guru
        st.markdown(f"**{kelas_aktif} · {tgl_fmt}**")
        df_siswa = get_siswa_by_kelas(kelas_aktif)

        with st.expander(f"{'Daftar siswa belum ada — tambah di sini' if df_siswa.empty else f'Kelola daftar siswa ({len(df_siswa)} siswa terdaftar)'}", expanded=df_siswa.empty):
            metode = st.radio("Cara menambah siswa:", ["Ketik nama","Upload file","Edit data siswa"], horizontal=True, key="metode_siswa_radio")
            if metode == "Ketik nama":
                ni = st.text_area("Tulis satu nama per baris:", placeholder="Ahmad Fauzan\nBunga Ramadhani\nCitra Dewi", height=150)
                if st.button("Simpan Daftar Siswa", use_container_width=True, type="primary"):
                    names = [n.strip() for n in ni.split("\n") if n.strip()]
                    if names: add_siswa_bulk(names, kelas_aktif); st.success(f"{len(names)} siswa disimpan."); st.rerun()
                    else: st.error("Belum ada nama yang dimasukkan.")
            elif metode == "Upload file":
                f = st.file_uploader("Upload file CSV atau TXT:", type=["csv","txt"])
                if f:
                    content = f.read().decode("utf-8-sig").strip()
                    names   = [line.split(",")[0].strip().strip('"') for line in content.split("\n")
                               if line.strip() and line.split(",")[0].strip().lower() not in ("nama","name","no","nomor")]
                    if names:
                        st.write(f"**{len(names)} nama terdeteksi:** {', '.join(names[:5])}{'...' if len(names)>5 else ''}")
                        if st.button("Simpan ke Database", type="primary", use_container_width=True):
                            add_siswa_bulk(names, kelas_aktif); st.success(f"{len(names)} siswa ditambahkan."); st.rerun()
            else:
                # Edit data siswa (NIS, NISN, alamat, fase)
                df_edit = get_siswa_by_kelas_lengkap(kelas_guru)
                if df_edit.empty:
                    st.info("Belum ada siswa. Tambahkan dulu di atas.")
                else:
                    st.caption("Lengkapi NIS, NISN, dan alamat siswa untuk rapor yang lengkap.")
                    ss_edit = st.selectbox("Pilih siswa:", df_edit["nama"].tolist(), key="ss_edit")
                    row_e   = df_edit[df_edit["nama"]==ss_edit].iloc[0]
                    sid_e   = int(row_e["id"])
                    ce1, ce2 = st.columns(2)
                    with ce1: nis_e  = st.text_input("NIS:",   value=row_e.get("nis",""),   placeholder="Nomor Induk Siswa")
                    with ce2: nisn_e = st.text_input("NISN:",  value=row_e.get("nisn",""),  placeholder="Nomor Induk Siswa Nasional")
                    fase_e  = st.selectbox("Fase:", ["A","B","C"], index=["A","B","C"].index(row_e.get("fase","A")) if row_e.get("fase") in ["A","B","C"] else 0, key="_ukey8")
                    almt_e  = st.text_input("Alamat:", value=row_e.get("alamat",""), placeholder="Alamat rumah siswa")
                    if st.button("Simpan Data Siswa", type="primary", use_container_width=True):
                        update_siswa_info(sid_e, nis_e, nisn_e, almt_e, fase_e)
                        st.success(f"Data {ss_edit} berhasil disimpan.")
                        st.rerun()

        df_siswa = get_siswa_by_kelas(kelas_guru)
        if df_siswa.empty:
            st.info("Tambahkan daftar siswa di atas untuk mulai mengisi absensi.")
        else:
            df_absen_s = get_absen_siswa_hari(kelas_aktif, today_str)
            status_map = dict(zip(df_absen_s["id"], df_absen_s["status"]))
            ket_map    = dict(zip(df_absen_s["id"], df_absen_s["keterangan"]))
            cnt = {s: sum(1 for v in status_map.values() if v==s) for s in ["H","A","I","S"]}
            total = len(df_siswa)
            st.markdown(f"""
            <div class="kpi-grid" style="margin:10px 0">
              {kpi_card("Hadir",       cnt.get("H",0), f"dari {total} siswa",  "green")}
              {kpi_card("Tidak Hadir", cnt.get("A",0), "Alpa",                  "red"  if cnt.get("A",0)>0 else "")}
              {kpi_card("Izin",        cnt.get("I",0), "",                       "amber" if cnt.get("I",0)>0 else "")}
              {kpi_card("Sakit",       cnt.get("S",0), "",                       "blue"  if cnt.get("S",0)>0 else "")}
            </div>""", unsafe_allow_html=True)

            new_st, new_kt = {}, {}
            for _, s in df_siswa.iterrows():
                sid = int(s["id"])
                cur = status_map.get(sid, "H")
                ket2 = ket_map.get(sid, "")
                st.markdown(f"**{s['nama']}**")
                c1, c2 = st.columns([1.5, 2])
                with c1:
                    new_st[sid] = st.selectbox("", ["H","A","I","S"], index=["H","A","I","S"].index(cur),
                                               key=f"ss_{sid}", format_func=lambda x: STATUS_LABEL_SHORT[x],
                                               label_visibility="collapsed")
                with c2:
                    new_kt[sid] = st.text_input("", value=ket2, key=f"sk_{sid}",
                                                placeholder="Keterangan...", label_visibility="collapsed")
                st.markdown("<div style='border-bottom:1px solid #f4f6fa;margin:2px 0 8px'></div>", unsafe_allow_html=True)

            if st.button("Simpan Absensi Siswa", type="primary", use_container_width=True):
                data = [(sid, new_st[sid], new_kt[sid]) for sid in new_st]
                upsert_absen_siswa_bulk(data, guru_id, today_str)
                st.success(f"Absensi {len(data)} siswa kelas {kelas_aktif} berhasil disimpan.")
                st.rerun()

    with tab_nv:
        # ── Pilih kelas ────────────────────────────────────────────
        if is_bidstudi:
            kelas_nilai = st.selectbox("Pilih kelas yang diajar:", get_semua_kelas(), key="sel_kelas_nilai")
        elif len(kelas_list) > 1:
            kelas_nilai = st.selectbox("Pilih kelas:", kelas_list, key="sel_kelas_nilai")
        else:
            kelas_nilai = kelas_guru

        df_siswa_n = get_siswa_by_kelas(kelas_nilai)
        if df_siswa_n.empty:
            st.warning(f"Belum ada data siswa untuk {kelas_nilai}. Tambahkan di tab Absen Siswa.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1: sem_n = st.selectbox("Semester:", ["Ganjil","Genap"], key="sem_n_guru")
            with c2: thn_n = st.selectbox("Tahun Ajaran:", THN_LIST, index=1, key="thn_n_guru")
            with c3: mp_n  = st.selectbox("Mata Pelajaran:", mapel_list if mapel_list else ["— tambah di tab Profil —"], key="mp_n_guru")

            st.markdown("---")
            sub_input, sub_rekap, sub_rapor = st.tabs(["Input Nilai TP","Rekap Nilai","Generate Rapor"])

            with sub_input:
                st.markdown(f"**Input nilai — {mp_n} · {kelas_nilai} · Semester {sem_n} · {thn_n}**")
                st.caption("Kosongkan kolom TP yang belum ada pertemuan. NR dihitung otomatis.")

                # Header
                cols_hdr = st.columns([2.2,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.9,0.9,0.8])
                for col, lbl in zip(cols_hdr,["Nama Siswa","TP1","TP2","TP3","TP4","TP5","TP6","TP7","TP8","TP9","TP10","ASTS","ASAS","NR"]):
                    col.markdown(f"<div style='font-size:9px;font-weight:700;color:#9aa0b8;text-transform:uppercase;letter-spacing:.05em;padding-bottom:5px;border-bottom:1px solid #e4e8f0;text-align:center'>{lbl}</div>", unsafe_allow_html=True)

                tp_inputs = {}
                for _, s in df_siswa_n.iterrows():
                    sid      = int(s["id"])
                    existing = get_nilai_tp_siswa(sid, sem_n, thn_n, mp_n)
                    tp_inputs[sid] = {"nama": s["nama"]}
                    row_cols = st.columns([2.2,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.9,0.9,0.8])
                    with row_cols[0]:
                        st.markdown(f"<div style='font-size:13px;font-weight:500;padding:6px 0'>{s['nama']}</div>", unsafe_allow_html=True)
                    tp_vals = {}
                    for ti, col_key in enumerate(['tp1','tp2','tp3','tp4','tp5','tp6','tp7','tp8','tp9','tp10','asts','asas'], 1):
                        ex_v = existing.get(col_key)
                        ex_str = str(int(ex_v)) if ex_v not in (None,"","None") and str(ex_v) not in ("nan","None","") else ""
                        try:
                            ex_str = str(int(float(ex_v))) if ex_v is not None and str(ex_v) not in ("","None","nan") else ""
                        except: ex_str = ""
                        raw = row_cols[ti].text_input("", value=ex_str, key=f"{col_key}_{sid}",
                                                       label_visibility="collapsed", placeholder="—")
                        tp_vals[col_key] = float(raw) if raw.strip().replace('.','',1).isdigit() else None
                    nr_prev = hitung_nr(tp_vals)
                    nr_col  = "#1a5c3a" if nr_prev >= 70 else "#c0281e" if nr_prev > 0 else "#9aa0b8"
                    row_cols[13].markdown(f"<div style='font-family:DM Mono,monospace;font-size:13px;font-weight:700;color:{nr_col};padding:6px 0;text-align:center'>{nr_prev if nr_prev>0 else chr(8212)}</div>", unsafe_allow_html=True)
                    tp_inputs[sid]["vals"] = tp_vals
                    st.markdown("<div style='border-bottom:1px solid #f8f9fc;margin:1px 0'></div>", unsafe_allow_html=True)

                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                if st.button("Simpan Nilai", type="primary", use_container_width=True, key="btn_simpan_tp"):
                    for sid, data in tp_inputs.items():
                        upsert_nilai_tp(sid, guru_id, kelas_nilai, sem_n, thn_n, mp_n, data["vals"])
                    st.success(f"Nilai {mp_n} disimpan untuk {len(tp_inputs)} siswa.")
                    st.rerun()

            with sub_rekap:
                st.markdown(f"**Rekap NR semua mapel — {kelas_nilai}**")
                df_rekap = get_rekap_nr_kelas(kelas_nilai, sem_n, thn_n)
                if df_rekap.empty or df_rekap["mapel"].isna().all():
                    st.info("Belum ada nilai tersimpan untuk periode ini.")
                else:
                    pv = df_rekap.pivot_table(
                        index=["siswa_id","siswa"], columns="mapel",
                        values="nr", aggfunc="first"
                    ).reset_index()
                    pv.columns.name = None
                    mapel_cols = [c for c in pv.columns if c not in ["siswa_id","siswa"]]
                    pv["JMLH"] = pv[mapel_cols].sum(axis=1).round(1)
                    pv["RT"]   = pv[mapel_cols].mean(axis=1).round(2)
                    pv["RANK"] = pv["RT"].rank(ascending=False, method="min").astype(int)
                    st.dataframe(pv.drop(columns=["siswa_id"], errors="ignore"),
                                 use_container_width=True, hide_index=True)

            with sub_rapor:
                st.markdown("**Generate Rapor & Rekap Excel**")
                cr1, cr2 = st.columns(2)
                with cr1:
                    st.markdown("*Rapor per siswa (PDF)*")
                    siswa_opts = [(int(r["id"]),r["nama"]) for _,r in df_siswa_n.iterrows()]
                    ss         = st.selectbox("Pilih siswa:", [n for _,n in siswa_opts], key="sel_siswa_rpr")
                    ss_id      = next(i for i,n in siswa_opts if n==ss)
                    if st.button("Buat Rapor PDF", use_container_width=True, key="btn_pdf"):
                        df_nr = get_nr_semua_mapel_siswa(ss_id, sem_n, thn_n)
                        if not df_nr.empty:
                            df_nr = df_nr.rename(columns={"nr":"pengetahuan","capaian_maksimal":"capaian"})
                            df_nr["keterampilan"] = None
                            df_nr["sikap"]        = "B"
                        df_ekskul    = get_ekskul_siswa(ss_id, sem_n, thn_n)
                        catatan_data = get_catatan(ss_id, sem_n, thn_n)
                        absen_ct     = get_absen_count_siswa(ss_id, sem_n, thn_n)
                        df_sl        = get_siswa_by_kelas_lengkap(kelas_nilai)
                        s_row        = df_sl[df_sl["id"]==ss_id].iloc[0] if (not df_sl.empty and ss_id in df_sl["id"].values) else None
                        pdf = generate_rapor_pdf(
                            nama_siswa=ss, kelas=kelas_nilai, semester=sem_n,
                            tahun_ajar=thn_n, nilai_df=df_nr,
                            nama_wali_kelas=guru_info["nama"], nuptk_wali=get_nuptk(guru_id),
                            fase=s_row["fase"] if s_row is not None else "",
                            nis=s_row["nis"] if s_row is not None else "",
                            nisn=s_row["nisn"] if s_row is not None else "",
                            alamat_siswa=s_row["alamat"] if s_row is not None else "",
                            ekskul_df=df_ekskul, absen_count=absen_ct,
                            catatan_wali=catatan_data.get("catatan_wali",""),
                            tanggapan_ortu=catatan_data.get("tanggapan_ortu",""),
                        )
                        st.download_button(f"Unduh Rapor {ss}", data=pdf,
                            file_name=f"rapor_{ss.replace(' ','_')}_{sem_n}.pdf",
                            mime="application/pdf", use_container_width=True)

                with cr2:
                    st.markdown("*Rekap nilai TP per mapel (Excel)*")
                    mapel_xl = st.selectbox("Pilih mapel:", mapel_list if mapel_list else ["—"], key="mp_xl_guru")
                    if st.button("Buat Rekap Excel", use_container_width=True, key="btn_xl"):
                        df_xl = get_nilai_tp_kelas(kelas_nilai, sem_n, thn_n, mapel_xl)
                        sl    = [(int(r["id"]),r["nama"]) for _,r in df_siswa_n.iterrows()]
                        xl    = generate_rekap_tp_excel(kelas_nilai, sem_n, thn_n, mapel_xl, df_xl, sl)
                        st.download_button("Unduh Rekap Excel", data=xl,
                            file_name=f"rekap_{kelas_nilai.replace(' ','_')}_{mapel_xl.replace(' ','_')}_{sem_n}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True)

            # ── Ekskul & Catatan ────────────────────────────────────
            st.markdown("---")
            st.markdown("**Ekstrakulikuler & Catatan Rapor**")
            with st.expander("Input Ekstrakulikuler & Catatan Wali Kelas", expanded=False):
                ss_ekskul  = st.selectbox("Pilih siswa:", [r["nama"] for _,r in df_siswa_n.iterrows()], key="sel_ekskul")
                sid_ekskul = next(int(r["id"]) for _,r in df_siswa_n.iterrows() if r["nama"]==ss_ekskul)
                df_eks_now = get_ekskul_siswa(sid_ekskul, sem_n, thn_n)
                n_ekskul   = st.number_input("Jumlah ekskul:", 1, 5, value=max(len(df_eks_now),3), key="n_ekskul")
                ekskul_inputs = []
                for ei in range(int(n_ekskul)):
                    en = df_eks_now.iloc[ei]["nama_ekskul"] if ei < len(df_eks_now) else ""
                    ek = df_eks_now.iloc[ei]["keterangan"]  if ei < len(df_eks_now) else ""
                    ce1, ce2 = st.columns(2)
                    with ce1: en_new = st.text_input(f"Ekskul {ei+1}:", value=en, key=f"en_{sid_ekskul}_{ei}", placeholder="Nama ekskul")
                    with ce2: ek_new = st.text_input("Keterangan:", value=ek, key=f"ek_{sid_ekskul}_{ei}", placeholder="Baik/Sangat Baik")
                    if en_new.strip(): ekskul_inputs.append((en_new.strip(), ek_new.strip()))
                cat_now  = get_catatan(sid_ekskul, sem_n, thn_n)
                cat_wali = st.text_area("Catatan Wali Kelas:", value=cat_now.get("catatan_wali",""),
                                         placeholder="Contoh: Siswa menunjukkan perkembangan yang baik...",
                                         height=80, key=f"cat_{sid_ekskul}")
                if st.button("Simpan Ekskul & Catatan", use_container_width=True, type="primary", key="btn_eks"):
                    for en_s, ek_s in ekskul_inputs:
                        upsert_ekskul(sid_ekskul, guru_id, sem_n, thn_n, en_s, ek_s)
                    upsert_catatan(sid_ekskul, guru_id, sem_n, thn_n, cat_wali)
                    st.success("Data berhasil disimpan.")

    with tab_jg:
        st.markdown("**Tulis jurnal mengajar hari ini**")
        with st.form("form_jurnal", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                tgl_j = st.date_input("Tanggal:", value=date.today(), key="_ukey9")
                mp_j  = st.selectbox("Mata pelajaran:", mapel_list if mapel_list else ["—"], key="_ukey10")
            with c2:
                if is_bidstudi:
                    kls_j = st.selectbox("Kelas yang diajar:", get_semua_kelas(), key="jg_kelas_sel_guru")
                else:
                    kls_j = st.text_input("Kelas:", value=kelas_guru)
                topik = st.text_input("Topik / Materi:", placeholder="Contoh: Pecahan senilai")
            akt = st.text_area("Kegiatan belajar mengajar:", placeholder="Ceritakan kegiatan yang dilakukan di kelas hari ini...", height=130)
            c3, c4 = st.columns(2)
            with c3: media  = st.text_input("Media / alat dipakai:", placeholder="Buku, papan tulis, LKS...")
            with c4: ctt    = st.text_input("Catatan / tindak lanjut:", placeholder="Temuan atau hal yang perlu ditindaklanjuti...")
            if st.form_submit_button("Simpan Jurnal", use_container_width=True):
                if not topik or not akt: st.error("Topik dan kegiatan wajib diisi.")
                else:
                    simpan_jurnal(guru_id, str(tgl_j), kls_j, mp_j, topik, akt, media, ctt)
                    st.success("Jurnal berhasil disimpan. Kepala sekolah dan wali murid dapat melihatnya.")

        st.markdown("---")
        st.markdown("**Jurnal yang sudah ditulis:**")
        df_jg = get_jurnal_guru(guru_id, limit=20)
        if df_jg.empty: st.info("Belum ada jurnal. Tulis jurnal pertama Anda di atas.")
        else:
            for _, j in df_jg.iterrows():
                with st.expander(f"{j['tanggal']} · {j['kelas']} · {j['topik']}"):
                    st.markdown(f"**Mata Pelajaran:** {j['mapel']}")
                    st.markdown(f"**Kegiatan:** {j['aktivitas']}")
                    if j["media"]:   st.markdown(f"**Media:** {j['media']}")
                    if j["catatan"]: st.markdown(f"**Catatan:** {j['catatan']}")

    with tab_agnd:
        with st.expander("Tambah agenda baru", expanded=False):
            with st.form("form_ag_gr"):
                judul = st.text_input("Judul agenda:", placeholder="Contoh: Kunjungan Belajar Kelas III")
                c1, c2 = st.columns(2)
                with c1: kat_ks = st.selectbox("Kategori:", KATEGORI, key="kat_agenda_ks")
                with c2: tgl_ag = st.date_input("Tanggal:", value=date.today(), key="tgl_ag_gr")
                desk = st.text_area("Keterangan:", placeholder="Informasi tambahan untuk wali murid...")
                if st.form_submit_button("Simpan Agenda", use_container_width=True):
                    if not judul: st.error("Judul wajib diisi.")
                    else:
                        tambah_agenda(judul, desk, tgl_ag, "", kat, guru_info["nama"].split(",")[0])
                        st.success("Agenda berhasil disimpan dan dapat dilihat oleh wali murid.")
                        st.rerun()

        df_ag_gr = get_agenda_mendatang()
        if df_ag_gr.empty: st.info("Belum ada agenda mendatang.")
        else:
            st.markdown("**Agenda mendatang:**")
            for _, ag in df_ag_gr.iterrows():
                st.markdown(agenda_card(ag), unsafe_allow_html=True)

    with tab_profil:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e4e8f0;border-radius:12px;padding:20px;margin-bottom:16px">
          <div style="font-size:17px;font-weight:700;color:#1a1d2e">{guru_info['nama']}</div>
          <div style="font-size:14px;color:#9aa0b8;margin-top:4px">{_kls_label}</div>
        </div>""", unsafe_allow_html=True)

        # NUPTK
        st.markdown("**NUPTK Anda:**")
        nuptk_now = get_nuptk(guru_id)
        nuptk_inp = st.text_input("Nomor NUPTK:", value=nuptk_now,
                                   placeholder="Contoh: 1234567890123456")
        if st.button("Simpan NUPTK", use_container_width=True):
            update_nuptk(guru_id, nuptk_inp)
            st.success("NUPTK berhasil disimpan.")
            st.rerun()
        st.markdown("---")

        st.markdown("**Mata pelajaran yang Anda ajar:**")
        if mapel_list:
            pills = " ".join([f'<span class="bdg bdg-blue" style="margin:2px;font-size:12px;padding:4px 12px">{m}</span>' for m in mapel_list])
            st.markdown(f'<div style="margin-bottom:14px">{pills}</div>', unsafe_allow_html=True)
            mh = st.selectbox("Hapus mata pelajaran:", ["— pilih —"]+mapel_list, key="mh_profil")
            if st.button("Hapus", key="btn_hapus") and mh != "— pilih —":
                delete_mapel_guru(guru_id, mh); st.success(f"{mh} dihapus."); st.rerun()
        else:
            st.info("Belum ada mata pelajaran. Tambahkan di bawah.")

        st.markdown("---")
        if is_bidstudi:
            st.info("Guru Bidang Studi — dapat mengajar dan input nilai di semua kelas sekolah.")
        else:
            st.markdown("**Kelas yang Anda ampu:**")
            for k in kelas_list:
                st.markdown(f'<span class="bdg bdg-green" style="margin:3px 3px 3px 0;font-size:13px;padding:5px 12px;display:inline-block">{k}</span>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Tambah mata pelajaran:**")
        SARAN = ["Tematik","Matematika","Bahasa Indonesia","Bahasa Inggris","IPA","IPS","PPKn","SBdP","PJOK","PAI","PADB","B. Arab","TIK","Tahfidh","Mulok"]
        mp_saran = st.selectbox("Pilih dari daftar:", ["— atau ketik di bawah —"]+SARAN, key="mp_saran_profil")
        mp_man   = st.text_input("Atau ketik nama mata pelajaran:", placeholder="Contoh: Seni Budaya")
        mp_final = mp_man.strip() if mp_man.strip() else (mp_saran if mp_saran!="— atau ketik di bawah —" else "")
        if st.button("Tambah Mata Pelajaran", type="primary", use_container_width=True):
            if not mp_final: st.error("Pilih atau ketik nama mata pelajaran.")
            elif mp_final in mapel_list: st.warning(f"{mp_final} sudah ada.")
            else:
                ok, msg = add_mapel_guru(guru_id, mp_final)
                if ok: st.success(f"{mp_final} berhasil ditambahkan."); st.rerun()
                else:  st.error(msg)


# ══════════════════════════════════════════════════════════════════
# WALI MURID
# ══════════════════════════════════════════════════════════════════
elif role == "walimurid":
    st.markdown("""
    <div class="wm-banner">
      <h3>Selamat datang, Wali Murid</h3>
      <p>SD Taman Harapan 1 Bekasi — Pilih kelas anak Anda untuk melihat kegiatan harian dan agenda sekolah.</p>
    </div>""", unsafe_allow_html=True)

    tab_wm_kelas, tab_wm_agenda = st.tabs(["Kegiatan Kelas", "Agenda Sekolah"])

    with tab_wm_kelas:
        semua_kelas = get_semua_kelas()
        if not semua_kelas:
            st.info("Data kelas belum tersedia.")
        else:
            kelas_wm = st.selectbox("Pilih kelas anak Anda:", semua_kelas, key="kelas_wm_sel")
            df_jk    = get_jurnal_by_kelas(kelas_wm)
            if df_jk.empty:
                st.markdown(f'<div class="alrt blue">Belum ada catatan kegiatan dari guru kelas <b>{kelas_wm}</b>.<br><span style="font-size:13px">Catatan akan muncul setelah guru mengisi jurnal harian.</span></div>', unsafe_allow_html=True)
            else:
                df_jk["tanggal_dt"] = pd.to_datetime(df_jk["tanggal"], errors="coerce")
                for tgl_dt, grp in df_jk.groupby("tanggal_dt", sort=False):
                    tgl_label = tgl_dt.strftime("%A, %d %B %Y") if pd.notna(tgl_dt) else str(tgl_dt)
                    st.markdown(f"""
                    <div style="background:#1a5c3a;color:#fff;border-radius:10px 10px 0 0;
                         padding:10px 16px;margin-top:14px;font-size:14px;font-weight:600">{tgl_label}</div>""", unsafe_allow_html=True)
                    for _, j in grp.iterrows():
                        guru_short = str(j.get("guru_nama","")).split(",")[0]
                        st.markdown(f"""
                        <div style="background:#fff;border:1px solid #e4e8f0;border-top:none;
                             padding:16px;margin-bottom:2px;border-radius:0 0 10px 10px">
                          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
                            <span style="font-size:15px;font-weight:600;color:#1a1d2e">{j.get('topik','')}</span>
                            <span class="bdg bdg-green" style="font-size:10px">{j.get('mapel','')}</span>
                            <span style="font-size:12px;color:#9aa0b8;margin-left:auto">{guru_short}</span>
                          </div>
                          <div style="font-size:14px;color:#5a6080;line-height:1.6;
                               background:#f4f6fa;border-radius:8px;padding:12px 14px">{j.get('aktivitas','')}</div>
                          {('<div style="margin-top:8px;font-size:13px;color:#9aa0b8">Media: '+j.get("media","")+"</div>") if j.get("media") else ""}
                          {('<div style="font-size:13px;color:#9aa0b8">Catatan guru: '+j.get("catatan","")+"</div>") if j.get("catatan") else ""}
                        </div>""", unsafe_allow_html=True)

    with tab_wm_agenda:
        st.markdown("**Agenda dan pengumuman resmi sekolah:**")
        df_ag_wm   = get_agenda_mendatang()
        df_ag_lalu = get_agenda_semua()
        if not df_ag_lalu.empty:
            df_ag_lalu = df_ag_lalu[df_ag_lalu["tanggal"] < str(date.today())]

        if df_ag_wm.empty and (df_ag_lalu.empty if not df_ag_lalu.empty else True):
            st.info("Belum ada agenda yang dipublikasikan.")
        else:
            if not df_ag_wm.empty:
                st.markdown("**Agenda mendatang:**")
                for _, ag in df_ag_wm.iterrows():
                    st.markdown(agenda_card(ag), unsafe_allow_html=True)
            if not df_ag_lalu.empty:
                with st.expander(f"Agenda yang sudah berlalu ({len(df_ag_lalu)})"):
                    for _, ag in df_ag_lalu.iterrows():
                        st.markdown(agenda_card(ag), unsafe_allow_html=True)
