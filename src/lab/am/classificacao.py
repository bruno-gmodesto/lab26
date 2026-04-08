"""
plot_decision_boundary.py
─────────────────────────
Visualise the decision boundary of any sklearn-compatible or PyTorch model
by projecting data into 2-D or 3-D via a chosen dimensionality-reduction method.

Supported DR methods (dr parameter)
────────────────────────────────────
  "pca"     – Principal Component Analysis          (sklearn)
  "tsne"    – t-SNE                                  (sklearn)
  "mds"     – Multi-Dimensional Scaling              (sklearn)
  "umap"    – UMAP  (requires `pip install umap-learn`)
  "ica"     – Independent Component Analysis         (sklearn)
  "isomap"  – Isomap manifold learning               (sklearn)

Backend detection
─────────────────
Pass X as a numpy ndarray  → sklearn predict path
Pass X as a torch.Tensor   → torch model predict path  (model called as model(X))

Versão inicial gerada no claude.ai em 2024-06-20.
"""

from __future__ import annotations

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _get_reducer(dr: str, d: int, **kw):
    """Return a fitted-able sklearn-compatible reducer."""
    dr = dr.lower()
    n_components = d

    if dr == "pca":
        from sklearn.decomposition import PCA
        return PCA(n_components=n_components, **kw)

    if dr == "tsne":
        from sklearn.manifold import TSNE
        # TSNE only supports n_components <= 3; perplexity default sensible
        kw.setdefault("perplexity", 30)
        kw.setdefault("random_state", 0)
        return TSNE(n_components=n_components, **kw)

    if dr == "mds":
        from sklearn.manifold import MDS
        kw.setdefault("random_state", 0)
        return MDS(n_components=n_components, **kw)

    if dr == "umap":
        try:
            from umap import UMAP
        except ImportError as e:
            raise ImportError("Install umap-learn:  pip install umap-learn") from e
        return UMAP(n_components=n_components, **kw)

    if dr == "ica":
        from sklearn.decomposition import FastICA
        kw.setdefault("random_state", 0)
        return FastICA(n_components=n_components, **kw)

    if dr == "isomap":
        from sklearn.manifold import Isomap
        return Isomap(n_components=n_components, **kw)

    raise ValueError(
        f"Unknown dr='{dr}'. Choose from: pca, tsne, mds, umap, ica, isomap"
    )


def _predict(model, X_np: np.ndarray) -> np.ndarray:
    """Call model.predict (sklearn) or model(tensor) (torch), always returns ndarray."""
    try:
        import torch as _torch
        if isinstance(X_np, _torch.Tensor) or (
                hasattr(model, "forward")  # duck-type: looks like nn.Module
        ):
            with _torch.no_grad():
                t = _torch.tensor(X_np, dtype=_torch.float32)
                out = model(t)
                # handle raw logits / probabilities / class indices
                if out.ndim == 2 and out.shape[1] > 1:  # multi-class logits
                    preds = out.argmax(dim=1).numpy()
                elif out.ndim == 2 and out.shape[1] == 1:  # binary logit/prob
                    preds = (out.squeeze(1) >= 0.5).long().numpy()
                else:  # already class indices
                    preds = out.round().long().numpy()
            return preds
    except ImportError:
        _torch = None
        pass

    # sklearn path
    return model.predict(X_np)


def _make_cmap_and_norm(labels: np.ndarray):
    """Return a discrete colormap + norm spanning all unique labels."""
    classes = np.unique(labels)
    n = len(classes)
    base = cm.get_cmap("tab10" if n <= 10 else "tab20", n)
    cmap = mcolors.ListedColormap(tuple(base(i) for i in range(n)))
    norm = mcolors.BoundaryNorm(
        boundaries=np.arange(-0.5, n + 0.5, 1), ncolors=n
    )
    return cmap, norm, classes


# ──────────────────────────────────────────────────────────────────────────────
# Main public function
# ──────────────────────────────────────────────────────────────────────────────

