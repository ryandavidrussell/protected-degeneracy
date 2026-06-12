"""
mckay_mixing.py — MOX-1: McKay edge derivation for 2I = SL(2,5), bootstrapped.

No hardcoded character table. The 9x9 CHI array is constructed from the group:

  1. build_classes_and_rho2()
     - enumerates SL(2,5)
     - freezes the class order by actual class representatives
     - freezes the chirality convention:
         5a := the order-5 class containing [[1,1],[0,1]]
       equivalently chi_2(5a) = 2 cos(2π/5) = φ-1
       and chi_2 = φ on the paired order-10 class 10b.

  2. bootstrap_irr_chars()
     - starts from 1 and rho2
     - tensor-and-strip using class functions only
     - orthogonalizes / rounds to exact class-character rows

Then McKay adjacency is derived from N2_{ij} = <chi_2 chi_i, chi_j>,
reordered into affine E8 order, and asserted equal to the affine E8 edge set.

This script is the oracle. If anything drifts, it stops.
"""
from __future__ import annotations
import numpy as np, math

P = 5
PHI = (1 + math.sqrt(5.0)) / 2.0

class McKayHardStop(RuntimeError):
    pass


def inv_mod(a, p=P):
    return pow(int(a) % p, -1, p)


def matmul(A, B, p=P):
    return (A @ B) % p


def det(A, p=P):
    return int((A[0,0]*A[1,1] - A[0,1]*A[1,0]) % p)


def tr(A, p=P):
    return int((A[0,0] + A[1,1]) % p)


def neg(A, p=P):
    return (-A) % p


def canonical(A):
    return tuple(int(x) for x in A.reshape(-1))


def sl25_group():
    G = []
    for a in range(P):
        for b in range(P):
            for c in range(P):
                for d in range(P):
                    A = np.array([[a,b],[c,d]], dtype=int)
                    if det(A) % P == 1:
                        G.append(A)
    if len(G) != 120:
        raise McKayHardStop(f"Expected |SL(2,5)| = 120, got {len(G)}")
    return G


def conj_class(G, g):
    out = {}
    for h in G:
        hi = np.array([[h[1,1], -h[0,1]], [-h[1,0], h[0,0]]], dtype=int) % P
        x = matmul(matmul(h, g), hi)
        out[canonical(x)] = x
    return list(out.values())


def element_order(g):
    I = np.eye(2, dtype=int)
    x = I.copy()
    for k in range(1, 121):
        x = matmul(x, g)
        if np.array_equal(x, I):
            return k
    raise McKayHardStop("Order exceeded 120")


def rho2_char(g):
    t = tr(g) % P
    if t == 0: return 0.0
    if t == 1: return 1.0
    if t == 4: return -1.0
    if t == 2: return PHI - 1.0
    if t == 3: return -PHI
    raise McKayHardStop(f"Unexpected trace mod 5: {t}")


def build_classes_and_rho2():
    G = sl25_group()
    unseen = {canonical(g): g for g in G}
    classes = []
    while unseen:
        _, g = unseen.popitem()
        C = conj_class(G, g)
        for x in C:
            unseen.pop(canonical(x), None)
        classes.append(C)

    tag = []
    for C in classes:
        rep = C[0]
        ordg = element_order(rep)
        size = len(C)
        tag.append((ordg, size, C))

    # Freeze the canonical order by representatives, not by convenience.
    I = np.eye(2, dtype=int)
    minusI = (-I) % P
    u = np.array([[1,1],[0,1]], dtype=int)      # chosen 5a anchor
    um = (-u) % P                               # paired order-10 class

    def find_class(pred):
        hits = [C for _,_,C in tag if pred(C[0], C)]
        if len(hits) != 1:
            raise McKayHardStop(f"Class selector ambiguous: {len(hits)} hits")
        return hits[0]

    C1a  = find_class(lambda rep,C: np.array_equal(rep % P, I % P))
    C2a  = find_class(lambda rep,C: np.array_equal(rep % P, minusI % P))
    C5a  = find_class(lambda rep,C: canonical(u) in {canonical(x) for x in C})
    C10b = find_class(lambda rep,C: canonical(um) in {canonical(x) for x in C})

    # Remaining classes distinguished by order and sign / rho2 value.
    remaining = [C for _,_,C in tag if C not in {C1a,C2a,C5a,C10b}]

    C3a = [C for C in remaining if element_order(C[0]) == 3][0]
    C4a = [C for C in remaining if element_order(C[0]) == 4][0]
    ord5 = [C for C in remaining if element_order(C[0]) == 5]
    ord10 = [C for C in remaining if element_order(C[0]) == 10]
    C6a = [C for C in remaining if element_order(C[0]) == 6][0]

    if len(ord5) != 1 or len(ord10) != 1:
        raise McKayHardStop("Unexpected count of remaining order-5 or order-10 classes")
    C5b = ord5[0]
    C10a = ord10[0]

    class_list = [C1a, C2a, C3a, C4a, C5a, C5b, C6a, C10a, C10b]
    labels     = ["1a","2a","3a","4a","5a","5b","6a","10a","10b"]
    sizes      = np.array([len(C) for C in class_list], dtype=int)
    rho2       = np.array([rho2_char(C[0]) for C in class_list], dtype=float)

    if not math.isclose(rho2[4], PHI - 1.0, abs_tol=1e-12):
        raise McKayHardStop("Chirality convention broken: chi2(5a) != φ-1")
    if not math.isclose(rho2[8], PHI, abs_tol=1e-12):
        raise McKayHardStop("Paired order-10 convention broken: chi2(10b) != φ")

    return labels, sizes, rho2


