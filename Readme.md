# IA - Trabalho 2

## Integrantes do grupo

- 288556 - Matheus Dussin Bampi
- 290401 - Gustavo Ribeiro Kremer
- 305303 - Marco Antonio Athayde de Aguiar Vieira

## Bibliotecas utilizadas

- import random
- import copy
- from threading import Thread

Para escolher qual jogada deve ser realizada, foi implementado o algoritmo minimax com a poda alpha beta.
O desenvolvimento do algoritmo teve grande inspiração no video do Youtuber Sebastian Lague.

Para avaliar as próximas jogadas do otello, é montada uma árvore de jogadas, cada nó da arvore tem como filho as jogadas futuras que são possiveis.
Cada jogada recebe uma pontuação com base em uma heuristica, a pontuação máxima dessa heurística é 100 pontos, e a mínima -100.
Para calcular a heurística da jogada, é feito um cálculo com 2 fatores: a quantidade de peças e a mobilidade.

A quantidade de peças é quantas peças da sua cor o jogador irá ter no tabuleiro.
A mobilidade é a quantidade de movimentos livres que a jogada possui.

Para calcular a heurística é levado em conta 60% a sua jogada e 30% a jogada do oponente. Além desses fatores, 10% do peso da heurística é relacionda ao "fator perigo" da jogada.
O fator perigo está relacionado com a posição em que a peça será colocada, se essa é uma posição perigosa ou não.
A escolha dessas heuristica se deu com base em um estudo das estratégias de Otello, encontradas em um site na internet.

Para tentar melhorar o desempenho do agente, foi implementado paralelismo na avaliação da primeira geração dos filhos da árvore de jogadas. Cada filho, e seus sucessores, são avaliados em uma Thread diferente.
A implementação do multithread não resultou em ganhos de desempenho significativos.

Para aproveitar melhor o tempo de processamento disponível, a árvore de jogadas é criada com diferentes níveis de profundidade, dependendo de quantos filhos serão gerados nas próximas jogadas.
No início do jogo, a árvore é gerada com profundidade 3, porém, no final do jogo, chega a 6 de profundidade.

- Vídeo sobre minimax do Youtuber Sebastian Lague:
<https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague>

- Site sobre estratégias de Otello:
<https://www.ultraboardgames.com/othello/tips.php>
