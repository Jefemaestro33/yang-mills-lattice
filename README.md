---
tags: [física, yang-mills, lattice, SU2, gluebolas, roadmap]
---
# Del framework muerto a la pregunta viva: búsqueda de estados ligeros en el espectro de gluebolas de SU(2)

## Documento de contexto y hoja de ruta

---

## Parte I — El framework original y por qué falló

### Qué proponía el paper

El artículo "A Structural Framework for the Mass Gap in Yang-Mills: Geometric Conjecture" (E.D. Zermeño, 2025) proponía que la brecha de masa en teorías de Yang-Mills es consecuencia inevitable de la geometría del espacio de configuraciones de gauge 𝒜/𝒢. La idea central era:

- Definir una distancia geodésica θ_YM en el espacio de órbitas 𝒜/𝒢 (conexiones módulo transformaciones de gauge).
- Postular que la acción de Yang-Mills crece al menos cuadráticamente con esa distancia: S_YM ≥ C·θ²_YM.
- Construir una categoría monoidal 𝒟_YM donde la "aniquilación" de configuraciones duales (A, Ā) está obstruida cuando θ_YM ≠ 0.
- Concluir que la obstrucción fuerza la existencia de un estado masivo intermedio Z con masa m_Z ~ 20–90 MeV, interpretado como la gluebola más ligera (0⁺⁺) y como la brecha de masa de la teoría.

El framework también conectaba con un trabajo previo del autor sobre "aniquilación condicional" en QED (positronio), proponiendo que la función de supresión f(θ) = cos²(θ/2) es universal, y con modelos de materia oscura donde los estados Z residuales del Big Bang compondrían la densidad de materia oscura observada.

### Evaluación: qué está mal y por qué

El paper fue sometido a tres evaluaciones independientes exhaustivas. Las tres convergen en el mismo diagnóstico. Los problemas son estructurales, no cosméticos.

**1. Los resultados rigurosos son conocidos desde los años 80**

El Teorema A (coercividad local del operador de fluctuación cerca de conexiones ASD irreducibles en S⁴) no es nuevo. Los ingredientes — Bochner-Weitzenböck con Ric_{S⁴} = 3g sobre 1-formas, absorción de Gagliardo-Nirenberg, desigualdad de Poincaré en el slice de Coulomb, compacidad de Rellich-Kondrachov — aparecen en:

- Bourguignon-Lawson (Commun. Math. Phys. 79, 1981): prueban que toda conexión Yang-Mills débilmente estable en S⁴ es ASD o SD. Esto implica que el hessiano es estrictamente positivo transversal al espacio de móduli — exactamente el contenido del Teorema A.
- Freed-Uhlenbeck (*Instantons and Four-Manifolds*, 1984): desarrollan el aparato completo de slices locales, la submersión riemanniana 𝒜 → 𝒜/𝒢, y la teoría de Fredholm para el operador de fluctuación.
- Feehan (Adv. Math. 312, 2017; Memoirs AMS 267, 2020): demuestra desigualdades de Łojasiewicz-Simon para el funcional de Yang-Mills cerca de puntos críticos — un resultado estrictamente más fuerte que la coercividad local.

El Lema 5.3 (expandir la acción a segundo orden alrededor de la conexión plana y aplicar Poincaré) es un ejercicio estándar de análisis en cualquier curso de QCD en retícula.

**2. El argumento categorial (DHR) es circular**

El paper invoca la teoría de superselección de Doplicher-Haag-Roberts para argumentar que, cuando dos sectores no fusionan al sector trivial, la teoría "requiere" un campo de extensión (el estado Z). Pero:

- El criterio de selección de DHR (que las representaciones sean unitariamente equivalentes al vacío en el complemento causal de conos dobles suficientemente grandes) presupone explícitamente la existencia de una brecha de masa. Doplicher y Roberts (Inventiones Math. 98, 1989) lo dicen directamente: el criterio está "tailored to theories without massless particles."
- En teorías confinantes, no existen sectores de superselección DHR con carga de color no trivial. Resultados rigurosos recientes en 1+1D (arXiv:2508.09172, arXiv:2507.14699) confirman que la categoría DHR de una teoría confinante es esencialmente trivial.
- La circularidad es: asumir brecha de masa → aplicar DHR → derivar existencia de estado masivo → concluir brecha de masa. No se puede reparar añadiendo más trabajo — es un error de arquitectura lógica.

**3. La predicción de masa contradice 40 años de evidencia**

