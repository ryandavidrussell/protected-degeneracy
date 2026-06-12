# protected-degeneracy

Pre-registered computational study of equivariant commutant stability,
McKay mixing, and deformation-space loop structure in the 600-cell Dirac geometry.
Companion structural correspondence with the Kaleidoworks compact holonomy
phase-locking audit (E₈×E₈ heterotic SUGRA).

---

## Repository layout

```
oracle/
  mckay_bootstrap.py      Bootstrap oracle: derives SL(2,5) character table and
                          affine Ẽ₈ McKay graph from first principles. No hardcoding.
                          Raises McKayHardStop on any integrality drift or graph mismatch.
                          Verified standalone — runs independently of the MOX-1 instrument.

  mckay_mixing.py         Extended oracle: character table + Ẽ₈ verification +
                          per-class projection utilities used by the bootstrap suite.

mox1/
  mox1_instrument.py      MOX-1 run instrument: isotypic projectors, M_rho_sigma,
                          M-hat (dimension-matched normalization), Q1, Q2, C(V),
                          JSON emission. Runs against H.npz / dirs.npz.
                          class_ids column-order: [1a,2a,3a,4a,5a,10a,5b,10b,6a]

  mox1_preflight.py       Artifact inspector. Run before mox1_instrument.py:
                          checks H.npz / dirs.npz key inventory, shape consistency,
                          and column-order contract for class_ids.

  MOX1_prereg.pdf         Frozen preregistration (MOX-1). Four design decisions
                          documented: D4 (F-control trap), block-size normalization,
                          H-A/H-B firewall, derived edge set.

loop/
  PREREGISTRATION_loop.md Frozen loop-experiment preregistration. Locked observable,
                          anchors, three loop pairs, four-outcome decision matrix,
                          falsification commitments.

  finalize_loop_report.py Mechanical bracket-closer. Reads loop_results.npz, recomputes
                          all metrics from raw arrays per prereg definitions, runs
                          consistency gate against frozen report assertions, substitutes
                          exact stored-precision values, generates cartesian figure.
                          Aborts with exit 2 on any contradiction — nothing written.

  LOOP_VERIFICATION_REPORT.md
                          Frozen loop verdict (PHASE-BOUNDARIES). Bracketed metric
                          values pending loop_results.npz substitution via finalizer.
                          Contains propagation-event record and registered taxonomy gap.

papers/
  protected_degeneracy_v1.1.md
                          PRIMARY DOCUMENT. Structural correspondence white paper.
                          Draft v1.1, June 2026. Brackets in §4.1 pending loop_results.npz.

  600cell_arXiv_v1.pdf    Equivariant Commutant Stability of Sparse Deformations in
                          the 600-Cell Dirac Geometry — preprint v1.0, June 2026.

  holonomy_whitepaper_v2.2.pdf
                          Compact Holonomy Phase-Locking in E₈×E₈ Heterotic Corridors
                          — Kaleidoworks technical white paper v2.2, June 2026.

test_data/
  loop_results_test.npz   Synthetic clean data (cardinal spikes, n_jumps=4 per loop).
                          Used to verify finalizer positive control.

  loop_results_tampered.npz
                          Synthetic tampered data (interior jump at pair (4,5) on AF).
                          Used to verify finalizer negative control (gate fires, exit 2).
```

---

## Blocked / pending

| Awaiting | Unblocks |
|---|---|
| `loop_results.npz` | Bracket substitution in LOOP_VERIFICATION_REPORT.md; cartesian figure; `[clust_F]` provenance |
| `H.npz` + `dirs.npz` | MOX-1 run (mox1_instrument.py) |

Run checklist once files arrive:
```bash
# Step 1: preflight
python mox1/mox1_preflight.py H.npz dirs.npz

# Step 2: MOX-1 run
python mox1/mox1_instrument.py H.npz dirs.npz --out mox1_results.json

# Step 3: loop finalization
python loop/finalize_loop_report.py loop_results.npz \
    loop/LOOP_VERIFICATION_REPORT.md \
    --out-report loop/LOOP_VERIFICATION_REPORT_FINAL.md \
    --out-figure loop/loop_combined_cartesian.png
```

---

## Naming-collision note

`oracle/mckay_bootstrap.py` and `mox1/mox1_instrument.py` are the current names.
Original filenames were `mckay-mixing.py` and `mckay_mixing.py` (one character apart).
They have been renamed here. Update MANIFEST.json and recompute hashes after any further rename.

---

## Pinned rules

1. **Never** pass `class_ids` generated under one CHI column order into projectors
   using the other CHI column order.
   - `oracle/mckay_bootstrap.py` column order: `[1, 2, 3, 4, 5a, 5b, 6, 10a, 10b]`
   - `mox1/mox1_instrument.py` column order: `[1a, 2a, 3a, 4a, 5a, 10a, 5b, 10b, 6a]`

2. Verdicts are read from `.npz` numbers, never from figures or narrative summaries
   of figures.

3. Instruments move as files with hashes. Hashes are computed where the instrument
   runs. A hash that traveled through a chat window certifies nothing.

---

## Citation

Russell, R.D. (2026). *Protected Degeneracy: A Structural Correspondence Between
Finite Spectral Geometry and Heterotic SUGRA*. Draft v1.1.

Russell, R.D. (2026). *Equivariant Commutant Stability of Sparse Deformations in
the 600-Cell Dirac Geometry*. Preprint v1.0.

Kaleidoworks (2026). *Compact Holonomy Phase-Locking in E₈×E₈ Heterotic Corridors*.
Technical White Paper v2.2.
