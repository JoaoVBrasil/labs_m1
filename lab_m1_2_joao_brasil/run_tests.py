from pathlib import Path

from pdi_lab.operations import (
    ler_imagem_cinza,
    salvar_imagem,
    brilho,
    contraste,
    negativo,
    limiarizacao,
    histograma,
    salvar_histograma_csv,
)


PASTA_INPUT = Path("images/input")
PASTA_OUTPUT = Path("images/output")
PASTA_RESULTS = Path("results")


def executar_imagem(nome, testes):
    caminho = PASTA_INPUT / nome

    print(f"\nTestando: {nome}")

    imagem = ler_imagem_cinza(str(caminho))

    pasta_saida = PASTA_OUTPUT / caminho.stem
    pasta_saida.mkdir(parents=True, exist_ok=True)

    for teste in testes:
        operacao = teste["operacao"]
        nome_saida = teste["nome"]

        if operacao == "brilho":
            resultado = brilho(imagem, teste["valor"])

        elif operacao == "contraste":
            resultado = contraste(imagem, teste["alpha"])

        elif operacao == "negativo":
            resultado = negativo(imagem)

        elif operacao == "limiarizacao":
            resultado = limiarizacao(imagem, teste["limiar"])

        elif operacao == "histograma":
            resultado = histograma(imagem)

            PASTA_RESULTS.mkdir(parents=True, exist_ok=True)

            salvar_histograma_csv(
                resultado,
                str(PASTA_RESULTS / nome_saida)
            )

            continue

        else:
            raise ValueError(f"Operação desconhecida: {operacao}")

        salvar_imagem(
            resultado,
            str(pasta_saida / nome_saida)
        )

        # Permite gerar o histograma de uma imagem transformada.
        if teste.get("histograma"):
            contagens = histograma(resultado)

            PASTA_RESULTS.mkdir(parents=True, exist_ok=True)

            nome_histograma = teste["histograma"]

            salvar_histograma_csv(
                contagens,
                str(PASTA_RESULTS / nome_histograma)
            )


# ============================================================
# IMAGEM SINTÉTICA
# ============================================================

executar_imagem(
    "test_sintetica.png",
    [
        {
            "operacao": "brilho",
            "valor": -50,
            "nome": "brilho_-50.png",
        },
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
            "histograma": "test_sintetica_brilho_+50.csv",
        },
        {
            "operacao": "brilho",
            "valor": 100,
            "nome": "brilho_+100_saturacao.png",
        },
        {
            "operacao": "contraste",
            "alpha": 0.5,
            "nome": "contraste_0.5.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.0,
            "nome": "contraste_1.0.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
            "histograma": "test_sintetica_contraste_1.5.csv",
        },
        {
            "operacao": "negativo",
            "nome": "negativo.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 100,
            "nome": "limiar_100.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 200,
            "nome": "limiar_200.png",
        },
        {
            "operacao": "histograma",
            "nome": "test_sintetica_original.csv",
        },
    ],
)


# ============================================================
# CENA EM ESCALA DE CINZA
# ============================================================

executar_imagem(
    "m1_gray_scene_256.png",
    [
        {
            "operacao": "brilho",
            "valor": -50,
            "nome": "brilho_-50.png",
        },
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
            "histograma": "m1_gray_scene_brilho_+50.csv",
        },
        {
            "operacao": "contraste",
            "alpha": 0.5,
            "nome": "contraste_0.5.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.0,
            "nome": "contraste_1.0.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
            "histograma": "m1_gray_scene_contraste_1.5.csv",
        },
        {
            "operacao": "negativo",
            "nome": "negativo.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 100,
            "nome": "limiar_100.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 180,
            "nome": "limiar_180.png",
        },
        {
            "operacao": "histograma",
            "nome": "m1_gray_scene_original.csv",
        },
    ],
)


# ============================================================
# ESCALA DE CINZA COM 16 NÍVEIS
# ============================================================

executar_imagem(
    "m1_gray_steps_16levels.png",
    [
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
        },
        {
            "operacao": "contraste",
            "alpha": 0.5,
            "nome": "contraste_0.5.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.0,
            "nome": "contraste_1.0.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
        },
        {
            "operacao": "negativo",
            "nome": "negativo.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 100,
            "nome": "limiar_100.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 180,
            "nome": "limiar_180.png",
        },
        {
            "operacao": "histograma",
            "nome": "m1_gray_steps_16levels_original.csv",
        },
    ],
)


# ============================================================
# IMAGEM CONSTANTE
# ============================================================

executar_imagem(
    "m1_constant_128_64.png",
    [
        {
            "operacao": "brilho",
            "valor": -100,
            "nome": "brilho_-100.png",
        },
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
            "histograma": "m1_constant_brilho_+50.csv",
        },
        {
            "operacao": "contraste",
            "alpha": 0.5,
            "nome": "contraste_0.5.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
        },
        {
            "operacao": "histograma",
            "nome": "m1_constant_original.csv",
        },
    ],
)


# ============================================================
# TABULEIRO
# ============================================================

executar_imagem(
    "m1_checkerboard_256.png",
    [
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
        },
        {
            "operacao": "contraste",
            "alpha": 0.5,
            "nome": "contraste_0.5.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
        },
        {
            "operacao": "negativo",
            "nome": "negativo.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 100,
            "nome": "limiar_100.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 200,
            "nome": "limiar_200.png",
        },
        {
            "operacao": "histograma",
            "nome": "m1_checkerboard_original.csv",
        },
    ],
)


# ============================================================
# IMAGEM 5x5
# ============================================================

executar_imagem(
    "m1_gray_5x5.png",
    [
        {
            "operacao": "brilho",
            "valor": 50,
            "nome": "brilho_+50.png",
        },
        {
            "operacao": "contraste",
            "alpha": 1.5,
            "nome": "contraste_1.5.png",
        },
        {
            "operacao": "negativo",
            "nome": "negativo.png",
        },
        {
            "operacao": "limiarizacao",
            "limiar": 128,
            "nome": "limiar_128.png",
        },
        {
            "operacao": "histograma",
            "nome": "m1_gray_5x5_original.csv",
        },
    ],
)


print("\n" + "=" * 40)
print("TODOS OS TESTES FORAM EXECUTADOS!")
print("=" * 40)

print("\nImagens geradas em:")
print("images/output/")

print("\nHistogramas gerados em:")
print("results/")