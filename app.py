import streamlit as st
import pulp
from fractions import Fraction

def solve_linear_program(obj_coeffs, constraints, constraint_sides, rhs_values, maximize=True):
    # Convertir todos los valores a fracciones para mayor precisión
    obj_coeffs = [Fraction(c) for c in obj_coeffs]
    constraints = [[Fraction(c) for c in row] for row in constraints]
    rhs_values = [Fraction(r) for r in rhs_values]
    
    # Imprimir los valores convertidos para verificar
    print("Función Objetivo:", obj_coeffs)
    print("Restricciones:", constraints)
    print("Lado Derecho:", rhs_values)
    print("Tipos de Restricción:", constraint_sides)
    
    prob = pulp.LpProblem("Linear_Programming", pulp.LpMaximize if maximize else pulp.LpMinimize)
    num_vars = len(obj_coeffs)
    variables = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(num_vars)]
    prob += pulp.lpDot(obj_coeffs, variables), "Objective"
    for i in range(len(constraints)):
        if constraint_sides[i] == "leq":
            prob += (pulp.lpDot(constraints[i], variables) <= rhs_values[i])
        elif constraint_sides[i] == "geq":
            prob += (pulp.lpDot(constraints[i], variables) >= rhs_values[i])
        elif constraint_sides[i] == "eq":
            prob += (pulp.lpDot(constraints[i], variables) == rhs_values[i])
    
    prob.solve(pulp.PULP_CBC_CMD(mip=True, msg=True, presolve=True, strong=True, cuts=True, timeLimit=10))
    
    result = {"Status": pulp.LpStatus[prob.status]}
    for var in variables:
        result[var.name] = str(Fraction(var.varValue).limit_denominator())  # Mostrar como fracción
    result["Objective Value"] = str(Fraction(pulp.value(prob.objective)).limit_denominator())  # Mostrar como fracción
    
    return result

st.title("Optimización Lineal - Método Simplex con Fracciones")

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
        obj_coeffs.append(cols[i].number_input(f"Coeficiente x{i+1}", value=1.0, key=f"obj_x{i+1}"))
    
    st.subheader("Restricciones")
    constraints = []
    constraint_sides = []
    rhs_values = []
    for i in range(st.session_state.num_constraints):
        cols = st.columns(st.session_state.num_vars + 2)
        row = []
        for j in range(st.session_state.num_vars):
            row.append(cols[j].number_input(f"x{j+1} en R{i+1}", value=1.0, key=f"coef_r{i+1}_x{j+1}"))
        constraints.append(row)
        constraint_sides.append(cols[st.session_state.num_vars].selectbox(f"Restricción {i+1}", ["≤", "≥", "="], key=f"constraint_type_{i+1}"))
        rhs_values.append(cols[st.session_state.num_vars+1].number_input(f"Valor R{i+1}", value=1.0, key=f"rhs_{i+1}"))
    
    submitted = st.form_submit_button("Resolver")
    if submitted:
        solution = solve_linear_program(
            obj_coeffs, 
            constraints, 
            ["leq" if s == "≤" else "geq" if s == "≥" else "eq" for s in constraint_sides], 
            rhs_values, 
            maximize
        )
        st.write("### Resultados (en fracciones)")
        st.write(solution)