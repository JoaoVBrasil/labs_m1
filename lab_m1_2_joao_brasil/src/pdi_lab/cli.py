import argparse

from .operations import (
    brilho,
    contraste,
    negativo,
    limiarizacao,
    histograma,
    ler_imagem_cinza,
    salvar_histograma_csv,
    salvar_imagem,
)


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Laboratório M1.2 - Transformações de intensidade."
    )
    parser.add_argument("--input", required=True, help="Imagem de entrada.")
    parser.add_argument("--output", required=True, help="Arquivo de saída.")
    parser.add_argument(
        "--operation",
        required=True,
        choices=["brightness", "contrast", "negative", "threshold", "histogram"],
        help="Operação a executar.",
    )
    parser.add_argument("--value", type=int, help="Valor do brilho.")
    parser.add_argument("--alpha", type=float, help="Fator de contraste.")
    parser.add_argument("--threshold", type=int, help="Limiar entre 0 e 255.")
    return parser


def main():
    parser = criar_parser()
    args = parser.parse_args()

    try:
        imagem = ler_imagem_cinza(args.input)

        if args.operation == "brightness":
            if args.value is None:
                raise ValueError("--value é obrigatório para brightness.")
            salvar_imagem(brilho(imagem, args.value), args.output)

        elif args.operation == "contrast":
            if args.alpha is None:
                raise ValueError("--alpha é obrigatório para contrast.")
            if args.alpha < 0:
                raise ValueError("--alpha deve ser maior ou igual a 0.")
            salvar_imagem(contraste(imagem, args.alpha), args.output)

        elif args.operation == "negative":
            salvar_imagem(negativo(imagem), args.output)

        elif args.operation == "threshold":
            if args.threshold is None:
                raise ValueError("--threshold é obrigatório para threshold.")
            salvar_imagem(limiarizacao(imagem, args.threshold), args.output)

        elif args.operation == "histogram":
            salvar_histograma_csv(histograma(imagem), args.output)

        return 0

    except (ValueError, FileNotFoundError, OSError) as erro:
        parser.error(str(erro))
