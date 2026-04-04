# Verificación Exhaustiva: Plan_Investigacion_v2_Corregido.md

**Versión 3 — Incluye corrección de confusión notacional g₂/m₂ entre Del Debbio y Bonanno**  
**Fecha de verificación**: 2026-04-03  
**Método**: Búsqueda sistemática en arXiv, INSPIRE-HEP, y journals; cálculos independientes de consistencia interna.

---

## A. ERRORES ENCONTRADOS

### A1. Valores de b₂ para SU(2) — ERROR CRÍTICO (afecta la motivación central)

**El plan dice**: "Hirasawa et al. (JHEP 07, 198, 2024) midieron b₂ ≈ −0.15 a −0.2 para SU(2), unas 6–8 veces mayor en valor absoluto que b₂ ≈ −0.023(7) de SU(3)."

**Realidad**: Hirasawa et al. (arXiv:2403.10767, JHEP 07, 198, 2024) reportan:
- b₂ ≈ −0.023(7) en la **fase confinada** (T < 0.95 T_c)
- b₂ ≈ −0.083 (≈ −1/12) en la **fase deconfinada**
- **Ningún valor en el rango −0.15 a −0.2 aparece en el paper.**

Kitano, Yamada y Yamazaki (JHEP 02, 073, 2021) obtuvieron b₂ = −0.049(20) para SU(2) en el límite continuo.

**Consecuencia**: La motivación central del plan — que SU(2) tiene una dependencia en θ "6–8 veces mayor" que SU(3) — se basa en un número incorrecto. Con b₂(SU(2)) ≈ −0.023 a −0.049, la "anomalía" de SU(2) es mucho más modesta (factor ~1–2× respecto a SU(3), no 6–8×). La estimación de |g₂(SU(2))| ~ 0.4–0.5 se infla correspondientemente.

---

### A2. Confusión notacional g₂/m₂ entre Del Debbio y Bonanno — ERROR CRÍTICO ⚠️ CORREGIDO EN v3

**El plan dice**: g₂(SU(3)) = −0.06(2), citando Del Debbio et al. (2006), y usa este valor como referencia para estimar g₂(SU(2)).

**Realidad — CONFUSIÓN NOTACIONAL**: Del Debbio y Bonanno usan "g₂" para cantidades **diferentes**:

| Cantidad física | Del Debbio (2006) la llama | Bonanno (2024) la llama |
|----------------|---------------------------|------------------------|
| M(θ) = M(1 + _·θ² + ...) — **masa** | **g₂** = −0.06(2) a β=6.0 | **m₂** = −0.0083(23) continuo |
| σ(θ) = σ(1 + _·θ² + ...) — **string tension** | s₂ = −0.08(1) a β=6.0 | s₂ = −0.0258(14) continuo |
| M/√σ(θ) = M/√σ(1 + _·θ² + ...) — **ratio** | (no definido) | **g₂** = 0.0046(24) continuo |

Relación: g₂(Bonanno) = m₂ − s₂/2

**La verificación v2 (nuestra anterior) decía "g₂ ≈ 0 en el continuo"** — esto era correcto para el **ratio** M/√σ pero INCORRECTO para la **masa**. El coeficiente de la masa es m₂ = −0.0083(23), distinto de cero a ~3.6σ. La masa del glueball SÍ depende de θ en el continuo.

**Fuente**: Bonanno et al., arXiv:2402.03096, Eq. (23) y Tabla 3.

**Consecuencias (revisadas)**:
1. La señal física EXISTE: m₂(SU(3)) = −0.0083(23) ≠ 0 en el continuo.
2. Los artefactos de discretización son grandes: Del Debbio a β=6.0 obtuvo −0.06, el continuo es −0.008, un factor ~7 de reducción.
3. Se siguen necesitando **al menos dos valores de β** porque los artefactos son dominantes a un solo β.
4. La señal esperada para SU(2) a un solo β será una mezcla de física + artefactos, pero la componente física NO es cero.
5. La estimación de significancia debe considerar que m₂ a espaciado finito es ~0.03–0.08, no los 0.003–0.007 que sugeríamos en la v2.

---

### A3. s₂ de Bonanno et al. (2024) — ERROR NUMÉRICO IMPORTANTE

**El plan dice**: "Bonanno, Bonati, Papace y Vadacchino (JHEP 05, 163, 2024; arXiv:2402.03096) obtuvieron s₂ = −0.0523(45) para SU(3)."

**Realidad**: El valor extrapolado al continuo es **s₂ = −0.0258(14)**, aproximadamente la mitad del valor citado.

---

### A4. Valores de gluebolas de Athenodorou-Teper (2021) — ERRORES EN MASAS

**El plan dice** (Sección 2.1, tabla de valores del continuo):

