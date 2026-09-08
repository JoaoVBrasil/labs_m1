import cv2
import numpy as np


def validar_imagem_cinza(imagem):
    if imagem is None:
        raise ValueError("Falha ao abrir a imagem.")

    if len(imagem.shape) != 2:
        raise ValueError("A operação exige uma imagem em níveis de cinza.")

    if imagem.dtype != np.uint8:
        raise ValueError("A imagem deve utilizar intensidades de 8 bits.")


def brilho(imagem, valor):
    validar_imagem_cinza(imagem)
    resultado = np.empty_like(imagem)

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            novo_valor = int(imagem[y, x]) + valor

            if novo_valor < 0:
                novo_valor = 0
            elif novo_valor > 255:
                novo_valor = 255

            resultado[y, x] = novo_valor

    return resultado


def contraste(imagem, alpha):
    validar_imagem_cinza(imagem)
    resultado = np.empty_like(imagem)

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            novo_valor = alpha * (int(imagem[y, x]) - 128) + 128
            novo_valor = int(round(novo_valor))

            if novo_valor < 0:
                novo_valor = 0
            elif novo_valor > 255:
                novo_valor = 255

            resultado[y, x] = novo_valor

    return resultado


def negativo(imagem):
    validar_imagem_cinza(imagem)
    resultado = np.empty_like(imagem)

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            resultado[y, x] = 255 - int(imagem[y, x])

    return resultado


def limiarizacao(imagem, limiar):
    validar_imagem_cinza(imagem)

    if limiar < 0 or limiar > 255:
        raise ValueError("O limiar deve estar entre 0 e 255.")

    resultado = np.empty_like(imagem)

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            resultado[y, x] = 0 if int(imagem[y, x]) < limiar else 255

    return resultado


def histograma(imagem):
    validar_imagem_cinza(imagem)
    contagens = [0] * 256

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            intensidade = int(imagem[y, x])
            contagens[intensidade] += 1

    return contagens


def salvar_histograma_csv(contagens, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("intensidade,quantidade\n")
        for intensidade in range(256):
            arquivo.write(f"{intensidade},{contagens[intensidade]}\n")


def ler_imagem_cinza(caminho):
    imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)

    if imagem is None:
        raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

    return imagem


def salvar_imagem(imagem, caminho):
    sucesso = cv2.imwrite(caminho, imagem)

    if not sucesso:
        raise OSError(f"Não foi possível salvar a imagem: {caminho}")
