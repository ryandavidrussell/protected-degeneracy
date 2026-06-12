# Protected Degeneracy: A Structural Correspondence Between Finite Spectral Geometry and Heterotic SUGRA

**Ryan David Russell / Kaleidoworks**
*Draft v1.1 — June 2026 (revised; see Appendix A for the change record)*

---

## Abstract

Two independent research programs — a pre-registered computational study of equivariant
spectral commutants in the 600-cell Dirac geometry, and a formal compatibility audit of
compact holonomy phase-locking in E₈×E₈ heterotic SUGRA — converge on the same structural
question: which deformations preserve a protected degeneracy structure, and what invariant
predicts it? We exhibit a structural dictionary between the two programs — line-by-line in form,
heuristic in epistemic status — and show that the SUGRA contamination analysis furnishes a
close analytic analogue of the 600-cell's representation-stability conjecture in a two-sector
system. Whether the analogue is a literal instance of the conjecture's mixing-matrix predictor is
posed as an explicit open construction problem (§7), and a McKay-bridge experiment —
re-indexing the cross-isotypic mixing matrix M_ρσ by affine Ẽ₈ node order — is identified as the
test that would connect the two programs on structural rather than analogical grounds. We also
report results from three pre-registered loop experiments in the 600-cell deformation space,
whose PHASE-BOUNDARIES verdict with the precise localization structure (cardinal-only spikes,
no interior walls) is interpreted as geometric evidence that the protective properties of
structured deformations are non-convex: the protected directions are measure-zero rays, and
any admixture is destructive.

**What this paper is not.** It does not claim that the 600-cell realizes a physical theory. It does
not claim that the SUGRA mechanism is correct. It does not close the seam between formal
correspondence and ontological claims. The defensible content is algebraic, computational, and
structural.

---

## 1. The Two Programs

### 1.1 The 600-Cell Spectral Geometry

Let K denote the boundary complex of the regular 600-cell. The face vector is
f(K) = (120, 720, 1200, 600), giving a graded cochain Hilbert space
H = ⊕_{p=0}^{3} C^p(K) with dim H = 2640. The Kähler–Dirac operator is D₀ = d + d†,
and the central observable is the dimension of the 2I-equivariant spectral commutant

    S(Δ) = dim Comm_{2I}(Δ) = dim{ T ∈ End(H) : [T,Δ] = 0, [T,U_g] = 0 ∀ g ∈ 2I }.

The undeformed geometry has S(Δ₀) = 3138. For a deformation D_V(χ) = D₀ + χV, the central
empirical object is S_V(χ) = S(D_V(χ)²).

The program began with conjectures about golden-ratio spectral towers, dimensional flow, and
compactified scale dimensions. Those conjectures were tested and mostly failed. What survives
is narrower and more useful: sparse commutator-type deformations preserve a large fraction of
the 2I-equivariant commutant, while denser random and generic non-equivariant perturbations
collapse it. At χ = 0.5, subgroup-coded sparse deformations satisfy S ∈ [2976, 3078]; a fully
Reynolds-projected equivariant random deformation drops to 968; a generic non-equivariant
random deformation drops to approximately 53.

The boundary test falsified the subgroup-rigidity reading: random non-subgroup sparse
supports of comparable size also preserve the commutant nearly as well. The locality predictor
experiment found that graph statistics do not generalize across deformation families
(held-out R² ≈ −2299). The surviving conjecture is representation-theoretic:

**Conjecture 1** (Representation Stability). The commutant score S(Δ_V(χ)) is controlled
primarily by preservation of isotypic multiplicity-space organization rather than by
graph-theoretic locality or subgroup order alone. A possible quantitative predictor is the
cross-isotypic mixing matrix

    M_ρσ(V) = ‖P_ρ V P_σ‖_F²,

where P_ρ projects onto the ρ-isotypic component of H.

### 1.2 The Heterotic SUGRA Audit

