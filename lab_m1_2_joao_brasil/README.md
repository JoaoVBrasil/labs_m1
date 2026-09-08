# Processamento de Imagens — Laboratório M1.2

## Transformações de intensidade

Implementação em Python das operações obrigatórias do Laboratório M1.2:

- ajuste de brilho;
- ajuste de contraste;
- negativo;
- limiarização binária;
- histograma manual.

As transformações são percorridas explicitamente pelos pixels e não utilizam funções prontas que realizem diretamente as operações avaliadas.

## Requisitos

- Python 3
- NumPy
- OpenCV
- pytest

## Preparação

### macOS/Linux

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Em outros ambientes, o comando `python` pode ser utilizado no lugar de `python3`, conforme a configuração local.

## Execução

Para verificar as opções disponíveis:

```
PYTHONPATH=src python3 -m pdi_lab --help
```

### Brilho

```
PYTHONPATH=src python3 -m pdi_lab --input images/input/test_sintetica.png --output images/output/brightness.png --operation brightness --value 30
```

### Contraste

```
PYTHONPATH=src python3 -m pdi_lab --input images/input/test_sintetica.png --output images/output/contrast.png --operation contrast --alpha 1.5
```

### Negativo

```
PYTHONPATH=src python3 -m pdi_lab --input images/input/test_sintetica.png --output images/output/negative.png --operation negative
```

### Limiarização

```
PYTHONPATH=src python3 -m pdi_lab --input images/input/test_sintetica.png --output images/output/threshold.png --operation threshold --threshold 128
```

### Histograma

```
PYTHONPATH=src python3 -m pdi_lab --input images/input/test_sintetica.png --output results/histogram.csv --operation histogram
```

## Testes experimentais

Os testes experimentais utilizados na entrega podem ser executados com:

```
PYTHONPATH=src python3 run_tests.py
```

Foram utilizados a imagem sintética `test_sintetica.png` e imagens fornecidas para o laboratório.

Os testes abrangem:

- brilho com valores positivos e negativos;
- casos de saturação;
- contraste com `α = 0,5`, `1,0` e `1,5`;
- negativo;
- limiarização com diferentes valores de limiar;
- geração de histogramas;
- conferência de histogramas originais e transformados.

As imagens processadas são armazenadas em `images/output/`.

Os histogramas em formato CSV são armazenados em `results/`.

## Testes automatizados

Para executar os testes automatizados:

```
PYTHONPATH=src pytest
```

A suíte possui 14 testes automatizados, incluindo verificações das operações, saturação e tratamento de entradas inválidas.

## Estrutura

```
.
├── images/
│   ├── input/
│   └── output/
├── results/
├── src/
│   └── pdi_lab/
│       ├── __init__.py
│       ├── main.py
│       ├── cli.py
│       └── operations.py
├── tests/
│   └── test_operations.py
├── run_tests.py
├── REPORT.md
├── AI_USAGE.md
├── lab.json
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```