La fórmula m₀ = c̃·Λ_YM·θ₀ con los priors declarados (Λ_YM ∈ [0.25, 0.30] GeV, θ₀ ∈ [0.10, 0.30], c̃ ∈ [0.8, 1.0]) produce m₀ ∈ [20, 90] MeV. Esto contradice el consenso de QCD en retícula por un factor de 20–85×:

| Grupo | Año | Masa 0⁺⁺ (MeV) |
|---|---|---|
| Morningstar-Peardon | 1999 | 1730 ± 80 |
| Vaccarino-Weingarten | 1999 | 1648 ± 58 |
| Chen et al. | 2006 | ~1710 |
| Athenodorou-Teper | 2020 | ~1650–1730 |

Un estado de 20–90 MeV sería más ligero que el pión (135 MeV) sin tener ningún mecanismo de protección (no hay bosones de Goldstone en YM puro, no hay simetría quiral que romper espontáneamente). Habría sido detectado trivialmente en dispersión pión-pión, que está medida con precisión hasta el umbral (~280 MeV). No existe.

La predicción es irrecuperable: si se ajusta θ₀ para reproducir ~1.6 GeV, se pierde la motivación geométrica ("pequeño twist cerca del vacío"), y el parámetro deja de ser pequeño.

**4. La analogía QED → YM carece de base física**

La función cos²(θ/2) es la fórmula de overlap de espín-1/2 (coherent states en la esfera de Bloch). Los gluones son espín-1. Las funciones de overlap para espín-1 involucran matrices d de Wigner con dependencia angular diferente. Además, QED es abeliana, débilmente acoplada, y no confinante. Yang-Mills puro es no abeliano, fuertemente acoplado, y confinante. No hay pares materia-antimateria que "aniquilen" en una teoría de gauge pura.

**5. El álgebra de Clifford Cl(6,0) es ad hoc**

En Yang-Mills puro no hay fermiones. Toda la literatura que usa Cl(6) o ℂl(6) en teoría de gauge (Furey, Stoica, Todorov, Trayling-Baylis) lo hace para describir el contenido fermiónico del Modelo Estándar — quarks y leptones. En una teoría con solo gluones (espín-1, representación adjunta), no hay "sector de espín interno" que requiera un álgebra de Clifford. La descomposición θ²_YM = w_Q(ΔQ)² + w_H‖ΔΦ‖² + w_S‖ΔS_Cliff‖² incluye un término que no emerge de la geometría de 𝒜/𝒢.

**6. La combinación de cotas energéticas es matemáticamente inválida**

La cota B1 (Bogomolny) es estándar y correcta. Las cotas B2 (holonomía) y B3 (estructura interna) son conjeturales y sin precedente. Pero incluso si fueran ciertas, sumar S_YM ≥ B1, S_YM ≥ B2, S_YM ≥ B3 para obtener S_YM ≥ B1 + B2 + B3 es inválido. De tres cotas inferiores independientes solo se puede concluir S_YM ≥ max(B1, B2, B3). La suma requiere una descomposición ortogonal de la acción en tres partes independientes, que no se demuestra.

**7. La verificación de Osterwalder-Schrader es incompleta y parcialmente circular**

OS-1 a OS-3 para n ≤ 2 en la red son estándar (Fröhlich-Osterwalder-Seiler, 1979), pero eso es un resultado sobre la teoría en la red, no sobre el límite continuo — que es precisamente la parte no resuelta del problema. El "esbozo condicional" de OS-4 asume la brecha de masa para derivar decaimiento exponencial, creando circularidad con la reconstrucción de Wightman que necesita OS-4 para producir la brecha de masa.

### Diagnóstico final del framework

**Los ingredientes rigurosos son conocidos. Los ingredientes novedosos no son rigurosos ni empíricamente viables.** El framework combina resultados estándar de los 80s con construcciones ad hoc (Cl(6,0), cos²(θ/2), categoría 𝒟_YM) y una predicción de masa errónea por dos órdenes de magnitud. No constituye un avance hacia el problema del milenio de Yang-Mills.

---

## Parte II — La pregunta que sobrevive

### Lo que queda después de tirar todo lo que no sirve

Debajo del aparato categorial, la analogía con QED, la materia oscura y la predicción fallida de masa, hay una pregunta legítima y no completamente resuelta:

> **¿Existe estructura no explorada en el espectro de baja energía de Yang-Mills que los operadores convencionales de gluebola no capturan?**