| Estado | Plan dice | Athenodorou-Teper dice realmente |
|--------|-----------|----------------------------------|
| **SU(2) 0⁺** | 3.74(5) | **3.781(23)** |
| **SU(2) 0⁻** | 5.8(2) | **6.017(61)** |
| SU(2) 2⁺ | 5.5(1) | ~5.35(2) (aproximado) |
| SU(3) 0⁺⁺ | 3.441(48) | **3.405(21)** |
| SU(3) 2⁺⁺ | 5.028(52) | **4.894(22)** |
| SU(3) 0⁻⁺ | 5.540(67) | **5.276(45)** |

Los valores de SU(3) están sistemáticamente inflados. Los de SU(2) tienen discrepancias significativas (especialmente 0⁻: 5.8 vs 6.0). Los valores citados podrían provenir de un paper anterior (Lucini, Rago, Rinaldi 2010 o Chen et al. 2006), no de Athenodorou-Teper (2021).

---

### A5. Valores de Del Debbio et al. (2006) — ERRORES EN TABLA SU(4) y SU(6)

**El plan dice**: g₂(SU(4)) = −0.034(18); s₂(SU(4)) = −0.050(10); s₂(SU(6)) = −0.025(12).

**Realidad**:
- g₂(SU(4)) = **−0.04(3)** (no −0.034(18))
- s₂(SU(4)) = **−0.057(10)** (no −0.050(10))
- s₂(SU(6)) = −0.025(**5**) (valor central correcto, incertidumbre incorrecta: 5, no 12)

---

### A6. ⟨Q²⟩ para volúmenes pequeños (Sección 5.2) — TODOS INCORRECTOS

Usando χ_lat = 5.05 × 10⁻⁵ (derivado de los propios parámetros del plan y verificado como correcto para 24³×48 → ⟨Q²⟩ ≈ 34):

| Lattice | Volumen | ⟨Q²⟩ calculado | ⟨Q²⟩ del plan | Factor de error |
|---------|---------|----------------|---------------|-----------------|
| 12³×24 | 41,472 | **2.1** | ~5 | 2.4× |
| 14³×28 | 76,832 | **3.9** | ~10 | 2.6× |
| 16³×32 | 131,072 | **6.6** | ~16 | 2.4× |
| 20³×40 | 320,000 | **16.2** | ~50 | 3.1× |

---

### A7. Poblaciones de bins (Sección 3.1) — INCORRECTAS

Para una distribución gaussiana con σ_Q = √34 ≈ 5.83 y 1000 configuraciones:

| Bin | Rango |Q| | Plan dice | Cálculo correcto |
|-----|---------|-----------|------------------|
| A | 0 | ~70 | ~68 (OK) |
| B | 1–2 | ~130 | **~264** |
| C | 3–5 | ~200 | **~323** |
| D | 6–8 | ~250 | **~201** |
| E | ≥9 | ~350 | **~144** |

---

### A8. Autores de Dromard et al. (arXiv:1505.03435 y 1510.08809) — INCORRECTOS

**El plan dice**: "Dromard, Czaban, García Vera, Molnár, Münster y Wagner"

**Realidad**: Los autores son **Dromard, Bietenholz, Gerber, Mejía-Díaz y Wagner**.

---

### A9. Dürr (2025) — χ_t^{1/4} valor incorrecto y co-autor omitido

**El plan dice**: χ_t^{1/4} = 198.1(0.7)(2.7) MeV, atribuido a "Dürr (2025)".

**Realidad**: El valor es **197.8(0.7)(2.7) MeV**, y el paper es de **Dürr y Fuwa** (arXiv:2501.08217).

---

### A10. Berg, Clarke (2017) — Journal incorrecto

**El plan cita**: Berg, Clarke — Phys. Rev. D 95, 094508 (2017); arXiv:1708.08408

**Realidad**: Publicado en **EPJ Web Conf. 175, 10007 (2018)**, no en Phys. Rev. D 95.

---

### A11. Barca et al. (2024) — Autor omitido

Falta **Sofie Martins** como tercer autor. El paper tiene 6 autores, no 5.

---

### A12. Masas am en Sección 5.3 — Valores de entrada erróneos

Con los valores correctos de Athenodorou-Teper:
- 0⁺: am = 3.781 × 0.190 = 0.718 (plan dice 0.71)
- 0⁻: am = 6.017 × 0.190 = 1.143 (plan dice 1.10)

---

### A13. Significancias 14–28σ — SOBREESTIMADAS ⚠️ ACTUALIZADO EN v3

**El plan de ejecución v1 estimaba**: ~14σ (g₂=0.06) a ~28σ (g₂=0.12) con 20,000 configs.

