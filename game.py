import pygame
from board_class import Board, Minotaur, Player
from file_io import get_maze2
import sys
import os

pygame.init()
base_path = os.path.dirname(os.path.abspath(__file__))
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Minotaur Maze Game")




def draw_game_over_menu(win_message):
    window = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Menu Principal")

    font = pygame.font.Font('freesansbold.ttf', 32)
    play_text = font.render("Rejouer", True, (255, 255, 255))
    quit_text = font.render("Quitter", True, (255, 255, 255))

    play_rect = play_text.get_rect(center=(300, 150))
    quit_rect = quit_text.get_rect(center=(300, 250))

    while True:
        window.fill((20, 20, 20))
        window.blit(play_text, play_rect)
        window.blit(quit_text, quit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main_menu():
    window = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Menu Principal")

    font = pygame.font.Font('freesansbold.ttf', 32)
    title_font = pygame.font.Font('freesansbold.ttf', 48)

    title_text = title_font.render("Menu Principal", True, (112, 0, 255))
    play_text = font.render("Jouer", True, (255, 255, 255))
    controls_text = font.render("Contrôles", True, (255, 255, 255))
    quit_text = font.render("Quitter", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(300, 80))
    play_rect = play_text.get_rect(center=(300, 180))
    controls_rect = controls_text.get_rect(center=(300, 240))
    quit_rect = quit_text.get_rect(center=(300, 300))

    while True:
        window.fill((20, 20, 20))
        window.blit(title_text, title_rect)
        window.blit(play_text, play_rect)
        window.blit(controls_text, controls_rect)
        window.blit(quit_text, quit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                if controls_rect.collidepoint(event.pos):
                    show_controls()
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def show_controls():
    window = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Contrôles")

    font = pygame.font.Font('freesansbold.ttf', 24)
    title_font = pygame.font.Font('freesansbold.ttf', 32)

    title_text = title_font.render("Contrôles", True, (112, 0, 255))
    move_up_text = font.render("Monter: Z ou Flèche Haut", True, (255, 255, 255))
    move_left_text = font.render("Gauche: Q ou Flèche Gauche", True, (255, 255, 255))
    move_down_text = font.render("Descendre: S ou Flèche Bas", True, (255, 255, 255))
    move_right_text = font.render("Droite: D ou Flèche Droite", True, (255, 255, 255))
    skip_text = font.render("Passer: Espace", True, (255, 255, 255))
    reset_text = font.render("Réinitialiser: Retour Arrière", True, (255, 255, 255))
    undo_text = font.render("Annuler: Maj", True, (255, 255, 255))
    back_text = font.render("Retour", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(300, 50))
    move_up_rect = move_up_text.get_rect(center=(300, 100))
    move_left_rect = move_left_text.get_rect(center=(300, 150))
    move_down_rect = move_down_text.get_rect(center=(300, 200))
    move_right_rect = move_right_text.get_rect(center=(300, 250))
    skip_rect = skip_text.get_rect(center=(300, 300))
    reset_rect = reset_text.get_rect(center=(300, 350))
    undo_rect = undo_text.get_rect(center=(300, 400))
    back_rect = back_text.get_rect(center=(300, 450))

    while True:
        window.fill((20, 20, 20))
        window.blit(title_text, title_rect)
        window.blit(move_up_text, move_up_rect)
        window.blit(move_left_text, move_left_rect)
        window.blit(move_down_text, move_down_rect)
        window.blit(move_right_text, move_right_rect)
        window.blit(skip_text, skip_rect)
        window.blit(reset_text, reset_rect)
        window.blit(undo_text, undo_rect)
        window.blit(back_text, back_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return


def calculate_window_size(board):
    """
    Calculate the size of the window based on the board size.
    """
    board_size = board.graph.graph["size_board"]
    tile_size = 20
    screen_buffer = 50
    scale_factor = 0.5

    max_board_dim = max(board_size[0], board_size[1])
    if max_board_dim > 128:
        tile_size_scaled = int(tile_size * scale_factor)
    else:
        tile_size_scaled = tile_size

    window_size = (board_size[0] * tile_size_scaled + screen_buffer * 2, board_size[1] * tile_size_scaled + screen_buffer * 2)
    return window_size, tile_size_scaled, screen_buffer

def load_and_scale_image(file_name, scale_size):
    file_path = os.path.join(base_path, file_name)
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, (scale_size, scale_size))

def draw_board(board, window, player_moves, mino_moves, win_message=" ", display_win_message=False):
    """
    Draw the board and animate the movements of the player and minotaur.
    """
    window_size, tile_size_scaled, screen_buffer = calculate_window_size(board)
    fps = 60
    time_to_move = 0.1
    frames = int(fps * time_to_move)
    # Load minotaur image
    minotaur_image = load_and_scale_image('minotaur.png', tile_size_scaled)
    player_image = load_and_scale_image('player.png', tile_size_scaled)
    exit_image = load_and_scale_image('exit.png', tile_size_scaled)
    minotaur_image = pygame.transform.scale(minotaur_image, (tile_size_scaled, tile_size_scaled))
    player_image = pygame.transform.scale(player_image, (tile_size_scaled, tile_size_scaled))
    exit_image = pygame.transform.scale(exit_image, (tile_size_scaled, tile_size_scaled))

    def adjust_token_coordinates(coordinates):
        """
        Adjust the coordinates of tokens to fit within the scaled tile size.
        """
        adj_coordinates = (screen_buffer + tile_size_scaled * coordinates[0] + tile_size_scaled / 2,
                           screen_buffer + tile_size_scaled * coordinates[1] + tile_size_scaled / 2)
        return adj_coordinates
    
    def adjust_wall_coordinates(wall):
        """
        Adjust the coordinates of walls to fit within the scaled tile size.
        """
        x1, y1, x2, y2 = wall[0][0], wall[0][1], wall[1][0], wall[1][1]
        if y2 - y1 == 0:
            if x1 > x2:
                x1, x2, y1, y2 = x2, x1, y2, y1
            return (adjust_token_coordinates((x1 + 0.5, y1 - 0.5)), adjust_token_coordinates((x2 - 0.5, y2 + 0.5)))
        elif x2 - x1 == 0:
            if y1 > y2:
                x1, x2, y1, y2 = x2, x1, y2, y1
            return (adjust_token_coordinates((x1 - 0.5, y1 + 0.5)), adjust_token_coordinates((x2 + 0.5, y2 - 0.5)))

    def get_animation_position(before, after, current_frame, max_frames):
        """
        Calculate the position of the token during animation.
        """
        x = before[0] + (current_frame / max_frames) * (after[0] - before[0])
        y = before[1] + (current_frame / max_frames) * (after[1] - before[1])
        return (x, y)

    def draw_walls():
        """
        Draw the walls of the maze.
        """
        wall_width = int(tile_size_scaled / 10)
        wall_width2 = int(tile_size_scaled / 5)
        width_buffer = wall_width / 2 - 1

        # Draw grids
        for i in range(1, board.graph.graph["size_board"][0]):
            pygame.draw.line(window, (20, 20, 20),
                             (screen_buffer + tile_size_scaled * i, screen_buffer - width_buffer),
                             (screen_buffer + tile_size_scaled * i, window_size[1] - screen_buffer + width_buffer),
                             wall_width)
        for i in range(1, board.graph.graph["size_board"][1]):
            pygame.draw.line(window, (20, 20, 20),
                             (screen_buffer - width_buffer, screen_buffer + tile_size_scaled * i),
                             (window_size[0] - screen_buffer + width_buffer, screen_buffer + tile_size_scaled * i),
                             wall_width)

        # Draw outer border
        pygame.draw.line(window, (40, 40, 40),
                         (screen_buffer - width_buffer, screen_buffer),
                         (window_size[0] - screen_buffer + width_buffer, screen_buffer),
                         wall_width)
        pygame.draw.line(window, (40, 40, 40),
                         (screen_buffer, screen_buffer - width_buffer),
                         (screen_buffer, window_size[1] - screen_buffer + width_buffer),
                         wall_width)
        pygame.draw.line(window, (40, 40, 40),
                         (window_size[0] - screen_buffer, screen_buffer - width_buffer),
                         (window_size[0] - screen_buffer, window_size[1] - screen_buffer + width_buffer),
                         wall_width)
        pygame.draw.line(window, (40, 40, 40),
                         (screen_buffer - width_buffer, window_size[1] - screen_buffer),
                         (window_size[0] - screen_buffer + width_buffer, window_size[1] - screen_buffer),
                         wall_width)

        # Draw walls
        walls = [list(edge) for edge, weight in board.graph.edges.items() if weight["weight"] == -1]
        for wall in walls:
            w1, w2 = adjust_wall_coordinates(wall)
            wx1, wy1 = w1
            wx2, wy2 = w2
            if wx2 - wx1 == 0:
                pygame.draw.line(window, (112, 0, 255),
                                 (wx1, wy1 - width_buffer),
                                 (wx2, wy2 + width_buffer),
                                 wall_width2)
            elif wy2 - wy1 == 0:
                pygame.draw.line(window, (112, 0, 255),
                                 (wx1 - width_buffer, wy1),
                                 (wx2 + width_buffer, wy2),
                                 wall_width2)

    def draw_text(display_win_message=False):
        """
        Draw the text on the screen.
        """
        num_moves = len(player_moves) - 2

        if display_win_message:
            font_win_message = pygame.font.Font('freesansbold.ttf', 32)
            text_win_message = font_win_message.render(win_message, True, (70, 70, 70))
            textRect_win_message = text_win_message.get_rect()
            textRect_win_message.center = (window_size[0] // 2, 25)
            window.blit(text_win_message, textRect_win_message)

        font_move_count = pygame.font.Font('freesansbold.ttf', 14)
        text_move_count = font_move_count.render("Moves: {}".format(num_moves), True, (50, 50, 50))
        textRect_move_count = text_move_count.get_rect()
        textRect_move_count.midleft = (50, window_size[1] - 25)
        window.blit(text_move_count, textRect_move_count)


    def draw_tokens(mino_location, player_location, goal_location):
        """
        Draw the tokens on the screen.
        """
        window.blit(minotaur_image, (mino_location[0] - tile_size_scaled / 2, mino_location[1] - tile_size_scaled / 2))
        window.blit(player_image, (player_location[0] - tile_size_scaled / 2, player_location[1] - tile_size_scaled / 2))
        window.blit(exit_image, (goal_location[0] - tile_size_scaled / 2, goal_location[1] - tile_size_scaled / 2))
        

    # Animate player token
    for frame in range(1, frames + 1):
        window.fill((10, 10, 10))
        draw_walls()

        mino_location = adjust_token_coordinates(mino_moves[-2])
        player_location_before = adjust_token_coordinates(player_moves[-2])
        player_location_after = adjust_token_coordinates(player_moves[-1])
        player_location_current = get_animation_position(player_location_before, player_location_after, frame, frames)
        goal_location = adjust_token_coordinates(board.graph.graph["goal"])

        draw_tokens(mino_location, player_location_current, goal_location)
        draw_text(display_win_message)
        pygame.display.update()
        pygame.time.delay(int(1000 / fps))

    # Animate minotaur token
    if mino_moves[- 2] != mino_moves[- 1]:
        for frame in range(1, frames + 1):
            window.fill((10, 10, 10))
            draw_walls()

            mino_location_before = adjust_token_coordinates(mino_moves[- 2])
            mino_location_after = adjust_token_coordinates(mino_moves[- 1])
            mino_location_current = get_animation_position(mino_location_before, mino_location_after, frame, frames)
            player_location = adjust_token_coordinates(player_moves[-1])
            goal_location = adjust_token_coordinates(board.graph.graph["goal"])

            draw_tokens(mino_location_current, player_location, goal_location)
            draw_text(display_win_message)
            pygame.display.update()
            pygame.time.delay(int(1000 / fps))
    else:
        window.fill((10, 10, 10))
        draw_walls()

        mino_location = adjust_token_coordinates(mino_moves[- 2])
        player_location = adjust_token_coordinates(player_moves[-1])
        goal_location = adjust_token_coordinates(board.graph.graph["goal"])

        draw_tokens(mino_location, player_location, goal_location)
        draw_text(display_win_message)
        pygame.display.update()

    draw_text(display_win_message=True)
    pygame.display.update()

def reset_board(maze, player, mino, player_moves, mino_moves):
    """
    Reset the board to its initial state.
    """
    maze.graph.graph["player_location"] = player_moves[0]
    maze.graph.graph["mino_location"] = mino_moves[0]
    player = Player(maze)
    mino = Minotaur(maze)
    player_moves = [maze.graph.graph["player_location"], maze.graph.graph["player_location"]]
    mino_moves = [maze.graph.graph["mino_location"], maze.graph.graph["mino_location"], maze.graph.graph["mino_location"]]
    return player, mino, player_moves, mino_moves

def undo_move(maze, player, mino, player_moves, mino_moves):
    """
    Undo the last move.
    """
    maze.graph.graph["player_location"] = player_moves[-2]
    maze.graph.graph["mino_location"] = mino_moves[-3]
    player = Player(maze)
    mino = Minotaur(maze)
    player_moves.append(player_moves[-2])
    mino_moves.extend([mino_moves[-2], mino_moves[-3]])
    return player, mino, player_moves, mino_moves

def run_game():
    # Possible options are
    # `size`
    #   `small`
    #   `medium`
    #   `large`
    #   `random`
    #   A board size #x# where # is an integer dimension
    # `difficulty`
    #   `easy`
    #   `medium`
    #   `hard`
    #   `random`

    if len(sys.argv) == 1:
        # No args were given
        # Use random board size and difficulty
        maze_key = get_maze2(size="random", difficulty="random")
    elif len(sys.argv) == 2:
        # Only one arg was given. Interpret as board size.
        try:
            maze_key = get_maze2(size=sys.argv[1], difficulty="random")
        except Exception as e:
            sys.exit(f"ERROR: Please provide a valid size argument. {e}")
    elif len(sys.argv) > 2:
        # Two or more args were given. Interpret first two as board size and difficulty
        try:
            maze_key = get_maze2(size=sys.argv[1], difficulty=sys.argv[2])
        except Exception as e:
            sys.exit(f"ERROR: Please provide a valid size and difficulty argument. {e}")

    print("Maze key retrieved.")
    print(maze_key)

    # Set up board_class objects
    maze = Board(maze_key)
    player = Player(maze)
    mino = Minotaur(maze)

    # Add extra moves to make animation work easily
    player_moves = [maze.graph.graph["player_location"], maze.graph.graph["player_location"]]
    mino_moves = [maze.graph.graph["mino_location"], maze.graph.graph["mino_location"], maze.graph.graph["mino_location"]]

    # Run main
    # Set window size
    window_size, _, _ = calculate_window_size(maze)
    window = pygame.display.set_mode(size=window_size)
    pygame.display.set_caption("Minotaur Project")

    run = True
    draw = True
    game_end = False
    win_message = " "
    display_win_message = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and not game_end:
                # Get KEYDOWN so that holding a key will not trigger repeated movements.
                if event.key in [pygame.K_z, pygame.K_UP]:
                    # Up
                    try:
                        player_moves.append(player.move("up"))
                        mino_moves.extend(mino.move()[1])
                        draw = True
                    except ValueError:
                        pass
                if event.key in [pygame.K_q, pygame.K_LEFT]:
                    # Move left
                    try:
                        player_moves.append(player.move("left"))
                        mino_moves.extend(mino.move()[1])
                        draw = True
                    except ValueError:
                        pass
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    # Down
                    try:
                        player_moves.append(player.move("down"))
                        mino_moves.extend(mino.move()[1])
                        draw = True
                    except ValueError:
                        pass
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    # Right
                    try:
                        player_moves.append(player.move("right"))
                        mino_moves.extend(mino.move()[1])
                        draw = True
                    except ValueError:
                        pass
                if event.key == pygame.K_SPACE:
                    # Skip
                    try:
                        player_moves.append(player.move("skip"))
                        mino_moves.extend(mino.move()[1])
                        draw = True
                    except ValueError:
                        pass
                if event.key == pygame.K_BACKSPACE:
                    # Reset board
                    player, mino, player_moves, mino_moves = reset_board(maze, player, mino, player_moves, mino_moves)
                    draw = True
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    # Undo move
                    undo_move(maze, player, mino, player_moves, mino_moves)
                    draw = True
        game_end, game_win = maze.check_win_condition()
        if game_end:
            win_message = "YOU WIN!" if game_win else "YOU LOSE!"
            display_win_message = True

        # Redraw window
        if draw:
            draw_board(maze, window, player_moves, mino_moves, win_message, display_win_message)
            draw = False

    pygame.quit()

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "play":
            run_game()