import pulp

def solve_linear_program(obj_coeffs, constraints, constraint_sides, rhs_values, maximize=True):
    # Crear el problema de optimización
    prob = pulp.LpProblem("Linear_Programming", pulp.LpMaximize if maximize else pulp.LpMinimize)
    
    # Definir las variables de decisión
    num_vars = len(obj_coeffs)
    variables = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(num_vars)]
    
    # Definir la función objetivo
    prob += pulp.lpDot(obj_coeffs, variables), "Objective"
    
    # Agregar restricciones
    for i in range(len(constraints)):
        if constraint_sides[i] == "leq":
            prob += (pulp.lpDot(constraints[i], variables) <= rhs_values[i])
        elif constraint_sides[i] == "geq":
            prob += (pulp.lpDot(constraints[i], variables) >= rhs_values[i])
        elif constraint_sides[i] == "eq":
            prob += (pulp.lpDot(constraints[i], variables) == rhs_values[i])
    
    # Resolver el problema
    prob.solve()
    
    # Mostrar resultados
    result = {"Status": pulp.LpStatus[prob.status]}
    for var in variables:
        result[var.name] = var.varValue
    result["Objective Value"] = pulp.value(prob.objective)
    
    return result

# Ejemplo de uso
def example():
    obj_coeffs = [3, 5]  # Coeficientes de la función objetivo
    constraints = [[1, 0], [0, 2], [3, 2]]  # Restricciones
    constraint_sides = ["leq", "leq", "leq"]  # Tipo de restricción
    rhs_values = [4, 12, 18]  # Lado derecho de las restricciones
    
    solution = solve_linear_program(obj_coeffs, constraints, constraint_sides, rhs_values, maximize=True)
    print(solution)
    
example()
