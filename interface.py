import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="PERT / CPM Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton>button[kind="secondary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d2d44 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h2 {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        animation: fadeIn 0.5s ease-in;
    }
    
    [data-testid="stHorizontalBlock"],
    [data-testid="column"],
    [data-testid="stVerticalBlock"],
    [data-testid="element-container"],
    div[data-testid="stMetric"],
    div[data-testid="stMetric"] > div,
    .row-widget,
    .stMarkdown {
        background: transparent !important;
    }
    
    /* Force remove all default backgrounds */
    div[class*="css"] {
        background: transparent !important;
    }
    
    /* Except for our custom cards */
    .glass-card,
    .input-card,
    .metric-card,
    .critical-path-banner,
    .empty-state,
    .sidebar-card {
        background: initial !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    .input-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(245,247,250,0.98) 100%) !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .critical-path-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
    }
    
    .empty-state {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,242,245,0.95) 100%) !important;
    }
    
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .input-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(245,247,250,0.98) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border: 2px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
    }
    
    .critical-path-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        margin: 2rem 0;
        border: 2px solid rgba(255,255,255,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,242,245,0.95) 100%);
        border-radius: 24px;
        border: 3px dashed rgba(102, 126, 234, 0.3);
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255,255,255,0.9);
    }
    
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    .stDataFrame tbody tr {
        background-color: white !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #f8fafc !important;
    }
    
    .stDataFrame td {
        background-color: transparent !important;
        color: #1e293b !important;
    }
    
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }
    
    .stTextInput input, .stNumberInput input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        font-size: 0.95rem;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def calculate_pert(task_list):
    tasks = {}
    for t in task_list:
        code = t["Code"]
        preds = [p.strip().upper() for p in t["Predecesseurs"].split(",") if p.strip()]
        tasks[code] = {
            "code": code,
            "duree": int(t["Duree"]),
            "preds": preds
        }
    computed = set()
    while len(computed) < len(tasks):
        progress = False
        for t, info in tasks.items():
            if t in computed:
                continue
            valid_preds = [p for p in info["preds"] if p in tasks]
            if all(p in computed for p in valid_preds):
                start = 0 if not valid_preds else max(tasks[p]["fin_tot"] for p in valid_preds)
                info["debut_tot"] = start
                info["fin_tot"] = start + info["duree"]
                computed.add(t)
                progress = True
        if not progress:
            return None, "Erreur: dépendance circulaire ou tâche manquante."
    project_duration = max(t["fin_tot"] for t in tasks.values())
    for t in tasks:
        tasks[t]["fin_tard"] = float("inf")
        tasks[t]["debut_tard"] = float("inf")
    all_preds = [p for t in tasks.values() for p in t["preds"]]
    end_tasks = [t for t in tasks if t not in all_preds]
    for t in end_tasks:
        tasks[t]["fin_tard"] = project_duration
        tasks[t]["debut_tard"] = project_duration - tasks[t]["duree"]
    sorted_tasks = sorted(tasks.keys(), key=lambda x: tasks[x]["fin_tot"], reverse=True)
    for _ in range(len(tasks)):
        for t in sorted_tasks:
            succs = [k for k, v in tasks.items() if t in v["preds"]]
            if succs:
                min_start = min(tasks[s]["debut_tard"] for s in succs)
                if min_start != float("inf"):
                    tasks[t]["fin_tard"] = min_start
                    tasks[t]["debut_tard"] = min_start - tasks[t]["duree"]
            if tasks[t]["debut_tard"] != float("inf"):
                tasks[t]["marge"] = tasks[t]["debut_tard"] - tasks[t]["debut_tot"]
    return tasks, project_duration

