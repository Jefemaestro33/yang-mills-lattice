# Plan de Ejecución v2: Estructura Topológica del Vacío y Espectro de Gluebolas en SU(2)

**Versión 4.1 — Corrige confusión notacional g₂/m₂; revisa significancias al alza; añade caveats sobre overlap ratios**  
**Fecha**: 2026-04-03  
**Repo**: Jefemaestro33/yang-mills-lattice

---

## Cambios principales respecto a v1

| Aspecto | Plan v1 | Plan v2 (este) |
|---------|---------|-----------------|
| Valores de β | Solo β=2.5 | **β=2.5 + β=2.6** (dos espaciados para continuum limit) |
| m₂ de referencia SU(3) | −0.06(2) (Del Debbio, β finito) | **−0.0083(23)** (Bonanno+ continuo) |
| Significancias | 14–28σ | **5–10σ a un β; ~2–5σ tras continuum** (realistas) |
| Prioridad | Med 1 → Med 2 → Med 3 | **Med 2 → Med 1 → Med 3** |
| Framing Paper 1 | "Primera medición de g₂(SU(2))" | **"g₂(SU(2)) con dos espaciados + extrapolación"** |
| Costo total | ~330 GPU-hrs | **~700 GPU-hrs** |

---

## 0. Parámetros del lattice — DOS VALORES DE β

### 0.1 β = 2.5 (grueso)

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| a√σ | 0.190(10) | Fingberg-Heller-Karsch (1993) |
| a | 0.085(5) fm | Derivado |
| Lattice principal | 24³×48 | L ≈ 2.0 fm, L√σ ≈ 4.6 |
| χ_lat | 5.05 × 10⁻⁵ | Derivado |
| ⟨Q²⟩ (24³×48) | 33.5 | Verificado |

### 0.2 β = 2.6 (fino) ⚠️ NUEVO

| Parámetro | Valor estimado | Fuente |
|-----------|---------------|--------|
| a√σ | ~0.140(8) | Interpolación Fingberg+(1993), Athenodorou-Teper(2021) |
| a | ~0.063(4) fm | Derivado |
| Lattice principal | **32³×64** | L ≈ 2.0 fm, L√σ ≈ 4.5 |
| χ_lat | ~1.54 × 10⁻⁵ | Derivado: (0.4437)⁴ × (0.140)⁴ |
| ⟨Q²⟩ (32³×64) | ~32 | 1.54×10⁻⁵ × 32³×64 |

**Nota**: El valor exacto de a√σ a β=2.6 debe verificarse midiendo la string tension o usando el Sommer parameter r₀ en las primeras configs generadas. Los valores arriba son estimaciones iniciales.

### 0.3 Masas de gluebolas corregidas

| Estado | m/√σ (continuo, Athenodorou-Teper 2021) | am (β=2.5) | am (β=2.6) |
|--------|------------------------------------------|------------|------------|
| 0⁺ (0++) | 3.781(23) | 0.718 | 0.529 |
| 2⁺ (2++) | 5.35(2) | 1.017 | 0.749 |
| 0⁻ (0−+) | 6.017(61) | 1.143 | 0.842 |

### 0.4 Estado del arte — CONTEXTO ACTUALIZADO (CONFUSIÓN NOTACIONAL RESUELTA)

⚠️ **IMPORTANTE**: Del Debbio (2006) y Bonanno (2024) usan "g₂" para cantidades DIFERENTES:

| Cantidad | Notación Del Debbio | Notación Bonanno | SU(3) β=6.0 | SU(3) continuo |
|----------|--------------------|--------------------|-------------|----------------|
| Coef. de la **masa** M(θ) | **g₂** | **m₂** | −0.06(2) | **−0.0083(23)** |
| Coef. de la **string tension** σ(θ) | s₂ | s₂ | −0.08(1) | −0.0258(14) |
| Coef. del **ratio** M/√σ(θ) | (no definido) | **g₂** | — | 0.0046(24) ≈ 0 |