def plot_decision_boundary(
        model,
        X,
        y,
        dr: str = "pca",
        d: int = 2,
        resolution: int = 300,
        alpha_bg: float = 0.35,
        title: str | None = None,
        figsize: tuple = (8, 6),
        dr_kw: dict | None = None,
        losses: list | None = None,
        ax=None,
):
    """
    Plot the decision boundary of *model* on data *X* with true labels *y*.

    Parameters
    ----------
    model       : sklearn estimator **or** torch nn.Module
                  Must support `.predict(X_np)` (sklearn) or `model(tensor)` (torch).
    X           : array-like of shape (n_samples, n_features)  –  numpy or torch
    y           : array-like of shape (n_samples,)             –  true class labels
    dr          : str, default "pca"
                  Dimensionality-reduction method.
                  One of: "pca", "tsne", "mds", "umap", "ica", "isomap"
    d           : int, default 2
                  Target dimension (2 or 3).
    resolution  : int, default 300
                  Grid resolution for background colourisation (points per axis).
    alpha_bg    : float, default 0.35
                  Opacity of the background prediction colours.
    title       : str or None
                  Plot title (auto-generated if None).
    figsize     : tuple, default (8, 6)
    dr_kw       : dict or None
                  Extra keyword arguments forwarded to the DR constructor.
    losses      : list or None
                  Optional list of loss values recorded during training.
                  When provided, a second subplot "Função de Erro" is drawn.

    Returns
    -------
    fig, axes   : matplotlib Figure and Axes (or list of axes)
    """
    if d not in (2, 3):
        raise ValueError("d must be 2 or 3")

    dr_kw = dr_kw or {}

    # ── 0. Normalise inputs to numpy ────────────────────────────────────────
    axes = None
    try:
        import torch as _torch
        if isinstance(X, _torch.Tensor):
            X = X.detach().cpu().numpy()
        if isinstance(y, _torch.Tensor):
            y = y.detach().cpu().numpy()
    except ImportError:
        _torch = None
        pass
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y).ravel()

    n_samples, n_features = X.shape

    # ── 1. Fit DR on X ──────────────────────────────────────────────────────
    reducer = _get_reducer(dr, d, **dr_kw)
    X_emb = reducer.fit_transform(X)  # (n, d)

    # ── 2. Build a dense background grid in the embedded space ──────────────
    mins = X_emb.min(axis=0)
    maxs = X_emb.max(axis=0)
    pad = (maxs - mins) * 0.10 + 1e-6  # 10 % margin

    axes_ranges = [
        np.linspace(mins[k] - pad[k], maxs[k] + pad[k], resolution)
        for k in range(d)
    ]
    grid_pts = np.stack(
        np.meshgrid(*axes_ranges, indexing="ij"), axis=-1
    ).reshape(-1, d)  # (resolution^d, d)

    # ── 3. Inverse-project grid → original space, then predict ──────────────
    #  For methods that have inverse_transform (PCA, ICA) we use it directly.
    #  For non-invertible methods (t-SNE, UMAP, MDS, Isomap) we use nearest-
    #  neighbour lookup in the embedded space to find the closest training point
    #  and inherit its prediction.
    if hasattr(reducer, "inverse_transform") and dr.lower() in ("pca", "ica"):
        X_grid_orig = reducer.inverse_transform(grid_pts)
        grid_preds = _predict(model, X_grid_orig)
    else:
        # Nearest-neighbour in embedded space
        from sklearn.neighbors import KNeighborsClassifier
        knn = KNeighborsClassifier(n_neighbors=1)
        train_preds = _predict(model, X)  # predictions on training data
        knn.fit(X_emb, train_preds)
        grid_preds = knn.predict(grid_pts)

    # ── 4. Colormap ─────────────────────────────────────────────────────────
    cmap, norm, classes = _make_cmap_and_norm(
        np.concatenate([y, grid_preds])
    )

    # ── 5. Plot ─────────────────────────────────────────────────────────────
    has_losses = losses is not None and len(losses) > 0
    ncols = 2 if has_losses else 1
    if d == 2:
        if ax is None:
            fig, axes = plt.subplots(1, ncols, figsize=(figsize[0] * ncols, figsize[1]))
            ax_main = axes[0] if has_losses else axes
        else:
            fig = None
            ax_main = ax

        Z = grid_preds.reshape(resolution, resolution)
        x0, x1 = axes_ranges
        ax_main.contourf(
            x0, x1, Z.T,
            levels=len(classes),
            cmap=cmap, norm=norm, alpha=alpha_bg,
        )

        sc = ax_main.scatter(
            X_emb[:, 0], X_emb[:, 1],
            c=y.astype(int), cmap=cmap, norm=norm,
            edgecolors="k", linewidths=0.4, s=40, zorder=3,
        )
        ax_main.set_xlabel(f"{dr.upper()} dim-1")
        ax_main.set_ylabel(f"{dr.upper()} dim-2")

    else:  # d == 3
        if has_losses:
            fig = plt.figure(figsize=(figsize[0] * ncols, figsize[1]))
            ax = fig.add_subplot(1, 2, 1, projection="3d")
        else:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection="3d")

        ax.scatter(
            *[grid_pts[:, k] for k in range(3)],
            c=grid_preds, cmap=cmap, norm=norm,
            alpha=alpha_bg * 0.5, s=2, zorder=1,
        )
        ax.scatter(
            *[X_emb[:, k] for k in range(3)],
            c=y.astype(int), cmap=cmap, norm=norm,
            edgecolors="k", linewidths=0.3, s=40, zorder=3,
        )
        ax.set_xlabel(f"{dr.upper()} 1")
        ax.set_ylabel(f"{dr.upper()} 2")
        ax.set_zlabel(f"{dr.upper()} 3")
        ax_main = ax

    # legend for classes
    handles = [
        plt.Line2D(
            [0], [0], marker="o", color="w",
            markerfacecolor=cmap(norm(int(c))),
            markeredgecolor="k", markersize=7,
            label=f"class {int(c)}",
        )
        for c in classes
    ]
    ax_main.legend(handles=handles, loc="best", framealpha=0.7)

    ax_main.set_title(
        title or f"Decision boundary — {dr.upper()} ({d}D)",
        fontsize=12, pad=10,
    )

    # ── 6. Loss curve ("Função de Erro") ────────────────────────────────────
    if has_losses:
        if d == 2:
            if ax is None:
                ax_loss = axes[1]
            else:
                # If ax is provided, we cannot plot the loss curve here
                ax_loss = None
        else:
            if fig is not None:
                ax_loss = fig.add_subplot(1, 2, 2)
            else:
                ax_loss = None
        if ax_loss is not None:
            ax_loss.plot(losses, color="steelblue", linewidth=1.5)
            ax_loss.set_xlabel("Época")
            ax_loss.set_ylabel("Erro")
            ax_loss.set_title("Função de Erro", fontsize=12, pad=10)
            ax_loss.grid(True, linestyle="--", alpha=0.5)

    if ax is None:
        plt.tight_layout()
        plt.show()
    fig_ret = fig if ax is None else None
    if ax is None and has_losses:
        axes_ret = axes
    else:
        axes_ret = (ax_main if ax is not None else ax)
    return fig_ret, axes_ret
