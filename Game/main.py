import pygame
import random
import os


def initialize():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 30)
    pygame.init()


def play_game():
    sound_piece = pygame.mixer.Sound("../Sounds/Piece-Move.wav")
    sound_win = pygame.mixer.Sound("../Sounds/Sunet-Invins.wav")
    sound_piece.set_volume(1)
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    background = pygame.image.load("../Images/Board.png")
    background = pygame.transform.scale(background, (800, 800))
    screen.blit(background, (0, 0))
    playing = True
    black_pips = 167
    white_pips = 167
    pygame.font.init()
    pipfont = pygame.font.SysFont('Times New Roman', 50)
    blacksurface = pipfont.render(str(black_pips), True, (0, 0, 0))
    whitesurface = pipfont.render(str(white_pips), True, (0, 0, 0))
    while playing:
        # mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()
        screen.blit(blacksurface, (362, -7))
        screen.blit(whitesurface, (362, 752))
        pygame.display.update()


if __name__ == '__main__':
    initialize()
    play_game()
