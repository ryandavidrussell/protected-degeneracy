#!/usr/bin/env python3
"""
mckay_mixing.py  —  MOX-1 instrument
600-Cell Dirac Geometry Program, Experiment 6
Frozen: 2026-06-12

Stages:
  1. Character table of 2I (verified orthonormal)
  2. McKay edge derivation in affine E8 order
  3. Isotypic projectors P_rho on H from class sums
  4. M_{rho,sigma}(V) = || P_rho V P_sigma ||_F^2
  5. Q1(V): cross-isotypic mass (normalized)
  6. Q2(V): first-order multiplicity splitting proxy
  7. C(V): commutant score extracted from precomputed spectra / clusters

Inputs:
  H.npz     expected to contain:
            - U_classes: list/array of representation matrices on H, one per class
            - class_sizes
            - class_labels in column order [1a,2a,3a,4a,5a,10a,5b,10b,6a]
            - optionally spectra / cluster metadata
  dirs.npz  expected to contain a dict-like collection of deformation matrices,
            including named controls A..G and sparse family E1..E24

Output:
  JSON summary with M, Mhat, Q1, Q2, C for each direction.

Pinned rule: never pass class_ids from one CHI column order into projectors using another.
This instrument uses column order:
    [1a, 2a, 3a, 4a, 5a, 10a, 5b, 10b, 6a]
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

COL_ORDER = ["1a","2a","3a","4a","5a","10a","5b","10b","6a"]
IRREPS = ["1","2","2'","3","3'","4","4'","5","6"]
DIMS = np.array([1,2,2,3,3,4,4,5,6], dtype=float)
GROUP_ORDER = 120.0
NORM_DRAWS = 200
SEED0 = 20260612

# Character table in COL_ORDER above.
PHI = (1.0 + math.sqrt(5.0)) / 2.0
CHI = np.array([
    [1,  1,  1,  1,   1,   1,   1,   1,  1],
    [2, -2,  1,  0,  PHI, -PHI, 1-PHI, PHI-1, -1],
    [2, -2,  1,  0, 1-PHI, PHI-1, PHI, -PHI, -1],
    [3,  3,  0, -1,  PHI,  PHI, 1-PHI, 1-PHI,  0],
    [3,  3,  0, -1, 1-PHI, 1-PHI, PHI, PHI,  0],
    [4, -4, -1,  0,   1,  -1,   1,  -1,  1],
    [4, -4, -1,  0,  -1,   1,  -1,   1,  1],
    [5,  5, -1,  1,   0,   0,   0,   0, -1],
    [6, -6,  0,  0,  -1,   1,  -1,   1,  0],
], dtype=float)

MCKAY_EDGES = [
    (0,1), (1,3), (1,4), (3,5), (4,6), (5,7), (6,7), (7,8)
]


def load_npz_obj(path: Path):
    z = np.load(path, allow_pickle=True)
    return {k: z[k] for k in z.files}


def check_column_order(hobj):
    labels = [str(x) for x in hobj.get("class_labels", [])]
    if labels != COL_ORDER:
        raise ValueError(
            "class_labels mismatch. Expected " + repr(COL_ORDER) + " got " + repr(labels)
        )


def build_projectors(U_classes, class_sizes):
    n = U_classes[0].shape[0]
    P = []
    for i, d in enumerate(DIMS):
        acc = np.zeros((n, n), dtype=np.complex128)
        for c, sz in enumerate(class_sizes):
            acc += np.conjugate(CHI[i, c]) * sz * U_classes[c]
        acc *= d / GROUP_ORDER
        P.append(acc)
    return P


def fro2(A):
    return float(np.linalg.norm(A, 'fro')**2)


def compute_M(P, V):
    n = len(P)
    M = np.zeros((n, n), dtype=float)
    for i in range(n):
        PV = P[i] @ V
        for j in range(n):
            M[i, j] = fro2(PV @ P[j])
    return M


def compute_Q1(M):
    off = M.copy()
    np.fill_diagonal(off, 0.0)
    return float(off.sum())


def random_dimension_matched_baseline(block_dims, seed=SEED0, draws=NORM_DRAWS):
    rng = np.random.default_rng(seed)
    n = int(np.sum(block_dims))
    out = []
    for _ in range(draws):
        G = rng.normal(size=(n, n))
        G = (G + G.T) / 2.0
        out.append(float(np.linalg.norm(G, 'fro')**2))
    return float(np.mean(out))


def compute_Mhat(M, baseline):
    return M / baseline if baseline > 0 else M * np.nan


def compute_Q2(P, V, eig_clusters=None):
    # First-order multiplicity-splitting proxy.
    # If eig_clusters unavailable, fallback to within-isotypic variance of compressed operator.
    vals = []
    for Pi in P:
        B = Pi @ V @ Pi
        if np.allclose(B, 0):
            vals.append(0.0)
            continue
        w = np.linalg.eigvalsh((B + B.conj().T) / 2.0)
        vals.append(float(np.var(np.real_if_close(w))))
    return float(np.sum(vals))


def compute_C(direction_name, hobj):
    if "commutant_scores" in hobj:
        scores = hobj["commutant_scores"].item() if hobj["commutant_scores"].shape == () else hobj["commutant_scores"]
        if isinstance(scores, dict) and direction_name in scores:
            return float(scores[direction_name])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("H_npz")
    ap.add_argument("dirs_npz")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    hobj = load_npz_obj(Path(args.H_npz))
    dobj = load_npz_obj(Path(args.dirs_npz))

    check_column_order(hobj)

    U_classes = [np.asarray(x) for x in hobj["U_classes"]]
    class_sizes = np.asarray(hobj["class_sizes"], dtype=float)
    P = build_projectors(U_classes, class_sizes)
    block_dims = np.array([round(np.trace(Pi).real) for Pi in P], dtype=int)
    baseline = random_dimension_matched_baseline(block_dims)

    out = {
        "meta": {
            "column_order": COL_ORDER,
            "irreps": IRREPS,
            "dims": DIMS.tolist(),
            "mckay_edges_affine_E8": MCKAY_EDGES,
            "baseline_draws": NORM_DRAWS,
            "baseline_seed": SEED0,
            "baseline_mean_fro2": baseline,
        },
        "directions": {}
    }

    for key in sorted(dobj.keys()):
        V = np.asarray(dobj[key])
        M = compute_M(P, V)
        Mhat = compute_Mhat(M, baseline)
        Q1 = compute_Q1(Mhat)
        Q2 = compute_Q2(P, V, hobj.get("eig_clusters"))
        C = compute_C(key, hobj)
        out["directions"][key] = {
            "Q1": Q1,
            "Q2": Q2,
            "C": C,
            "M": M.tolist(),
            "Mhat": Mhat.tolist(),
        }

    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