The compact holonomy phase-locking mechanism is a toy effective potential in which a single
locked phase combination Φ minimizes a two-sector cosine potential at a dynamically stabilized
compact radius. The potential takes the form

    V(α_A, α_B, ζ, R) = Λ⁴(R)[1 − cos Φ] + V_rad(R),
    Φ = n_A α_A − n_B α_B − κ_{AB} ζ + δ.

Twelve load-bearing walls are identified, classified by tier (structural T1, source-form T2,
kinetic T3), and checked explicitly. All twelve pass within their stated corridors.

The tier classification carries a critical asymmetry. T3 walls (kinetic) are never irreducible —
they are recoverable by basis change. T1 and T2 walls, when in the irreducible set, have no
compensating mechanism inside the present audit. The irreducible walls are W1, W2, W3, W5,
W6, W7. W2 (flat-direction exactness) carries the CC-isolation argument: it is the wall that
ensures the phase sector contributes exactly zero to V_eff at the locked minimum under A1.

Extension E1 audits the leading worldsheet-instanton correction as a two-channel structure.
The channel-1 dominance factor V₁/V₂ = 2t★ is a structural consequence of no-scale
violation, independent of A_C. The instanton corridor at benchmark is |A_C|/|W₀| ≲ 1.04 at
t★ = 5.

---

## 2. The Dictionary

The two programs are organized by the same schema: a protected degeneracy structure, a
family of deformations, and a candidate algebraic invariant that predicts survival. The
dictionary below is line-by-line in form and heuristic in status: a table of structural analogues,
not a functor. No entry is claimed as a theorem-level identification. The McKay-bridge
experiment (§5) is the test that would upgrade entries from analogy to shared structure; until it
runs, the dictionary's role is to organize questions, not to transfer results.

| 600-cell program | Heterotic SUGRA program (analogue) |
|---|---|
| S(χ): equivariant commutant dimension, central order parameter | Wall register: whether a protected degeneracy structure (locked phase, flat direction, portal zero) survives deformation |
| Sparse family E₁, …, E₂₄: one structured direction, corridor-bounded | E1 extension: one structured direction (leading instanton cosine in τ alone), corridor \|A_C\|/\|W₀\| ≲ 1.04 |
| D and G controls: failure mode — generic random direction collapses commutant | W1 failure mode: a second independent phase combination enters; W3 failure mode: uncontrolled tadpole |
| F control: exactly equivariant, still collapses to 968 | T3 lesson: symmetry-type membership certifies labels, not protection (see caveat below) |
| Multiplicity-space clustering carries S(χ) | W2 carries CC-isolation: flatness in orthogonal directions is algebraic, not kinematic |
| Conjecture 1: M_ρσ predicts stability | Wall-register audit: algebraic invariants (rank-one phase block, portal zero) predict which deformations preserve protection |

The F-control row is the sharpest entry, and the one most in need of a stated caveat. Exact
equivariance (Reynolds projection, enforcing isotypic block structure) preserves symmetry-type
membership yet collapses the commutant to 968, because the commutant is quadratic in
multiplicities, not in symmetry labels. This plays the role the tier hierarchy assigns to T3-grade
facts — certification without protection. The pairing holds at the level of lesson, not
classification: equivariance is a genuine symmetry property, not literally recoverable by basis
change, so the F ↔ T3 entry is an analogy about what fails to be load-bearing, not an
identification of categories.

With that caveat in place, the shared lesson is real, and both programs arrived at it
independently: **degeneracy organization, not symmetry, sits in the load-bearing position.**

---

## 3. The Contamination Analysis as a Structural Analogue of M_ρσ

The §4.5 contamination analysis of the holonomy white paper identifies two Φ-routes into the
locked sector:

- Channel-2 condensate cross with amplitude ~ 1/(2t★) ≈ 0.10 at benchmark
- Channel-1 condensate cross with amplitude ~ b₀/(3s★ + b₀) ≈ 0.087 at the A = B minimum