Esta pregunta no depende del framework de Zermeño. No requiere cos²(θ/2), ni el estado Z, ni la categoría 𝒟_YM. Es una pregunta sobre completitud de bases de operadores en simulaciones de QCD en retícula.

### Por qué la pregunta es legítima

El consenso de ~1.6 GeV para la gluebola 0⁺⁺ más ligera proviene de simulaciones que construyen operadores de interpolación a partir de loops de Wilson (plaquetas, plaquetas smeared, loops rectangulares, etc.) y los optimizan mediante análisis variacional (GEVP). Estos operadores son combinaciones de trazas de productos de matrices de enlace alrededor de caminos cerrados.

La suposición implícita es que esta base de operadores tiene overlap suficiente con todos los estados físicos relevantes del espectro. Para los estados más pesados y bien establecidos, esto está ampliamente verificado. Pero:

- Nadie ha demostrado matemáticamente que los operadores de loops de Wilson forman una base completa para el espectro de baja energía.
- Si existiera un estado con overlap exponencialmente pequeño con todos los operadores convencionales, sería invisible incluso con estadística perfecta — el análisis variacional simplemente no lo vería.
- Estados con estructura topológica no trivial (dependencia fuerte en la carga topológica Q, sensibilidad al ángulo θ del vacío) podrían tener overlap pobre con operadores construidos de plaquetas locales, que son topológicamente triviales.

La probabilidad de que tal estado exista es baja. Pero "baja" no es "cero", y la forma de convertir una probabilidad en una respuesta es medir.

### La conexión con el ángulo θ del vacío de QCD

Esta es la dirección concreta más interesante, y no requiere nada del framework original.

La teoría de Yang-Mills tiene un parámetro físico real: el ángulo θ del vacío, que entra en la acción como un término topológico θ·Q (donde Q es la carga topológica). La energía del vacío depende de θ como E(θ) ∝ 1 − cos(θ) para θ pequeño (Witten, 1979; di Vecchia-Veneziano). El espectro de masas también depende de θ.

**Lo que se sabe:**
- A θ = 0 (la QCD real), el espectro de gluebolas es el estándar (~1.6 GeV para 0⁺⁺).
- La susceptibilidad topológica χ_t = d²E/dθ² está bien medida en la retícula.
- La θ-dependencia de masas individuales de gluebolas no ha sido estudiada sistemáticamente en SU(2) con estadística moderna.

**Lo que no se sabe:**
- Si hay estados que solo "se encienden" a θ ≠ 0 — estados cuya función de onda tiene nodo a θ = 0 y por tanto son invisibles en simulaciones estándar.
- Cómo se reorganiza el espectro de baja energía cuando θ se acerca a π (el punto de Dashen, donde hay una transición de fase de primer orden en SU(N≥3)).
- Si la base de operadores convencional captura adecuadamente los estados sensibles a la topología.

**Advertencia importante:** El ángulo θ del vacío de QCD y el θ_YM del paper de Zermeño son objetos matemáticos completamente distintos. Uno es un parámetro fijo de la teoría lagrangiana; el otro es un funcional sobre el espacio de configuraciones. Que ambos se denoten con θ y que cos²(θ/2) aparezca en ambos contextos es coincidencia notacional. Este documento no afirma conexión entre ellos.

---

## Parte III — Qué buscar y cómo

### El experimento numérico

**Objetivo:** Medir el espectro de gluebolas de SU(2) en la retícula como función del ángulo θ del vacío, usando una base extendida de operadores que incluya componentes sensibles a la topología.

**Diseño:**

1. **Simulación base (control).** SU(2) puro a θ = 0, con operadores estándar (plaquetas + smearing). Debe reproducir el espectro conocido: 0⁺⁺ a ~1.6 GeV (en unidades de la tensión de cuerda √σ). Esto verifica que el código funciona.

2. **Extensión a θ ≠ 0.** Introducir el término topológico mediante el método de "θ imaginario" (simular a θ_I = iθ, donde la acción es real, y continuar analíticamente). Alternativamente, usar reweighting: generar configuraciones a θ = 0 y repesar con exp(iθQ). Para SU(2), el sign problem es manejable a θ pequeño.

3. **Base extendida de operadores.** Además de los operadores estándar (plaquetas, loops rectangulares, smeared), incluir operadores que sean explícitamente sensibles a la carga topológica:
   - Densidad topológica: q(x) = (1/32π²) εμνρσ Tr[Fμν Fρσ] (discretizada con el método de campo-teórico o con gradient flow).
   - Productos mixtos: Tr[F²] × q(x), que tienen overlap con estados que acoplan simultáneamente a excitaciones de gauge y topológicas.
   - Operadores smeared con gradient flow a diferentes tiempos de flujo, que cambian el contenido topológico de la señal.

