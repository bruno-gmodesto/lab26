from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from lab.am.classificacao import plot_decision_boundary
from lab.am.modelos import Perceptron, MLP, train_model
import torch
import matplotlib.pyplot as plt


X, y = make_moons(n_samples=300, noise=0.2, random_state=42)
X = StandardScaler().fit_transform(X)

Xt = torch.tensor(X, dtype=torch.float32)
yt = torch.tensor(y, dtype=torch.float32)

# --- Perceptron ---
perceptron = Perceptron(in_features=2)
losses_p = train_model(perceptron, Xt, yt, epochs=500, lr=1e-2)

plot_decision_boundary(perceptron, Xt, yt, dr="pca", d=2,
                       title="Perceptron · moons · PCA 2D",
                       losses=losses_p)

# --- MLP ---
mlp = MLP(in_features=2, hidden=16)
losses_m = train_model(mlp, Xt, yt, epochs=500, lr=1e-2)

plot_decision_boundary(mlp, Xt, yt, dr="pca", d=2,
                       title="MLP · moons · PCA 2D",
                       losses=losses_m)
plot_decision_boundary(mlp, Xt, yt, dr="tsne", d=2,
                       title="MLP · moons · t-SNE 2D",
                       losses=losses_m)

# --- Decision Tree ---
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X, y)

plot_decision_boundary(tree, X, y, dr="pca", d=2,
                       title="Decision Tree · moons · PCA 2D")
plot_decision_boundary(tree, X, y, dr="tsne", d=2,
                       title="Decision Tree · moons · t-SNE 2D")

projections = ["pca", "tsne"]
models = [
    ("Perceptron", perceptron, Xt, yt, losses_p),
    ("MLP", mlp, Xt, yt, losses_m),
    ("Decision Tree", tree, X, y, None),
]

for dr in projections:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, (name, model, Xdata, ydata, losses) in enumerate(models):
        plot_decision_boundary(
            model, Xdata, ydata, dr=dr, d=2,
            title=f"{name} · moons · {dr.upper()} 2D",
            losses=losses,
            ax=axes[i]
        )
    fig.suptitle(f"Decision Boundaries ({dr.upper()})", fontsize=16)
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()
