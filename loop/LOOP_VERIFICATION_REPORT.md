# LOOP_VERIFICATION_REPORT.md
**Experiment:** Deformation-space loop test (monodromy)  
**Preregistration:** PREREGISTRATION_loop.md (locked 2026-06-06)  
**Status:** FROZEN VERDICT — brackets pending loop_results.npz substitution

---

## Verdict: PHASE-BOUNDARIES

The four-outcome decision tree (§6 of prereg) applied as registered.

| Loop | ret = \|O(2π)−O(0)\| | Δmax | n_jumps |
|---|---|---|---|
| AF | [ret_AF] | 0.699 | 4 |
| AG | [ret_AG] | 0.935 | 4 |
| FG | [ret_FG] | 0.291 | 4 |

MONODROMY does not fire: O(2π) and O(0) agree at displayed precision at all cardinal values
(0.9520, 0.3085, 0.0170 — anchors verified against boundary_results.npz). Exact ret values
are bracketed pending loop_results.npz substitution via finalize_loop_report.py.

PHASE-BOUNDARIES fires: n_jumps = 4 ≥ 1 on every loop.

**Verdict: PHASE-BOUNDARIES.**

---

## Jump localization

All four jumps on every loop are adjacent to θ = 0, π, 2π — the pure-first-anchor cardinal
points where sin θ vanishes. There are no interior phase boundaries.

The cos θ-vanishing points (θ = π/2, 3π/2) produce no jumps on any loop.

---

## Non-convexity of protective properties

V_A's protection derives from sparsity (sparse-commutator on the 24-cell subset).
V_F's protection derives from equivariance (Reynolds projection to 10⁻¹⁴).
The combination cos θ·V_A + sin θ·V_F has neither.

Plateau anomaly on loop AF: O(θ) ≈ 0.25–0.28 on the plateau sits below both anchor values
(0.952 and 0.308), even though ‖V(θ)‖ < 1 off-cardinal.

The protective directions are measure-zero rays in deformation space.

---

## Registered taxonomy gap

PHASE-BOUNDARIES was written to mean "regions of deformation space separated by walls."
The data triggered the criterion via cardinal spikes at isolated rays, with a uniform collapsed
plateau between them. The A-stratum and F-stratum are isolated rays (measure zero in the
loop). This is recorded as a limitation of the registered taxonomy, not relabeled post hoc.

---

## Open question: EV_TOL scaling

Jump location is coupled to EV_TOL = 10⁻⁴. Whether the sharpness is structural or
resolution-set must be the subject of a new preregistration.

---

## Propagation-event record

One propagation event occurred during preparation of this report: the figure caption in an
early draft described interior jumps that were not present in the data. The error was caught
before the caption entered any frozen document. Recorded here per the program's
propagation-tracking discipline.

---

## Finalization instruction

Run:
```bash
python loop/finalize_loop_report.py loop_results.npz \
    loop/LOOP_VERIFICATION_REPORT.md \
    --out-report loop/LOOP_VERIFICATION_REPORT_FINAL.md \
    --out-figure loop/loop_combined_cartesian.png
```
The finalizer substitutes exact values for [ret_AF], [ret_AG], [ret_FG] and generates the
cartesian figure. It aborts with exit 2 on any consistency failure.
