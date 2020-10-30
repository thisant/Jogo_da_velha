import os
import time
from random import choice
from math import inf as infinity

humano = -1
ia = +1
tabuleiro = [[0, 0, 0], [0, 0, 0], [0, 0, 0], ]

def vitoria(estado, jogador):
    jogos_vitoriosos = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador, jogador, jogador] in jogos_vitoriosos:
        return True
    else:
        return False

def fimDoJogo(estado):
    return vitoria(estado, humano) or vitoria(estado, ia)

def calculandoPlacar(estado):
    if vitoria(estado, ia):
        placar = +1
    elif vitoria(estado, humano):
        placar = -1
    else:
        placar = 0

    return placar

def espacoVazio(state):
    celulas = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                celulas.append([x, y])

    return celulas

def movimento_valido(x, y):
    if [x, y] in espacoVazio(tabuleiro):
        return True
    else:
        return False

def escolherMovimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False

def miniMax(estado, profundidade, jogador):
    if jogador == ia:
        melhor_pontuacao = [-1, -1, -infinity]
    else:
        melhor_pontuacao = [-1, -1, +infinity]

    if profundidade == 0 or fimDoJogo(estado):
        placar = calculandoPlacar(estado)
        return [-1, -1, placar]

    for espaco in espacoVazio(estado):
        x, y = espaco[0], espaco[1]
        estado[x][y] = jogador
        placar = miniMax(estado, profundidade - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == ia:
            if placar[2] > melhor_pontuacao[2]:
                melhor_pontuacao = placar
        else:
            if placar[2] < melhor_pontuacao[2]:
                melhor_pontuacao = placar

    return melhor_pontuacao

def exibir(estado, computador_simbolo, jogador_simbolo):
    simbolos = {
        -1: jogador_simbolo,
        +1: computador_simbolo,
        0: ' '
    }
    separacao = '-------------'

    print('\n' + separacao)
    for coluna in estado:
        for celula in coluna:
            simbolo = simbolos[celula]
            print(f'| {simbolo}', end='|')
        print('\n' + separacao)


def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def vezJogador(computador_simbolo, humano_simbolo):
    profundidade = len(espacoVazio(tabuleiro))
    if profundidade == 0 or fimDoJogo(tabuleiro):
        return

    posicao = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpar()
    print('Tua vez!')
    exibir(tabuleiro, computador_simbolo, humano_simbolo)

    while posicao < 1 or posicao > 9:
        try:
            posicao = int(input('Escolha uma posição de 1 a 9: '))
            coord = movimentos[posicao]
            pode_mover = escolherMovimento(coord[0], coord[1], humano)

            if not pode_mover:
                print('Local errado')
                posicao = -1
        except (EOFError, KeyboardInterrupt):
            print('Jogo encerrado')
            exit()
        except (KeyError, ValueError):
            print('Local errado')


def vezComputador(computador_simbolo, jogador_simbolo):
    profundidade = len(espacoVazio(tabuleiro))
    if profundidade == 0 or fimDoJogo(tabuleiro):
        return

    limpar()
    print('Vez do adversário!')
    exibir(tabuleiro, computador_simbolo, jogador_simbolo)

    if profundidade == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        movimento = miniMax(tabuleiro, profundidade, ia)
        x, y = movimento[0], movimento[1]

    escolherMovimento(x, y, ia)
    time.sleep(1)


def main():
    limpar()
    jogador_simbolo = 'O'
    computador_simbolo = 'X'

    while len(espacoVazio(tabuleiro)) > 0 and not fimDoJogo(tabuleiro):
        vezComputador(computador_simbolo, jogador_simbolo)
        vezJogador(computador_simbolo, jogador_simbolo)

    if vitoria(tabuleiro, humano):
        limpar()
        print(f'Tua vez! [{jogador_simbolo}]')
        exibir(tabuleiro, computador_simbolo, jogador_simbolo)
        print('Vitória!')
    elif vitoria(tabuleiro, ia):
        limpar()
        print(f'Vez do adversário! [{computador_simbolo}]')
        exibir(tabuleiro, computador_simbolo, jogador_simbolo)
        print('Derrota!')
    else:
        limpar()
        exibir(tabuleiro, computador_simbolo, jogador_simbolo)
        print('Empate!')
    exit()

if __name__ == '__main__':
    main()