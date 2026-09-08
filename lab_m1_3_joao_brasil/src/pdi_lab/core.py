from __future__ import annotations
from typing import Sequence
import math
import numpy as np
from PIL import Image

Array = np.ndarray


def load_grayscale(path: str) -> Array:
    img = Image.open(path).convert("L")
    return np.asarray(img, dtype=np.uint8)


def save_image(arr: Array, path: str) -> None:
    clipped = np.clip(np.rint(arr), 0, 255).astype(np.uint8)
    Image.fromarray(clipped, mode="L").save(path)


def validate_kernel(kernel: Array) -> None:
    if kernel is None or np.asarray(kernel).size == 0:
        raise ValueError("kernel vazio")
    k = np.asarray(kernel, dtype=np.float64)
    if k.ndim != 2 or k.shape[0] != k.shape[1]:
        raise ValueError("kernel deve ser quadrado")
    if k.shape[0] % 2 == 0:
        raise ValueError("kernel deve ter dimensão ímpar")


def read_kernel(path: str) -> Array:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except OSError as e:
        raise ValueError(f"não foi possível abrir o kernel: {e}") from e
    if not lines:
        raise ValueError("kernel vazio")
    try:
        dims = lines[0].split()
        if len(dims) != 2:
            raise ValueError
        rows, cols = map(int, dims)
        values = [float(x) for line in lines[1:] for x in line.split()]
    except ValueError as e:
        raise ValueError("formato de kernel inválido") from e
    if rows <= 0 or cols <= 0 or len(values) != rows * cols:
        raise ValueError("quantidade de valores do kernel inválida")
    kernel = np.array(values, dtype=np.float64).reshape(rows, cols)
    validate_kernel(kernel)
    return kernel


def _coord(i: int, limit: int, border: str) -> int | None:
    if 0 <= i < limit:
        return i
    if border == "replicate":
        return max(0, min(i, limit - 1))
    if border == "copy":
        return None
    raise ValueError("estratégia de borda inválida: use copy ou replicate")


def convolution(image: Array, kernel: Array, border: str = "copy") -> Array:
    validate_kernel(kernel)
    if image.ndim != 2:
        raise ValueError("a imagem deve estar em níveis de cinza")
    if border not in {"copy", "replicate"}:
        raise ValueError("estratégia de borda inválida: use copy ou replicate")
    k = np.asarray(kernel, dtype=np.float64)
    h, w = image.shape
    r = k.shape[0] // 2
    out = image.astype(np.float64).copy()
    # Convolução propriamente dita: o kernel é invertido nos dois eixos.
    k = np.flip(k, axis=(0, 1))
    src = image.astype(np.float64)
    for y in range(h):
        for x in range(w):
            acc = 0.0
            valid = True
            for ky in range(-r, r + 1):
                sy = _coord(y + ky, h, border)
                if sy is None:
                    valid = False
                    break
                for kx in range(-r, r + 1):
                    sx = _coord(x + kx, w, border)
                    if sx is None:
                        valid = False
                        break
                    acc += src[sy, sx] * k[ky + r, kx + r]
                if not valid:
                    break
            if valid:
                out[y, x] = acc
    return out


def mean_kernel(size: int) -> Array:
    if size <= 0 or size % 2 == 0:
        raise ValueError("tamanho do kernel deve ser positivo e ímpar")
    return np.full((size, size), 1.0 / (size * size), dtype=np.float64)


def weighted_mean_kernel() -> Array:
    return np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float64) / 16.0


def laplacian_kernel() -> Array:
    return np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)


def sobel_kernels() -> tuple[Array, Array]:
    gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    return gx, gy


def laplacian_enhance(image: Array, response: Array, amount: float = 1.0) -> Array:
    # Realce: f - alpha * Laplaciano, mantendo o cálculo em ponto flutuante.
    return image.astype(np.float64) - amount * response


def sobel(image: Array, border: str = "copy") -> tuple[Array, Array, Array, Array]:
    gx_kernel, gy_kernel = sobel_kernels()
    gx = convolution(image, gx_kernel, border)
    gy = convolution(image, gy_kernel, border)
    approx = np.abs(gx) + np.abs(gy)
    euclidean = np.sqrt(gx * gx + gy * gy)
    return gx, gy, approx, euclidean
