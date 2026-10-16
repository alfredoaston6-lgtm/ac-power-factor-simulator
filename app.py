import numpy as np
import plotly.graph_objects as go
import streamlit as st

from calculations import hitung_daya_ac, validasi_input

st.set_page_config(
    page_title="AC Power Factor Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS ringan untuk nuansa laboratorium virtual.
st.markdown("""
<style>
    .main { background: #f5f8fc; }
    .block-container { padding-top: 1.4rem; padding-bottom: 2rem; }
    .hero {
        padding: 1.25rem 1.5rem; border-radius: 18px;
        background: linear-gradient(120deg, #102a43, #176b87);
        color: white; margin-bottom: 1rem;
    }
    .hero h1 { color: white; margin: 0 0 .35rem 0; }
    .hero p { color: #e5f3fa; margin: 0; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e3eaf2;
        padding: 1rem; border-radius: 14px;
    }
    .note {
        background: #eaf4fb; border-left: 4px solid #168aad;
        padding: .8rem 1rem; border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

if "hasil" not in st.session_state:
    st.session_state.hasil = None
if "nilai_form" not in st.session_state:
    st.session_state.nilai_form = {
        "jenis": "Induktif",
        "tegangan": 220.0,
        "arus": 5.0,
        "sudut": 30.0,
    }

st.markdown("""
<div class="hero">
  <h1>⚡ AC POWER FACTOR SIMULATOR</h1>
  <p>Simulasi Faktor Daya Rangkaian AC · Laboratorium virtual untuk memahami fase dan daya listrik.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Pengaturan simulasi")
    # Reset diproses sebelum widget dibuat agar state widget benar-benar kembali ke awal.
    if st.button("↺ Reset", use_container_width=True):
        st.session_state.hasil = None
        st.session_state.nilai_form = {
            "jenis": "Induktif", "tegangan": 220.0, "arus": 5.0, "sudut": 30.0
        }
        for k in ("jenis_input", "tegangan_input", "arus_input", "sudut_input"):
            st.session_state.pop(k, None)
        st.rerun()

    defaults = st.session_state.nilai_form
    with st.form("form_simulasi"):
        jenis = st.selectbox(
            "Jenis beban",
            ["Resistif", "Induktif", "Kapasitif"],
            index=["Resistif", "Induktif", "Kapasitif"].index(defaults["jenis"]),
            help="Pilih karakter beban ideal yang akan dimodelkan.",
            key="jenis_input",
        )
        tegangan = st.number_input(
            "Tegangan AC (V RMS)", min_value=-1_000_000.0, max_value=1_000_000.0,
            value=float(defaults["tegangan"]), step=10.0, format="%.2f", key="tegangan_input"
        )
        arus = st.number_input(
            "Arus AC (A RMS)", min_value=-1_000_000.0, max_value=1_000_000.0,
            value=float(defaults["arus"]), step=0.5, format="%.2f", key="arus_input"
        )
        sudut = st.number_input(
            "Sudut fase φ (derajat)", min_value=-89.9, max_value=89.9,
            value=float(defaults["sudut"]), step=1.0, format="%.1f",
            help="Induktif: positif; kapasitif: negatif; resistif ideal: 0°.",
            key="sudut_input",
        )
        mulai = st.form_submit_button("▶ Mulai Simulasi", use_container_width=True)

    st.markdown("---")
    st.caption("Model pembelajaran")
    st.write("Sudut fase adalah parameter masukan pada model ini. Sudut tidak dihitung otomatis dari nilai komponen fisik R, L, dan C.")

if mulai:
    kesalahan = validasi_input(jenis, tegangan, arus, sudut)
    if kesalahan:
        st.session_state.hasil = None
        st.error("Input belum valid: " + " ".join(kesalahan))
    else:
        st.session_state.nilai_form = {
            "jenis": jenis, "tegangan": tegangan, "arus": arus, "sudut": sudut
        }
        st.session_state.hasil = hitung_daya_ac(jenis, tegangan, arus, sudut)

hasil = st.session_state.hasil

if hasil is None:
    st.info("Atur parameter di panel kiri, lalu tekan **Mulai Simulasi** untuk menghitung dan menampilkan hasil.")
    st.markdown("""
    <div class="note"><b>Petunjuk:</b> Gunakan nilai RMS untuk tegangan dan arus. Pada beban induktif arus tertinggal dari tegangan (lagging), sedangkan pada beban kapasitif arus mendahului tegangan (leading).</div>
    """, unsafe_allow_html=True)
    st.stop()

st.subheader("Panel hasil pengukuran")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Faktor daya (PF)", f"{hasil['pf']:.4f}")
m2.metric("Daya aktif (P)", f"{hasil['p']:.2f} W")
m3.metric("Daya reaktif (Q)", f"{hasil['q']:.2f} VAR")
m4.metric("Daya semu (S)", f"{hasil['s']:.2f} VA")
st.caption(f"Karakter faktor daya: **{hasil['karakter_pf']}** · Sudut fase: **{hasil['sudut']}°**")

kiri, kanan = st.columns([1, 1.35], gap="large")

with kiri:
    st.subheader("Rangkaian AC")
    # Diagram vektor/rangkaian skematis yang dibuat dengan SVG; simbol beban berubah.
    if hasil["jenis"] == "Resistif":
        simbol = '<rect x="300" y="98" width="90" height="38" rx="4" fill="#fff" stroke="#176b87" stroke-width="3"/><text x="345" y="122" text-anchor="middle" font-size="16" fill="#102a43">R</text>'
        jenis_teks = "Beban resistif"
    elif hasil["jenis"] == "Induktif":
        simbol = '<path d="M300 117 c0 -24 22 -24 22 0 c0 -24 22 -24 22 0 c0 -24 22 -24 22 0 c0 -24 22 -24 22 0" fill="none" stroke="#176b87" stroke-width="3"/><text x="345" y="155" text-anchor="middle" font-size="15" fill="#102a43">L</text>'
        jenis_teks = "Beban induktif"
    else:
        simbol = '<path d="M325 95 V139 M365 95 V139" stroke="#176b87" stroke-width="4"/><text x="345" y="158" text-anchor="middle" font-size="15" fill="#102a43">C</text>'
        jenis_teks = "Beban kapasitif"
    svg = f"""
    <svg viewBox="0 0 520 245" width="100%" xmlns="http://www.w3.org/2000/svg">
      <rect x="1" y="1" width="518" height="243" rx="14" fill="#ffffff" stroke="#d9e4ef"/>
      <path d="M110 117 H170 M170 117 V70 H300 M390 117 H440 V190 H110 V157" fill="none" stroke="#263746" stroke-width="3"/>
      <circle cx="110" cy="117" r="40" fill="#f1f8fc" stroke="#176b87" stroke-width="3"/>
      <path d="M78 117 C88 91 99 91 110 117 S132 143 142 117" fill="none" stroke="#176b87" stroke-width="2.5"/>
      <path d="M110 157 V190" fill="none" stroke="#263746" stroke-width="3"/>
      {simbol}
      <path d="M215 58 H268" stroke="#d97706" stroke-width="3" fill="none"/>
      <path d="M258 50 L268 58 L258 66" stroke="#d97706" stroke-width="3" fill="none"/>
      <text x="240" y="43" text-anchor="middle" font-size="14" fill="#9a5800">I = {hasil['arus']:.2f} A</text>
      <text x="110" y="176" text-anchor="middle" font-size="14" fill="#102a43">Sumber AC</text>
      <text x="345" y="82" text-anchor="middle" font-size="14" fill="#102a43">{jenis_teks}</text>
      <text x="270" y="220" text-anchor="middle" font-size="14" fill="#102a43">V = {hasil['tegangan']:.2f} V RMS · φ = {hasil['sudut']:+.1f}°</text>
    </svg>
    """
    st.markdown(svg, unsafe_allow_html=True)
    st.caption("Skema konseptual, bukan gambar instalasi atau penentuan nilai komponen fisik.")

with kanan:
    st.subheader("Gelombang tegangan dan arus")
    frekuensi = 50.0  # Frekuensi ilustrasi, bukan input model daya.
    t = np.linspace(0, 2 / frekuensi, 1000)
    omega = 2 * np.pi * frekuensi
    phi_rad = np.deg2rad(hasil["sudut"])
    v = np.sqrt(2) * hasil["tegangan"] * np.sin(omega * t)
    i = np.sqrt(2) * hasil["arus"] * np.sin(omega * t - phi_rad)
    fig_gel = go.Figure()
    fig_gel.add_trace(go.Scatter(x=t * 1000, y=v, mode="lines", name="Tegangan v(t)", line=dict(width=3, color="#176b87")))
    fig_gel.add_trace(go.Scatter(x=t * 1000, y=i, mode="lines", name="Arus i(t)", line=dict(width=3, color="#e58a2b")))
    fig_gel.update_layout(
        template="plotly_white", height=330, margin=dict(l=10, r=10, t=25, b=10),
        xaxis_title="Waktu (ms)", yaxis_title="Nilai sesaat (V / A)",
        legend=dict(orientation="h", y=1.12), hovermode="x unified"
    )
    st.plotly_chart(fig_gel, use_container_width=True)
    st.caption("Frekuensi ilustrasi ditetapkan 50 Hz. Amplitudo puncak menggunakan √2 × nilai RMS.")

st.subheader("Segitiga daya")
fig_day = go.Figure()
P, Q, S = hasil["p"], hasil["q"], hasil["s"]
fig_day.add_trace(go.Scatter(
    x=[0, P], y=[0, 0], mode="lines+markers+text",
    text=["", f"P = {P:.2f} W"], textposition="bottom center",
    name="Daya aktif P", line=dict(color="#176b87", width=4)
))
fig_day.add_trace(go.Scatter(
    x=[P, P], y=[0, Q], mode="lines+markers+text",
    text=["", f"Q = {Q:+.2f} VAR"], textposition="middle right",
    name="Daya reaktif Q", line=dict(color="#e58a2b", width=4)
))
fig_day.add_trace(go.Scatter(
    x=[0, P], y=[0, Q], mode="lines+markers+text",
    text=["", f"S = {S:.2f} VA"], textposition="top left",
    name="Daya semu S", line=dict(color="#2f855a", width=4)
))
# Arc sudut phi, ditarik kecil di sekitar titik asal.
if S > 0:
    theta = np.linspace(0, phi_rad, 40)
    radius = max(S * 0.14, 0.001)
    fig_day.add_trace(go.Scatter(
        x=radius * np.cos(theta), y=radius * np.sin(theta),
        mode="lines", name=f"φ = {hasil['sudut']:+.1f}°",
        line=dict(color="#8b5cf6", width=2, dash="dot")
    ))
fig_day.update_layout(
    template="plotly_white", height=420, margin=dict(l=20, r=20, t=25, b=20),
    xaxis_title="Daya aktif P (W)", yaxis_title="Daya reaktif Q (VAR)",
    legend=dict(orientation="h", y=-0.2), showlegend=True
)
fig_day.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#64748b")
fig_day.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#64748b")
st.plotly_chart(fig_day, use_container_width=True)
st.caption(f"Pemeriksaan identitas: S² = {S**2:.2f} VA² dan P² + Q² = {(P**2 + Q**2):.2f} VA².")

st.subheader("Interpretasi otomatis")
if hasil["jenis"] == "Resistif":
    hubungan = "Tegangan dan arus sefase. Untuk beban resistif ideal, daya reaktif bernilai nol."
elif hasil["jenis"] == "Induktif":
    hubungan = "Arus tertinggal terhadap tegangan sebesar sudut fase yang dimasukkan (lagging); daya reaktif bernilai positif."
else:
    hubungan = "Arus mendahului tegangan sebesar nilai mutlak sudut fase (leading); daya reaktif bernilai negatif."

st.markdown(
    f"Pada model **{hasil['jenis'].lower()}**, tegangan adalah **{hasil['tegangan']:.2f} V RMS** dan arus **{hasil['arus']:.2f} A RMS**. "
    f"{hubungan} Faktor daya adalah **{hasil['pf']:.4f} ({hasil['karakter_pf']})**. "
    f"Daya aktif **P = {P:.2f} W** menyatakan laju rata-rata transfer energi; "
    f"daya reaktif **Q = {Q:+.2f} VAR** merepresentasikan pertukaran energi bolak-balik; "
    f"dan daya semu **S = {S:.2f} VA** adalah hasil kali tegangan dan arus RMS."
)
with st.expander("Lihat rumus yang digunakan"):
    st.latex(r"PF = |\cos(\phi)|")
    st.latex(r"S = V_{RMS} I_{RMS}")
    st.latex(r"P = V_{RMS} I_{RMS}\cos(\phi)")
    st.latex(r"Q = V_{RMS} I_{RMS}\sin(\phi)")
    st.latex(r"S^2 = P^2 + Q^2")
    st.write("Dalam rentang sudut yang divalidasi, cos(φ) positif. PF ditampilkan tanpa tanda negatif; tanda Q menunjukkan sifat induktif atau kapasitif.")
