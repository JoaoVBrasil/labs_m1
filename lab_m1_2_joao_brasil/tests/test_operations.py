import numpy as np
import pytest

from pdi_lab.operations import brilho, contraste, negativo, limiarizacao, histograma


def imagem_teste():
    return np.array([[0, 64, 128], [192, 255, 100]], dtype=np.uint8)


def test_brilho_positivo():
    esperado = np.array([[30, 94, 158], [222, 255, 130]], dtype=np.uint8)
    assert np.array_equal(brilho(imagem_teste(), 30), esperado)


def test_brilho_negativo():
    esperado = np.array([[0, 14, 78], [142, 205, 50]], dtype=np.uint8)
    assert np.array_equal(brilho(imagem_teste(), -50), esperado)


def test_brilho_saturacao():
    imagem = np.array([[250, 5]], dtype=np.uint8)
    esperado = np.array([[255, 25]], dtype=np.uint8)
    assert np.array_equal(brilho(imagem, 20), esperado)


def test_contraste_1():
    imagem = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    esperado = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    assert np.array_equal(contraste(imagem, 1.0), esperado)


def test_contraste_05():
    imagem = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    esperado = np.array([[64, 96, 128, 160, 192]], dtype=np.uint8)
    assert np.array_equal(contraste(imagem, 0.5), esperado)


def test_contraste_15():
    imagem = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
    esperado = np.array([[0, 32, 128, 224, 255]], dtype=np.uint8)
    assert np.array_equal(contraste(imagem, 1.5), esperado)


def test_negativo():
    esperado = np.array([[255, 191, 127], [63, 0, 155]], dtype=np.uint8)
    assert np.array_equal(negativo(imagem_teste()), esperado)


def test_limiarizacao():
    imagem = np.array([[0, 100, 128, 200, 255]], dtype=np.uint8)
    esperado = np.array([[0, 0, 255, 255, 255]], dtype=np.uint8)
    assert np.array_equal(limiarizacao(imagem, 128), esperado)


def test_limiar_invalido():
    imagem = imagem_teste()
    with pytest.raises(ValueError):
        limiarizacao(imagem, -1)
    with pytest.raises(ValueError):
        limiarizacao(imagem, 256)


def test_histograma():
    imagem = np.array([[0, 1, 1], [2, 2, 2]], dtype=np.uint8)
    resultado = histograma(imagem)
    assert len(resultado) == 256
    assert resultado[0] == 1
    assert resultado[1] == 2
    assert resultado[2] == 3
    assert sum(resultado) == 6

def test_brilho_saturacao_inferior():
    imagem = np.array([[10, 50]], dtype=np.uint8)
    esperado = np.array([[0, 0]], dtype=np.uint8)

    assert np.array_equal(brilho(imagem, -100), esperado)


def test_imagem_colorida_invalida():
    imagem = np.zeros((2, 2, 3), dtype=np.uint8)

    with pytest.raises(ValueError):
        brilho(imagem, 10)


def test_tipo_invalido():
    imagem = np.zeros((2, 2), dtype=np.float32)

    with pytest.raises(ValueError):
        brilho(imagem, 10)


def test_imagem_invalida():
    with pytest.raises(ValueError):
        brilho(None, 10)