def create_gantt_chart(results):
    data = []
    for code, info in results.items():
        is_critical = info["marge"] == 0
        data.append({
            "Task": code,
            "Start": info["debut_tot"],
            "Finish": info["fin_tot"],
            "Duration": info["duree"],
            "Critical": is_critical
        })
    df = pd.DataFrame(data)
    df = df.sort_values("Start")
    fig = go.Figure()
    for _, row in df.iterrows():
        if row["Critical"]:
            color = "#ff6b6b"
            line_color = "#ee5a6f"
        else:
            color = "#667eea"
            line_color = "#764ba2"
        fig.add_trace(go.Bar(
            x=[row["Duration"]],
            y=[row["Task"]],
            orientation='h',
            name=row["Task"],
            marker=dict(
                color=color,
                line=dict(color=line_color, width=2),
                pattern=dict(shape="/" if row["Critical"] else "")
            ),
            text=f"<b>{row['Task']}</b> ({row['Duration']}j)",
            textposition='inside',
            textfont=dict(color='white', size=14, family='Inter'),
            base=row["Start"],
            showlegend=False,
            hovertemplate=f"<b>{row['Task']}</b><br>Début: {row['Start']}<br>Fin: {row['Finish']}<br>Durée: {row['Duration']}j<br>{'🔴 Critique' if row['Critical'] else '✅ Non-critique'}<extra></extra>"
        ))
    fig.update_layout(
        title=dict(
            text="📊 Diagramme de Gantt Interactif",
            font=dict(size=24, color="#1e293b", family="Inter", weight=800)
        ),
        xaxis_title="Temps (jours)",
        yaxis_title="Tâches",
        height=500,
        barmode='overlay',
        plot_bgcolor='rgba(248,250,252,0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13, family='Inter', color="#475569"),
        margin=dict(l=80, r=50, t=80, b=50),
        xaxis=dict(
            gridcolor='rgba(203,213,225,0.3)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgba(203,213,225,0.3)',
            showgrid=True
        )
    )
    return fig