In Conjecture 1 language, these amplitudes play the role of off-diagonal entries of a 2×2 mixing
block between the (Φ, τ) sectors. The identification is structural, not literal. M_ρσ is defined
through isotypic projectors of a group representation on a Hilbert space; the (Φ, τ) directions of
the toy potential are field directions, and no group, representation, or projector realizing them
as isotypic components has been exhibited.

Accordingly: **the heterotic audit furnishes a close analytic analogue of the
representation-stability conjecture in a two-sector system — not a worked instance of it.**
For the analogue to become an instance, three things must be constructed: (i) a group G acting
on an identified state space of the model; (ii) isotypic projectors P_Φ, P_τ realizing the sector
split; (iii) a demonstration that the contamination amplitudes equal ‖P_ρ V P_σ‖_F² for the
relevant deformation V. None of the three is constructed here. The construction problem is
recorded in §7; if it succeeds, §3 upgrades; if it fails or is ruled out, the dictionary entry remains
an analogy and is still useful as one.

On the corridor bound: |A_C|/|W₀| ≲ 1.04 at t★ = 5 controls the off-diagonal mass induced in
the (τ, Φ) sector by the instanton correction — functionally parallel to bounding a mixing norm,
and the corridor successfully predicted that the instanton extension does not reopen any
audited wall. It is not a bound on the normalized M̂ in the registered sense: M̂'s normalization
is a 200-draw dimension-matched random ensemble, and the corridor has no analogous
normalization.

The channel-dominance parallel survives the demotion. The heat-kernel finding in the 600-cell
— structured directions concentrate drift in few irrep sectors — and the SUGRA
channel-dominance result — at t★ = 5, Channel 1 dominates by the factor 2t★ = 10, with the
leading instanton cosine in τ alone — both say the deformation preferentially loads one sector,
the locked direction. On the 600-cell side the sectors are irreps; on the SUGRA side, field
directions. That asymmetry is exactly what the §7 construction problem would resolve.

---

## 4. The Loop Experiment: Non-Convexity of Protective Properties

Three pre-registered loop experiments traced the equivariant commutant
O(θ) = S(D(0.5, θ)²)/3138 around closed paths

    D(0.5, θ) = D₀ + 0.5·(cos θ · V_X + sin θ · V_Y)

for the three pairs (AF), (AG), (FG) from the boundary-test anchors.

### 4.1 Verdict: PHASE-BOUNDARIES

The locked four-outcome decision tree applied as registered:

| Loop | ret = \|O(2π) − O(0)\| | Δmax | n_jumps |
|---|---|---|---|
| AF | [ret_AF] | 0.699 | 4 |
| AG | [ret_AG] | 0.935 | 4 |
| FG | [ret_FG] | 0.291 | 4 |

MONODROMY does not fire: O(2π) and O(0) agree at displayed precision at all cardinal values
(0.9520, 0.3085, 0.0170 — anchors verified against boundary_results.npz); exact ret values are
bracketed pending substitution. PHASE-BOUNDARIES fires: n_jumps = 4 ≥ 1 on every loop.
**Verdict: PHASE-BOUNDARIES.**

*Bracketed metric values to be substituted from loop_results.npz via finalize_loop_report.py
before this paper is finalized.*

### 4.2 Jump Localization and Non-Convexity

All four jumps on every loop are adjacent to θ = 0, π, 2π — the pure-first-anchor cardinal
points where sin θ vanishes. There are no interior phase boundaries.

The cos θ-vanishing points (θ = π/2, 3π/2) produce no jumps on any loop. This is informative:
spikes appear only where an anchor's protection level is large relative to the mixed plateau. V_F
at O = 0.308 sits within ~0.05 of the AF plateau (~0.26); V_G at O = 0.017 is essentially at
plateau level. The jump criterion is sensitive to the contrast between anchor level and plateau
level, not to cardinal-point status per se.

