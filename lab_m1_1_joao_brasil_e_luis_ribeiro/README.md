# Laboratório M1.1 — Processamento de Imagens

## Objetivo

Implementar operações básicas de leitura, inspeção, cópia, separação de canais, conversão para tons de cinza e quantização de imagens.

## Estrutura

```text
lab_m1_1/
├── README.md
├── REPORT.md
├── AI_USAGE.md
├── lab.json
├── pyproject.toml
├── requirements.txt
├── images/
│   ├── input/
│   └── output/
├── results/
├── src/
│   └── pdi_lab/
│       ├── __init__.py
│       ├── __main__.py
│       └── lab_m1_1.py
└── tests/
```

## Ambiente

```bash
cd lab_m1_1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Execução

```bash
python -m pdi_lab --help
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation inspect
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation copy
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation channel_b
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation grayscale_average
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation grayscale_weighted
```

```bash
python -m pdi_lab \
  --input images/input/aranha.png \
  --output images/output \
  --operation quantize \
  --levels 8
```

## Saídas esperadas

A execução do laboratório produz arquivos no diretório `images/output`, incluindo, por exemplo:

- `copy.png`
- `channel_b.png`
- `channel_g.png`
- `channel_r.png`
- `gray_average.png`
- `gray_weighted.png`
- `quant_16.png`
- `quant_8.png`
- `quant_4.png`
- `quant_2.png`

## Validação

```bash
python -m pytest -q
```

Os testes automatizados validam cópia, ordem dos canais, conversões de cinza, quantização e comportamento em valores de fronteira.

## Observações

- O projeto usa linha de comando e não depende de interface gráfica.
- A entrada e saída são tratadas via caminhos relativos ao projeto.
- O pytest serve como mecanismo de verificação automatizada das operações e das saídas esperadas.
