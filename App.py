import streamlit as st
import pandas as pd 

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestor IB")
st.title(" Gestor de Presupuestos")

# --- LA MEMORIA (Session State) ---


if 'presupuesto' not in st.session_state:
    st.session_state['presupuesto'] = 0.0

if 'gastos' not in st.session_state:
    st.session_state['gastos'] = []

# --- BARRA LATERAL (MENU) ---
menu = st.sidebar.selectbox(
    "Menú Principal",
    ["Resumen (Balance)", "Registrar Gasto", "Agregar Ingreso"]
)

# --- OPCIÓN 1: AGREGAR INGRESO ---
if menu == "Agregar Ingreso":
    st.header("💵 Depositar Dinero")
    st.write("Agrega dinero a tu presupuesto inicial o actual.")
    
    col1, col2 = st.columns(2)
    with col1:
        nuevo_monto = st.number_input("Monto a ingresar:", min_value=0.0, step=10.0)
    with col2:
        origen = st.text_input("Concepto (Ej. Mesada):")
        
    if st.button("Depositar Dinero"):
        if nuevo_monto > 0:
            st.session_state['presupuesto'] += nuevo_monto
            st.success(f"✅ ¡Se agregaron ${nuevo_monto} por '{origen}'!")
        else:
            st.error("El monto debe ser mayor a 0.")

# --- REGISTRAR GASTO ---
elif menu == "Registrar Gasto":
    st.header("💸 Registrar un Gasto")
    
    # Calculamos cuánto hay disponible antes de gastar
    total_gastado = sum(g['costo'] for g in st.session_state['gastos'])
    disponible = st.session_state['presupuesto'] - total_gastado
    
    st.info(f"Tienes disponible para gastar: ${disponible}")

    concepto_gasto = st.text_input("¿En qué gastaste?")
    costo_gasto = st.number_input("¿Cuánto costó?", min_value=0.0, step=5.0)

    if st.button("Guardar Gasto"):
        if costo_gasto > disponible:
            st.error("⚠️ ¡ALERTA! No tienes fondos suficientes.")
        elif costo_gasto > 0 and concepto_gasto:
            nuevo_gasto = {"concepto": concepto_gasto, "costo": costo_gasto}
            st.session_state['gastos'].append(nuevo_gasto)
            st.success("✅ Gasto guardado correctamente.")
        else:
            st.warning("Por favor ingresa un monto y un nombre válidos.")

# --- OPCIÓN 3: RESUMEN (Tu antigua Opción 2) ---
elif menu == "Resumen (Balance)":
    st.header("📊 Balance Financiero")

    # Cálculos
    total_gastado = sum(g['costo'] for g in st.session_state['gastos'])
    restante = st.session_state['presupuesto'] - total_gastado

    # Métricas 
    col1, col2, col3 = st.columns(3)
    col1.metric("Presupuesto Total", f"${st.session_state['presupuesto']}")
    col2.metric("Total Gastado", f"${total_gastado}", delta=-total_gastado)
    col3.metric("Disponible", f"${restante}")

    st.divider() # Una línea divisoria

    st.subheader("Historial de Gastos")
    if len(st.session_state['gastos']) > 0:
       
        df = pd.DataFrame(st.session_state['gastos'])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Aún no has registrado gastos.")
        
