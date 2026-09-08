# Mini Relatório — Laboratório M1.2

## 1. Identificação

- **Laboratório:** M1.2 — Transformações de intensidade
- **Linguagem:** Python
- **Estudante:** João Vitor Schwambach Brasil

## 2. Objetivo

Implementar transformações pontuais em imagens em níveis de cinza e analisar como essas operações alteram os valores dos pixels e a distribuição das intensidades.

## 3. Operações implementadas

Foram implementadas as seguintes operações:

- Ajuste de brilho: `g(x,y) = f(x,y) + b`
- Ajuste de contraste: `g(x,y) = α(f(x,y)-128)+128`
- Negativo: `g(x,y) = 255-f(x,y)`
- Limiarização binária
- Histograma manual com 256 posições

As operações foram implementadas com percurso explícito dos pixels, sem utilizar funções prontas para realizar as transformações solicitadas.

## 4. Testes realizados

Os testes foram realizados utilizando as imagens fornecidas para o laboratório e uma imagem sintética pequena, permitindo também a conferência manual dos resultados.

Foram realizados testes com:

- brilho negativo (`b = -50`);
- brilho positivo (`b = +50`);
- brilho positivo com saturação (`b = +100` na imagem sintética);
- contraste reduzido (`α = 0,5`);
- contraste identidade (`α = 1,0`);
- contraste aumentado (`α = 1,5`);
- negativo;
- dois valores distintos de limiarização na mesma imagem;
- histogramas da imagem original;
- histogramas de imagens após transformações;
- casos de saturação abaixo de 0 e acima de 255;
- imagem sintética de `4 × 4` pixels para conferência direta dos valores.

Também foram executados testes automatizados com `pytest`, totalizando 14 testes, todos aprovados.

## 5. Resultados

### 5.1 Brilho

O ajuste de brilho apresentou o comportamento esperado. Com `b > 0`, os valores dos pixels foram aumentados, tornando a imagem mais clara. Com `b < 0`, os valores foram reduzidos, tornando a imagem mais escura.

Nos casos em que o resultado ultrapassou o intervalo válido de `0` a `255`, os valores foram limitados ao respectivo extremo.

Os resultados foram testados tanto na imagem sintética quanto nas imagens fornecidas para o laboratório.

### 5.2 Contraste

Com `α = 1,0`, os valores de intensidade foram mantidos.

Com `α = 0,5`, os valores foram aproximados de 128, reduzindo a diferença entre regiões claras e escuras.

Com `α = 1,5`, os valores foram afastados de 128, aumentando a diferença entre as intensidades. Valores que ultrapassaram os limites de `0` e `255` foram saturados.

### 5.3 Negativo

A transformação de negativo foi aplicada utilizando `255 - f(x,y)`.

Os valores baixos da imagem original passaram a apresentar valores altos e os valores altos passaram a apresentar valores baixos. Por exemplo, uma intensidade 0 passou para 255, enquanto uma intensidade 255 passou para 0.

### 5.4 Limiarização

Foram utilizados dois valores diferentes de limiar na mesma imagem, conforme solicitado.

Na limiarização, os pixels com intensidade menor que o limiar foram convertidos para `0`, enquanto os pixels com intensidade maior ou igual ao limiar foram convertidos para `255`.

O resultado é uma imagem contendo apenas duas intensidades.

### 5.5 Histograma

Foi implementado manualmente um histograma com 256 posições, correspondentes às intensidades de `0` a `255`.

Foram gerados histogramas para imagens originais e transformadas. A soma das quantidades de pixels dos histogramas foi conferida e corresponde ao número total de pixels das respectivas imagens.

Por exemplo, os histogramas das imagens de `256 × 256` pixels contabilizaram `65536` pixels, enquanto o histograma da imagem sintética de `4 × 4` contabilizou `16` pixels.

Os histogramas foram armazenados em arquivos CSV na pasta `results/`.

## 6. Análise

### 6.1 Diferença entre alteração de brilho e alteração de contraste

