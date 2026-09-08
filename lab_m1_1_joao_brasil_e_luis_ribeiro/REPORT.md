# Mini relatório técnico — Lab M1.1

## Identificação

- Estudante: Luis Gustavo de Souza Ribeiro
- Matrícula: 8128243
- Laboratório: M1.1
- Linguagem: Python

## 1. Objetivo

Implementar manualmente operações básicas de processamento de imagens para inspeção, cópia, separação de canais, conversão para tons de cinza e quantização de níveis. O objetivo foi manter a lógica em código explícito, sem depender de funções prontas que substituíssem a operação avaliada.

## 2. Operações implementadas

- inspeção da imagem;
- cópia manual de pixels;
- separação dos canais B, G e R;
- conversão para escala de cinza por média;
- conversão para escala de cinza por ponderação luminosa;
- quantização em níveis discretos.

## 3. Testes realizados

| Teste | Entrada | Operação | Parametros | Resultado esperado |
|---|---|---|---|---|
| inspeção | images/input/aranha.png | inspect | sem parâmetros | exibe largura, altura, canais e estatísticas |
| cópia | imagens sintéticas | copy | sem parâmetros | imagem preservando os pixels em mesma dimensão |
| canais | imagens sintéticas | channel_b / channel_g / channel_r | sem parâmetros | canal correto preservado e demais zeros |
| cinza médio | imagens sintéticas | grayscale_average | sem parâmetros | valores calculados por média simples |
| cinza ponderado | imagens sintéticas | grayscale_weighted | sem parâmetros | valores calculados pela fórmula ponderada |
| quantização | imagens sintéticas | quantize | --levels 16/8/4/2 | níveis reduzidos mantidos dentro do intervalo |

## 4. Análise do enunciado

1. Resolução espacial e radiométrica: a resolução espacial se refere à quantidade de pixels e à forma como a imagem discrimina detalhes no plano, enquanto a resolução radiométrica refere-se ao número de níveis de intensidade que cada pixel pode assumir. Em outras palavras, a imagem pode ter muitos pixels e ainda assim poucos níveis por pixel, ou vice-versa.

2. Por que a média ponderada difere da média simples: porque a fórmula ponderada atribui pesos diferentes aos canais, refletindo a sensibilidade do olho humano à luminância. O canal verde tem maior peso e o azul menor, então o resultado final não é a média aritmética simples.

3. O que ocorre visualmente ao reduzir os níveis: a imagem ganha bandas de intensidade mais marcadas, o gradiente fica menos suave, e detalhes finos tendem a desaparecer, especialmente em regiões com transição gradual de brilho.

4. Regiões em que a perda fica mais evidente: normalmente nas áreas com transições suaves, sombras, texturas e bordas delicadas. Em uma imagem real, o efeito é mais perceptível em regiões de gradação tonal contínua e em contornos com pouca diferença entre níveis adjacentes.

5. Tipo e número de canais e acesso ao pixel: imagens em níveis de cinza são acessadas como uma matriz 2D, enquanto imagens coloridas normalmente são acessadas como uma matriz 3D em ordem BGR no OpenCV. O número de canais determina quantas componentes existem por pixel, e cada canal exige um índice específico ao ler e escrever o valor.

## 5. Resultados

Os resultados foram gerados na pasta `images/output` do projeto, usando o CLI do laboratório. A execução foi confirmada por testes automatizados e a geração de saídas foi feita em múltiplos formatos e níveis de quantização.

## 6. Limitações

- a execução depende da presença de imagens válidas no diretório de entrada;
- imagens PNG corrompidas ou quebradas não podem ser lidas;
- o projeto foi estruturado para o Lab M1.1 e não inclui os demais laboratórios em um único pacote.

## 7. Referências

- Contrato técnico dos laboratórios da M1.
- Rubrica geral dos laboratórios da M1.
- Documentação do OpenCV headless.
- Template base do projeto de processamento de imagens.
