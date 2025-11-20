import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------- CONFIGURACIÓN GENERAL -----------------
st.set_page_config(
    page_title="Movimiento Armónico Simple - Física II",
    layout="wide"
)

st.title("Desafío de Programación - Movimiento Armónico Simple (MAS)")
st.markdown("""
Aplicación interactiva para explorar el Movimiento Armónico Simple (MAS)
y sus variantes: masa–resorte, péndulo simple, efecto de parámetros
y MAS amortiguado.
""")

# Menú lateral
seccion = st.sidebar.selectbox(
    "Selecciona la simulación",
    [
        "1) MAS masa–resorte",
        "2) Péndulo simple",
        "3) Análisis de periodo vs k y m",
        "4) MAS amortiguado (caso extendido)"
    ]
)

# Tiempo común
st.sidebar.markdown("### Parámetros de simulación")
t_max = st.sidebar.slider("Tiempo máximo [s]", 5.0, 60.0, 20.0, 1.0)
n_puntos = st.sidebar.slider("Número de puntos", 200, 2000, 1000, 100)
t = np.linspace(0, t_max, n_puntos)

# ----------------- 1) MAS MASA-RESORTE -----------------
if seccion.startswith("1"):
    st.subheader("1) Sistema masa–resorte (horizontal / vertical)")

    col1, col2 = st.columns(2)
    with col1:
        orientacion = st.radio("Orientación", ["Horizontal", "Vertical"])
        k = st.slider("Constante elástica k [N/m]", 10.0, 500.0, 100.0, 10.0)
        m = st.slider("Masa m [kg]", 0.1, 10.0, 1.0, 0.1)
        A = st.slider("Amplitud A [m]", 0.01, 1.0, 0.2, 0.01)
    with col2:
        fase = st.slider("Fase inicial φ [rad]", 0.0, 2*np.pi, 0.0, 0.1)
        x0_label = "Posición inicial desde el equilibrio" if orientacion == "Vertical" else "Posición inicial"
        st.write(f"*Nota:* Para MAS ideal, la ecuación es la misma en ambas orientaciones, solo cambia el equilibrio.")
        # Frecuencia angular
        omega = np.sqrt(k / m)

    # Solución analítica MAS ideal
    x = A * np.cos(omega * t + fase)
    v = -A * omega * np.sin(omega * t + fase)
    a = -omega**2 * x
    Ek = 0.5 * m * v**2
    Ep = 0.5 * k * x**2
    Et = Ek + Ep

    # Gráfica posición, velocidad, aceleración
    fig1 = go.Figure()
    fig1.add_scatter(x=t, y=x, name="Posición x(t) [m]")
    fig1.add_scatter(x=t, y=v, name="Velocidad v(t) [m/s]")
    fig1.add_scatter(x=t, y=a, name="Aceleración a(t) [m/s²]")
    fig1.update_layout(
        xaxis_title="Tiempo [s]",
        yaxis_title="Magnitud",
        title="Posición, velocidad y aceleración en función del tiempo"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfica energías
    fig2 = go.Figure()
    fig2.add_scatter(x=t, y=Ek, name="Energía cinética Ek")
    fig2.add_scatter(x=t, y=Ep, name="Energía potencial Ep")
    fig2.add_scatter(x=t, y=Et, name="Energía total Et")
    fig2.update_layout(
        xaxis_title="Tiempo [s]",
        yaxis_title="Energía [J]",
        title="Energías en el MAS"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    *Explicación física (resumen)*  
    En un sistema masa–resorte ideal, la fuerza restauradora es \(F = -kx\),
    lo que conduce a la ecuación diferencial:
    \[
        m \ddot{x} + kx = 0 \quad \Rightarrow \quad
        x(t) = A \cos(\omega t + \varphi), \quad \omega = \sqrt{k/m}
    \]
    La energía total \(E_T = E_k + E_p\) se conserva y oscila entre cinética
    y potencial, manteniéndose constante en el tiempo en ausencia de rozamiento.
    """)

# ----------------- 2) PÉNDULO SIMPLE -----------------
elif seccion.startswith("2"):
    st.subheader("2) Péndulo simple: modelo lineal vs no lineal")

    col1, col2 = st.columns(2)
    with col1:
        L = st.slider("Longitud L [m]", 0.1, 5.0, 1.0, 0.1)
        g = st.slider("Gravedad g [m/s²]", 1.0, 15.0, 9.81, 0.1)
    with col2:
        theta0_deg = st.slider("Ángulo inicial θ₀ [°]", 1.0, 90.0, 20.0, 1.0)
        theta0 = np.deg2rad(theta0_deg)
        omega0 = 0.0  # velocidad angular inicial

    # Frecuencia angular lineal
    omega_lin = np.sqrt(g / L)

    # Solución lineal: θ_lin(t)
    theta_lin = theta0 * np.cos(omega_lin * t)

    # Solución no lineal numérica (Euler simple)
    theta = np.zeros_like(t)
    omega = np.zeros_like(t)
    theta[0] = theta0
    omega[0] = omega0
    dt = t[1] - t[0]

    for i in range(len(t) - 1):
        # Ecuación no lineal: θ'' + (g/L) sin θ = 0
        alpha = -(g / L) * np.sin(theta[i])
        omega[i + 1] = omega[i] + alpha * dt
        theta[i + 1] = theta[i] + omega[i + 1] * dt

    fig = go.Figure()
    fig.add_scatter(x=t, y=np.rad2deg(theta_lin), name="Modelo lineal (pequeños ángulos)")
    fig.add_scatter(x=t, y=np.rad2deg(theta), name="Modelo no lineal (numérico)")
    fig.update_layout(
        xaxis_title="Tiempo [s]",
        yaxis_title="Ángulo θ [°]",
        title="Comparación: péndulo lineal vs no lineal"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    *Período aproximado modelo lineal:*
    \[
        T_{{lin}} = 2\pi \sqrt{{\\frac{{L}}{{g}}}} \approx {2*np.pi*np.sqrt(L/g):.2f} \ \text{{s}}
    \]

    *Comentario físico*  
    - Para ángulos pequeños (≈ hasta 10–15°), el modelo lineal \( \sin\theta \approx \theta \)
      es una muy buena aproximación.  
    - Para ángulos grandes (\(θ_0 = {theta0_deg:.1f}°\)), el período real aumenta y la
      solución no lineal se separa de la lineal.
    """)

# ----------------- 3) ANÁLISIS DE PERIODO VS K Y M -----------------
elif seccion.startswith("3"):
    st.subheader("3) Análisis del efecto de k y m en el periodo")

    modo = st.radio("¿Qué quieres analizar?", ["Variar k (m fija)", "Variar m (k fija)"])

    if modo == "Variar k (m fija)":
        m_fija = st.slider("Masa fija m [kg]", 0.1, 10.0, 1.0, 0.1)
        k_min, k_max = st.slider("Rango de k [N/m]", 10.0, 1000.0, (50.0, 500.0), 10.0)
        k_vals = np.linspace(k_min, k_max, 100)
        T_vals = 2 * np.pi * np.sqrt(m_fija / k_vals)

        fig = go.Figure()
        fig.add_scatter(x=k_vals, y=T_vals, name="Periodo T(k)")
        fig.update_layout(
            xaxis_title="k [N/m]",
            yaxis_title="Periodo T [s]",
            title="Dependencia del periodo con la constante elástica k"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        *Conclusión:*  
        A mayor constante elástica \(k\), el periodo disminuye. Es decir,
        un resorte más "duro" oscila más rápido para una misma masa.
        """)

    else:
        k_fija = st.slider("Constante fija k [N/m]", 10.0, 1000.0, 100.0, 10.0)
        m_min, m_max = st.slider("Rango de m [kg]", 0.1, 20.0, (0.5, 10.0), 0.1)
        m_vals = np.linspace(m_min, m_max, 100)
        T_vals = 2 * np.pi * np.sqrt(m_vals / k_fija)

        fig = go.Figure()
        fig.add_scatter(x=m_vals, y=T_vals, name="Periodo T(m)")
        fig.update_layout(
            xaxis_title="m [kg]",
            yaxis_title="Periodo T [s]",
            title="Dependencia del periodo con la masa m"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        *Conclusión:*  
        A mayor masa \(m\), el periodo aumenta. Un sistema más "pesado"
        oscila más lentamente para un mismo resorte.
        """)

    st.markdown("""
    Recordemos que para el MAS ideal:
    \[
        T = 2\pi \sqrt{\\frac{m}{k}}
    \]
    Esta ecuación muestra explícitamente cómo influyen \(m\) y \(k\) en el periodo.
    """)

# ----------------- 4) MAS AMORTIGUADO -----------------
elif seccion.startswith("4"):
    st.subheader("4) MAS amortiguado (caso extendido)")

    col1, col2 = st.columns(2)
    with col1:
        k = st.slider("Constante elástica k [N/m]", 10.0, 500.0, 100.0, 10.0)
        m = st.slider("Masa m [kg]", 0.1, 10.0, 1.0, 0.1)
        A = st.slider("Amplitud inicial A [m]", 0.01, 1.0, 0.2, 0.01)
    with col2:
        zeta = st.slider("Factor de amortiguamiento ζ", 0.0, 2.0, 0.2, 0.05)
        st.write("ζ < 1: subamortiguado, ζ = 1: críticamente amortiguado, ζ > 1: sobreamortiguado")

    omega0 = np.sqrt(k / m)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    x[0] = A
    v[0] = 0.0
    dt = t[1] - t[0]

    # Integración numérica simple: x'' + 2ζω0 x' + ω0² x = 0
    for i in range(len(t) - 1):
        acc = -2 * zeta * omega0 * v[i] - omega0**2 * x[i]
        v[i + 1] = v[i] + acc * dt
        x[i + 1] = x[i] + v[i + 1] * dt

    fig = go.Figure()
    fig.add_scatter(x=t, y=x, name="x(t) amortiguado")
    fig.update_layout(
        xaxis_title="Tiempo [s]",
        yaxis_title="Desplazamiento x [m]",
        title="Movimiento Armónico Simple Amortiguado"
    )
    st.plotly_chart(fig, use_container_width=True)