4. **GEVP (Generalized Eigenvalue Problem).** Construir la matriz de correladores C_ij(t) = ⟨O_i(t) O_j(0)⟩ con la base extendida. Resolver el GEVP para extraer masas y eigenvectores. Buscar si algún eigenvector tiene componente dominante en los operadores topológicos y masa significativamente diferente de los estados conocidos.

### Parámetros concretos

| Parámetro | Valor | Justificación |
|---|---|---|
| Grupo | SU(2) | Más barato que SU(3), sin sign problem fermiónico, gluebolas bien estudiadas |
| Lattice (mínimo viable) | 32³ × 64 | Volumen suficiente para gluebolas; L ≈ 3.8 fm |
| Lattice (serio) | 48³ × 96 | Control de efectos de volumen finito |
| β | 2.5, 2.6, 2.7 | Tres espaciamientos para extrapolación al continuo |
| Configuraciones | 500–1000 por β | Estadística mínima para señal de gluebola |
| Decorrelación | 200+ sweeps entre configuraciones | Para SU(2) el tiempo de autocorrelación topológica es manejable |
| Smearing | Gradient flow a t_flow/a² = 1, 2, 4 | Define los operadores topológicos |
| Valores de θ | 0, π/6, π/3, π/2 (vía reweighting o θ imaginario) | Rango accesible sin sign problem severo |

### Qué resultados esperamos (siendo honestos)

**Resultado más probable (~90%):** El espectro no cambia significativamente con θ en el rango explorado, y los operadores topológicos no revelan estados por debajo de ~1 GeV. Resultado nulo. Esto cierra la pregunta limpiamente y es publicable como: "No evidence for light topological glueball states in SU(2) at nonzero vacuum angle."

**Resultado interesante pero no revolucionario (~9%):** La θ-dependencia de las masas de gluebolas existentes se mide con precisión nueva. Por ejemplo, se obtiene dm/dθ² para el 0⁺⁺, que es un observable físico no medido con estadística moderna en SU(2). Publicable y útil para la comunidad.

**Resultado extraordinario (~1%):** Un estado nuevo aparece en el espectro que no se veía con operadores convencionales. Si sobrevive a todas las verificaciones (continuo, volumen infinito, independencia del operador base, simetrías correctas), sería un descubrimiento.

---

## Parte IV — Qué significaría si encontramos algo

### Si hay un estado ligero: qué cambia y qué no

**Lo que cambiaría:**

- La suposición de completitud de las bases de operadores convencionales en QCD en retícula quedaría cuestionada. Esto tendría implicaciones para toda la espectroscopía de gluebolas y posiblemente para el espectro hadrónico completo.
- La conexión entre estructura topológica y espectro de baja energía de Yang-Mills se convertiría en un área activa de investigación.
- La intuición geométrica detrás del framework de Zermeño — que hay estructura en 𝒜/𝒢 relacionada con la topología que afecta el espectro — recibiría evidencia indirecta. No como validación del framework (que tiene errores independientes), sino como indicación de que la dirección general no estaba equivocada.

**Lo que NO cambiaría:**

- El argumento DHR seguiría siendo circular.
- La función cos²(θ/2) seguiría sin derivación desde primeros principios.
- La analogía QED → YM seguiría siendo injustificada.
- El álgebra de Clifford Cl(6,0) seguiría siendo ad hoc.
- La conexión con materia oscura seguiría sin evidencia.
- La predicción específica de 20–90 MeV casi seguramente no coincidiría con la masa del estado encontrado (si es que existe), porque la fórmula que la produce tiene priors arbitrarios.

En otras palabras: encontrar un estado ligero validaría la pregunta, no la respuesta. Es la diferencia entre "tenía razón en que hay algo ahí" y "su teoría explica qué es ese algo."

### Si no hay nada: qué aprendimos

- Confirmación con base extendida de operadores de que el espectro de SU(2) está completo tal como se conoce. Resultado nulo valioso.
- Medición de la θ-dependencia del espectro con estadística moderna. Contribución menor pero publicable.
- La pregunta queda cerrada de forma verificable: se buscó con los operadores adecuados y no se encontró nada.
- El framework de Zermeño pierde su último punto de contacto con la realidad.

---

## Parte V — Sobre el código existente y qué hay que arreglar

### Estado actual

