# REPORT — Laboratório M1.3

## 1. Identificação

- **Laboratório:** M1.3 — Convolução e filtragem espacial
- **Linguagem:** Python
- **Estudante:** João Vitor Schwambach Brasil

## 2. Objetivo

Implementar manualmente operações de vizinhança e convolução no domínio espacial, incluindo tratamento de bordas, suavização, Laplaciano, realce e Sobel, mantendo precisão numérica durante os cálculos.

## 3. Operações implementadas

Foram implementadas as seguintes operações:

- Convolução genérica com kernel quadrado de dimensão ímpar;
- Estratégias de tratamento de bordas `copy` e `replicate`;
- Filtro de média 3×3;
- Filtro de média ponderada 3×3;
- Filtro de média 5×5;
- Laplaciano;
- Realce por combinação da imagem original com a resposta do Laplaciano;
- Sobel Gx;
- Sobel Gy;
- Magnitude aproximada do Sobel `|Gx| + |Gy|`;
- Magnitude Euclidiana do Sobel `sqrt(Gx² + Gy²)`.

## 4. Decisões de implementação

O percurso da vizinhança é realizado explicitamente com laços sobre cada pixel da imagem e cada posição do kernel.

A convolução realiza a inversão do kernel nos dois eixos antes do acúmulo, seguindo a definição matemática de convolução.

Foram implementadas duas estratégias para tratamento das bordas:

- `copy`: quando a vizinhança ultrapassa os limites da imagem, o pixel original é preservado;
- `replicate`: as coordenadas fora dos limites são ajustadas para o pixel válido mais próximo.

Os acumuladores utilizam ponto flutuante para evitar perda de precisão e permitir valores negativos durante os cálculos, especialmente nas operações de Laplaciano e Sobel.

A conversão para imagem de 8 bits ocorre somente na etapa de saída, com arredondamento e saturação dos valores para o intervalo `[0, 255]`.

## 5. Testes

Foram implementados testes automatizados utilizando pytest, verificando diferentes aspectos da implementação, incluindo:

- convolução com kernel identidade;
- comportamento em imagem constante;
- filtro de média ponderada;
- validação de kernels inválidos;
- validação de estratégia de borda inválida;
- comportamento de respostas negativas do Laplaciano;
- dimensões das respostas produzidas pelo Sobel.

Também foram utilizadas imagens sintéticas para avaliar diferentes situações:

- imagem constante;
- impulso;
- degrau vertical;
- degrau horizontal;
- conteúdo tocando as bordas da imagem.

Os testes automatizados foram executados com sucesso, com 9 testes aprovados.

Além dos testes unitários, foi criado o script auxiliar `run_tests.py`, localizado na raiz do projeto. Ele executa automaticamente as operações do M1.3 e gera as respectivas imagens de saída, facilitando a reprodução dos experimentos.

## 6. Resultados

O kernel identidade reproduz a imagem de entrada, servindo como uma verificação básica da implementação da convolução.

Os filtros de média reduzem as variações locais da imagem. O filtro 5×5 considera uma vizinhança maior que o 3×3 e, consequentemente, produz uma suavização mais intensa, com maior custo computacional.

A média ponderada 3×3 atribui maior importância aos pixels próximos ao centro da vizinhança, apresentando comportamento diferente da média uniforme.

O Laplaciano produz respostas positivas e negativas principalmente nas regiões de transição da imagem. A resposta numérica bruta é preservada em `results/laplacian_raw.csv` antes da conversão para visualização.

O realce utiliza a resposta do Laplaciano em conjunto com a imagem original, buscando destacar transições e detalhes.

No Sobel, a componente Gx responde principalmente a variações associadas a bordas verticais, enquanto Gy responde principalmente a variações associadas a bordas horizontais.

Foram calculadas duas formas de magnitude:

- `|Gx| + |Gy|`, como aproximação;
- `sqrt(Gx² + Gy²)`, como magnitude Euclidiana.

As imagens resultantes das operações são armazenadas em `images/output/`.

## 7. Análise técnica

### 7.1 Operação pontual × operação de vizinhança

Uma operação pontual utiliza somente o valor do próprio pixel para determinar o resultado. Já uma operação de vizinhança utiliza também pixels próximos, fazendo com que o resultado dependa do contexto espacial ao redor do pixel.

### 7.2 Dimensões ímpares dos kernels

Dimensões ímpares permitem definir um elemento central único no kernel. Isso facilita o alinhamento da vizinhança com o pixel que está sendo processado.

### 7.3 Efeito do aumento do kernel de média

Ao aumentar o tamanho do kernel, mais pixels são considerados no cálculo. Isso aumenta a suavização, podendo reduzir detalhes e pequenas variações da imagem. O custo computacional também aumenta.

### 7.4 Efeito das estratégias de borda

A estratégia `copy` preserva o valor original quando a vizinhança ultrapassa os limites da imagem. A estratégia `replicate` utiliza o pixel válido mais próximo. Por isso, as principais diferenças entre as estratégias aparecem nas regiões próximas às bordas.

### 7.5 Valores negativos no Laplaciano

O Laplaciano possui coeficientes positivos e negativos. Em regiões de transição, a soma ponderada pode resultar em valores negativos. Esses valores são importantes durante o cálculo e não devem ser descartados antes da análise.

### 7.6 Gx × Gy no Sobel

Gx mede principalmente variações na direção horizontal do cálculo, destacando bordas verticais. Gy mede principalmente variações na direção vertical do cálculo, destacando bordas horizontais.

### 7.7 Magnitude aproximada × Euclidiana

A magnitude aproximada `|Gx| + |Gy|` é simples e possui menor custo computacional. A magnitude Euclidiana `sqrt(Gx² + Gy²)` representa a norma das duas componentes e fornece uma medida mais direta da intensidade do gradiente.

## 8. Guardas e tratamento de erros

O programa possui verificações para:

- falha na leitura da imagem;
- imagem vazia ou inválida;
- kernel vazio;
- kernel não quadrado;
- kernel com dimensão par;
- estratégia de borda inválida;
- parâmetros obrigatórios ausentes;
- acesso à vizinhança fora dos limites da imagem.

Durante os cálculos, os valores são mantidos em ponto flutuante, permitindo resultados negativos e valores superiores a 255. A saturação para o intervalo `[0, 255]` ocorre somente na conversão para a imagem final.

## 9. Limitações

A implementação trabalha com imagens em níveis de cinza, conforme especificado para as operações de convolução do laboratório.

Como respostas como a do Laplaciano podem conter valores negativos, sua visualização em uma imagem convencional de 8 bits exige conversão. Para evitar perda da resposta numérica original, os valores brutos do Laplaciano são preservados separadamente em `results/laplacian_raw.csv`.

## 10. Conclusão

A implementação atende às operações solicitadas no M1.3, mantendo a lógica de convolução, percurso da vizinhança, aplicação dos kernels e tratamento de bordas explicitamente no código-fonte.

Os testes automatizados apresentaram 9 testes aprovados, e o script `run_tests.py` permite reproduzir automaticamente os experimentos e gerar as imagens de saída.

Os resultados obtidos permitem observar na prática os efeitos da suavização, das diferentes estratégias de borda, do Laplaciano e dos operadores Sobel, atendendo aos objetivos técnicos propostos para o laboratório.