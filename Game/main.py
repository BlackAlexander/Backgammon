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
    sound_dice = pygame.mixer.Sound("../Sounds/Dice-Sound.wav")

    # screen
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    background = pygame.image.load("../Images/Board.png")

    # buttons
    button_roll = pygame.image.load("../Images/Button-Roll.png")
    # button_roll = pygame.transform.scale(button_roll, (100, 100))
    button_undo = pygame.image.load("../Images/Button-Undo.png")
    button_done = pygame.image.load("../Images/Button-Done.png")

    # game data
    table = default_table()
    playing = True
    black_pips = 167
    white_pips = 167
    stage = ['roll', 'piece moved', 'all pieces', 'start roll', 'nothing']
    turn = ['white', 'black']
    current_stage = 3
    dices_thrown = 0
    dices1 = dices2 = 1
    # text
    pygame.font.init()
    pipfont = pygame.font.SysFont('Times New Roman', 50)

    while playing:
        # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)

        # text
        blacksurface = pipfont.render(str(black_pips), True, (0, 0, 0))
        whitesurface = pipfont.render(str(white_pips), True, (0, 0, 0))

        # blit
        screen.blit(background, (0, 0))
        screen.blit(blacksurface, (362, -7))
        screen.blit(whitesurface, (362, 752))
        put_pieces(screen, table)
        if dices_thrown:
            put_dice(screen, dices1, dices2)

        if stage[current_stage] == 'roll' or stage[current_stage] == 'start roll':
            screen.blit(button_roll, (541, 353))
        if stage[current_stage] == 'piece moved':
            screen.blit(button_undo, (541, 353))
        if stage[current_stage] == 'all pieces':
            screen.blit(button_undo, (471, 353))
            screen.blit(button_done, (611, 353))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

            if event.type == pygame.MOUSEBUTTONUP:
                # print(mouse[0], mouse[1])
                # print(click)
                pos_x = mouse[0]
                pos_y = mouse[1]
                if current_stage == 0 or current_stage == 3:
                    if 368 <= pos_y <= 438 and 541 <= pos_x <= 640:
                        [dices1, dices2] = get_dice()
                        dices_thrown = True
                        pygame.mixer.Sound.play(sound_dice)
                        clear_file()
                        play_sound(dices1, dices2)

        # screen.blit(pygame.transform.rotate(screen, 180), (0, 0))

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
    f = open("../Dice.txt")
    value1 = 1
    value2 = 1
    line = str(f.readline())
    try:
        x = int(line[0])
        if 1 <= x <= 6:
            value1 = x
        x = int(line[2])
        if 1 <= x <= 6:
            value2 = x
    except (Exception,):
        value1 = random.randint(1, 6)
        value2 = random.randint(1, 6)

    f.close()
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
    screen.blit(dice_s, (153, 368))
    screen.blit(first_dice, (148, 363))
    screen.blit(dice_s, (232, 398))
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


def clear_file():
    f = open("../Dice.txt", "w")
    f.write("x x")
    f.close()


def play_sound(value1, value2):
    if value1 < value2:
        value2, value1 = value1, value2
    sound_66 = pygame.mixer.Sound("../Sounds/Sunet-66.wav")
    sound_66_2 = pygame.mixer.Sound("../Sounds/Sunet-66-2.wav")
    sound_64 = pygame.mixer.Sound("../Sounds/Sunet-64.wav")
    sound_44 = pygame.mixer.Sound("../Sounds/Sunet-44.wav")
    sound_11 = pygame.mixer.Sound("../Sounds/Sunet-11.wav")
    sound_12 = pygame.mixer.Sound("../Sounds/Sunet-12.wav")
    if value1 == 6 and value2 == 6:
        if random.randint(1, 2) == 1:
            pygame.mixer.Sound.play(sound_66_2)
        else:
            pygame.mixer.Sound.play(sound_66)
    if value1 == 6 and value2 == 4:
        pygame.mixer.Sound.play(sound_64)
    if value1 == 4 and value2 == 4:
        pygame.mixer.Sound.play(sound_44)
    if value1 == 1 and value2 == 1:
        pygame.mixer.Sound.play(sound_11)
    if value1 == 2 and value2 == 1:
        pygame.mixer.Sound.play(sound_12)


if __name__ == '__main__':
    initialize()
    play_game()