**The protective properties are not convex.** V_A's protection derives from sparsity
(sparse-commutator on the 24-cell subset). V_F's protection derives from equivariance
(Reynolds projection to 10⁻¹⁴). The combination cos θ·V_A + sin θ·V_F has neither: union
support destroys V_A's sparsity; the V_A component destroys V_F's equivariance.

Plateau anomaly on loop AF: O(θ) ≈ 0.25–0.28 on the plateau sits below both anchor values
(0.952 and 0.308), even though ‖V(θ)‖ < 1 off-cardinal. A weaker mixed deformation does more
damage than either pure component — it belongs to neither protected class.

**The compact direction is destructive, not decorative.** O(θ) is single-valued with no
monodromy, but the loop spends almost its entire length on a collapsed plateau. The protective
directions are measure-zero rays in deformation space.

### 4.3 Registered Taxonomy Gap

The PHASE-BOUNDARIES outcome was written to mean "regions of deformation space
separated by walls." The data triggered the criterion via cardinal spikes at isolated rays, with a
uniform collapsed plateau between them. There are no extended high-O regions separated by a
wall; the A-stratum and F-stratum are isolated rays (measure zero in the loop). This is recorded
as a limitation of the registered taxonomy, not relabeled post hoc.

### 4.4 Open Question: EV_TOL Scaling

Jump location is coupled to EV_TOL = 10⁻⁴. First-order perturbation theory predicts eigenvalue
splittings grow ~linearly in the admixture coefficient, so the apparent boundary sits where
splittings cross the clustering tolerance — within the first 11.25° step at this grid resolution.
Whether the sharpness is structural or resolution-set must be the subject of a new
preregistration.

---

## 5. The McKay Bridge

The 600-cell vertex set is identified with the binary icosahedral group 2I ≅ SL(2,5) realized as
unit icosians. The unit icosians generate the E₈ root lattice (Conway–Smith). The nine irreps of
2I are canonically the nine nodes of affine Ẽ₈.

The bootstrap oracle derives this from first principles: it enumerates SL(2,5), bootstraps the
full 9×9 character table by tensor-and-strip (no hardcoding), computes the McKay
tensor-product multiplicities from characters via N₂ⁱʲ = ⟨χ₂χᵢ, χⱼ⟩, asserts the derived edge
set equals E(Ẽ₈) exactly, and verifies the Perron condition A·d = 2d on the affine marks. The
edge set is derived, not hardcoded, and the script raises McKayHardStop on any integrality
drift or graph mismatch.

The chirality convention is frozen as registered in the oracle, quoted here verbatim rather than
re-derived: 5a is the order-5 conjugacy class containing [[1,1],[0,1]] (unipotent, b = 1, a
quadratic residue mod 5), with χ₂(5a) = 2cos(2π/5) = φ − 1; equivalently χ₂ = 2cos(π/5) = φ
on the paired order-10 class 10b (the negation class of 5b). The opposite choice is the Galois
automorphism √5 → −√5, i.e. the relabeling 2 ↔ 2′, 3 ↔ 3′, 4 ↔ 4′; the Ẽ₈ match is
invariant under it, so the convention pins which arm of the diagram is called primed and
nothing else.

### 5.1 The Preregistered Experiment (MOX-1)

The McKay-ordering experiment re-indexes M_ρσ by Ẽ₈ node order and asks whether the
mixing has visible structure in that ordering — concentrated near Dynkin-adjacent pairs, say.

This is stated as exploratory (H-A), not predicted: D₀ is not tensoring-with-the-2, so adjacency
structure may not appear. H-A failing does not touch Conjecture 1 (H-B). The prereg says
explicitly what each cross-outcome means — including the publishable negative where mixing
has real McKay structure that nonetheless does not control the commutant.

Four design decisions close the main failure modes:

**D4 (F-control trap).** F is exactly equivariant, so Q₁(F) = 0 to machine precision — yet
S(F) = 968. Any predictor built on cross-isotypic mass alone calls F safe. That is why Q₂
exists: a first-order multiplicity-splitting score computed from compressions of the Reynolds
projection onto each (irrep, eigencluster) multiplicity space. D4 requires the predictor set to
get F right or record the limitation.

