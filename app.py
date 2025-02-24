import streamlit as st
import pulp
import numpy as np
import shap
import matplotlib.pyplot as plt

# 🔹 **Función para Resolver el Problema de Programación Lineal (Sin Flotantes)**
def solve_linear_program(obj_coeffs, constraints, constraint_sides, rhs_values, maximize=True):
    prob = pulp.LpProblem("Linear_Programming", pulp.LpMaximize if maximize else pulp.LpMinimize)
    
    num_vars = len(obj_coeffs)
    variables = [pulp.LpVariable(f"x{i+1}", lowBound=0, cat='Integer') for i in range(num_vars)]
    
    prob += pulp.lpDot(obj_coeffs, variables), "Objective"
    
    for i in range(len(constraints)):
        if constraint_sides[i] == "leq":
            prob += (pulp.lpDot(constraints[i], variables) <= rhs_values[i])
        elif constraint_sides[i] == "geq":
            prob += (pulp.lpDot(constraints[i], variables) >= rhs_values[i])
        elif constraint_sides[i] == "eq":
            prob += (pulp.lpDot(constraints[i], variables) == rhs_values[i])
    
    prob.solve()
    
    result = {"Status": pulp.LpStatus[prob.status]}
    for var in variables:
        result[var.name] = int(var.varValue) if var.varValue is not None else None
    result["Objective Value"] = int(pulp.value(prob.objective)) if pulp.value(prob.objective) is not None else None
    
    return result, obj_coeffs, constraints, rhs_values

# 🔹 **Interfaz en Streamlit**
st.set_page_config(page_title="Optimización Operativa", layout="wide")
st.title("📊 Optimización Lineal - Método Simplex con Análisis de Sensibilidad")

if "num_vars" not in st.session_state:
    st.session_state.num_vars = 2
if "num_constraints" not in st.session_state:
    st.session_state.num_constraints = 2

def update_model():
    st.session_state.num_vars = st.session_state.new_num_vars
    st.session_state.num_constraints = st.session_state.new_num_constraints

with st.form("formulario_config"):
    st.subheader("Definir Problema")
    st.session_state.new_num_vars = st.number_input("Cantidad de Variables:", min_value=1, step=1, value=st.session_state.num_vars, key="input_vars")
    st.session_state.new_num_constraints = st.number_input("Cantidad de Restricciones:", min_value=1, step=1, value=st.session_state.num_constraints, key="input_constraints")
    if st.form_submit_button("Actualizar Modelo"):
        update_model()
        st.rerun()

with st.form("formulario"):
    maximize = st.radio("Objetivo:", ("Maximizar", "Minimizar"), key="maximize") == "Maximizar"
    
    st.subheader("Función Objetivo")
    obj_coeffs = []
    cols = st.columns(st.session_state.num_vars)
    for i in range(st.session_state.num_vars):
        obj_coeffs.append(int(cols[i].number_input(f"Coeficiente x{i+1}", value=1, step=1, key=f"obj_x{i+1}")))
    
    st.subheader("Restricciones")
    constraints = []
    constraint_sides = []
    rhs_values = []
    for i in range(st.session_state.num_constraints):
        cols = st.columns(st.session_state.num_vars + 2)
        row = []
        for j in range(st.session_state.num_vars):
            row.append(int(cols[j].number_input(f"x{j+1} en R{i+1}", value=1, step=1, key=f"coef_r{i+1}_x{j+1}")))
        constraints.append(row)
        constraint_sides.append(cols[st.session_state.num_vars].selectbox(f"Restricción {i+1}", ["≤", "≥", "="], key=f"constraint_type_{i+1}"))
        rhs_values.append(int(cols[st.session_state.num_vars+1].number_input(f"Valor R{i+1}", value=1, step=1, key=f"rhs_{i+1}")))
    
    submitted = st.form_submit_button("Resolver")

if submitted:
    # 🔹 **Resolver el problema de Programación Lineal**
    solution, obj_coeffs, constraints, rhs_values = solve_linear_program(
        obj_coeffs, 
        constraints, 
        ["leq" if s == "≤" else "geq" if s == "≥" else "eq" for s in constraint_sides], 
        rhs_values, 
        maximize
    )
    
    st.write("### 📌 Resultados")
    st.write(solution)

    # 🔹 **Análisis de Sensibilidad con SHAP**
    st.subheader("🔍 Análisis de Sensibilidad")

    # **Datos en Enteros para SHAP**
    datos_np = np.array([[v for v in obj_coeffs] + 
                         [v for row in constraints for v in row] + 
                         [v for v in rhs_values]])

    # **Modelo Proxy para SHAP**
    def modelo_proxy(X):
        return np.dot(X, np.array(obj_coeffs + [0] * (X.shape[1] - len(obj_coeffs))))

    # Explicador SHAP usando KernelExplainer
    explainer = shap.KernelExplainer(modelo_proxy, datos_np)
    shap_values = explainer.shap_values(datos_np)

    # **Visualización de SHAP**
    fig, ax = plt.subplots(figsize=(6, 4))
    shap.summary_plot(shap_values, datos_np, show=False)
    st.pyplot(fig)
