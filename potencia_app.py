import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. Configuración de pantalla para Móvil/Tablet
st.set_page_config(page_title="PowerTrack Pro", layout="centered")

# 2. Base de datos simple (CSV local)
DB_FILE = "entrenos_potencia.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE, parse_dates=['Fecha'])
    return pd.DataFrame(columns=['Fecha', 'Dia', 'Ejercicio', 'Peso', 'Velocidad', 'Power_Index'])

def guardar_dato(dia, ejercicio, peso, velocidad):
    df = cargar_datos()
    nuevo = pd.DataFrame([{
        'Fecha': datetime.now().strftime("%Y-%m-%d"),
        'Dia': dia,
        'Ejercicio': ejercicio,
        'Peso': peso,
        'Velocidad': velocidad,
        'Power_Index': peso * velocidad
    }])
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# 3. Interfaz de Usuario
st.title("⚡ PowerTrack Pro")
st.subheader("Registro de Potencia y Velocidad")

# Selector de Bloque (Días A, B, C, D)
dia_seleccionado = st.selectbox("Selecciona tu sesión:", ["Día A: Potencia Piernas", "Día B: Empuje + HIIT", "Día C: Velocidad y Agilidad", "Día D: Tracción + HIIT"])

# Lista de ejercicios según el día
ejercicios_dict = {
    "Día A: Potencia Piernas": ["Sentadilla Trasera", "Salto Vertical CMJ", "Trap Bar Deadlift", "Power Clean", "Búlgara Explosiva"],
    "Día B: Empuje + HIIT": ["Press Banca", "Press Militar", "Fondos", "Kettlebell Swings"],
    "Día C: Velocidad y Agilidad": ["Sprints 20m", "Saltos al Cajón", "Broad Jump", "Landmine Rotation"],
    "Día D: Tracción + HIIT": ["Dominadas", "Remo con Barra", "Face Pulls", "HIIT Remo"]
}

ejercicio = st.selectbox("Ejercicio:", ejercicios_dict[dia_seleccionado])

# Inputs optimizados para dedos (Slidder y botones)
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Carga (kg):", min_value=0.0, step=2.5, value=60.0)
with col2:
    velocidad = st.select_slider("Velocidad (1-10):", options=range(1, 11), value=7)

if st.button("🚀 REGISTRAR SERIE", use_container_width=True):
    guardar_dato(dia_seleccionado, ejercicio, peso, velocidad)
    st.balloons()
    st.success(f"¡Serie guardada! Power Index: {peso * velocidad}")

# 4. Visualización de Gráficas
st.divider()
df_hist = cargar_datos()

if not df_hist.empty:
    st.subheader("📊 Tu Progreso Real")
    
    # Filtro para la gráfica
    ej_grafica = st.selectbox("Ver gráfica de:", df_hist['Ejercicio'].unique())
    df_filtrado = df_hist[df_hist['Ejercicio'] == ej_grafica]
    
    # Gráfica de Índice de Potencia (Peso x Velocidad)
    fig = px.line(df_filtrado, x='Fecha', y='Power_Index', 
                  title=f"Evolución de Potencia: {ej_grafica}",
                  markers=True, line_shape="spline")
    
    fig.update_layout(yaxis_title="Power Index (Peso x Vel)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Historial reciente
    with st.expander("Ver historial completo"):
        st.dataframe(df_hist.sort_values(by='Fecha', ascending=False), use_container_width=True)
else:
    st.info("Aún no hay datos. ¡Haz tu primera serie y dale a registrar!")
