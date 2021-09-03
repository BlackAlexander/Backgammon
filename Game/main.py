import pygame
import random
import os


def initialize():
    """
    Initializes PyGame and the window
    :return:
    """
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 30)
    pygame.init()
    pygame.display.set_caption('Backgammon')


def play_game():
    """
    Long-ass function to play the whole game.
    :return:
    """

    # sound
    sound_dice = pygame.mixer.Sound("../Sounds/Dice-Sound.wav")
    sound_piece = pygame.mixer.Sound("../Sounds/Piece-Move.wav")

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
    # Table has w or b for pieces from 0 to 23,
    # and the number of out pieces on 24(b) and 25(w)
    playing = True
    black_pips = 167
    white_pips = 167
    moved_dice = 0
    dice_capacity = 2
    stage = ['roll', 'piece moved', 'all pieces', 'start roll', 'nothing']
    turn = ['white', 'black']
    current_turn = 0
    current_stage = 3
    dices_thrown = 0
    dices1 = dices2 = 1
    undo_stack = []

    # text
    pygame.font.init()
    pipfont = pygame.font.SysFont('Times New Roman', 50)
    turnfont = pygame.font.SysFont('Times New Roman', 15)

    while playing:
        # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed(3)

        # text
        blacksurface = pipfont.render(str(black_pips), True, (0, 0, 0))
        whitesurface = pipfont.render(str(white_pips), True, (0, 0, 0))
        who_turns = turnfont.render(turn[current_turn], True, (0, 0, 0))

        # blit
        screen.blit(background, (0, 0))
        screen.blit(blacksurface, (362, -7))
        screen.blit(whitesurface, (362, 752))
        screen.blit(who_turns, (40, 21))
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
                # Roll
                if current_stage == 0 or current_stage == 3:
                    # Roll Button
                    if 368 <= pos_y <= 438 and 541 <= pos_x <= 640:
                        [dices1, dices2] = get_dice()
                        dices_thrown = True
                        pygame.mixer.Sound.play(sound_dice)
                        clear_file()
                        if dices1 < dices2:
                            dices2, dices1 = dices1, dices2
                        if dices1 == dices2:
                            dice_capacity = 4
                        else:
                            dice_capacity = 2
                        play_sound(dices1, dices2)
                        current_stage = 4
                if current_stage == 4 or current_stage == 1:
                    # Move pieces
                    click_on_piece = False
                    if 40 <= pos_x <= 760 and 40 <= pos_y <= 356:
                        click_on_piece = True
                    if 40 <= pos_x <= 760 and 450 <= pos_y <= 760:
                        click_on_piece = True
                    if click_on_piece:
                        row = pos_x - 40
                        row = row // 56
                        if 450 <= pos_y <= 760:
                            row += 12
                        if 40 <= pos_y <= 356:
                            row = 11 - row
                        if row == 5:
                            row = -1
                        elif row < 5:
                            row += 1
                        if row == 18:
                            row = -1
                        elif row > 18:
                            row -= 1
                        if moved_dice < dice_capacity:
                            undo_stack.append(full_copy(table))
                            if row != -1:
                                if perform_move(table, turn[current_turn], row, dices1):
                                    moved_dice += 1
                                    if dice_capacity == 2 and moved_dice < 2:
                                        dices2, dices1 = dices1, dices2
                                        current_stage = 1
                                    if dice_capacity == 2 and moved_dice == 2:
                                        current_stage = 2
                                    if dice_capacity == 4 and moved_dice < 4:
                                        current_stage = 1
                                    if dice_capacity == 4 and moved_dice == 4:
                                        current_stage = 2
                                else:
                                    undo_stack.pop(-1)
                            else:
                                # if perform_move(table, turn[current_turn], row, dices1):
                                if discard_out_piece(table, turn[current_turn], dices1):
                                    moved_dice += 1
                                    if dice_capacity == 2 and moved_dice < 2:
                                        current_stage = 1
                                    if dice_capacity == 2 and moved_dice == 2:
                                        current_stage = 2
                                    if dice_capacity == 4 and moved_dice < 4:
                                        current_stage = 1
                                    if dice_capacity == 4 and moved_dice == 4:
                                        current_stage = 2
                                else:
                                    undo_stack.pop(-1)
                if current_stage == 1:
                    # Undo Button
                    if 368 <= pos_y <= 438 and 541 <= pos_x <= 640:
                        if len(undo_stack) > 0:
                            table = undo_stack.pop(-1)
                            pygame.mixer.Sound.play(sound_piece)
                            moved_dice -= 1
                            if len(undo_stack) == 0:
                                current_stage = 4
                if current_stage == 2:
                    # Undo Shifted Left
                    if 368 <= pos_y <= 438 and 470 <= pos_x <= 570:
                        if len(undo_stack) > 0:
                            table = undo_stack.pop(-1)
                            pygame.mixer.Sound.play(sound_piece)
                            moved_dice -= 1
                            current_stage = 1
                    if 368 <= pos_y <= 438 and 610 <= pos_x <= 710:
                        dices_thrown = False
                        if current_turn == 0:
                            current_turn = 1
                        elif current_turn == 1:
                            current_turn = 0
                        current_stage = 0
                        undo_stack = []
                        moved_dice = 0

        # screen.blit(pygame.transform.rotate(screen, 180), (0, 0))

        pygame.display.update()


