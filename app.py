import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Reporte Financiero Daniel", layout="wide")

# --- ESTILO APA 7 (Fondo Blanco y Tipografía Académica) ---
st.markdown("""
    <style>
    /* Forzar tema claro */
    .stApp { background-color: white; color: black; }
    
    /* Fuentes Times New Roman para todo */
    html, body, [class*="st-"] {
        font-family: "Times New Roman", Times, serif;
        color: black;
    }

    /* Estilo de Tabla APA */
    .apa-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    .apa-table th {
        border-top: 1.5pt solid black;
        border-bottom: 1pt solid black;
        padding: 10px;
        text-align: center;
    }
    .apa-table td {
        padding: 8px;
        text-align: center;
        border-bottom: 0.5pt solid #ddd;
    }
    .apa-table tr:last-child {
        border-bottom: 1.5pt solid black;
    }
    .apa-label { font-weight: bold; margin-bottom: 0px; }
    .apa-title { font-style: italic; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS INTEGRADA (Hardcoded) ---
def cargar_datos_iniciales():
    meses = ["Nov 2025", "Dic 2025"] + [f"{m} 2026" for m in ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]]
    
    # Categorías según tu imagen
    categorias = [
        ("Smart Fit", "Gasto"), ("Salsa", "Gasto"), ("Gasto Hormiga (bodega, yape, plin, etc)", "Gasto"),
        ("Gastos Familia Suntuarios", "Gasto"), ("Lukers", "Gasto"), ("Icloud", "Gasto"),
        ("Chillis", "Gasto"), ("Zara", "Gasto"), ("Mantenimiento de Tarjeta BBVA", "Gasto"),
        ("Ingles Diana", "Gasto"), ("Pago Tarjeta Interbank (Crédito)", "Gasto"), ("Spotify", "Gasto"),
        ("Pro", "Ingreso"), ("Saldo Anterior", "Balance"), ("Meta de Ahorro", "Meta")
    ]
    
    df = pd.DataFrame([{"Detalle": c[0], "Tipo": c[1]} for c in categorias])
    for m in meses: df[m] = 0.0
    
    # LLENADO DE DATOS DESDE TU IMAGEN
    # Noviembre 2025
    df.loc[df["Detalle"] == "Pro", "Nov 2025"] = 3000.0
    df.loc[df["Detalle"] == "Meta de Ahorro", "Nov 2025"] = 1000.0
    
    # Diciembre 2025
    gastos_dic = {
        "Smart Fit": 111.0, "Salsa": 80.0, "Gasto Hormiga (bodega, yape, plin, etc)": 614.0,
        "Gastos Familia Suntuarios": 358.0, "Lukers": 50.0, "Icloud": 15.0, "Chillis": 55.0,
        "Zara": 448.0, "Mantenimiento de Tarjeta BBVA": 10.0, "Ingles Diana": 160.0,
        "Pago Tarjeta Interbank (Crédito)": 500.0, "Spotify": 12.0
    }
    for cat, val in gastos_dic.items():
        df.loc[df["Detalle"] == cat, "Dic 2025"] = val
    
    df.loc[df["Detalle"] == "Pro", "Dic 2025"] = 3000.0
    df.loc[df["Detalle"] == "Saldo Anterior", "Dic 2025"] = 713.0
    df.loc[df["Detalle"] == "Meta de Ahorro", "Dic 2025"] = 1000.0
    
    # Enero 2026
    df.loc[df["Detalle"] == "Pro", "Ene 2026"] = 3000.0
    df.loc[df["Detalle"] == "Saldo Anterior", "Ene 2026"] = 1669.21
    
    # Metas de ahorro automáticas (1000)
    for m in meses:
        df.loc[df["Detalle"] == "Meta de Ahorro", m] = 1000.0
        
    return df

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos_iniciales()

# --- TÍTULOS ---
st.markdown('<h2 style="color: black;">Gestión de Finanzas Personales</h2>', unsafe_allow_html=True)

# --- EDITOR INTERACTIVO ---
with st.expander("📝 Ajustar Montos o Agregar Filas", expanded=True):
    # El editor permite agregar filas con el botón (+) abajo de la tabla
    df_editado = st.data_editor(
        st.session_state.df, 
        hide_index=True, 
        use_container_width=True,
        num_rows="dynamic" # Permite que agregues o borres filas tú mismo
    )
    if st.button("Actualizar Cálculos"):
        st.session_state.df = df_editado
        st.rerun()

# --- LÓGICA DE CÁLCULO APA ---
st.divider()
st.markdown('<p class="apa-label">Tabla 1</p>', unsafe_allow_html=True)
st.markdown('<p class="apa-title">Análisis de flujos de caja, egresos y metas de ahorro (2025-2026)</p>', unsafe_allow_html=True)

meses_cols = [c for c in df_editado.columns if c not in ["Detalle", "Tipo"]]
resumen_data = []

for mes in meses_cols:
    gastos_totales = df_editado[df_editado["Tipo"] == "Gasto"][mes].sum()
    ingresos_totales = df_editado[df_editado["Tipo"] == "Ingreso"][mes].sum()
    saldo_anterior = df_editado[df_editado["Detalle"] == "Saldo Anterior"][mes].values[0]
    meta = df_editado[df_editado["Detalle"] == "Meta de Ahorro"][mes].values[0]
    
    ahorro_real = ingresos_totales - gastos_totales
    saldo_final = (ingresos_totales + saldo_anterior) - gastos_totales
    
    resumen_data.append({
        "Mes": mes,
        "Ingresos": f"{ingresos_totales:,.2f}",
        "Gastos": f"{gastos_totales:,.2f}",
        "Ahorro": f"{ahorro_real:,.2f}",
        "Meta": f"{meta:,.2f}",
        "Saldo Final": f"{saldo_final:,.2f}"
    })

# Mostrar Tabla Resumen con estilo APA
df_res = pd.DataFrame(resumen_data)
st.markdown(df_res.to_html(index=False, classes='apa-table'), unsafe_allow_html=True)

st.markdown('<p style="font-size: 0.9em; margin-top:10px;"><i>Nota.</i> Elaboración propia con base en el registro de movimientos diarios.</p>', unsafe_allow_html=True)