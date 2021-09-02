import pygame
import random
import os


def initialize():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 30)
    pygame.init()
    pygame.display.set_caption('Backgammon')


def play_game():
    # sound
    sound_piece = pygame.mixer.Sound("../Sounds/Piece-Move.wav")
    sound_piece.set_volume(1)

    # screen
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    background = pygame.image.load("../Images/Board.png")

    # game data
    table = default_table()
    playing = True
    black_pips = 167
    white_pips = 167

    # text
    pygame.font.init()
    pipfont = pygame.font.SysFont('Times New Roman', 50)

    while playing:

        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        # text
        blacksurface = pipfont.render(str(black_pips), True, (0, 0, 0))
        whitesurface = pipfont.render(str(white_pips), True, (0, 0, 0))

        # blit
        screen.blit(background, (0, 0))
        screen.blit(blacksurface, (362, -7))
        screen.blit(whitesurface, (362, 752))
        put_pieces(screen, table)
        # put_dice(screen, 2, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        pygame.display.update()


def default_table():
    to_return = []
    for i in range(0, 24):
        to_return.append([])
    b = 'b'
    w = 'w'
    to_return[0] = [b, b]
    to_return[5] = [w, w, w, w, w]
    to_return[7] = [w, w, w]
    to_return[11] = [b, b, b, b, b]
    to_return[12] = [w, w, w, w, w]
    to_return[16] = [b, b, b]
    to_return[18] = [b, b, b, b, b]
    to_return[23] = [w, w]
    return to_return


def put_pieces(screen, table):
    white_piece = pygame.image.load("../Images/Piece-White.png")
    black_piece = pygame.image.load("../Images/Piece-Black.png")
    for i in range(0, 24):
        for j in range(0, len(table[i])):
            if table[i][j] == 'w':
                screen.blit(white_piece, get_piece_position(i, j))
            if table[i][j] == 'b':
                screen.blit(black_piece, get_piece_position(i, j))


def get_dice():
    value1 = random.randint(1, 6)
    value2 = random.randint(1, 6)
    return [value1, value2]


def put_dice(screen, value1, value2):
    # dice_first = rotated_image = pygame.transform.rotate(dice_2, 30)
    dice_1 = pygame.image.load("../Images/Dice-1.png")
    dice_2 = pygame.image.load("../Images/Dice-2.png")
    dice_3 = pygame.image.load("../Images/Dice-3.png")
    dice_4 = pygame.image.load("../Images/Dice-4.png")
    dice_5 = pygame.image.load("../Images/Dice-5.png")
    dice_6 = pygame.image.load("../Images/Dice-6.png")
    dice_s = pygame.image.load("../Images/Dice-Shadow.png")
    dices = [dice_s, dice_1, dice_2, dice_3, dice_4, dice_5, dice_6]
    first_dice = dices[value1]
    second_dice = dices[value2]
    screen.blit(dice_s, (158, 373))
    screen.blit(first_dice, (148, 363))
    screen.blit(dice_s, (237, 403))
    screen.blit(second_dice, (227, 393))


def get_piece_position(row, height):
    # piece_x = 700
    # piece_y = 40
    x_positions = [700, 644, 588, 532, 476, 420, 320, 264, 208, 152, 96, 40, 40, 96, 152, 208, 264, 320, 420, 476, 532, 588, 644, 700]
    piece_x = x_positions[row]
    if row <= 11:
        piece_y = 35 + height * 52
    else:
        piece_y = 703 - height * 52
    return (piece_x, piece_y)


if __name__ == '__main__':
    initialize()
    play_game()