def full_copy(table):
    to_ret = []
    for i in range(0, 24):
        to_ret.append([])
        for j in table[i]:
            to_ret[i].append(j)
    to_ret.append(table[24])
    to_ret.append(table[25])
    return to_ret


def default_table():
    """
    Initializes the default table
    :return: List
    """
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
    to_return.append(0)  # Number of out black-pieces
    to_return.append(0)  # Number of out white-pieces
    # game_sample(to_return)
    return to_return


def game_sample(table):
    """
    Sample game for debugging purposes
    """
    to_return = table
    perform_move(to_return, 'black', 16, 1)
    perform_move(to_return, 'white', 23, 6)
    discard_out_piece(to_return, 'black', 4)
    perform_move(to_return, 'white', 23, 4)
    perform_move(to_return, 'black', 16, 1)
    perform_move(to_return, 'black', 18, 1)
    # return
    discard_out_piece(to_return, 'white', 4)
    discard_out_piece(to_return, 'white', 5)
    discard_out_piece(to_return, 'black', 4)


def check_moves(table, colour):
    """
    Checks the possible moves for the given colour (black/white)
    :return: List of booleans
    """
    to_ret = []
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'
    for i in range(0, 24):
        to_ret.append(False)
    for i in range(0, 24):
        if len(table[i]) == 0:
            to_ret[i] = True
        if len(table[i]) == 1 and table[i][0] != colour:
            to_ret[i] = True
        if len(table[i]) > 0 and table[i][0] == colour:
            to_ret[i] = True
    return to_ret


def perform_move(table, colour, row, value):
    """
    Performs a valid move
    :return: True if move was performed, False otherwise
    """
    if row < -1 or row > 23:
        print('Move not available!')
        return False
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'
    if colour == 'b':
        new_position = row + value
    else:
        new_position = row - value
    if colour == 'w' and table[25] > 0 and row != -1:
        print('Move not available!')
        return False
    if colour == 'b' and table[24] > 0 and row != -1:
        print('Move not available!')
        return False
    performable = True
    if row == -1:
        new_position = value - 1
    else:
        if row != -1:
            if len(table[row]) == 0 or table[row][0] != colour:
                print('Move not available!')
                return False
        else:
            if colour == 'b' and table[24] == 0:
                print('Move not available!')
                return False
            if colour == 'w' and table[25] == 0:
                print('Move not available!')
                return False
        if new_position > 23 or new_position < 0:
            print('Move not available!')
            return False
    if check_moves(table, colour)[new_position] is False:
        performable = False
    if performable:
        sound_piece = pygame.mixer.Sound("../Sounds/Piece-Move.wav")
        sound_oo = pygame.mixer.Sound("../Sounds/Sunet-Oo.wav")
        pygame.mixer.Sound.play(sound_piece)
        if row != -1:
            table[row].pop(-1)
        if len(table[new_position]) == 0:
            table[new_position] = [colour]
        else:
            if table[new_position][0] != colour:
                table[new_position] = [colour]
                if colour == 'w':
                    # If colour is white, it means that the other piece is black
                    # print("Out Black Piece!")
                    pygame.mixer.Sound.play(sound_oo)
                    table[24] += 1
                if colour == 'b':
                    table[25] += 1
                    # print("Out White Piece!")
                    pygame.mixer.Sound.play(sound_oo)
            else:
                table[new_position].append(colour)
        return True
    else:
        print('Move not available!')
        return False


def discard_out_piece(table, colour, value):
    """
    Puts a piece back on the table after it was taken out
    """
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'

    if colour == 'b':
        if table[24] < 1:
            print('Move not available!')
            return False
        if check_moves(table, colour)[value - 1] is True:
            if perform_move(table, colour, -1, value - 1):
                table[24] -= 1
                return True
        else:
            print('Move not available!')
            return False
    if colour == 'w':
        if table[25] < 1:
            print('Move not available!')
            return False
        if check_moves(table, colour)[24 - value] is True:
            if perform_move(table, colour, -1, 24 - value):
                table[25] -= 1
                return True
        else:
            print('Move not available!')
            return False