**En este plan usamos la notación de Bonanno**: m₂ = coeficiente de masa, g₂ = coeficiente del ratio.

**Implicación**: La masa del glueball SÍ depende de θ (m₂ ≠ 0 a 3.6σ en SU(3)), pero los artefactos de discretización son un factor ~7 (de −0.06 a −0.008). Lo que nuestra Medición 1 mide es equivalente a m₂. Para SU(2) no existe medición — esta es la pregunta abierta.

---

## 1. Diagnóstico: el problema de ⟨Q²⟩ = 3.4

Sin cambios respecto a v1. **Antes de cualquier medición nueva, resolver este bug.**

### Fase 0A: Diagnóstico (1–3 días)

**Paso 1**: Histograma de Q crudo → ¿se redondean a enteros?  
**Paso 2**: Verificar normalización de q(x) para SU(2)  
**Paso 3**: Verificar que Q = Σ_x q(x) suma sobre 24³×48 completo  
**Paso 4**: Recalcular Q a t_flow = 0.5, 1.0, 1.5, 2.0, 3.0 en 100 configs  

**Criterio de éxito**: ⟨Q²⟩ = 30–40, distribución gaussiana con σ_Q ≈ 5.8.

---

## 2. Medición 2: GEVP mixto con q(x) — PRIORIDAD #1

**Razón del cambio de prioridad**: La Medición 2 es la más novedosa y sin competencia directa. **Caveat importante (v2.1)**: los overlap ratios SÍ tienen artefactos O(a²) — los autovectores del GEVP heredan la discretización de cada operador (Blossier et al., 2009), y q(x) vía gradient flow tiene efectos O(a²/t_flow) adicionales (Cè et al., 2016). Sin embargo, los patrones **cualitativos** (qué estado tiene más carácter topológico) son robustos. El paper debe enmarcarse como **avance metodológico** con caveats explícitos, no como medición de overlap ratios físicos.

### Fase 2A: Generación de estadística + desarrollo de código (4–6 semanas)

**En paralelo**:

**Track 1 — Generación** (semanas 1–3):
- Completar 1,000 configs existentes
- Generar 19,000 configs adicionales en 24³×48, β=2.5
- Total: 20,000 configs
- Tiempo: ~20 GPU-horas
- En cada config: medir Q (gradient flow), correladores 0++ (4 niveles APE)

**Track 2 — Desarrollo** (semanas 1–6):

1. **Operadores 0⁻⁺** (representación A₁⁻ del grupo octaédrico):
```
- Combinaciones de Wilson loops impares bajo paridad
- Loops tipo "chair" y "twisted" (Morningstar-Peardon 1999)
- 4 niveles de APE smearing (0, 5, 10, 20)
→ 4 operadores convencionales O_i(t), i = 1..4
```

2. **Q_slice por time-slice**:
```
Para cada config y t_flow ∈ {0.5, 1.0, 2.0}:
    Para cada time-slice t:
        Q_slice(t) = Σ_{x espacial} q(x,t)
→ 3 operadores topológicos T_j(t), j = 1..3
```

3. **Matriz de correladores 7×7**:
```
C_αβ(t) = ⟨α(t) β(0)⟩ - ⟨α⟩⟨β⟩
Bloques: C_OO (4×4), C_TT (3×3), C_OT (4×3)
```

4. **GEVP solver con análisis de errores sistemáticos**:
```python
def solve_gevp(C, t, t0):
    eigenvalues, eigenvectors = scipy.linalg.eigh(C[:,:,t], C[:,:,t0])
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]
```
- Implementar variación de t₀ = 1, 2, 3 para estimar sistemáticos
- Jackknife con bloques de 100 configs

### Fase 2B: Medición sobre 20,000 configs (1–2 semanas)

Reusar configs de Fase 2A. En cada config:
1. Gradient flow a t_flow = 0.5, 1.0, 2.0
2. Q_slice(t) por time-slice
3. Operadores 0⁻⁺ con APE smearing
4. Matriz completa 7×7

