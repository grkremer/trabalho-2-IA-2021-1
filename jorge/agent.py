import random
import sys
import copy

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class Arvore:
    jogada = []
    filhos = []
    profundidade = 0
   
    pontos = 0
    max_pontos = 100
    min_pontos = -100

    def __init__(self, tabuleiro, cor_peca_jogador, cor_peca_atual, profundidade):
        self.filhos = []
        possiveis_jogadas = tabuleiro.legal_moves(cor_peca_atual)
        if(profundidade == 0 or len(possiveis_jogadas) == 0 or tabuleiro.is_terminal_state()):
            self.pontos = self.custo(cor_peca_jogador, tabuleiro)
            self.profundidade = 0
        else:
            for possivel_jogada in possiveis_jogadas:
                novo_tabuleiro = copy.deepcopy(tabuleiro)
                novo_tabuleiro.process_move(possivel_jogada, cor_peca_atual)
                proximas_jogadas = Arvore(novo_tabuleiro, cor_peca_jogador, novo_tabuleiro.opponent(cor_peca_atual), profundidade-1)
                proximas_jogadas.jogada = possivel_jogada
                self.filhos.append(proximas_jogadas)

            maior_profundidade_filho = 0
            for filho in self.filhos:
                maior_profundidade_filho = max(maior_profundidade_filho, filho.pontos)
            self.profundidade = maior_profundidade_filho+1 

    def minimax(self, maximiza, alpha, beta):
        if(self.profundidade != 0):
            if(maximiza):
                pontuacao_maxima = self.min_pontos
                for i in range(0,len(self.filhos)):
                    pontuacao_filho = self.filhos[i].minimax(False, alpha, beta)
                    pontuacao_maxima = max(pontuacao_maxima, pontuacao_filho)
                    alpha = max(alpha, pontuacao_filho)
                    if(beta <= alpha):
                        self.filhos = self.filhos[0:i]
                        break
                self.pontos = pontuacao_maxima
                return pontuacao_maxima
            else:
                pontuacao_minima = self.max_pontos;
                for i in range(0,len(self.filhos)):
                    pontuacao_filho = self.filhos[i].minimax(True, alpha, beta)
                    pontuacao_minima = min(pontuacao_minima, pontuacao_filho)
                    beta = min(beta, pontuacao_filho)
                    if(beta <= alpha):
                        self.filhos = self.filhos[0:i]
                        break
                self.pontos = pontuacao_minima
                return pontuacao_minima
        return self.pontos

    def normaliza_pontuacao(self, min_antigo, max_antigo, valor):
        return ((valor-min_antigo)/(max_antigo-min_antigo) * (self.max_pontos-self.min_pontos) + self.min_pontos)

    def custo(self, cor_peca, tabuleiro):
        if(tabuleiro.piece_count[tabuleiro.opponent(cor_peca)] == 0):
            return self.max_pontos
        else:
            return self.normaliza_pontuacao(0, 64, tabuleiro.piece_count[cor_peca])

def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta

    profundidade = 3
    jogadas = Arvore(the_board, color, color, profundidade)
    random.shuffle(jogadas.filhos)
    jogadas.minimax(True, jogadas.min_pontos, jogadas.max_pontos)

    melhor_jogada = jogadas.filhos[0]
    pontuacao_maxima = jogadas.min_pontos

    for filho in jogadas.filhos:
        if(pontuacao_maxima < filho.pontos):
            melhor_jogada = filho.jogada
            pontuacao_maxima = filho.pontos

    print("pontuacao = "+str(pontuacao_maxima))
    return melhor_jogada