**Problemas con esta estimación**:
1. **Ignora sistemáticos del GEVP**: elección de t₀, rango del plateau, contaminación de estados excitados. Ref: Blossier et al. (JHEP 04, 094, 2009; arXiv:0902.1265).
2. **Ignora correlaciones entre bins**: configs en bins adyacentes comparten fluctuaciones del ensamble.
3. **Los artefactos de discretización dominan a un solo β**: en SU(3), m₂ (coeficiente de masa, que es lo que medimos) pasa de ~−0.06 a espaciado finito a −0.0083 en el continuo — factor ~7 de reducción.

**Estimación revisada (v3)**: A un solo β, m₂ a espaciado finito es ~0.03–0.08. Con 20,000 configs la significancia sería **~5–10σ a un solo β**. Tras extrapolación al continuo con dos β, el resultado se reduciría a **~2–5σ** dependiendo de la magnitud de los artefactos. La v2 de esta verificación subestimaba la señal porque confundía g₂(Bonanno) = ratio ≈ 0 con m₂ = masa ≠ 0.

### A14. Autovectores del GEVP tienen artefactos O(a²) ⚠️ NUEVO EN v3

Los overlap ratios propuestos como observable principal de la Medición 2 **no son automáticamente libres de artefactos de discretización**. Blossier et al. (JHEP 04, 094, 2009) muestran que los autovectores del GEVP heredan los artefactos O(a²) de cada operador en la base. Además, el operador q(x) definido vía gradient flow tiene efectos O(a²/t_flow) adicionales (Cè et al., PLB 762, 2016).

**Consecuencia**: Un solo β es suficiente para un **paper metodológico** ("demostramos que q(x) funciona en un GEVP de gluebolas") pero NO para claims cuantitativos sobre overlap ratios como cantidades físicas. Un referee probablemente aceptará Paper 2 con caveats apropiados, pero rechazará claims fuertes sin un segundo espaciado.

---

## B. VERIFICADO CORRECTO

### B1. Citas verificadas correctamente
- **Del Debbio et al. (2006)**: Autores, journal (JHEP 06, 005, 2006), arXiv (hep-th/0603041) correctos. g₂(SU(3)) = −0.06(2) a β=6.0 correcto (pero es espaciado finito — ver A2).
- **Bonanno et al. (2024)**: Autores, journal (JHEP 05, 163, 2024), arXiv (2402.03096) correctos.
- **Kitano, Yamada, Yamazaki (2021)**: Todo correcto. JHEP 02, 073 (2021); arXiv:2010.08810.
- **Berg, Clarke (2018)**: Phys. Rev. D 97, 054506 (2018); arXiv:1710.09474. χ^{1/4}/T_c = 0.643(12) correcto.
- **Fingberg, Heller, Karsch (1993)**: Nucl. Phys. B 392, 493 (1993). T_c/√σ = 0.69(2) correcto.
- **Abbott et al. (2026)**: Phys. Rev. Lett. 136, 041901; arXiv:2508.21821. Radio de masa 0.263(31) fm correcto.
- **BESIII (2024)**: Phys. Rev. Lett. 132, 181901. J^PC = 0⁻⁺, M = 2395 ± 11 MeV (stat) correcto.
- **Matchev, Verner (2025)**: Phys. Rev. D 112, 113009 y 113010; arXiv:2505.05607 y 2505.05608. E_sph ≈ 9.1 TeV correcto.
- **D'Onofrio, Rummukainen, Tranberg (2014)**: Phys. Rev. Lett. 113, 141602. T* = (131.7 ± 2.3) GeV y T_c = (159 ± 1) GeV correctos.
- **Brennan, Wang, Xiao (2024)**: arXiv:2412.14239. Contenido correcto.
- **Csáki et al. (2024)**: JHEP 11, 165; arXiv:2406.13738. Contenido correcto.
- **Tanizaki, Tomiya, Watanabe (2025)**: JHEP 04, 123; arXiv:2411.14812. Contenido correcto.
- **Morningstar (2025)**: arXiv:2502.02547. Review plenario Lattice 2024, contenido correcto.
- **Athenodorou, Teper (2021)**: Cita bibliográfica correcta — los errores son en los valores numéricos extraídos.

### B2. Valores numéricos verificados
- **⟨Q²⟩ ≈ 34 para 24³×48**: Correcto. Cálculo independiente da 33.5.
- **a ≈ 0.085 fm a β=2.5**: Correcto.
- **a√σ ≈ 0.190 a β=2.5**: Valor estándar, correcto.
- **χ^{1/4} ~ 195(10) MeV para SU(2)**: Correcto.

### B3. Claims de novedad — TODOS VERIFICADOS COMO CORRECTOS
1. **"Nadie ha medido masas de gluebolas por sector topológico Q"** — Confirmado. Búsqueda exhaustiva.
2. **"q(x) nunca ha sido incluido en un GEVP de gluebolas"** — Confirmado.
3. **"El correlador Q²(t)Q²(0) como herramienta espectroscópica no tiene precedente"** — Confirmado.
4. **"g₂ nunca ha sido medido para SU(2)"** — Confirmado (ni a espaciado finito ni en el continuo).

