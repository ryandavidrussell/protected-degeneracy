#!/usr/bin/env python3
"""
mox1_preflight.py  —  artifact inspection before MOX-1 run
Run this first. Only proceed to the full mckay_mixing.py run if all checks pass.
"""
import numpy as np, sys

def fail(msg):
    print("PRECHECK FAIL:", msg, file=sys.stderr)
    raise SystemExit(2)

def main(H_path, dirs_path):
    H = np.load(H_path, allow_pickle=True)
    D = np.load(dirs_path, allow_pickle=True)

    required_H = ["U_classes", "class_sizes", "class_labels"]
    for k in required_H:
        if k not in H.files:
            fail(f"H.npz missing key: {k}")

    labels = [str(x) for x in H["class_labels"]]
    expected = ["1a","2a","3a","4a","5a","10a","5b","10b","6a"]
    if labels != expected:
        fail(f"class_labels mismatch. expected {expected}, got {labels}")

    Uc = H["U_classes"]
    if len(Uc) != 9:
        fail(f"Expected 9 class matrices, got {len(Uc)}")

    n = None
    for i, U in enumerate(Uc):
        if U.ndim != 2 or U.shape[0] != U.shape[1]:
            fail(f"U_classes[{i}] not square")
        n = U.shape[0] if n is None else n
        if U.shape != (n, n):
            fail(f"U_classes[{i}] shape mismatch: expected {(n,n)}, got {U.shape}")

    cs = H["class_sizes"]
    if len(cs) != 9:
        fail(f"class_sizes length {len(cs)} != 9")
    if int(np.sum(cs)) != 120:
        fail(f"sum(class_sizes) = {np.sum(cs)} != 120")

    if len(D.files) == 0:
        fail("dirs.npz contains no deformation directions")

    bad = []
    for k in D.files:
        V = D[k]
        if V.shape != (n, n):
            bad.append((k, V.shape))
    if bad:
        fail("direction shapes mismatch: " + repr(bad[:5]))

    print("PRECHECK OK")
    print(f"dimension n = {n}")
    print(f"directions  = {len(D.files)}")
    print(f"keys sample = {sorted(D.files)[:12]}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python mox1_preflight.py H.npz dirs.npz", file=sys.stderr)
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])
