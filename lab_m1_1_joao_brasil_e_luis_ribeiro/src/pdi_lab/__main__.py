import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


def inspect_image(image: np.ndarray) -> None:
    if image is None:
        return

    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]
    dtype = image.dtype
    pixels = width * height

    print("=== Inspeção da imagem ===")
    print(f"Largura: {width}")
    print(f"Altura: {height}")
    print(f"Canais: {channels}")
    print(f"Tipo: {dtype}")
    print(f"Quantidade de pixels: {pixels}")

    if channels == 1:
        values = image.flatten().astype(np.float64)
        print(f"Valor mínimo: {int(values.min())}")
        print(f"Valor máximo: {int(values.max())}")
        print(f"Média das intensidades: {float(values.mean()):.2f}")
    else:
        for idx, name in enumerate(["B", "G", "R"][:channels]):
            channel = image[:, :, idx].astype(np.float64)
            print(f"--- Canal {name} ---")
            print(f"Mínimo: {int(channel.min())}")
            print(f"Máximo: {int(channel.max())}")
            print(f"Média: {float(channel.mean()):.2f}")


def manual_copy(image: np.ndarray) -> np.ndarray:
    result = np.zeros_like(image)
    height, width = image.shape[:2]

    if image.ndim == 2:
        for row in range(height):
            for col in range(width):
                result[row, col] = image[row, col]
    else:
        channels = image.shape[2]
        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    result[row, col, channel] = image[row, col, channel]
    return result


def separate_channel(image: np.ndarray, channel_index: int) -> np.ndarray:
    if image.ndim == 2:
        raise ValueError("A imagem deve ser colorida para separar canais.")

    result = np.zeros_like(image)
    result[:, :, channel_index] = image[:, :, channel_index]
    return result


def grayscale_average(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    result = np.zeros((height, width), dtype=np.uint8)

    if image.ndim == 2:
        return manual_copy(image)

    for row in range(height):
        for col in range(width):
            b, g, r = image[row, col]
            average = int(round((int(b) + int(g) + int(r)) / 3.0))
            result[row, col] = np.clip(average, 0, 255)

    return result


def grayscale_weighted(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    result = np.zeros((height, width), dtype=np.uint8)

    if image.ndim == 2:
        return manual_copy(image)

    for row in range(height):
        for col in range(width):
            b, g, r = image[row, col]
            weighted = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)
            result[row, col] = np.clip(int(round(weighted)), 0, 255)

    return result


def quantize_grayscale(image: np.ndarray, levels: int) -> np.ndarray:
    if levels < 2:
        raise ValueError("A quantização exige pelo menos 2 níveis.")

    if image.ndim != 2:
        image = grayscale_weighted(image)

    result = np.zeros_like(image)
    height, width = image.shape[:2]
    max_level = levels - 1
    for row in range(height):
        for col in range(width):
            value = int(image[row, col])
            quantized = int(round((value * max_level) / 255.0))
            result[row, col] = int(round((quantized * 255.0) / max_level))

    return result


def save_image(image: np.ndarray, path: Path) -> None:
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), image)
    if not success:
        raise IOError(f"Falha ao salvar a imagem em {path}")


def get_output_path(base_output: Path, default_name: str) -> Path:
    if base_output.is_dir() or str(base_output).endswith(("/", "\\")):
        return base_output / default_name
    return base_output


def generate_all_outputs(image: np.ndarray, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        (manual_copy(image), "copy.png"),
        (separate_channel(image, 0), "channel_b.png"),
        (separate_channel(image, 1), "channel_g.png"),
        (separate_channel(image, 2), "channel_r.png"),
        (grayscale_average(image), "gray_average.png"),
        (grayscale_weighted(image), "gray_weighted.png"),
        (quantize_grayscale(image, 16), "quant_16.png"),
        (quantize_grayscale(image, 8), "quant_8.png"),
        (quantize_grayscale(image, 4), "quant_4.png"),
        (quantize_grayscale(image, 2), "quant_2.png"),
    ]

    saved_paths: list[Path] = []
    for result, filename in tasks:
        output = output_dir / filename
        save_image(result, output)
        saved_paths.append(output)

    return saved_paths


def lab_1(args: argparse.Namespace) -> None:
    print("Executando o laboratório M1.1 - Processamento de Imagens")

    image = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Erro: não foi possível ler a imagem em {args.input}")
        sys.exit(1)

    inspect_image(image)

    operation = args.operation
    output_base = Path(args.output)

    if operation == "inspect":
        print("Inspeção concluída.")
        return

    if operation == "all":
        saved = generate_all_outputs(image, output_base)
        print("Resultados salvos em:")
        for item in saved:
            print(item)
        return

    if operation == "copy":
        result = manual_copy(image)
        output = get_output_path(output_base, "copy.png")
    elif operation == "channel_b":
        result = separate_channel(image, 0)
        output = get_output_path(output_base, "channel_b.png")
    elif operation == "channel_g":
        result = separate_channel(image, 1)
        output = get_output_path(output_base, "channel_g.png")
    elif operation == "channel_r":
        result = separate_channel(image, 2)
        output = get_output_path(output_base, "channel_r.png")
    elif operation == "grayscale_average":
        result = grayscale_average(image)
        output = get_output_path(output_base, "gray_average.png")
    elif operation == "grayscale_weighted":
        result = grayscale_weighted(image)
        output = get_output_path(output_base, "gray_weighted.png")
    elif operation == "quantize":
        if args.levels is None:
            print("Erro: --levels é obrigatório para a operação de quantização.")
            sys.exit(1)
        result = quantize_grayscale(image, args.levels)
        output = get_output_path(output_base, f"quant_{args.levels}.png")
    else:
        print(f"Operação desconhecida: {operation}")
        sys.exit(1)

    save_image(result, output)
    print(f"Resultado salvo em: {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Laboratório M1.1 - Processamento de Imagens")
    parser.add_argument("--input", required=True, help="Caminho da imagem de entrada")
    parser.add_argument("--output", required=True, help="Caminho da imagem de saída ou diretório")
    parser.add_argument(
        "--operation",
        required=True,
        choices=[
            "inspect",
            "all",
            "copy",
            "channel_b",
            "channel_g",
            "channel_r",
            "grayscale_average",
            "grayscale_weighted",
            "quantize",
        ],
        help="Operação a ser realizada",
    )
    parser.add_argument("--levels", type=int, help="Quantidade de níveis para a quantização")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    lab_1(args)


if __name__ == "__main__":
    main()
