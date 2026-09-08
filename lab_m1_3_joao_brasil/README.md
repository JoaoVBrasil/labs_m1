# Laboratório M1.3 — Convolução e Filtragem Espacial

Implementação em Python das operações de convolução, tratamento de bordas, suavização, Laplaciano e Sobel solicitadas no laboratório M1.3.

## Requisitos

- Python 3.10 ou superior
- Pillow
- NumPy
- pytest

## Preparação

A partir da raiz do projeto:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows:

```
.venv\Scripts\activate
```

## Testes automatizados

Para executar os testes unitários:

```
PYTHONPATH=src python -m pytest -q
```

Para executar automaticamente todas as operações do M1.3 e gerar as imagens de saída:

```
python run_tests.py
```

O script `run_tests.py` executa as operações implementadas e salva os resultados em:

```
images/output/
```

Após a execução, no macOS, a pasta pode ser aberta com:

```
open images/output
```

## Operações implementadas

O projeto implementa:

- Convolução genérica com kernels arbitrários;
- Tratamento de bordas `copy` e `replicate`;
- Filtro de média 3×3;
- Filtro de média ponderada 3×3;
- Filtro de média 5×5;
- Laplaciano;
- Realce utilizando a resposta do Laplaciano;
- Sobel Gx;
- Sobel Gy;
- Magnitude aproximada do Sobel;
- Magnitude Euclidiana do Sobel.

## Execução manual

As operações também podem ser executadas individualmente pela linha de comando.

### Convolução com kernel identidade

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/identity.png \
  --operation convolution \
  --kernel kernels/identity_3x3.txt \
  --border copy
```

### Média 3×3

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/mean3.png \
  --operation mean_filter \
  --size 3 \
  --border replicate
```

### Média ponderada 3×3

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/weighted3.png \
  --operation weighted_mean \
  --border replicate
```

### Média 5×5

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/mean5.png \
  --operation mean_filter \
  --size 5 \
  --border replicate
```

### Laplaciano

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/laplacian.png \
  --operation laplacian \
  --border replicate
```

### Laplaciano + realce

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/enhanced.png \
  --operation laplacian_enhance \
  --alpha 1.0 \
  --border replicate
```

### Sobel Gx

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/sobel_gx.png \
  --operation sobel_gx \
  --border replicate
```

### Sobel Gy

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/sobel_gy.png \
  --operation sobel_gy \
  --border replicate
```

### Sobel — magnitude aproximada

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/sobel_approx.png \
  --operation sobel_approx \
  --border replicate
```

### Sobel — magnitude Euclidiana

```
PYTHONPATH=src python -m pdi_lab \
  --input images/input/test.png \
  --output images/output/sobel_euclidean.png \
  --operation sobel_euclidean \
  --border replicate
```

## Implementação manual

O percurso da vizinhança, a convolução, a aplicação dos kernels e o tratamento das bordas são implementados explicitamente em:

```
src/pdi_lab/core.py
```

Pillow é utilizado para leitura e escrita das imagens, enquanto NumPy é utilizado para representar matrizes e realizar operações aritméticas.

Não são utilizados filtros prontos de bibliotecas para substituir as operações avaliadas no laboratório.

## Tratamento de bordas

Foram implementadas duas estratégias:

- `copy`: pixels fora dos limites não são utilizados e o valor original do pixel é preservado;
- `replicate`: as coordenadas fora dos limites são ajustadas para o pixel válido mais próximo.

Exemplo:

```
--border copy
```

ou:

```
--border replicate
```

## Estrutura do projeto

```
lab_m1_3_joao_brasil/
├── README.md
├── REPORT.md
├── AI_USAGE.md
├── lab.json
├── run_tests.py
├── requirements.txt
│
├── src/
│   └── pdi_lab/
│       ├── __init__.py
│       ├── __main__.py
│       └── core.py
│
├── tests/
│   └── test_core.py
│
├── kernels/
│   ├── identity_3x3.txt
│   ├── mean_3x3.txt
│   ├── weighted_mean_3x3.txt
│   ├── mean_5x5.txt
│   ├── laplacian_3x3.txt
│   ├── sobel_gx_3x3.txt
│   └── sobel_gy_3x3.txt
│
├── images/
│   ├── input/
│   └── output/
│
└── results/
```

## Resultados

As imagens geradas pelos experimentos ficam armazenadas em:

```
images/output/
```

Os registros e resultados auxiliares dos testes ficam em:

```
results/
```

## Relatório

O arquivo `REPORT.md` contém o mini relatório técnico do laboratório, incluindo objetivo, operações implementadas, decisões de implementação, testes, resultados e análise dos conceitos solicitados.

## Uso de Inteligência Artificial

O arquivo `AI_USAGE.md` apresenta a declaração de uso de ferramentas de Inteligência Artificial durante o desenvolvimento do laboratório, conforme solicitado pelas orientações da atividade.