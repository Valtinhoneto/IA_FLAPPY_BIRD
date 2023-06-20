import pygame
import os
import random
import neat

ia_jogando = True
geracao = 0
rede_atual = None

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        nova_posicao = imagem_rotacionada.get_rect(center=self.imagem.get_rect(topleft=(self.x, self.y)).center)
        tela.blit(imagem_rotacionada, nova_posicao.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.topo = 0
        self.baixo = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BAIXO = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.topo = self.altura - self.CANO_TOPO.get_height()
        self.baixo = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.topo))
        tela.blit(self.CANO_BAIXO, (self.x, self.baixo))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        baixo_mask = pygame.mask.from_surface(self.CANO_BAIXO)

        topo_offset = (self.x - passaro.x, self.topo - round(passaro.y))
        baixo_offset = (self.x - passaro.x, self.baixo - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, topo_offset)
        baixo_ponto = passaro_mask.overlap(baixo_mask, baixo_offset)

        if topo_ponto or baixo_ponto:
            return True

        return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos, geracao):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto_pontos, (TELA_LARGURA - 10 - texto_pontos.get_width(), 10))

    texto_geracao = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
    tela.blit(texto_geracao, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()


def main(genomas, configuracao):
    global geracao
    geracao += 1

    redes = []
    genomas_lista = []
    passaros = []

    for _, genoma in genomas:
        rede = neat.nn.FeedForwardNetwork.create(genoma, configuracao)
        redes.append(rede)
        genoma.fitness = 0
        genomas_lista.append(genoma)
        passaros.append(Passaro(230, 350))

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        for i, passaro in enumerate(passaros):
            passaro.mover()
            genomas_lista[i].fitness += 0.1

            saida = redes[i].activate((passaro.y,
                                       abs(passaro.y - canos[indice_cano].altura),
                                       abs(passaro.y - canos[indice_cano].baixo)))

            if saida[0] > 0.5:
                passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    genomas_lista[i].fitness -= 1
                    redes.pop(i)
                    genomas_lista.pop(i)
                    passaros.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

            cano.mover()

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.imagem.get_height() >= 730 or passaro.y < 0:
                redes.pop(i)
                genomas_lista.pop(i)
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos, geracao)

        if pontos > 50:
            rodando = False
            break


def run(configuracao_file):
    configuracao = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                      configuracao_file)

    populacao = neat.Population(configuracao)

    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    vencedor = populacao.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    configuracao_path = os.path.join(local_dir, 'Inteligencia Artificia Flappy.txt')
    run(configuracao_path)
