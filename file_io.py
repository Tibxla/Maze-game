import random
"""import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"




def generate_maze_with_llm(size, difficulty):

    def generate_maze_position(size):
        x, y = size
        position_mino=(random.randint(1, x - 2), random.randint(1, y - 2))
        position_exit = (size[0] - 1, size[1] - 1)
        return position_mino,position_exit
    
    def generate_maze_walls(size, difficulty,goal,mino_start):
        # Préparer la requête pour le LLM
        prompt = 
        
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama2",
            "prompt": prompt,
            "max_tokens": 512
        }

        # Afficher la requête avant de l'envoyer
        print("Requête envoyée à l'API :")
        print(json.dumps(data, indent=2))

         # Envoyer la requête à l'API
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data), stream=True)

        if response.status_code != 200:
            raise Exception(f"Erreur lors de la requête LLM : {response.text}")

        # Collecter toutes les parties de la réponse
        collected_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    part = json.loads(line.decode("utf-8"))
                    collected_response += part.get("response", "")
                except json.JSONDecodeError:
                    continue

        # Vérifier si la réponse est complète
        try:
            # Évaluer la réponse comme une liste Python
            walls = eval(collected_response.strip())
            return walls
        except Exception as e:
            raise ValueError(f"Erreur lors du traitement de la réponse collectée : {collected_response}\nErreur : {e}")
    
    mino_start,goal=generate_maze_position(size)
    walls=generate_maze_walls(size, difficulty,goal,mino_start)
    maze_key = {
        "size_board": size,
        "goal": goal,
        "mino_start": mino_start,
        "player_start": (0, 0),
        "walls": walls
    }
    return maze_key"""


def generate_mazetest(size, difficulty):
    x, y = size
    maze_key = {
        'size_board': size,
        'goal': (x - 1, y - 1),
        'mino_start': (random.randint(1, x - 2), random.randint(1, y - 2)),
        'player_start': (0, 0),
        'walls': []
    }

    # Create a grid to represent the maze
    grid = [[0] * y for _ in range(x)]

    # Directions for moving in the grid (right, down, left, up)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def in_bounds(x, y):
        # Check if the coordinates are within the grid bounds
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def dfs(x, y):
        # Mark the current cell as visited
        grid[x][y] = 1
        # Shuffle the directions to randomize the maze generation
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if in_bounds(nx, ny) and grid[nx][ny] == 0:
                # Mark the wall between the current cell and the next cell as visited
                grid[x + dx][y + dy] = 1
                dfs(nx, ny)

    # Start DFS from the player start position
    dfs(0, 0)

    # Convert the grid to a list of walls
    for i in range(x):
        for j in range(y):
            if grid[i][j] == 0:
                if i > 0 and grid[i - 1][j] == 1:
                    maze_key['walls'].append(((i, j), (i - 1, j)))
                if j > 0 and grid[i][j - 1] == 1:
                    maze_key['walls'].append(((i, j), (i, j - 1)))

    # Remove some walls based on difficulty
    if difficulty == 'easy':
        num_walls_to_remove = int(len(maze_key['walls']) * 0.6)
    elif difficulty == 'medium':
        num_walls_to_remove = int(len(maze_key['walls']) * 0.3)
    elif difficulty == 'hard':
        num_walls_to_remove = int(len(maze_key['walls']) * 0)
    else:
        num_walls_to_remove = int(len(maze_key['walls']) * random.uniform(0, 0.6))

    walls_to_remove = random.sample(maze_key['walls'], num_walls_to_remove)
    maze_key['walls'] = [wall for wall in maze_key['walls'] if wall not in walls_to_remove]

    return maze_key


def get_maze2(size="random", difficulty="random"):
    """
    Get a maze key based on size and difficulty.
    """
    if size == "small":
        size = (8, 8)
    elif size == "medium":
        size = (16, 16)
    elif size == "large":
        size = (32, 32)
    elif size == "random":
        size = (random.randint(8, 32), random.randint(8, 32))
    elif isinstance(size, str) and 'x' in size:
        size = tuple(map(int, size.split('x')))

    print("Generating {} difficulty maze of size {}...".format(difficulty, size))
    maze_key = generate_mazetest(size, difficulty)
    return maze_key