### Fase 2C: Análisis GEVP (3–4 semanas)

1. **GEVP convencional 4×4** (baseline) → masas del 0⁻⁺
2. **GEVP mixto 7×7** → masas + autovectores
3. **Observable clave — overlap ratios**:
```
r_n = |⟨T|n⟩|² / |⟨O|n⟩|²
```

**Escenarios**:

| Resultado | Interpretación | Paper target |
|-----------|----------------|-------------|
| r_n ≈ constante | q(x) no aporta info nueva | PRD, resultado negativo limpio |
| r₁ ≠ r₂ significativamente | Carácter topológico diferenciado | **PRL** |
| Estado invisible al 4×4 | "Glueball topológica" | **PRL alto impacto** (improbable) |

→ **DRAFT PAPER 2** al final de esta fase.

---

## 3. Medición 1: g₂(SU(2)) con dos espaciados

### Fase 1A: Generación del segundo ensamble (3–4 semanas)

**Ensamble a β = 2.6** ⚠️ NUEVO:

| Parámetro | Valor |
|-----------|-------|
| Lattice | 32³×64 |
| β | 2.6 |
| Configs | 20,000 |
| Separación | ≥ 200 sweeps |
| Tiempo estimado (1 GPU) | ~200 horas |
| Almacenamiento | ~300 GB |

**Mediciones por config**: Q (gradient flow), correladores 0++ (4 niveles APE), GEVP 4×4.

**Primera tarea**: medir a√σ a β=2.6 con 500 configs para confirmar ~0.140 antes de generar el ensamble completo.

### Fase 1B: Análisis por sector Q a dos β (3–4 semanas)

**Bins para β=2.5** (24³×48, N=20,000, σ_Q=5.79):

| Bin | |Q| | Configs | ⟨Q²⟩_bin |
|-----|----|---------|----------|
| A | 0 | 1,368 | 0.0 |
| B | 1–2 | 5,277 | 2.5 |
| C | 3–5 | 6,455 | 16.0 |
| D | 6–8 | 4,011 | 47.8 |
| E | 9–12 | 2,252 | 103.7 |
| F | ≥13 | 481 | 189.2 |

**Bins para β=2.6** (32³×64, N=20,000, σ_Q ≈ 5.7):
Distribución similar ya que ⟨Q²⟩ ≈ 32 es comparable.

**Protocolo de análisis**:
1. GEVP 4×4 en cada bin, cada β
2. Extraer g₂(β=2.5) y g₂(β=2.6) independientemente
3. **Extrapolación al continuo**: g₂(a) = g₂(0) + c₁·a² (ajuste lineal en a²)
4. Con solo 2 puntos: la "extrapolación" es una interpolación — el error será grande pero informativo

**Significancias revisadas** (realistas, incluyendo sistemáticos GEVP):

| Escenario | m₂ a espaciado finito | Significancia por β | m₂ continuo (2 puntos) |
|-----------|----------------------|---------------------|------------------------|
| SU(2) similar a SU(3) | ~0.03–0.06 | 3–6σ | −0.008 ± 0.005 (~2σ) |
| SU(2) anómalo (viola 1/N²) | ~0.08–0.15 | 5–10σ | −0.03 ± 0.01 (~3σ) |

**Nota**: Usamos m₂ (notación Bonanno) = coeficiente de masa. En SU(3), m₂ pasa de ~−0.06 a β finito a −0.0083 en el continuo (factor ~7 de artefactos).

→ Publicable en ambos escenarios como **primera medición de m₂(SU(2)) con dos espaciados**.

**Controles sistemáticos reforzados**:
- Variación de t₀ en GEVP (t₀ = 1, 2, 3)
- Variación del rango de plateau [t_min, t_max]
- Comparación con/sin bin F (baja estadística)
- Verificar m₀(β=2.5) y m₀(β=2.6) vs valores publicados de Athenodorou-Teper

→ **DRAFT PAPER 1** al final de esta fase.

---

