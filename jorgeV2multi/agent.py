import random
import sys
import copy
from threading import Thread

# Agente que utiliza minimax com heuristica de número de peças e mobilidade


class Arvore:
    jogada = []
    filhos = []

    pontos = 0
    max_pontos = 100
    min_pontos = -100

    def inicializa(possivel_jogada, tabuleiro, cor_peca_jogador, cor_peca_atual, profundidade):
        novo_tabuleiro = copy.deepcopy(tabuleiro)
        novo_tabuleiro.process_move(possivel_jogada, cor_peca_atual)
        proximas_jogadas = Arvore(novo_tabuleiro, cor_peca_jogador, novo_tabuleiro.opponent(
        cor_peca_atual), profundidade-1, False)
        proximas_jogadas.jogada = possivel_jogada
        return proximas_jogadas

    def __init__(self, tabuleiro, cor_peca_jogador, cor_peca_atual, profundidade, usa_multiprocess, irmaos, jogada_atual = []):
        self.filhos = []
        self.jogada = jogada_atual
        possiveis_jogadas = tabuleiro.legal_moves(cor_peca_atual)
        if(profundidade == 0 or len(possiveis_jogadas) == 0 or tabuleiro.is_terminal_state()):
            self.pontos = self.custo(
                cor_peca_jogador, tabuleiro, len(possiveis_jogadas))
        elif usa_multiprocess:
            threads = [None] * len(possiveis_jogadas)
            for i in range(len(threads)):
                novo_tabuleiro = copy.deepcopy(tabuleiro)
                novo_tabuleiro.process_move(possiveis_jogadas[i], cor_peca_atual)
                threads[i] = Thread(target=Arvore, args=(novo_tabuleiro, cor_peca_jogador, novo_tabuleiro.opponent(
                    cor_peca_atual), profundidade-1, False, self.filhos, possiveis_jogadas[i]))
                threads[i].start()
            for i in range(len(threads)):   
                threads[i].join()
        else:
            for possivel_jogada in possiveis_jogadas:
                novo_tabuleiro = copy.deepcopy(tabuleiro)
                novo_tabuleiro.process_move(possivel_jogada, cor_peca_atual)
                Arvore(novo_tabuleiro, cor_peca_jogador, novo_tabuleiro.opponent(
                    cor_peca_atual), profundidade-1, False, self.filhos, possivel_jogada)
                #proximas_jogadas.jogada = possivel_jogada
                #self.filhos.append(proximas_jogadas)
            irmaos.append(self)


    def minimax(self, maximiza, alpha, beta):
        if(self.filhos != []):
            if(maximiza):
                pontuacao_maxima = self.min_pontos
                for i in range(0, len(self.filhos)):
                    pontuacao_filho = self.filhos[i].minimax(
                        False, alpha, beta)
                    pontuacao_maxima = max(pontuacao_maxima, pontuacao_filho)
                    alpha = max(alpha, pontuacao_filho)
                    if(beta <= alpha):
                        self.filhos = self.filhos[0:i]
                        break
                self.pontos = pontuacao_maxima
                return pontuacao_maxima
            else:
                pontuacao_minima = self.max_pontos
                for i in range(0, len(self.filhos)):
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

    def custo(self, cor_peca, tabuleiro, possiveis_jogadas_tamanho):
        if(tabuleiro.piece_count[tabuleiro.opponent(cor_peca)] == 0):
            return self.max_pontos
        else:
            return self.normaliza_pontuacao(0, 64, tabuleiro.piece_count[cor_peca])*0.6 + self.normaliza_pontuacao(0, 32, possiveis_jogadas_tamanho)*0.4


def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    profundidade = 3
    jogadas = Arvore(the_board, color, color, profundidade, True, [])
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
