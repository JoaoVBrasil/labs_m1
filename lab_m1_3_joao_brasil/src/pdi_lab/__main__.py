from __future__ import annotations
import argparse
import sys
import numpy as np
from .core import (load_grayscale, save_image, read_kernel, convolution,
                   mean_kernel, weighted_mean_kernel, laplacian_kernel,
                   laplacian_enhance, sobel)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Laboratório M1.3 - convolução e filtragem espacial")
    p.add_argument("--input", required=True, help="imagem de entrada")
    p.add_argument("--output", required=True, help="arquivo de saída ou diretório")
    p.add_argument("--operation", required=True, choices=[
        "convolution", "mean_filter", "weighted_mean", "laplacian", "laplacian_enhance",
        "sobel_gx", "sobel_gy", "sobel_approx", "sobel_euclidean"
    ])
    p.add_argument("--kernel", help="arquivo do kernel")
    p.add_argument("--border", choices=["copy", "replicate"], default="copy")
    p.add_argument("--size", type=int, choices=[3, 5], help="tamanho do filtro de média")
    p.add_argument("--alpha", type=float, default=1.0, help="fator do realce Laplaciano")
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        image = load_grayscale(args.input)
        op = args.operation
        if op == "convolution":
            if not args.kernel:
                raise ValueError("--kernel é obrigatório para convolution")
            result = convolution(image, read_kernel(args.kernel), args.border)
        elif op == "mean_filter":
            result = convolution(image, mean_kernel(args.size or 3), args.border)
        elif op == "weighted_mean":
            result = convolution(image, weighted_mean_kernel(), args.border)
        elif op == "laplacian":
            result = convolution(image, laplacian_kernel(), args.border)
        elif op == "laplacian_enhance":
            response = convolution(image, laplacian_kernel(), args.border)
            result = laplacian_enhance(image, response, args.alpha)
        else:
            gx, gy, approx, euclidean = sobel(image, args.border)
            result = {"sobel_gx": gx, "sobel_gy": gy,
                      "sobel_approx": approx, "sobel_euclidean": euclidean}[op]
        save_image(result, args.output)
        return 0
    except (OSError, ValueError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