A alteração de brilho modifica todos os pixels adicionando ou subtraindo um mesmo valor. Dessa forma, a distribuição das intensidades tende a se deslocar para valores maiores ou menores.

A alteração de contraste modifica a distância dos valores em relação à intensidade 128. Com contraste reduzido, os valores ficam mais próximos de 128. Com contraste aumentado, os valores ficam mais afastados de 128.

Assim, o brilho altera principalmente a posição das intensidades, enquanto o contraste altera a distribuição das intensidades em torno de um valor central.

### 6.2 Saturação

A saturação ocorreu quando uma transformação produziu valores fora do intervalo permitido de `0` a `255`.

No teste de brilho negativo, valores que ficaram abaixo de `0` foram limitados a `0`. No teste de brilho positivo, valores que ultrapassaram `255` foram limitados a `255`.

Também podem ocorrer saturações com o aumento do contraste (`α = 1,5`) para intensidades suficientemente distantes de 128.

O efeito da saturação é a perda da diferença entre valores que ultrapassam o limite. Por exemplo, valores diferentes que resultariam em intensidades maiores que 255 passam a ser representados pelo mesmo valor `255`.

### 6.3 Histograma após alteração do brilho

Após o aumento do brilho, o histograma se deslocou em direção às intensidades maiores.

No teste com `b = +50`, os valores foram deslocados em aproximadamente 50 níveis para a direita quando não ocorreu saturação.

Quando os valores ultrapassaram 255, eles foram concentrados na intensidade 255. Dessa forma, a saturação pode aumentar a quantidade de pixels nessa extremidade do histograma.

No caso de redução do brilho, ocorre o comportamento contrário, com deslocamento para intensidades menores e possibilidade de concentração na intensidade 0.

### 6.4 Distribuição após alteração do contraste

Com `α = 0,5`, a distribuição das intensidades foi comprimida em direção ao valor central 128. Isso reduz a diferença entre regiões claras e escuras.

Com `α = 1,0`, a distribuição permanece igual à original.

Com `α = 1,5`, a distribuição é expandida em relação a 128. As intensidades menores tendem a ficar ainda menores e as maiores tendem a ficar ainda maiores. Quando os valores ultrapassam os limites da imagem, ocorre saturação em 0 ou 255.

### 6.5 Informação perdida após a limiarização

A limiarização transforma a imagem em apenas dois valores: `0` e `255`.

Com isso, as diferentes intensidades presentes na imagem original deixam de ser representadas. Pixels que possuíam valores diferentes, mas estavam do mesmo lado do limiar, passam a ter exatamente o mesmo valor.

Portanto, a operação mantém principalmente a separação entre as regiões abaixo e acima do limiar, mas perde as informações de intensidade dentro dessas regiões.

## 7. Guardas e limitações

A implementação possui verificações para:

- falha na leitura da imagem;
- imagens que não estão em níveis de cinza;
- imagens que não utilizam intensidades de 8 bits;
- limiar fora do intervalo de `0` a `255`;
- valores menores que `0`;
- valores maiores que `255`;
- conversão dos valores `uint8` para inteiros durante os cálculos;
- conversão dos resultados para `uint8`;
- arredondamento dos resultados do cálculo de contraste.

Esses comportamentos também foram incluídos nos testes automatizados. Ao final, foram executados 14 testes com `pytest`, todos aprovados.

## 8. Execução

Os testes experimentais podem ser executados com:

```
PYTHONPATH=src python3 run_tests.py
```

Os testes automatizados podem ser executados com:

```
PYTHONPATH=src pytest
```

As imagens processadas são armazenadas em:

```
images/output/
```

Os histogramas em formato CSV são armazenados em:

```
results/
```

## 9. Conclusão

Os testes realizados permitiram verificar o funcionamento das transformações de intensidade implementadas.

Os resultados mostraram os comportamentos esperados para alteração de brilho, contraste, negativo e limiarização. Também foi possível observar o efeito da saturação e a alteração da distribuição das intensidades por meio dos histogramas.

A utilização da imagem sintética permitiu conferir diretamente os valores dos pixels e validar as operações em um caso pequeno antes da análise das imagens maiores.