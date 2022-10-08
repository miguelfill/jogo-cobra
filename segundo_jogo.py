import pygame
from pygame.locals import *
from sys import exit  # Essa função é chamada quando eu clico para fechar a janela
from random import randint


pygame.init()
pygame.mixer.music.load('boxcat-games.mp3')
pygame.mixer.music.play(-1)
colisao = pygame.mixer.Sound('efeito-sonoro-coin.wav')


largura = 830
altura = 640

x_cobra = int(largura / 2)
y_cobra = int(altura / 2)
velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = randint(0, 600)
y_maca = randint(0, 430)
pontos = 0
fonte = pygame.font.SysFont('arial', 30, True, False)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da cobra')  # Serve para alterar o nome da janela
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False


def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(20, 600)
    y_maca = randint(20, 430)
    morreu = False


while True:  # Todo jogo sempre roda dentro de um loop principal, quer dizer que a cada segundo vai atualizando
    relogio.tick(48)  # Aqui é quantos números de frames eu quero que o jogo tenha
    tela.fill((255, 255, 255))
    mensagem = f'Pontos: {pontos}'
    texto = fonte.render(mensagem, False, (0, 0, 0))

    for event in pygame.event.get():  # Esse loop 'for' tem a tarefa de checar se algum evento ocorreu, dentro do loop principal
        if event.type == QUIT:  # Essa condiçao vai fechar a janela quando eu clicar em fechar
            pygame.quit()
            exit()  # O jogo fecha

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a or event.key == K_KP4:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0

            if event.key == K_RIGHT or event.key == K_d or event.key == K_KP6:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0

            if event.key == K_UP or event.key == K_w or event.key == K_KP8:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0

            if event.key == K_DOWN or event.key == K_s or event.key == K_KP2:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra += x_controle
    y_cobra += y_controle

    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 20, 20))

    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(40, 430)
        '''x_cobra = randint(40, 600)
        y_cobra = randint(40, 430)'''
        pontos += 1
        colisao.play()
        comprimento_inicial += 1

    lista_cabeca = [x_cobra, y_cobra]  # Essa lista armazena os valores mais recentes que x e y assumiram
    lista_cobra.append(lista_cabeca)  # Essa lista tem todas as posições que a cobra ja assumiu

    if lista_cobra.count(lista_cabeca) > 1:  # Se tiver uma outra lista que seja igual a minha lista_cabeca, dentro da lista_cobra
        fonte2 = pygame.font.SysFont('arial', 20, True, True)       # quer dizer que a cobra encostou nela mesma
        mensagem = 'Game Over, Pressione R para jogar de novo'
        texto_formatado = fonte2.render(mensagem, True, (0, 0, 0))
        ret_texto = texto_formatado.get_rect()
        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_texto.center = (largura//2, altura//2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto, (450, 40))  # Posição do texto

    pygame.display.update()  # A cada iteração do loop principal, essa função atualiza a tela do jogo
