import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página sin sidebar nativa
st.set_page_config(
    page_title="SP 2021–2025 | Atlas de Locação Residencial",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estado del botón para mostrar/esconder el panel de control
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = False

def alternar_menu():
    st.session_state.mostrar_menu = not st.session_state.mostrar_menu

# 2. CSS Editorial Minimalista (Inspiración Solara / Swiss Grid)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,400&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Esconder por completo la barra lateral nativa, el header y el footer de Streamlit */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header, footer {
        display: none !important;
    }

    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, sans-serif;
        background-color: #F6F5F2;
        color: #141413;
    }

    /* Barra de navegación superior minimalista */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 1px solid #DFDDD6;
        padding-bottom: 14px;
        margin-bottom: 28px;
    }
    .brand-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #5C5B57;
    }

    /* Tipografía Hero Editorial */
    .editorial-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 3.4rem;
        font-weight: 400;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #141413;
        margin-bottom: 12px;
    }
    .editorial-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.02rem;
        font-weight: 400;
        color: #5C5B57;
        max-width: 680px;
        line-height: 1.55;
    }

    /* Cinta de Métricas Estilo Arquitectónico */
    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        background: #FFFFFF;
        border: 1px solid #E2E0D8;
        border-radius: 12px;
        margin: 26px 0 30px 0;
        overflow: hidden;
    }
    .metric-cell {
        padding: 22px 24px;
        border-right: 1px solid #E2E0D8;
    }
    .metric-cell:last-child {
        border-right: none;
    }
    .m-index {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #8C8A84;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }
    .m-number {
        font-family: 'Instrument Serif', serif;
        font-size: 2.35rem;
        line-height: 1.0;
        color: #141413;
        margin-bottom: 8px;
    }
    .m-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #2E5A44;
        background: #E9F0EC;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }

    /* Contenedores blancos limpios */
    .clean-box {
        background: #FFFFFF;
        border: 1px solid #E2E0D8;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
    }
    .box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #F0EFEA;
        padding-bottom: 12px;
        margin-bottom: 14px;
    }
    .box-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        letter-spacing: -0.01em;
        color: #141413;
    }
    .box-code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #8C8A84;
    }

    /* Botón de alternar menú estilizado */
    div.stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.76rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        background-color: #141413 !important;
        color: #F6F5F2 !important;
        border: 1px solid #141413 !important;
        border-radius: 999px !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #141413 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data_processed/aluguel_distritos_2021_2025.csv")
    gdf = gpd.read_file("geodata/distritos_sp_wgs84.geojson")
    return df, gdf

