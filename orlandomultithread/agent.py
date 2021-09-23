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

    def __init__(self, tabuleiro, cor_peca_jogador, cor_peca_atual, profundidade, usa_multiprocess, irmaos, jogada_atual = []):
        self.filhos = []
        self.jogada = jogada_atual
        possiveis_jogadas = tabuleiro.legal_moves(cor_peca_atual)
        if(profundidade == 0 or len(possiveis_jogadas) == 0 or tabuleiro.is_terminal_state()):
            self.pontos = self.custo(
                cor_peca_jogador, tabuleiro, len(possiveis_jogadas),jogada_atual)
            irmaos.append(self)
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
                        self.filhos = self.filhos[0:(i+1)]
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
                        self.filhos = self.filhos[0:(i+1)]
                        break
                self.pontos = pontuacao_minima
                return pontuacao_minima
        return self.pontos

    def normaliza_pontuacao(self, min_antigo, max_antigo, valor):
        return ((valor-min_antigo)/(max_antigo-min_antigo) * (self.max_pontos-self.min_pontos) + self.min_pontos)

    def custo_peca(self, cor_peca, tabuleiro, possiveis_jogadas_tamanho):
        num_pecas = self.normaliza_pontuacao(
                0, 64, tabuleiro.piece_count[cor_peca])
        zone = self.normaliza_pontuacao(
                80, 256, danger_zone(tabuleiro.tiles, cor_peca))
        mobilidade = self.normaliza_pontuacao(
                0, 32, possiveis_jogadas_tamanho)
        proporcao_mobilidade = (tabuleiro.piece_count[tabuleiro.EMPTY]/60)*0.2
        return num_pecas * (1 - proporcao_mobilidade) + mobilidade * proporcao_mobilidade

    def custo(self, cor_peca, tabuleiro, possiveis_jogadas_tamanho,jogada_atual):
        if(tabuleiro.is_terminal_state()):
            if (tabuleiro.piece_count[cor_peca] > tabuleiro.piece_count[tabuleiro.opponent(cor_peca)]):
                return self.max_pontos
            else:
                return self.min_pontos 
        else:
            cor_peca_oponente = tabuleiro.opponent(cor_peca)
            possiveis_jogadas_tamanho_oponente = len(tabuleiro.legal_moves(cor_peca_oponente))
            return self.custo_peca(cor_peca, tabuleiro, possiveis_jogadas_tamanho) * 0.7 + self.custo_peca(cor_peca_oponente, tabuleiro, possiveis_jogadas_tamanho_oponente) * -0.3 - perigo(jogada_atual)

def perigo(jogada_atual):
    if is_bad_zone(jogada_atual[0],jogada_atual[1]):
        return 2
    if is_danger_zone(jogada_atual[0],jogada_atual[1]):
        return 4
    else:
        return 0

def danger_zone(board, color):
    points = 0
    for x in range(8):
        for y in range(8):
            if (board[x][y] == color):
                if is_danger_zone(x, y):
                    points += 1
                elif is_bad_zone(x, y):
                    points += 2
                else:
                    points += 4
            else:
                points += 4
    return points

def is_danger_zone(x, y):
    return (((y in [0, 7]) and (x in [1, 6])) or ((y in [1, 6]) and (x in [0, 1, 6, 7])))

def is_bad_zone(x, y):
    return (((y in [1, 6]) and (x >= 2 and x <= 5)) or ((x in [1, 6]) and (y >= 2 and y <= 5)))

def calcula_profundidade(tabuleiro, cor):
    nro_jogadas = len(tabuleiro.legal_moves(cor))
    vazios = tabuleiro.piece_count[tabuleiro.EMPTY]
    if(nro_jogadas < 8):
        if(vazios < 10):
            return 6
        if(vazios < 15):
            return 5
        if(vazios < 22):
            return 4
        else:
            return 3
    elif(vazios < 18 or (50 < vazios < 61)):
        return 4
    else:
        return 3

def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    profundidade = calcula_profundidade(the_board, color)
    jogadas = Arvore(the_board, color, color, profundidade, True, [])
    random.shuffle(jogadas.filhos)
    jogadas.minimax(True, jogadas.min_pontos, jogadas.max_pontos)

    melhor_jogada = jogadas.filhos[0].jogada
    pontuacao_maxima = jogadas.min_pontos

    for filho in jogadas.filhos:
        if(pontuacao_maxima < filho.pontos):
            melhor_jogada = filho.jogada
            pontuacao_maxima = filho.pontos

    return melhor_jogada