**Block-size normalization.** Raw M_ρσ scales with isotypic block dimensions — trivially larger
for dimension-6 and dimension-5 irreps. All H-A statistics use M̂ normalized against a 200-draw
dimension-matched random ensemble. Without this, H-A measures representation sizes, not
mixing structure.

**H-A/H-B firewall.** McKay organization failing does not touch Conjecture 1, and the prereg
says explicitly what each cross-outcome means.

**Derived edge set.** The oracle computes ρ₂ ⊗ ρᵢ from the character table and asserts it
reproduces the affine Ẽ₈ adjacency, with the chirality convention frozen as above. This removes
the convention ambiguity between ρ₂ and ρ₂′ as a silent failure mode.

---

## 6. Instrument Registry

All claims in this paper backed by computation have a registered instrument. Per pinned rule 3
(below), **no hash in this table is authoritative until computed on the machine where the
instrument runs and recorded with date and host.** One value previously circulated for
finalize_loop_report.py traveled through a chat channel; it is listed as claimed, not certified.

| Instrument | Role | Hash / Status |
|---|---|---|
| mckay-mixing.py | Bootstrap / character-table / Ẽ₈ oracle | Verified standalone; hash pending local computation (rule 3) |
| mckay_mixing.py | MOX-1 run instrument (M_ρσ, Q₁, Q₂, C(V)) | Frozen — awaiting H.npz / dirs.npz; hash pending local computation (rule 3) |
| finalize_loop_report.py | Loop-report bracket substitution + cartesian figure | SHA-256 2074487d… claimed locally, uncertified — recompute on run machine and record before freeze |
| LOOP_VERIFICATION_REPORT.md | Loop experiment frozen verdict | Bracketed pending loop_results.npz |
| MOX1-prereg-mckay-mixing-v1.pdf | MOX-1 preregistration | Frozen |
| PREREGISTRATION_loop.md | Loop experiment preregistration | Frozen (locked 2026-06-06) |

**Naming-collision note:** mckay-mixing.py and mckay_mixing.py differ by a single character
and serve different roles. Before any public release they are to be renamed (proposed:
mckay_oracle.py and mox1_instrument.py), with this registry updated at rename and hashes
recomputed.

**Pinned rules (session log):**

1. Never pass class_ids generated under one CHI column order into projectors using the other
   CHI column order.
2. Verdicts are read from .npz numbers, never from figures or narrative summaries of figures.
3. Instruments move as files with hashes. Hashes are computed where the instrument runs. A
   hash that traveled through a chat window certifies nothing.

---

## 7. Open Questions

**Immediate (gated on file arrivals):**

- loop_results.npz → close brackets in LOOP_VERIFICATION_REPORT.md, generate cartesian
  figure, resolve [clust_F] provenance
- H.npz + dirs.npz → run MOX-1 instrument

**Next preregistrations:**

- EV_TOL scaling experiment: does the loop jump position scale with tolerance, or is it stable?
  The two outcomes (measurement-resolution edge vs. genuine fragility threshold with
  extractable width) are stated explicitly in the loop report.
- McKay-ordering: MOX-1 is frozen and ready to run.

**Theorem-level:**

- Characterize the finite-dimensional perturbations V for which
  dim Comm_{2I}((D₀ + χV)²) remains close to 3138. The problem is finite, computationally
  reproducible, and representation-theoretic. It does not require physical interpretation to be
  meaningful.
- Determine whether M_ρσ(V) is a sufficient statistic for S(χ), and if so, identify the algebraic
  structure in V that makes M̂ small off-diagonal (sparsity; commutator type; neither alone
  for F).
- Upgrade-or-rule-out for §3: exhibit a group representation on the heterotic toy model's
  state space whose isotypic projectors realize the (Φ, τ) split with contamination amplitudes
  equal to ‖P_ρ V P_σ‖_F² — the construction that would turn the §3 analogue into an
  instance — or show that no such representation exists.