## 4. Medición 3: Correlador Q²(t)

### Fase 3A: Generación de ensambles pequeños (2–4 semanas)

50,000 configs por volumen, ambos β:

**β = 2.5**:

| Lattice | L (fm) | L√σ | ⟨Q²⟩ | Configs | GPU-hrs |
|---------|--------|-----|-------|---------|---------|
| 12³×24 | 1.02 | 2.3 | 2.1 | 50,000 | ~8 |
| 16³×32 | 1.36 | 3.0 | 6.6 | 50,000 | ~30 |
| 20³×40 | 1.70 | 3.8 | 16.2 | 50,000 | ~80 |

**β = 2.6** (para verificar escalamiento) ⚠️ NUEVO:

| Lattice | L (fm) | L√σ | ⟨Q²⟩ | Configs | GPU-hrs |
|---------|--------|-----|-------|---------|---------|
| 16³×32 | 1.01 | 2.2 | 0.8 | 50,000 | ~15 |
| 22³×44 | 1.39 | 3.1 | 5.5 | 50,000 | ~60 |
| 28³×56 | 1.76 | 3.9 | 15.1 | 50,000 | ~150 |

### Fase 3B: Análisis del correlador Q² (3–4 semanas)

Sin cambios conceptuales respecto a v1:
1. Calcular C_{Q²}(τ) = ⟨Q(t+τ)²·Q(t)²⟩_conn
2. Masa efectiva m_eff(τ) = −ln[C(τ+1)/C(τ)]
3. Comparar con m(0++) del GEVP estándar
4. Estudiar dependencia en volumen y en a (dos β)

→ **DRAFT PAPER 3** al final de esta fase.

---

## 5. Pipeline de código

```
yang-mills-lattice/
├── su2_lattice.py          # Código principal (modificar)
├── run_phase0.py           # Diagnóstico Q² (existente)
├── run_phase1.py           # Generación + medición (existente)
├── analysis.py             # Análisis (existente)
│
├── src/
│   ├── topology.py         # Gradient flow, q(x), Q_slice
│   ├── operators_0pp.py    # Operadores 0++ (refactorizar)
│   ├── operators_0mp.py    # Operadores 0⁻⁺ (NUEVO)
│   ├── gevp.py             # Solver GEVP + sistemáticos
│   ├── jackknife.py        # Errores jackknife/bootstrap
│   ├── continuum.py        # Extrapolación al continuo (NUEVO)
│   └── io_utils.py         # I/O
│
├── scripts/
│   ├── phase0_diagnose_Q.py
│   ├── phase1_calibrate_beta26.py    # NUEVO: medir a√σ a β=2.6
│   ├── phase1_generate.py            # Generación (ambos β)
│   ├── phase1_measure_bins.py        # Análisis por sector Q
│   ├── phase1_continuum_extrap.py    # NUEVO: extrapolación g₂
│   ├── phase2_measure_qx.py
│   ├── phase2_gevp_mixed.py
│   ├── phase3_generate_small.py
│   ├── phase3_Q2_correlator.py
│   └── phase3_volume_scaling.py
│
├── results/{phase0,phase1,phase2,phase3}/
└── notebooks/{phase0,phase1,phase2,phase3}_results.ipynb
```

---

## 6. Cronograma revisado

```
Semana 1–2:     FASE 0   — Diagnóstico ⟨Q²⟩ = 3.4, fix del código

Semana 3–8:     FASE 2A  — Generación 20k configs β=2.5 (Track 1, sem 3-4)
                           Desarrollo operadores 0⁻⁺ + GEVP (Track 2, sem 3-8)

Semana 9–10:    FASE 2B  — Medición Q_slice + correladores 7×7

Semana 11–14:   FASE 2C  — Análisis GEVP mixto
                           → DRAFT PAPER 2 (la prioridad #1)

Semana 9–14:    FASE 1A  — Calibración a√σ a β=2.6 (sem 9)
(paralelo)                 Generación 20k configs β=2.6 32³×64 (sem 9-14)

Semana 15–18:   FASE 1B  — Análisis g₂ a dos β + extrapolación continuo
                           → DRAFT PAPER 1

Semana 15–18:   FASE 3A  — Generación ensambles pequeños (ambos β)
(paralelo)

Semana 19–22:   FASE 3B  — Correlador Q², masas efectivas, scaling
                           → DRAFT PAPER 3

Semana 23–28:   REDACCIÓN — Finalización papers 1-3
                            Paper 4 (síntesis) si amerita
```

