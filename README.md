# TP2 SO

## Universidad de la Cuenca del Plata - Sistemas Operativos

### Trabajo Práctico N°2

**Fecha de entrega y defensa:** 2-10-24

### Informe Teórico

**Informe detallado que incluya:**

1. **Introducción al Problema:**
   - Explicación del concepto de gestión de memoria en sistemas operativos, incluyendo paginación y compactación.
   - Breve explicación sobre las colas de procesos y cómo los procesos solicitan recursos dentro de un sistema operativo.

2. **Objetivos del Simulador:**
   - Definir el propósito del simulador y lo que se busca al implementarlo, incluyendo la simulación de exclusión mutua y la gestión de memoria.

3. **Conceptos Técnicos:**
   - Explicación de los estados de los procesos (Nuevo, Listo, Ejecutando, Bloqueado, Terminado) y cómo transicionan entre ellos.
   - Descripción de la memoria principal y virtual.
   - Breve descripción de los algoritmos de asignación de memoria a elegir o analizar (First-Fit, Best-Fit, Worst-Fit).
   - Explicación de la exclusión mutua y cómo será aplicada a un recurso en el simulador.

### Desarrollo Práctico

**Simulador de Gestión de Procesos y Memoria:**

- El simulador debe ser desarrollado en un lenguaje a elección (se recomienda Python).
- Implementación de un sistema de gestión de memoria que permita elegir entre paginación y compactación.
- La memoria principal debe tener un límite predefinido.
- Los procesos deben solicitar memoria de manera aleatoria.
- Si hay suficiente memoria, el proceso debe ingresar a la cola de procesos listos.
- Si no hay suficiente memoria, el proceso debe esperar en la cola de procesos nuevos hasta que otro proceso finalice y libere memoria.
- Se debe gestionar exclusión mutua: un recurso compartido (por ejemplo, un archivo o dispositivo) debe estar protegido, de modo que sólo un proceso pueda acceder a él a la vez.

**Profesores:** Ing. Gabriel Kutz; Ing Juan de Dios Benitez

### Interfaz del Simulador:

- Debe mostrar el estado de los procesos en tiempo real (Listo, Ejecutando, Bloqueado, Terminado).
- Visualización de la asignación y liberación de la memoria en la memoria principal.
- Visualización de la tabla de páginas en tiempo de ejecución.
- Interfaz gráfica (recomendada Tkinter en Python) para visualizar el simulador.

### Defensa del Trabajo

1. **Presentación Formal:**
   - Explicación detallada del diseño del simulador, con énfasis en los desafíos encontrados.
   - Justificación de las decisiones tomadas (por ejemplo, elección de algoritmos de asignación de memoria, métodos de exclusión mutua).

2. **Demostración Práctica:**
   - Ejecución del simulador mostrando su funcionamiento en diferentes escenarios (procesos que esperan, uso de paginación o compactación, conflictos por recursos).
   - Defensa del código explicando cómo se gestionan los procesos, la memoria y los estados de los procesos, así como la implementación de la exclusión mutua.

### Estructura del Informe

1. **Portada:** Título del trabajo, nombres, fecha, materia.
2. **Introducción:** Explicación general del problema y los objetivos del simulador.
3. **Desarrollo:** Explicación teórica de los conceptos clave, los algoritmos utilizados y el diseño del simulador.
4. **Resultados:** Descripción del comportamiento del simulador en diferentes escenarios.
5. **Conclusión:** Reflexión sobre lo aprendido durante el desarrollo del trabajo.
6. **Bibliografía:** Fuentes utilizadas para la parte teórica.

**Profesores:** Ing. Gabriel Kutz; Ing Juan de Dios Benitez
