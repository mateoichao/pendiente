import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calcular_pendiente(x1, y1, x2, y2):
    """
    Calcula la pendiente entre dos puntos
    """
    if x2 - x1 == 0:
        return None  # Pendiente indefinida (línea vertical)
    return (y2 - y1) / (x2 - x1)

def ecuacion_recta(x1, y1, pendiente):
    """
    Calcula la ecuación de la recta en forma y = mx + b
    """
    if pendiente is None:
        return None
    b = y1 - pendiente * x1
    return pendiente, b

def crear_grafico(x1, y1, x2, y2, pendiente):
    """
    Crea el gráfico de la línea entre los dos puntos
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Puntos
    ax.plot([x1, x2], [y1, y2], 'ro-', markersize=10, linewidth=2, label='Línea entre puntos')
    
    # Etiquetas de los puntos
    ax.annotate(f'P1({x1}, {y1})', (x1, y1), xytext=(10, 10), 
                textcoords='offset points', fontsize=12, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    ax.annotate(f'P2({x2}, {y2})', (x2, y2), xytext=(10, 10), 
                textcoords='offset points', fontsize=12,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Extender la línea si la pendiente existe
    if pendiente is not None:
        m, b = ecuacion_recta(x1, y1, pendiente)
        x_min = min(x1, x2) - 2
        x_max = max(x1, x2) + 2
        x_line = np.linspace(x_min, x_max, 100)
        y_line = m * x_line + b
        ax.plot(x_line, y_line, 'b--', alpha=0.5, label=f'Recta extendida: y = {m:.3f}x + {b:.3f}')
    
    # Configuración del gráfico
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Gráfico de la Línea entre Dos Puntos', fontsize=14, fontweight='bold')
    ax.legend()
    
    # Ajustar los límites del gráfico
    margin = max(abs(x2-x1), abs(y2-y1)) * 0.2 + 1
    ax.set_xlim(min(x1, x2) - margin, max(x1, x2) + margin)
    ax.set_ylim(min(y1, y2) - margin, max(y1, y2) + margin)
    
    return fig

def main():
    st.set_page_config(page_title="Calculadora de Pendiente", page_icon="📊", layout="wide")
    
    st.title("📊 Calculadora de Pendiente entre Dos Puntos")
    st.markdown("---")
    
    # Sidebar para inputs
    st.sidebar.header("📍 Coordenadas de los Puntos")
    
    # Punto 1
    st.sidebar.subheader("Punto 1 (P1)")
    x1 = st.sidebar.number_input("Coordenada X₁:", value=0.0, step=0.1, format="%.2f")
    y1 = st.sidebar.number_input("Coordenada Y₁:", value=0.0, step=0.1, format="%.2f")
    
    # Punto 2
    st.sidebar.subheader("Punto 2 (P2)")
    x2 = st.sidebar.number_input("Coordenada X₂:", value=1.0, step=0.1, format="%.2f")
    y2 = st.sidebar.number_input("Coordenada Y₂:", value=1.0, step=0.1, format="%.2f")
    
    # Opción para mostrar gráfico
    mostrar_grafico = st.sidebar.checkbox("📈 Mostrar Gráfico", value=True)
    
    # Crear dos columnas para el layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Resultados")
        
        # Calcular pendiente
        pendiente = calcular_pendiente(x1, y1, x2, y2)
        
        # Mostrar información de los puntos
        st.subheader("Puntos ingresados:")
        st.info(f"**P1:** ({x1}, {y1})")
        st.info(f"**P2:** ({x2}, {y2})")
        
        # Mostrar resultado de la pendiente
        st.subheader("Cálculo de la Pendiente:")
        
        if pendiente is None:
            st.error("⚠️ **Pendiente indefinida** (línea vertical)")
            st.latex(r"m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{" + f"{y2} - {y1}" + "}{" + f"{x2} - {x1}" + "} = \\frac{" + f"{y2-y1}" + "}{0} = \\text{indefinida}")
        else:
            st.success(f"**Pendiente (m):** {pendiente:.6f}")
            st.latex(
    rf"m = \frac{{y_2 - y_1}}{{x_2 - x_1}} = \frac{{{y2} - {y1}}}{{{x2} - {x1}}} = \frac{{{y2 - y1}}}{{{x2 - x1}}} = {pendiente:.6f}"
)

            
            # Mostrar ecuación de la recta
            m, b = ecuacion_recta(x1, y1, pendiente)
            st.subheader("Ecuación de la Recta:")
            if b >= 0:
                st.latex(f"y = {m:.6f}x + {b:.6f}")
            else:
                st.latex(f"y = {m:.6f}x - {abs(b):.6f}")
            
            # Interpretación de la pendiente
            st.subheader("Interpretación:")
            if pendiente > 0:
                st.info("📈 **Pendiente positiva:** La línea es creciente")
            elif pendiente < 0:
                st.info("📉 **Pendiente negativa:** La línea es decreciente")
            else:
                st.info("➡️ **Pendiente cero:** La línea es horizontal")
        
        # Calcular distancia entre puntos
        distancia = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        st.subheader("Información adicional:")
        st.info(f"**Distancia entre puntos:** {distancia:.6f}")
    
    with col2:
        if mostrar_grafico:
            st.header("📊 Gráfico")
            fig = crear_grafico(x1, y1, x2, y2, pendiente)
            st.pyplot(fig)
        else:
            st.header("📊 Gráfico")
            st.info("Activa la opción 'Mostrar Gráfico' en el panel lateral para ver la visualización.")
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    ### 📚 Información sobre la Pendiente
    
    La **pendiente** de una línea es una medida de su inclinación y se calcula como:
    
    $$m = \\frac{y_2 - y_1}{x_2 - x_1}$$
    
    - **Pendiente positiva**: La línea asciende de izquierda a derecha
    - **Pendiente negativa**: La línea desciende de izquierda a derecha  
    - **Pendiente cero**: La línea es horizontal
    - **Pendiente indefinida**: La línea es vertical (división por cero)
    """)

if __name__ == "__main__":
    main()