- Identify, or rule out, a unitary intertwiner S satisfying SD₀S† = −D₀ and SVS† = V that
  would explain the observed θ → θ + π symmetry of the loop observable.

---

## 8. Non-Claims Register

1. The 600-cell realizes a physical theory.
2. The SUGRA mechanism is correct or complete.
3. The dictionary between the two programs implies a shared physical interpretation.
4. The loop PHASE-BOUNDARIES verdict implies a genuine phase transition (EV_TOL scaling is
   unresolved).
5. The McKay-bridge experiment is expected to show adjacency structure (D₀ is not
   tensoring-with-the-2).
6. The W₂ CC-isolation result solves the cosmological constant problem.
7. The heterotic compatibility audit validates E₈×E₈ heterotic string theory as the correct
   theory of nature.
8. The §2 dictionary is a theorem-level correspondence. It is a heuristic schema pending the
   McKay bridge (§5) and the §7 upgrade-or-rule-out construction.

*The seam between formal structural correspondence and ontological claims is not closeable
within this program and is not claimed to be closed.*

---

## References (project artifacts)

[1] Equivariant_Commutant_Stability_600Cell_arXiv_v1.pdf — 600-cell program manuscript.
[2] Kaleidoworks-Compact-Holonomy-White-Paper-v2-2.pdf — heterotic SUGRA compatibility audit.
[3] PREREGISTRATION_loop.md — loop experiment preregistration (locked 2026-06-06) and
    LOOP_VERIFICATION_REPORT.md.
[4] mckay-mixing.py — SL(2,5) bootstrap / Ẽ₈ oracle.
[5] MOX1-prereg-mckay-mixing-v1.pdf — MOX-1 preregistration.
[6] mckay_mixing.py — MOX-1 run instrument.

---

## Appendix A. Revision Record, v1.0 → v1.1

Five edits, applied 2026-06-12 following internal review. Recorded here so the changes are
themselves on the record.

**A1 (mathematical error + convention drift, §5).** v1.0 stated the chirality convention as
"χ(ρ₂) = φ on the nearest-neighbor class (order-10, trace = 2cos(2π/5) = φ)." The equation is
false (2cos(2π/5) = φ − 1; it is 2cos(π/5) that equals φ), and the description did not match the
oracle's registered convention, which is anchored on the order-5 class containing [[1,1],[0,1]].
v1.1 quotes the registered convention verbatim. Classified as a transcription-mutation of a
frozen convention — the failure class pinned rule 3 exists to prevent.

**A2 (over-completion, §3 and abstract).** v1.0 claimed the SUGRA contamination analysis is
"the first analytic proof-of-concept" and a "worked 2×2 instance" of M_ρσ. No group,
representation, or isotypic projectors realizing the (Φ, τ) split were exhibited; the claim was an
instance of anchored over-completion (true anchor, unauthorized mechanism identity). v1.1
demotes throughout to "structural analogue" and adds the upgrade-or-rule-out construction to
§7. The M̂ normalization claim is corrected in the same pass.

**A3 (registry self-consistency, §6).** v1.0 listed one uncertified hash and no hashes for five
other instruments, in a document stating pinned rule 3. v1.1 marks every hash as pending local
computation or claimed-uncertified, and adds the naming-collision note for mckay-mixing.py /
mckay_mixing.py.

**A4 (epistemic status of the dictionary, §2 and abstract).** v1.0 stated the status only in
the non-claims register while §2 read as identification ("instances of the same structural
question"). v1.1 states the heuristic status in §2's opening, revises the F ↔ T3 entry to
lesson-level pairing with the caveat that equivariance is not recoverable by basis change, and
adds non-claim 8.

**A5 (precision phrasing, §4.1).** v1.0 asserted O(2π) = O(0) while ret remained bracketed.
v1.1 phrases the agreement at displayed precision, exact values pending substitution —
consistent with pinned rule 2.
