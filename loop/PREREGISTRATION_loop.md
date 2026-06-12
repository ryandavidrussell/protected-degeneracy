# PRE-REGISTRATION — Deformation-space loop test (monodromy)

**Date:** 2026-06-06  
**Status:** FROZEN — do not modify after this date

---

## 1. Motivation

The boundary-test program established that three anchor deformations (A, F, G) of the 600-cell
Dirac operator preserve qualitatively different amounts of the 2I-equivariant commutant:

- V_A (sparse, 24-cell support): S ≈ 0.952 × 3138 ≈ 2987
- V_F (fully Reynolds-projected equivariant): S ≈ 0.308 × 3138 ≈ 968
- V_G (generic non-equivariant random): S ≈ 0.017 × 3138 ≈ 53

This experiment traces closed loops in deformation space between pairs of anchors and asks
whether the commutant score O(θ) = S(D(0.5,θ)²)/3138 is single-valued (no monodromy),
and whether there are phase boundaries between qualitatively distinct deformation regimes.

---

## 2. Observable

For anchor pair (X, Y) and interpolation parameter θ ∈ [0, 2π]:

    D(χ, θ) = D₀ + χ·(cos θ · V_X + sin θ · V_Y)

with χ = 0.5 fixed throughout. The observable is:

    O(θ) = S(D(0.5, θ)²) / 3138

where S(Δ) = dim Comm_{2I}(Δ). Grid: 32 equally-spaced θ values in [0, 2π).

---

## 3. Anchor definitions (frozen)

- V_A: sparse deformation on the 24-cell vertex subset of the 600-cell. Boundary-test anchor A.
- V_F: Reynolds projection of a fixed Gaussian random matrix to the 2I-equivariant subspace.
  Equivariance verified to machine precision (‖V_F - Reynolds(V_F)‖ < 10⁻¹⁴).
- V_G: a fixed Gaussian random matrix with no equivariance enforcement.

Anchor values (from boundary_results.npz, verified before loop runs):
- O_A = 0.9520
- O_F = 0.3085
- O_G = 0.0170

---

## 4. Three loop pairs

Loop AF: X = A, Y = F  
Loop AG: X = A, Y = G  
Loop FG: X = F, Y = G

---

## 5. Eigenvalue clustering

Spectral commutant S(Δ) is computed by clustering eigenvalues of Δ with tolerance
EV_TOL = 10⁻⁴ and counting 2I-equivariant block structure. This tolerance is fixed for the
primary run. EV_TOL sensitivity is an open question (see §9).

---

## 6. Pre-specified outcomes (four-way decision tree)

Applied in order. First matching condition determines the verdict.

**MONODROMY:** ret = |O(2π) − O(0)| > 0.05 on any loop.  
→ The observable is not single-valued; the loop detects a discontinuity.

**PHASE-BOUNDARIES:** ret ≤ 0.05 on all loops AND n_jumps ≥ 1 on any loop,  
where a jump is defined as |O(θ_{i+1}) − O(θ_i)| > 0.10.  
→ The observable is single-valued but has sharp transitions between regimes.

**SMOOTH:** ret ≤ 0.05 on all loops AND n_jumps = 0 on all loops  
AND max_i |O(θ_i) − O_interp(θ_i)| < 0.05 (smooth interpolation within 5%).  
→ Commutant varies smoothly between anchor values with no phase structure.

**FLAT-COLLAPSE:** ret ≤ 0.05 on all loops AND n_jumps = 0 on all loops  
AND the plateau value O_plateau satisfies O_plateau < min(O_X, O_Y) − 0.05 for any loop.  
→ The mixed deformation collapses the commutant below both anchors everywhere.

---

## 7. Falsification commitments

- The verdict is determined by the above decision tree applied to loop_results.npz.
- No post-hoc relabeling of outcomes is permitted.
- If the data triggers PHASE-BOUNDARIES, the jump locations must be reported and interpreted
  without claiming they reflect a genuine phase transition until EV_TOL scaling is checked.
- If the data triggers MONODROMY, the paper must report this as evidence of a discontinuity
  and not reframe it as a boundary.

---

## 8. Finalization procedure

finalize_loop_report.py reads loop_results.npz, recomputes all metrics from raw arrays,
runs a consistency gate against the frozen assertions in LOOP_VERIFICATION_REPORT.md,
and substitutes exact values for bracketed placeholders. It aborts with exit code 2 if any
consistency check fails — nothing is written on failure.

---

## 9. Open questions (not resolved by this experiment)

- EV_TOL scaling: does jump position scale with tolerance or is it stable? The two outcomes
  (measurement-resolution edge vs. genuine fragility threshold with extractable width) must
  be distinguished by a new preregistration.
- Whether the θ → θ + π symmetry of O(θ) has a structural explanation (unitary intertwiner).
