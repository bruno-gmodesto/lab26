"""
modelos.py
----------
Pequeno módulo com modelos PyTorch reutilizáveis e um utilitário de treino.
Objetivo: manter a parte experimental (`aprendizado/decision-boundary-torch.py`) pura.
"""

from __future__ import annotations

import torch
import torch.nn as nn
from typing import Optional, Iterable, Union


class Perceptron(nn.Module):
    """Perceptron binário simples com saída sigmoide (probabilidade).

    Forward retorna um tensor 1-D de probabilidades (shape: (n,)).
    """

    def __init__(self, in_features: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(1)


class MLP(nn.Module):
    """Pequena MLP para classificação binária com saída sigmoide.

    Forward retorna um tensor 1-D de probabilidades (shape: (n,)).
    """

    def __init__(self, in_features: int = 2, hidden: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(1)


def train_model(
    model: nn.Module,
    X: Union[torch.Tensor, Iterable[float]],
    y: Union[torch.Tensor, Iterable[float]],
    loss_fn: Optional[nn.Module] = None,
    optimizer: Optional[torch.optim.Optimizer] = None,
    lr: float = 1e-2,
    epochs: int = 500,
    device: Optional[str] = None,
) -> list:
    """Train a PyTorch model on the provided tensors or array-likes.

    Returns the list of loss values (one per epoch).

    Notes
    -----
    - If X or y are numpy arrays (or lists), they will be converted to torch.float32.
    - By default uses BCE loss and Adam optimizer (matching the original experimental script).
    - The model is moved temporarily to `device` for training and returned to CPU afterwards.
    """
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    if not isinstance(X, torch.Tensor):
        X = torch.tensor(X, dtype=torch.float32, device=device)
    else:
        X = X.to(device)

    if not isinstance(y, torch.Tensor):
        y = torch.tensor(y, dtype=torch.float32, device=device)
    else:
        y = y.to(device)

    loss_fn = loss_fn or nn.BCELoss()
    optimizer = optimizer or torch.optim.Adam(model.parameters(), lr=lr)

    losses: list = []
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        out = model(X)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    model.to("cpu")
    return losses


__all__ = ["Perceptron", "MLP", "train_model"]