with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 📌 Guide d'utilisation")
    st.markdown("""
    **Étapes simples:**
    
    1️⃣ Ajoutez vos tâches avec leur code  
    2️⃣ Définissez la durée de chaque tâche  
    3️⃣ Indiquez les prédécesseurs  
    4️⃣ Cliquez sur "Calculer"
    
    **💡 Le saviez-vous ?**
    - Tâches critiques = marge de 0
    - Le chemin critique = durée minimale
    - Codes courts recommandés (A, B, C...)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 📖 Définitions")
    with st.expander("🎯 PERT/CPM"):
        st.markdown("""
        Techniques de gestion de projet permettant de:
        - ✅ Planifier les tâches
        - ✅ Identifier les dépendances
        - ✅ Calculer la durée minimale
        - ✅ Trouver le chemin critique
        """)
    with st.expander("📚 Glossaire"):
        st.markdown("""
        **Début Tôt** → Date la plus précoce  
        **Fin Tôt** → Date de fin au plus tôt  
        **Début Tard** → Date de début au plus tard  
        **Fin Tard** → Date de fin au plus tard  
        **Marge** → Retard possible sans impact  
        **Chemin Critique** → Séquence sans marge
        """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <h1 class='hero-title'>📊 PERT / CPM Pro</h1>
        <p class='hero-subtitle'>✨ Planifiez, optimisez et maîtrisez vos projets avec élégance</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">➕ Nouvelle Tâche</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1.5, 1.5, 3, 1.5])
with col1:
    code_input = st.text_input("📝 Code", placeholder="A", label_visibility="visible").upper()
with col2:
    duree_input = st.number_input("⏱️ Durée (j)", min_value=1, step=1, value=1)
with col3:
    preds_input = st.text_input("🔗 Prédécesseurs", placeholder="A, B")
with col4:
    st.write("")
    st.write("")
    if st.button("✨ Ajouter", type="primary"):
        if code_input:
            if any(t["Code"] == code_input for t in st.session_state.tasks):
                st.error(f"❌ La tâche **{code_input}** existe déjà")
            else:
                st.session_state.tasks.append({
                    "Code": code_input,
                    "Duree": duree_input,
                    "Predecesseurs": preds_input
                })
                st.success(f"✅ Tâche **{code_input}** ajoutée!")
                st.rerun()
        else:
            st.warning("⚠️ Le code est obligatoire")
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.tasks:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_header, col_badge, col_button = st.columns([3, 1, 1])
    with col_header:
        st.markdown('<div class="section-title">📋 Mes Tâches</div>', unsafe_allow_html=True)
    with col_badge:
        st.markdown(f'<div class="badge">{len(st.session_state.tasks)} tâches</div>', unsafe_allow_html=True)
    with col_button:
        if st.button("🗑️ Effacer", type="secondary"):
            st.session_state.tasks = []
            st.rerun()
    df_tasks = pd.DataFrame(st.session_state.tasks)
    st.dataframe(
        df_tasks,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Code": st.column_config.TextColumn("📝 Code", width="small"),
            "Duree": st.column_config.NumberColumn("⏱️ Durée", width="small"),
            "Predecesseurs": st.column_config.TextColumn("🔗 Prédécesseurs", width="medium")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    col_calc1, col_calc2, col_calc3 = st.columns([1, 2, 1])
    with col_calc2:
        if st.button("🚀 Lancer le Calcul PERT/CPM", type="primary", use_container_width=True):
            with st.spinner("⚡ Analyse en cours..."):
                results, duration = calculate_pert(st.session_state.tasks)
                if isinstance(duration, str):
                    st.error(f"❌ {duration}")
                else:
                    final_data = []
                    critical_path = []
                    for code, data in results.items():
                        is_critical = data["marge"] == 0
                        if is_critical:
                            critical_path.append(code)
                        final_data.append({
                            "Tâche": code,
                            "Durée": data["duree"],
                            "Début Tôt": data["debut_tot"],
                            "Fin Tôt": data["fin_tot"],
                            "Début Tard": data["debut_tard"],
                            "Fin Tard": data["fin_tard"],
                            "Marge": data["marge"],
                            "Critique": "🔴 Oui" if is_critical else "✅ Non"
                        })
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📊 Métriques Clés</div>', unsafe_allow_html=True)
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(
                            label="⏱️ Durée Totale",
                            value=f"{duration}",
                            help="Durée minimale du projet"
                        )
                        st.markdown("jours")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(
                            label="🔴 Tâches Critiques",
                            value=f"{len(critical_path)}",
                            help="Tâches sans marge"
                        )
                        st.markdown(f"sur {len(st.session_state.tasks)}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with metric_col3:
                        non_critical = len(st.session_state.tasks) - len(critical_path)
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(
                            label="✨ Flexibilité",
                            value=f"{non_critical}",
                            help="Tâches avec marge"
                        )
                        st.markdown("tâches")
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    critical_path_str = " → ".join(critical_path)
                    st.markdown(f"""
                        <div class='critical-path-banner'>
                            🔥 Chemin Critique: {critical_path_str}
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    gantt_chart = create_gantt_chart(results)
                    st.plotly_chart(gantt_chart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📋 Analyse Détaillée</div>', unsafe_allow_html=True)
                    df_res = pd.DataFrame(final_data)
                    def highlight_critical(row):
                        if row["Critique"] == "🔴 Oui":
                            return ["background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b; font-weight: 700;"] * len(row)
                        return ["background: white;"] * len(row)
                    st.dataframe(
                        df_res.style.apply(highlight_critical, axis=1),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Tâche": st.column_config.TextColumn("📝 Tâche", width="small"),
                            "Durée": st.column_config.NumberColumn("⏱️ Durée", width="small"),
                            "Début Tôt": st.column_config.NumberColumn("▶️ Début Tôt", width="small"),
                            "Fin Tôt": st.column_config.NumberColumn("⏸️ Fin Tôt", width="small"),
                            "Début Tard": st.column_config.NumberColumn("⏩ Début Tard", width="small"),
                            "Fin Tard": st.column_config.NumberColumn("⏹️ Fin Tard", width="small"),
                            "Marge": st.column_config.NumberColumn("📊 Marge", width="small"),
                            "Critique": st.column_config.TextColumn("🎯 Critique", width="small")
                        }
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>🚀</div>
            <h2 style='color: #1e293b; font-weight: 800; margin-bottom: 1rem;'>Prêt à commencer ?</h2>
            <p style='color: #64748b; font-size: 1.1rem;'>Ajoutez votre première tâche pour démarrer l'analyse de votre projet</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='footer'>
        <p>✨ Développé avec passion | PERT/CPM Calculator Pro v3.0 ✨</p>
        <p style='font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;'>Gestion de projet intelligente et moderne</p>
    </div>
""", unsafe_allow_html=True)