try:
    df, gdf = carregar_dados()

    # --- CABECERA Y BOTÓN PARA ESCONDER/MOSTRAR MENÚ ---
    c_brand, c_btn = st.columns([4, 1])
    with c_brand:
        st.markdown(
            '<div class="brand-tag">UFMS DIGITAL • OBSERVATÓRIO URBANO DE SÃO PAULO // SÉRIE 2021–2025</div>',
            unsafe_allow_html=True
        )
    with c_btn:
        texto_btn = "✕ Fechar Parâmetros" if st.session_state.mostrar_menu else "☰ Parâmetros & Filtros"
        st.button(texto_btn, on_click=alternar_menu, use_container_width=True)

    st.markdown('<hr style="margin: 6px 0 24px 0; border: none; border-top: 1px solid #DFDDD6;">', unsafe_allow_html=True)

    # --- MENÚ DINÁMICO COLAPSABLE (OCULTO POR DEFECTO) ---
    if st.session_state.mostrar_menu:
        st.markdown('<div class="clean-box" style="background:#EFECE6; border-color:#DFDDD6;">', unsafe_allow_html=True)
        st.markdown('<div class="box-header"><span class="box-title">Painel de Parâmetros Metodológicos</span><span class="box-code">CONFIG // 00</span></div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1.2, 1.3, 1.5])
        with f1:
            ano_selecionado = st.select_slider("Ano de Referência Temporal", options=[2021, 2022, 2023, 2024, 2025], value=2025)
        with f2:
            metrica_mapa = st.radio(
                "Dimensão Cartográfica",
                ["valor_medio_m2", "variacao_acumulada_pct"],
                format_func=lambda x: "Valor Locatício (R$/m²)" if x == "valor_medio_m2" else "Variação Acumulada 2021–2025 (%)",
                horizontal=True
            )
        with f3:
            filtro_qualidade = st.multiselect(
                "Filtro de Governança (Status do Registro)",
                options=["Válido", "Estimado", "Incompleto"],
                default=["Válido", "Estimado", "Incompleto"]
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Controles rápidos en línea cuando el menú está escondido
        bar_left, bar_right = st.columns([2.5, 1.5])
        with bar_left:
            st.markdown('<div class="editorial-title">Atlas de Locação Residencial.</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="editorial-sub">'
                'Mapeamento histórico, qualificação metodológica e rastreabilidade do custo habitacional '
                'por metro quadrado nos 96 distritos administrativos de São Paulo.'
                '</div>',
                unsafe_allow_html=True
            )
        with bar_right:
            ano_selecionado = st.segmented_control(
                "Recorte Anual",
                options=[2021, 2022, 2023, 2024, 2025],
                default=2025
            )
            metrica_mapa = st.segmented_control(
                "Indicador Principal",
                options=["valor_medio_m2", "variacao_acumulada_pct"],
                format_func=lambda x: "Preço (R$/m²)" if x == "valor_medio_m2" else "Variação (%)",
                default="valor_medio_m2"
            )
            filtro_qualidade = ["Válido", "Estimado", "Incompleto"]

    # Valores por defecto por si el usuario desmarca algún segmented_control
    if not ano_selecionado:
        ano_selecionado = 2025
    if not metrica_mapa:
        metrica_mapa = "valor_medio_m2"

    df_ano = df[(df["ano"] == ano_selecionado) & (df["situacao_predominante"].isin(filtro_qualidade))]

    # --- CINTA EDITORIAL DE INDICADORES (BENTO STRIP) ---
    media_sp = df_ano["valor_medio_m2"].mean() if not df_ano.empty else 0
    mediana_sp = df_ano["valor_medio_m2"].median() if not df_ano.empty else 0
    var_media_sp = df_ano["variacao_acumulada_pct"].mean() if not df_ano.empty else 0
    dist_max = df_ano.loc[df_ano["valor_medio_m2"].idxmax()] if not df_ano.empty else None
    validos_cnt = len(df_ano[df_ano["situacao_predominante"] == "Válido"])

    nome_caro = dist_max["distrito_padronizado"].title() if dist_max is not None else "-"
    val_caro = dist_max["valor_medio_m2"] if dist_max is not None else 0

    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-cell">
            <div class="m-index">01 // Média Municipal ({ano_selecionado})</div>
            <div class="m-number">R$ {media_sp:.2f}</div>
            <span class="m-meta">Mediana: R$ {mediana_sp:.2f} /m²</span>
        </div>
        <div class="metric-cell">
            <div class="m-index">02 // Variação Acumulada</div>
            <div class="m-number">+{var_media_sp:.1f}%</div>
            <span class="m-meta">Base de referência: 2021</span>
        </div>
        <div class="metric-cell">
            <div class="m-index">03 // Valor Máximo Distrital</div>
            <div class="m-number">{nome_caro}</div>
            <span class="m-meta">R$ {val_caro:.2f} /m² observados</span>
        </div>
        <div class="metric-cell">
            <div class="metric-index m-index">04 // Cobertura & Governança</div>
            <div class="m-number">{len(df_ano)} <span style="font-size:1.2rem;color:#8C8A84;">/ 96</span></div>
            <span class="m-meta">{validos_cnt} diretos • {len(df_ano)-validos_cnt} estimados</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- LAYOUT ASIMÉTRICO PRINCIPAL ---
    col_mapa, col_inspetor = st.columns([1.85, 1.15], gap="medium")

    with col_mapa:
        st.markdown(f"""
        <div class="clean-box" style="padding-bottom:10px;">
            <div class="box-header">
                <span class="box-title">Cartografia dos Distritos Administrativos — {ano_selecionado}</span>
                <span class="box-code">GEOSAMPA // EPSG:4326</span>
            </div>
        """, unsafe_allow_html=True)

        # Paleta sobria y arquitectónica (Arena -> Verde Salvia -> Carbón / Terracota)
        escala_editorial = ["#EAE6DF", "#A3B899", "#4A7C59", "#1E3A2F", "#141413"] if metrica_mapa == "valor_medio_m2" else ["#D8E2DC", "#84A59D", "#F6BD60", "#F28482", "#9B2226"]

        fig_mapa = px.choropleth_map(
            df_ano,
            geojson=gdf.__geo_interface__,
            locations="distrito_padronizado",
            featureidkey="properties.distrito_padronizado",
            color=metrica_mapa,
            color_continuous_scale=escala_editorial,
            map_style="carto-positron",
            zoom=9.45,
            center={"lat": -23.625, "lon": -46.633},
            opacity=0.88,
            hover_name="distrito_padronizado",
            hover_data={
                "distrito_padronizado": False,
                "valor_medio_m2": ":.2f",
                "variacao_acumulada_pct": ":.2f",
                "fontes": True,
                "situacao_predominante": True
            },
            labels={
                "valor_medio_m2": "R$/m²",
                "variacao_acumulada_pct": "Acum. %",
                "fontes": "Fonte",
                "situacao_predominante": "Qualidade"
            }
        )
        fig_mapa.update_traces(marker_line_width=0.6, marker_line_color="#FFFFFF")
        fig_mapa.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            height=580,
            paper_bgcolor="#FFFFFF",
            font=dict(family="DM Sans", color="#141413"),
            coloraxis_colorbar=dict(
                title=dict(text="R$/m²" if metrica_mapa == "valor_medio_m2" else "Var. %", font=dict(family="JetBrains Mono", size=11)),
                thickness=10,
                len=0.6,
                x=0.96,
                bgcolor="rgba(255,255,255,0.85)"
            )
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_inspetor:
        st.markdown("""
        <div class="clean-box">
            <div class="box-header">
                <span class="box-title">Inspetor de Série Temporal e Rastreabilidade</span>
                <span class="box-code">SÉRIE // 21–25</span>
            </div>
        """, unsafe_allow_html=True)

        lista_distritos = sorted(df["distrito_padronizado"].unique())
        idx_padrao = lista_distritos.index("ITAIM BIBI") if "ITAIM BIBI" in lista_distritos else 0

        distrito_foco = st.selectbox(
            "Selecionar Distrito Administrativo",
            lista_distritos,
            index=idx_padrao,
            label_visibility="collapsed"
        )

        df_dist = df[df["distrito_padronizado"] == distrito_foco].sort_values("ano")
        reg_atual = df_dist[df_dist["ano"] == ano_selecionado].iloc[0]

        # Ficha tipográfica limpia del distrito
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin: 10px 0 16px 0;">
            <div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#8C8A84;">DISTRITO SELECIONADO</div>
                <div style="font-family:'Instrument Serif',serif; font-size:2.1rem; color:#141413; line-height:1.1;">{distrito_foco.title()}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#8C8A84;">VALOR EM {ano_selecionado}</div>
                <div style="font-family:'Instrument Serif',serif; font-size:2.1rem; color:#2E5A44; line-height:1.1;">R$ {reg_atual['valor_medio_m2']:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gráfico minimalista sin rejillas ruidosas
        fig_linha = go.Figure()
        fig_linha.add_trace(go.Scatter(
            x=df_dist["ano"],
            y=df_dist["valor_medio_m2"],
            mode="lines+markers+text",
            text=[f"R${v:.0f}" for v in df_dist["valor_medio_m2"]],
            textposition="top center",
            textfont=dict(family="JetBrains Mono", size=10, color="#5C5B57"),
            line=dict(color="#141413", width=2),
            marker=dict(size=7, color="#FFFFFF", line=dict(width=2, color="#141413")),
            fill="tozeroy",
            fillcolor="rgba(20, 20, 19, 0.04)"
        ))
        fig_linha.update_layout(
            height=225,
            margin=dict(l=5, r=5, t=24, b=5),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            showlegend=False,
            xaxis=dict(dtick=1, showgrid=False, linecolor="#E2E0D8", tickfont=dict(family="JetBrains Mono", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#F2F0EA", zeroline=False, showticklabels=False, range=[df_dist["valor_medio_m2"].min()*0.85, df_dist["valor_medio_m2"].max()*1.15])
        )
        st.plotly_chart(fig_linha, use_container_width=True)

        # Metadados de Governança e Ranking Rápido
        st.markdown(f"""
        <div style="border-top:1px solid #E2E0D8; padding-top:14px; margin-top:6px; font-size:0.84rem;">
            <div style="display:flex; justify-content:space-between; padding:5px 0;">
                <span style="color:#5C5B57;">Fonte Primária</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.76rem; color:#141413;">{reg_atual['fontes']}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:5px 0;">
                <span style="color:#5C5B57;">Qualificação do Dado</span>
                <span class="m-meta">{reg_atual['situacao_predominante'].upper()}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:5px 0;">
                <span style="color:#5C5B57;">Variação Acumulada (2021–{ano_selecionado})</span>
                <span style="font-family:'JetBrains Mono',monospace; font-weight:500;">+{reg_atual['variacao_acumulada_pct']:.2f}%</span>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Mini-tabla comparativa de extremos (Top 5 mais caros no ano)
        st.markdown("""
        <div class="clean-box" style="padding:18px 22px;">
            <div class="box-header" style="margin-bottom:8px; padding-bottom:8px;">
                <span class="box-title">Extremos Territoriais (Top 5 Distritos)</span>
                <span class="box-code">RANK // R$/M²</span>
            </div>
        """, unsafe_allow_html=True)
        top5 = df_ano.nlargest(5, "valor_medio_m2")[["distrito_padronizado", "valor_medio_m2", "situacao_predominante"]]
        for i, row in enumerate(top5.itertuples(), 1):
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid #F6F5F2; font-size:0.82rem;">
                <span><strong style="font-family:'JetBrains Mono',monospace; color:#8C8A84; margin-right:8px;">0{i}</strong> {row.distrito_padronizado.title()}</span>
                <span style="font-family:'JetBrains Mono',monospace; font-weight:500;">R$ {row.valor_medio_m2:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao renderizar a aplicação: {e}")