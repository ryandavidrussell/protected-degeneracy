from __future__ import annotations
import math, sys
import numpy as np

P = 5
GROUP_ORDER = 120
N_CLASSES = 9
PHI = (1.0 + math.sqrt(5.0)) / 2.0
ORTHO_TOL = 1e-12
INT_TOL = 1e-9
IRREP_ORDER = ("1","2","2p","3","3p","4","4p","5","6")
CLASS_ORDER = ("1a","2a","3a","4a","5a","5b","6a","10a","10b")
AFFINE_E8_EDGES = {
    (0,1),(1,3),(1,4),(3,5),(4,6),(5,7),(6,7),(7,8)
}


def inv2(m):
    a,b = int(m[0,0]), int(m[0,1])
    c,d = int(m[1,0]), int(m[1,1])
    det = (a*d - b*c) % P
    if det != 1:
        raise ValueError("matrix not in SL(2,5)")
    return np.array([[d,-b],[-c,a]], dtype=int) % P


def key2(m):
    return tuple(int(x) for x in np.asarray(m, dtype=int).reshape(-1))


def mul2(a,b):
    return (np.asarray(a, dtype=int) @ np.asarray(b, dtype=int)) % P


def sl25_group():
    G = []
    for a in range(P):
        for b in range(P):
            for c in range(P):
                for d in range(P):
                    m = np.array([[a,b],[c,d]], dtype=int)
                    if (a*d - b*c) % P == 1:
                        G.append(m)
    if len(G) != GROUP_ORDER:
        raise RuntimeError(f"expected 120 elements, found {len(G)}")
    return G


def conjugacy_classes(G):
    unseen = {key2(g): g for g in G}
    classes = []
    while unseen:
        _, g = unseen.popitem()
        cls = {}
        for h in G:
            x = mul2(mul2(h, g), inv2(h))
            cls[key2(x)] = x
        for k in cls:
            unseen.pop(k, None)
        classes.append(list(cls.values()))
    return classes


def order_of(g):
    I = np.eye(2, dtype=int)
    x = I.copy()
    for k in range(1, 121):
        x = mul2(x, g)
        if np.array_equal(x, I):
            return k
    raise RuntimeError("order exceeded 120")


def trace_mod5(g):
    return int((int(g[0,0]) + int(g[1,1])) % P)


def rho2_char_from_trace(tr):
    if tr == 2:   # 2 cos(pi/5)
        return PHI
    if tr == 3:   # 2 cos(3pi/5)
        return 1.0 - PHI
    if tr == 1:
        return 1.0
    if tr == 4:
        return -1.0
    if tr == 0:
        return 0.0
    raise ValueError(tr)


def build_oracle():
    G = sl25_group()
    raw = conjugacy_classes(G)
    reps = [cls[0] for cls in raw]
    sizes = np.array([len(cls) for cls in raw], dtype=int)
    orders = [order_of(r) for r in reps]

    class_info = list(zip(raw, reps, sizes, orders))
    I = np.eye(2, dtype=int)
    minusI = (-I) % P
    u = np.array([[1,1],[0,1]], dtype=int)

    def class_contains(target):
        kt = key2(target)
        hits = [i for i,(cls,_,_,_) in enumerate(class_info) if kt in {key2(x) for x in cls}]
        if len(hits) != 1:
            raise RuntimeError(f"target selector ambiguous for {target}: {hits}")
        return hits[0]

    idx_1a = class_contains(I)
    idx_2a = class_contains(minusI)
    idx_5a = class_contains(u)
    idx_10b = class_contains((-u) % P)

    remaining = [i for i in range(len(class_info)) if i not in {idx_1a, idx_2a, idx_5a, idx_10b}]
    idx_3a = [i for i in remaining if class_info[i][3] == 3][0]
    idx_4a = [i for i in remaining if class_info[i][3] == 4][0]
    idx_6a = [i for i in remaining if class_info[i][3] == 6][0]
    ord5_rem = [i for i in remaining if class_info[i][3] == 5]
    ord10_rem = [i for i in remaining if class_info[i][3] == 10]
    if len(ord5_rem) != 1 or len(ord10_rem) != 1:
        raise RuntimeError("unexpected remaining order-5/order-10 class count")
    idx_5b = ord5_rem[0]
    idx_10a = ord10_rem[0]

    perm = [idx_1a, idx_2a, idx_3a, idx_4a, idx_5a, idx_5b, idx_6a, idx_10a, idx_10b]
    sizes_ord = np.array([class_info[i][2] for i in perm], dtype=int)
    reps_ord = [class_info[i][1] for i in perm]

    tr = [trace_mod5(r) for r in reps_ord]
    rho2 = np.array([rho2_char_from_trace(t) for t in tr], dtype=float)

    # Freeze chirality convention: chi_2(5a)=phi-1, chi_2(10b)=phi
    if abs(rho2[4] - (PHI-1.0)) > 1e-12 or abs(rho2[8] - PHI) > 1e-12:
        raise RuntimeError("chirality convention drift in rho2")

    CHI = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2,-2, 1, 0, PHI-1, PHI, -1, 1-PHI, -PHI],
        [2,-2, 1, 0, PHI, 1-PHI, -1, -PHI, PHI-1],
        [3, 3, 0,-1, 1-PHI, PHI, 0, 1-PHI, PHI],
        [3, 3, 0,-1, PHI, 1-PHI, 0, PHI, 1-PHI],
        [4,-4,-1, 0, -1, 1, 1,-1, 1],
        [4,-4,-1, 0, 1,-1, 1, 1,-1],
        [5, 5,-1, 1, 0, 0,-1, 0, 0],
        [6,-6, 0, 0, 1,-1, 0,-1, 1],
    ], dtype=float)

    gram = (CHI * sizes_ord) @ CHI.T / GROUP_ORDER
    if np.max(np.abs(gram - np.eye(9))) > ORTHO_TOL:
        raise RuntimeError("character table failed orthogonality")

    chi2 = CHI[1]
    A = np.zeros((9,9), dtype=int)
    for i in range(9):
        for j in range(9):
            nij = np.dot(sizes_ord, chi2 * CHI[i] * CHI[j]) / GROUP_ORDER
            if abs(nij - round(nij)) > INT_TOL:
                raise RuntimeError(f"nonintegral McKay multiplicity N_2^{{{i},{j}}}={nij}")
            if int(round(nij)) > 0 and i != j:
                A[i,j] = 1
    A = np.maximum(A, A.T)

    edge_set = {(i,j) for i in range(9) for j in range(i+1,9) if A[i,j] == 1}
    if edge_set != AFFINE_E8_EDGES:
        raise RuntimeError(f"affine E8 mismatch: {edge_set} != {AFFINE_E8_EDGES}")

    d = np.array([1,2,2,3,3,4,4,5,6], dtype=int)
    if not np.array_equal(A @ d, 2*d):
        raise RuntimeError("Perron condition A·d = 2d failed")

    return {
        "class_sizes": sizes_ord,
        "class_reps": reps_ord,
        "rho2": rho2,
        "CHI": CHI,
        "adjacency": A,
    }


if __name__ == "__main__":
    obj = build_oracle()
    print("oracle OK")
    print("class order:", CLASS_ORDER)
    print("rho2:", obj["rho2"])
    print("CHI shape:", obj["CHI"].shape)
