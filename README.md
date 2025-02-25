Proyecto Final - Investigación Operativa
Este repositorio contiene la implementación de una solución computacional diseñada para optimizar la distribución de medicamentos en el sector salud. La aplicación integra técnicas de Programación Lineal, Métodos de Transporte, Optimización en Redes y un módulo de Análisis de Sensibilidad con Inteligencia Artificial (IA), con el fin de mejorar la asignación de recursos, reducir costos operativos y optimizar tiempos de entrega.

Descripción
La aplicación se desarrolló como parte del Proyecto Final de Investigación Operativa, orientado a resolver problemas logísticos en la distribución de medicamentos desde tres centros de distribución hacia hospitales y farmacias. Se aplican diversas técnicas de optimización:

Programación Lineal (Simplex): Para asignar de manera óptima los medicamentos minimizando costos.
Métodos de Transporte (Costo Mínimo, Esquina Noroeste, Voguel, MODI): Para la distribución eficiente de suministros.
Optimización en Redes (Flujo Máximo, Ruta Más Corta, Árbol de Expansión Mínima): Para determinar la capacidad máxima de la red y optimizar los tiempos de entrega.
Análisis de Sensibilidad con IA: Para evaluar la robustez del modelo ante variaciones en la demanda y en los costos, proporcionando recomendaciones estratégicas.
Características
Optimización Multi-Método: Integración de algoritmos clásicos de optimización.
Análisis de Sensibilidad: Uso de IA para simular escenarios y proponer mejoras.
Entrada de Datos Personalizada: Soporte para datos en formato .txt en la optimización en redes.
Resultados y Visualización: Generación de resultados que facilitan la toma de decisiones estratégicas.
Requisitos
Lenguaje: Python 3.x (se recomienda Python 3.8 o superior)
Dependencias:
NumPy
SciPy
Pandas
Matplotlib
[Otras dependencias específicas según el módulo]
Consulte el archivo requirements.txt para la lista completa de dependencias.

Instalación
Clona el repositorio:
bash
Copiar
Editar
git clone https://github.com/Jonablo/PROYECTO-FINAL.git
Navega al directorio del proyecto:
bash
Copiar
Editar
cd PROYECTO-FINAL
Instala las dependencias:
bash
Copiar
Editar
pip install -r requirements.txt
Uso
La aplicación se divide en módulos que se pueden ejecutar individualmente para cada método de optimización:

Programación Lineal (Simplex): Ejecuta el modelo para la asignación óptima.
Métodos de Transporte: Ejecuta los modelos para la asignación de suministros mediante los métodos de Costo Mínimo, Esquina Noroeste, Voguel y MODI.
Optimización en Redes: Ejecuta los modelos para Flujo Máximo, Ruta Más Corta y Árbol de Expansión Mínima.
Análisis de Sensibilidad con IA: Ejecuta el módulo que simula escenarios variables y evalúa la robustez del modelo.
Cada módulo cuenta con su propia documentación interna para el uso y la interpretación de los resultados.

Estructura del Proyecto
bash
Copiar
Editar
PROYECTO-FINAL/
├── simplex.py               # Modelo de Programación Lineal (Simplex)
├── transporte.py            # Métodos de Transporte
├── redes.py                 # Optimización en Redes (Flujo Máximo, Ruta Más Corta, etc.)
├── sensibilidad.py          # Módulo de Análisis de Sensibilidad con IA
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este archivo
└── docs/                    # Documentación adicional y capturas de pantalla
Contribuciones
Se agradecen las contribuciones al proyecto. Para proponer mejoras o correcciones:

Haz un fork del repositorio.
Crea una rama para tu funcionalidad o corrección:
bash
Copiar
Editar
git checkout -b feature/nueva-funcionalidad
Realiza los cambios y haz commit:
bash
Copiar
Editar
git commit -am 'Añadir nueva funcionalidad'
Envía tu rama:
bash
Copiar
Editar
git push origin feature/nueva-funcionalidad
Abre un Pull Request explicando tus cambios.
Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.