**Duración total: ~7 meses** (1 mes más que v1, por el segundo β).

---

## 7. Criterios de go/no-go

### Gate 0 (fin Semana 2):
- ✅ ⟨Q²⟩ = 30–40 en 24³×48 → GO
- ❌ ⟨Q²⟩ < 10 después de fixes → STOP

### Gate 2 (fin Semana 14) — PRIMERO porque es prioridad #1:
- ✅ GEVP 7×7 estable, overlap ratios definidos → GO Paper 2
- ⚠️ Señal ruidosa → más smearing levels o stats
- ❌ C_OT ≈ 0 → resultado nulo publicable

### Gate 1 (fin Semana 14, paralelo):
- ✅ a√σ(β=2.6) medido, consistente con ~0.140 → GO generación completa
- ❌ Valor inesperado → recalibrar antes de generar 20k configs

### Gate 1b (fin Semana 18):
- ✅ g₂ detectado a >3σ en al menos un β → GO extrapolación
- ⚠️ g₂ compatible con 0 a ambos β → publicar como cota superior (aún publicable)
- ❌ Masas inconsistentes con Athenodorou-Teper → revisar código

### Gate 3 (fin Semana 22):
- ✅ Plateau en m_eff(Q²) en ≥2 volúmenes → GO Paper 3
- ❌ Sin plateau → estudio de viabilidad con cotas

---

## 8. Recursos computacionales revisados

| Recurso | Fase 0 | Fase 2 | Fase 1 | Fase 3 | Total |
|---------|--------|--------|--------|--------|-------|
| GPU-hrs (generación) | 0 | 20 | **220** | **343** | **583** |
| GPU-hrs (medición) | 5 | 60 | 60 | 80 | 205 |
| Almacenamiento | 0 | 22 MB | **385 GB** | **300 GB** | **~690 GB** |

**Total: ~790 GPU-horas** (~33 días en 1 GPU, ~4 días en 8 GPUs).

**Costo estimado en GCP**:
- T4 spot: ~790 hrs × $0.11/hr = **~$87**
- V100 spot: ~790/4 hrs × $0.74/hr = **~$146** (4× más rápido)

El segundo β (32³×64) es el principal costo adicional: ~300 GPU-hrs para generación + medición. Sigue siendo accesible.

---

## 9. Papers target — REVISADOS

### Paper 2 (PRIMERO): "Topological charge density in the glueball variational basis"
- **Target**: Physical Review Letters (si overlap ratios distintos) o JHEP
- **Mensaje**: Primera inclusión de q(x) en un GEVP de gluebolas — demostración metodológica + primera observación de acoplamiento diferenciado
- **Competencia**: Ninguna directa
- **Framing**: Paper metodológico. Overlap ratios cualitativos, no cuantitativos. Caveats sobre O(a²) explícitos. Estabilidad bajo variación de t_flow como control parcial de sistemáticos.
- **Timeline**: Draft semana 14

### Paper 1: "θ-dependence of the SU(2) glueball mass: first measurement with two lattice spacings"
- **Target**: Physical Review D
- **Mensaje**: m₂(SU(2)) medido a dos espaciados con extrapolación rudimentaria al continuo
- **Framing clave**: "En SU(3), m₂ = −0.0083(23) en el continuo (Bonanno+ 2024), con artefactos de discretización de factor ~7. ¿SU(2) muestra la misma supresión, o m₂(SU(2)) sobrevive al continuo? Los datos de b₂ sugieren desviaciones del escalamiento 1/N²."
- **Notación**: Usar m₂ (Bonanno) explícitamente, no g₂ (Del Debbio), para evitar confusión
- **Competencia**: Bonanno et al. podrían hacerlo — publicar antes de Lattice 2027
- **Timeline**: Draft semana 18