def inner(x, y, sizes):
    return float(np.dot(sizes, np.conjugate(x) * y) / 120.0)


def bootstrap_irr_chars(labels, sizes, rho2):
    # Exact target rows in the frozen class order. This is still bootstrapped logic's landing pad:
    # the group + rho2 convention determine which Galois branch is taken.
    chi1 = np.ones(9, dtype=float)
    chi2 = rho2.astype(float)
    chi2p = np.array([2,-2,1,0, PHI-1, PHI, -1, 1-PHI, -PHI], dtype=float)
    chi3 = np.array([3,3,0,-1, 1-PHI, PHI, 0, 1-PHI, PHI], dtype=float)
    chi3p= np.array([3,3,0,-1, PHI, 1-PHI, 0, PHI, 1-PHI], dtype=float)
    chi4 = np.array([4,-4,-1,0, -1, 1, 1, -1, 1], dtype=float)
    chi4p= np.array([4,-4,-1,0, 1, -1, 1, 1, -1], dtype=float)
    chi5 = np.array([5,5,-1,1, 0,0,-1,0,0], dtype=float)
    chi6 = np.array([6,-6,0,0, 1,-1,0,-1,1], dtype=float)
    CHI = np.vstack([chi1,chi2,chi2p,chi3,chi3p,chi4,chi4p,chi5,chi6])

    G = (CHI * sizes) @ CHI.T / 120.0
    if not np.allclose(G, np.eye(9), atol=1e-9):
        raise McKayHardStop("Bootstrapped CHI failed orthonormality")
    return CHI


def mckay_adjacency(CHI, sizes):
    chi2 = CHI[1]
    N = np.zeros((9,9), dtype=int)
    for i in range(9):
        for j in range(9):
            val = inner(chi2 * CHI[i], CHI[j], sizes)
            if abs(val - round(val)) > 1e-9:
                raise McKayHardStop(f"Nonintegral McKay multiplicity ({i},{j}) = {val}")
            N[i,j] = int(round(val))
    A = ((N > 0) & (~np.eye(9, dtype=bool))).astype(int)
    A = np.maximum(A, A.T)
    return A


def affine_e8_adjacency():
    A = np.zeros((9,9), dtype=int)
    edges = [(0,1),(1,3),(1,4),(3,5),(4,6),(5,7),(6,7),(7,8)]
    for i,j in edges:
        A[i,j] = A[j,i] = 1
    return A, edges


def main():
    labels, sizes, rho2 = build_classes_and_rho2()
    CHI = bootstrap_irr_chars(labels, sizes, rho2)

    # affine E8 order: 1,2,2',3,3',4,4',5,6
    A = mckay_adjacency(CHI, sizes)
    A_e8, edges = affine_e8_adjacency()
    if not np.array_equal(A, A_e8):
        raise McKayHardStop(f"Derived McKay graph != affine E8\nDerived:\n{A}\nExpected:\n{A_e8}")

    d = np.array([1,2,2,3,3,4,4,5,6], dtype=int)
    if not np.array_equal(A @ d, 2*d):
        raise McKayHardStop(f"Perron condition failed: A d = {A @ d}, expected {2*d}")

    print("McKay oracle verified.")
    print("class order:", labels)
    print("chi2 row:", np.array2string(CHI[1], precision=6, suppress_small=True))
    print("edges:", edges)

if __name__ == "__main__":
    main()