Existe un código en Python puro (`SU2LatticeQCD`) que implementa la estructura básica: lattice SU(2), acción de Wilson, heat-bath, medición de correladores, extracción de masa efectiva. La estructura es correcta pero tiene bugs críticos que invalidan cualquier resultado numérico.

### Bugs que deben corregirse antes de cualquier simulación

**Bug 1 — Factor de 2 en el exponente del heat-bath.** El código usa `lambda_val = 0.5 * beta * k` y acepta con `exp(lambda_val * (x - 1))`. El peso de Boltzmann correcto para SU(2) es exp(β·k·a₀), no exp(β·k·a₀/2). El código muestrea de la distribución a temperatura doble.

**Bug 2 — Falta la medida de Haar.** La distribución correcta para el parámetro a₀ del cuaternión es P(a₀) ∝ √(1 − a₀²) · exp(β·k·a₀). El factor √(1 − a₀²) viene de integrar las direcciones del 3-vector sobre S² y es la medida de Haar de SU(2). Sin él, se sobrepesan configuraciones cercanas a ±I. El algoritmo estándar de Kennedy-Pendleton lo incluye explícitamente.

**Bug 3 — Acoplamiento anisotrópico incorrecto.** Un enlace espacial U_i(x) participa en plaquetas espaciales (con β_s) y temporales (con β_t). El código aplica β_s uniformemente a todas las grapas de un enlace espacial, perdiendo la ponderación correcta de las grapas temporales. Con anisotropía ξ = 3.5, el error es grande.

**Bug 4 — Parte desconectada del correlador.** El correlador se calcula como C(t) = ⟨O(t)O(0)⟩ sin sustraer ⟨O⟩². Para Tr F², el VEV es no nulo (proporcional a la densidad de acción). Sin sustracción, la masa efectiva a tiempos largos está dominada por la constante, no por el decaimiento exponencial.

### Limitación fundamental: rendimiento

Python puro con bucles anidados sobre todos los sitios es ~10,000× más lento que una implementación vectorizada en GPU. Para que la simulación sea viable con presupuesto limitado ($200–300 en cloud), el código debe reescribirse con:

- **CuPy** (numpy en GPU) con actualización checkerboard (todos los sitios pares simultáneamente, luego impares).
- O usar una librería existente: **LatticeQCD.jl** (Julia) o **Grid** (C++).

### Escalera de fases: del $0 al dato

Cada fase valida la anterior antes de gastar más. Se puede parar en cualquier punto sin desperdiciar lo invertido.

#### Fase 0 — $0 (Google Colab, GPU T4 gratuita)

**Objetivo:** Demostrar que el código funciona. No se gasta nada hasta que este paso esté completo.

| Parámetro | Valor |
|---|---|
| Lattice | 12³ × 24 |
| Grupo | SU(2) |
| β | 2.5 |
| Configuraciones | 200 |
| Decorrelación | 100 sweeps |
| Implementación | CuPy vectorizado (checkerboard) |
| Tiempo estimado | ~2–4 horas en T4 |

**Qué se mide y qué se espera:**

1. **Plaqueta promedio.** Para SU(2) a β = 2.5 en volumen grande, el valor tabulado es ~0.62. Si el código da eso (±0.01), funciona. Si no, hay bug. Este es el primer checkpoint absoluto.
2. **Correlador de plaqueta y masa efectiva.** En un lattice tan pequeño no se resuelve la gluebola limpiamente, pero se debe ver decaimiento exponencial con masa efectiva del orden de ~1 en unidades del lattice. Esto confirma que la extracción de masa funciona.

**Criterio para avanzar:** Plaqueta promedio correcta Y decaimiento exponencial visible en el correlador.

#### Fase 1 — $15–20 (Google Cloud, A100 spot instance ~$1/hora)

**Objetivo:** Medir la gluebola estándar y buscar dependencia topológica en el correlador.

| Parámetro | Valor |
|---|---|
| Lattice | 24³ × 48 |
| Grupo | SU(2) |
| β | 2.5 |
| Configuraciones | 500 |
| Decorrelación | 200 sweeps |
| Implementación | CuPy en A100 |
| Tiempo estimado | ~15 horas de GPU (~$15) |

**Qué se mide:**