### B4. Competencia verificada ⚠️ NUEVO
- **arXiv:2601.20708** (Bonanno et al., enero 2026): Existe. "A scalable flow-based approach to mitigate topological freezing." Es sobre métodos (Stochastic Normalizing Flows en SU(3)), no mide g₂ ni trabaja con SU(2). Amenaza indirecta, no directa.
- **Bonanno ganó el Wilson Award 2025** por trabajo en topología. Es la referencia mundial en θ-dependencia.
- **No se encontró ningún paper de Bonanno sobre g₂(SU(2))** a abril 2026. La ventana sigue abierta.

### B5. Sección 1.5 (sphalerons, Rubakov-Callan, skyrmiones)
Las citas individuales son correctas. Sin embargo, esta sección es motivación contextual — no conecta operativamente con ninguna de las tres mediciones propuestas.

---

## C. NO VERIFICABLE

### C1. Sun et al./CLQCD (2018) — Interpretación parcialmente verificable
El plan dice que q(x) "se acopla preferentemente a la η′ (~1 GeV)." El paper sí muestra acoplamiento diferenciado, pero la identificación del estado ligero como η′ es interpretación del plan. El paper lo llama "flavor singlet qq̄ meson".

### C2. Dromard et al. (2015) — Medición del potencial estático
Los arXiv IDs citados (1505.03435 y 1510.08809) tienen autores incorrectos (ver A8) y sus abstracts no confirman V_{qq̄}(r) en sectores |Q| = 0–4 a β = 2.5.

### C3. Número de operadores en Barca et al. (2024)
175 operadores (35 × 5) confirmado, pero "por canal" vs "total" no verificado.

### C4. m₂ vs b₂ — Justificación física (CORREGIDO en v3)
Con la notación correcta: m₂(SU(3)) = −0.0083(23) en el continuo, b₂(SU(3)) ≈ −0.023. El ratio m₂/b₂ ≈ 0.36 en el continuo. Para SU(2) con b₂ ≈ −0.023(7), la extrapolación m₂(SU(2)) ~ 0.36 × (−0.023) ≈ −0.008 es posible pero especulativa. Si SU(2) viola el escalamiento 1/N², m₂ podría ser significativamente mayor. **La estimación no puede ser cuantitativa sin datos.**

### C5. Discrepancia ⟨Q²⟩ = 3.4 en datos preliminares
Causas más probables: (1) gradient flow insuficiente, (2) error de normalización en q(x), (3) confusión de volumen (⟨Q²⟩ = 3.4 ≈ lo esperado para 16⁴). No verificable sin acceso al código.

### C6. Varios papers menores
Polyakov-Shmatikov (1996), Halasz-Amado (2000), Sommermann et al. (1992), Choi-Lam-Shao (2022), Dumitrescu-Hsin (2024): no verificados en detalle.

---

## Resumen de severidad

| Categoría | Cuenta | Items |
|-----------|--------|-------|
| **Errores críticos** (afectan motivación/diseño) | 4 | A1 (b₂ incorrecto), A2 (confusión g₂/m₂), A13 (significancias infladas), A14 (overlap ratios no son a-independientes) |
| **Errores numéricos significativos** | 3 | A3 (s₂), A4 (masas gluebolas), A6 (⟨Q²⟩ volúmenes) |
| **Errores menores** (citas, autores) | 6 | A5, A7, A8, A9, A10, A11, A12 |
| **Verificado correcto** | ~25 items | B1–B5 |
| **No verificable** | 6 items | C1–C6 |

### Cambio principal respecto a la verificación v1

Los hallazgos clave de esta verificación v3:

1. **La confusión notacional g₂/m₂** (Error A2) obligó a revisar las conclusiones de la v2. La masa del glueball SÍ depende de θ (m₂ ≠ 0), pero los artefactos de discretización son grandes (factor ~7 entre β finito y continuo).
2. **Se necesitan al menos dos β** para separar señal física de artefactos — esto no cambió.
3. **La Medición 2 sigue siendo la prioridad**, pero por razones parcialmente diferentes: no porque "la señal de m₂ podría ser cero" (sí hay señal), sino porque Paper 2 es más novedoso, tiene menos competencia, y puede enmarcarse como paper metodológico sin necesidad estricta de continuum limit (aunque los overlap ratios SÍ tienen artefactos O(a²) — ver A14).
4. **Las significancias se revisan al alza** respecto a la v2 (~5–10σ a un β, no 3–8σ), pero siguen por debajo de las 14–28σ originales.
5. **El framing de Paper 1** debe ser: "primera medición de m₂(SU(2)) con dos espaciados", usando la notación de Bonanno para evitar confusión.