### Paper 3: "Spectroscopy of topological fluctuations with the Q² operator in SU(2)"
- **Target**: Physical Review D
- **Mensaje**: Primer uso de Q²(t) como herramienta espectroscópica + estudio multi-volumen a dos espaciados
- **Competencia**: Ninguna
- **Timeline**: Draft semana 22

### Paper 4 (condicional): "Topological anatomy of the SU(2) glueball spectrum"
- Solo si ≥2 mediciones dan resultados no triviales

---

## 10. Riesgos y mitigaciones — ACTUALIZADO

| Riesgo | Prob. | Impacto | Mitigación |
|--------|-------|---------|------------|
| ⟨Q²⟩ no se arregla | 15% | Bloquea todo | Comparar con openQCD/Grid |
| m₂ muy pequeño en continuo (~−0.008 como SU(3)) | **35%** ⚠️ | Paper 1 es cota/detección marginal | Publicable como primera medición; comparar con SU(3) |
| m₂ dominado por artefactos (~factor 7 como SU(3)) | **50%** ⚠️ | Segundo β es imprescindible | Por eso incluimos β=2.6; discutir scaling |
| Operadores 0⁻⁺ difíciles | 30% | Retrasa Med. 2 | Morningstar-Peardon como referencia |
| C_OT ≈ 0 | 25% | Paper 2 nulo | Publicable como resultado negativo |
| Correlador Q² sin plateau | 40% | Paper 3 débil | Estudio de viabilidad |
| **Bonanno mide g₂(SU(2)) primero** | **15%** ⚠️ | Reduce novedad Paper 1 | Priorizar Paper 2 (sin competencia); framing diferente para Paper 1 (Aoki-Fukaya vs θ imaginario) |
| β=2.6 tiene topología congelada | 10% | Bloquea segundo β | SU(2) congela mucho menos que SU(3); Berg-Clarke midieron hasta β=2.928 |

---

## 11. Checklist de inicio inmediato

```
ESTA SEMANA:
□ Terminar las 1000 configs (faltan ~100)
□ Diagnóstico ⟨Q²⟩ = 3.4
    □ Histograma de Q crudo
    □ Verificar normalización q(x) para SU(2)
    □ Verificar volumen en el código
    □ t_flow = 0.5, 1.0, 2.0, 3.0

SEMANA 2:
□ Fix del bug de Q
□ Verificar ⟨Q²⟩ = 30-40 con 1000 configs corregidas
□ Empezar generación de 19,000 configs adicionales

SEMANA 3-4:
□ Mientras genera: implementar operadores 0⁻⁺
□ Implementar GEVP solver con tests
□ Crear estructura de directorios src/

SEMANA 5+:
□ Setup para β=2.6 (preparar scripts)
□ Paper 2 es la prioridad — todo lo demás es secundario
```

---

## 12. Resumen ejecutivo para presentaciones

> Medimos por primera vez cómo la densidad de carga topológica q(x) se acopla al espectro de gluebolas de SU(2) mediante un GEVP mixto que combina operadores convencionales con operadores topológicos. Complementamos con la primera medición de m₂(SU(2)) — el coeficiente de θ-dependencia de la masa del glueball (notación de Bonanno et al. 2024) — a dos espaciados de red. En SU(3), m₂ = −0.0083(23) en el continuo con artefactos de discretización de factor ~7 (Bonanno+ 2024). Para SU(2) no existe medición. Los datos de b₂(SU(2)) (Kitano+ 2021, Hirasawa+ 2024) sugieren posibles desviaciones del escalamiento 1/N², haciendo esta la teoría gauge donde la θ-dependencia del espectro podría ser más detectable.