1. **Masa del 0⁺⁺ con operadores estándar.** Debe dar ~1.5–1.7 GeV al convertir a unidades físicas. Este es el segundo checkpoint: reproducir el resultado conocido.
2. **Carga topológica Q por configuración.** Usando gradient flow para definir la densidad topológica. Se obtiene la distribución P(Q) y la susceptibilidad χ_t = ⟨Q²⟩/V.
3. **Correlador por bin topológico.** Separar las 500 configuraciones en bins según |Q| (ej: Q = 0, |Q| = 1, |Q| ≥ 2). Medir el correlador de gluebola en cada bin por separado. Comparar las masas efectivas.

**El dato interesante de esta fase:** ¿La masa efectiva del 0⁺⁺ depende de |Q|? Si la masa no cambia con Q, no hay señal topológica y probablemente la búsqueda termina aquí — resultado nulo limpio. Si cambia, hay algo que investigar y se justifica la Fase 2.

**Criterio para avanzar:** Masa del 0⁺⁺ en el rango correcto (~1.6 GeV) Y dependencia estadísticamente significativa de la masa o el correlador con |Q|.

#### Fase 2 — $30–50 (solo si Fase 1 muestra algo)

**Objetivo:** Explorar θ ≠ 0 y base extendida de operadores.

| Parámetro | Valor |
|---|---|
| Lattice | 24³ × 48 (mismas configuraciones de Fase 1) + 32³ × 64 nuevo |
| Grupo | SU(2) |
| β | 2.5, 2.6 (dos espaciamientos) |
| Configuraciones | 500 por β (reutilizar Fase 1 + generar nuevo) |
| Valores de θ | 0, π/6, π/3, π/2 (vía reweighting) |
| Operadores extra | Densidad topológica q(x) smeared, Tr[F²]·q(x) |
| Tiempo estimado | ~30–50 horas de GPU |

**Qué se mide:**

1. **Reweighting a θ ≠ 0.** Tomar las configuraciones de Fase 1 y repesar con exp(iθQ). Para SU(2) y θ ≤ π/2, la distribución de Q es suficientemente estrecha para que el reweighting funcione (verificar que el overlap de distribuciones no sea despreciable).
2. **θ-dependencia de la masa del 0⁺⁺.** Medir m(θ) y extraer la curvatura d²m/dθ². Este es un observable físico no medido con estadística moderna en SU(2).
3. **GEVP con base extendida.** Meter la densidad topológica smeared y los operadores mixtos en la matriz de correladores junto con los operadores estándar. Buscar si aparece un eigenvalor nuevo por debajo de ~1 GeV.
4. **Control de volumen.** Comparar 24³ × 48 con 32³ × 64 para verificar que cualquier señal no sea un artefacto de volumen finito.

**Resultados posibles:**

- **Nada nuevo (~90%).** El espectro no cambia significativamente con θ. Los operadores topológicos no revelan estados nuevos. Resultado nulo. Publicable como: "Topological operator basis and θ-dependence of the SU(2) glueball spectrum." Gasto total: ~$50. Se aprendió lattice QCD.
- **θ-dependencia medida (~9%).** Se obtiene dm/dθ² con barras de error competitivas. Contribución menor pero publicable. No valida ni refuta el framework original.
- **Estado nuevo (~1%).** Un eigenvalor del GEVP aparece con masa significativamente por debajo del 0⁺⁺ estándar, con componente dominante en operadores topológicos. Si esto ocurre, NO publicar inmediatamente. Primero: verificar con tercer valor de β (escalar a Fase 3, ~$100 adicionales), verificar independencia de volumen, verificar simetrías (C, P, T), descartar artefactos de smearing. Solo después de que todo eso pase, se tiene un resultado.

#### Fase 3 — $100–200 (solo si Fase 2 muestra señal)

Se escala a 48³ × 96, tres o más valores de β para extrapolación al continuo, múltiples volúmenes, y análisis variacional completo con 10+ operadores. Este es el nivel donde un resultado se vuelve publicable en una revista seria. Solo se llega aquí si las fases anteriores producen evidencia concreta.

**Gasto total acumulado si se llega a Fase 3:** ~$150–270.

---

## Nota final

Este documento no afirma que el framework de Zermeño sea correcto. Afirma que, después de descartar todo lo que está mal, queda una pregunta empírica legítima que se puede responder con una simulación en retícula bien diseñada y honestamente ejecutada. La respuesta más probable es "no hay nada nuevo." Pero vale la pena verificarlo, porque las preguntas que nadie hace son las que más pueden sorprender.

La escalera de fases está diseñada para que cada paso produzca un resultado verificable independientemente de los siguientes. Se puede parar en cualquier punto. El primer gasto real ocurre solo después de que el código haya demostrado que funciona en hardware gratuito.