def put_pieces(screen, table):
    """
    Blits the pieces to the screen
    """
    white_piece = pygame.image.load("../Images/Piece-White.png")
    black_piece = pygame.image.load("../Images/Piece-Black.png")
    for i in range(0, 24):
        for j in range(0, len(table[i])):
            if table[i][j] == 'w':
                screen.blit(white_piece, get_piece_position(i, j))
            if table[i][j] == 'b':
                screen.blit(black_piece, get_piece_position(i, j))
    for i in range(0, table[24]):
        black_piece = pygame.transform.scale(black_piece, (50, 50))
        screen.blit(black_piece, get_piece_position(-1, i))  # -1 for black pieces
    for i in range(0, table[25]):
        white_piece = pygame.transform.scale(white_piece, (50, 50))
        screen.blit(white_piece, get_piece_position(-2, i))  # -2 for white pieces


def get_dice():
    """
    Checks if there is a value in the file. If there is not, generates a random one.
    If there are 2 values in the file, then it takes the values.
    :return:
    """
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
    """
    Blits the dice with a given value to the screen.
    """
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
    screen.blit(dice_s, (153 + value1, 368 + value2))
    screen.blit(first_dice, (148 + value1, 363 + value2))
    second_dice = pygame.transform.scale(second_dice, (45, 45))
    dice_s = pygame.transform.scale(dice_s, (45, 45))
    screen.blit(dice_s, (232 + value2, 398 + value1))
    screen.blit(second_dice, (227 + value2, 393 + value1))


def get_piece_position(row, height):
    """
    Gets the pixel position for a given piece.
    -1 for black out pieces, -2 for white out pieces
    #TODO: solve if there are more than 7 pieces on the same place
    """
    # piece_x = 700
    # piece_y = 40
    if row == -1:
        piece_x = 374
        piece_y = 28 + height * 43
        return piece_x, piece_y
    elif row == -2:
        piece_x = 374
        piece_y = 710 - height * 43
        return piece_x, piece_y
    else:
        x_positions = [700, 644, 588, 532, 476, 420, 320, 264, 208, 152, 96, 40, 40, 96, 152, 208, 264, 320, 420, 476, 532, 588, 644, 700]
        piece_x = x_positions[row]
        if row <= 11:
            piece_y = 40 + height * 52
        else:
            piece_y = 703 - height * 52
        return piece_x, piece_y


def clear_file():
    """
    Clears the file with dice values
    """
    f = open("../Dice.txt", "w")
    f.write("x x")
    f.close()


def play_sound(value1, value2):
    """
    Plays certain sound effects for certain dice values. Mostly manele.
    """
    if value1 < value2:
        value2, value1 = value1, value2
    sound_66 = pygame.mixer.Sound("../Sounds/Sunet-66.wav")
    sound_66_2 = pygame.mixer.Sound("../Sounds/Sunet-66-2.wav")
    sound_66_3 = pygame.mixer.Sound("../Sounds/Sunet-66-3.wav")
    sound_65 = pygame.mixer.Sound("../Sounds/Sunet-65.wav")
    sound_64 = pygame.mixer.Sound("../Sounds/Sunet-64.wav")
    sound_44 = pygame.mixer.Sound("../Sounds/Sunet-44.wav")
    sound_42 = pygame.mixer.Sound("../Sounds/Sunet-42.wav")
    sound_41 = pygame.mixer.Sound("../Sounds/Sunet-41.wav")
    sound_11 = pygame.mixer.Sound("../Sounds/Sunet-11.wav")
    sound_12 = pygame.mixer.Sound("../Sounds/Sunet-12.wav")
    if value1 == 6 and value2 == 6:
        rdm = random.randint(1, 3)
        if rdm == 1:
            pygame.mixer.Sound.play(sound_66)
        if rdm == 2:
            pygame.mixer.Sound.play(sound_66_2)
        if rdm == 3:
            pygame.mixer.Sound.play(sound_66_3)
    if value1 == 6 and value2 == 4:
        pygame.mixer.Sound.play(sound_64)
    if value1 == 6 and value2 == 5:
        pygame.mixer.Sound.play(sound_65)
    if value1 == 4 and value2 == 4:
        pygame.mixer.Sound.play(sound_44)
    if value1 == 4 and value2 == 2:
        pygame.mixer.Sound.play(sound_42)
    if value1 == 4 and value2 == 1:
        pygame.mixer.Sound.play(sound_41)
    if value1 == 1 and value2 == 1:
        pygame.mixer.Sound.play(sound_11)
    if value1 == 2 and value2 == 1:
        pygame.mixer.Sound.play(sound_12)


if __name__ == '__main__':
    initialize()
    play_game()
