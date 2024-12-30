import networkx as nx
import copy


class Board:
    def __init__(self, maze_key=None):
        """
        Initialize the board with a maze key, or generate a random maze.
        """
        self.maze_key = None
        self.graph = None

        if maze_key:
            self.maze_key = maze_key
            self.graph = self.build_maze(self.maze_key)
            if not self.validate_maze(self.graph):
                raise ValueError("Invalid maze key provided.")

        self.add_move_options()

    def get_player_location(self):
        """
        Get the current player location.
        """
        return self.graph.graph["player_location"]

    def get_minotaur_location(self):
        """
        Get the current minotaur location.
        """
        return self.graph.graph["mino_location"]

    def get_goal_location(self):
        """
        Get the goal location.
        """
        return self.graph.graph["goal"]

    def build_maze(self, maze_key, verbose=False):
        """
        Build the maze graph from a maze key.
        """
        size_board = maze_key["size_board"]
        graph = nx.grid_2d_graph(*size_board)
        graph.graph['size_board'] = size_board
        graph.graph["player_location"] = maze_key["player_start"]
        graph.graph["mino_location"] = maze_key["mino_start"]
        graph.graph["goal"] = maze_key["goal"]

        # Add edges with default weight 0
        graph.add_edges_from(graph.edges, weight=0)
        # Add walls with weight -1
        walls = maze_key["walls"]
        graph.add_edges_from(walls, weight=-1)

        if verbose:
            print(maze_key)

        return graph

    def remove_wall_edges(self, maze):
        """
        Remove wall edges from the maze graph.
        """
        if "weight" in maze.edges[list(maze.edges)[0]]:
            walls = [edge for edge in maze.edges if maze.edges[edge]["weight"] == -1]
            maze_remove_wall_edges = copy.deepcopy(maze)
            maze_remove_wall_edges.remove_edges_from(walls)

        return maze_remove_wall_edges

    def validate_maze(self, maze):
        """
        Validate the maze to ensure it has no closed-off sections.
        """
        maze_remove_wall_edges = self.remove_wall_edges(maze)
        return nx.is_connected(maze_remove_wall_edges)

    def add_move_options(self):
        """
        Add move options to each node in the graph.
        """
        reference = self.remove_wall_edges(self.graph)

        for node in self.graph.nodes:
            self.graph.nodes[node]["options"] = ["skip"]

            connected_nodes = nx.neighbors(reference, node)

            for neighbor in connected_nodes:
                if neighbor == (node[0] + 1, node[1] + 0):
                    self.graph.nodes[node]["options"].append("right")
                elif neighbor == (node[0] - 1, node[1] + 0):
                    self.graph.nodes[node]["options"].append("left")
                elif neighbor == (node[0] + 0, node[1] - 1):
                    self.graph.nodes[node]["options"].append("up")
                elif neighbor == (node[0] + 0, node[1] + 1):
                    self.graph.nodes[node]["options"].append("down")

    def get_move_options(self, node=None):
        """
        Get the move options for the player and minotaur.
        """
        move_options = {}
        if node:
            move_options["player"] = self.graph.nodes[node]["options"]
            move_options["mino"] = self.graph.nodes[node]["options"][1:]
            return move_options

        player_location = self.get_player_location()
        mino_location = self.get_minotaur_location()
        move_options["player"] = self.graph.nodes[player_location]["options"]
        move_options["mino"] = self.graph.nodes[mino_location]["options"][1:]

        return move_options

    def check_win_condition(self):
        """
        Check the win condition of the game.
        """
        if self.graph.graph["mino_location"] == self.graph.graph["player_location"]:
            return True, False
        elif self.graph.graph["player_location"] == self.graph.graph["goal"] and self.graph.graph["mino_location"] != self.graph.graph["player_location"]:
            return True, True
        else:
            return False, False

class Minotaur:
    def __init__(self, maze):
        """
        Initialize the minotaur with the maze.
        """
        self.maze = maze
        self.location = maze.graph.graph["mino_location"]

    def move(self):
        """
        Move the minotaur based on the movement ruleset.
        """
        mino_location = self.maze.graph.graph["mino_location"]
        player_location = self.maze.graph.graph["player_location"]

        remaining_moves = 1
        move_to = []

        while remaining_moves > 0:
            move_options = self.maze.get_move_options()["mino"]

            if "right" in move_options and player_location[0] > mino_location[0]:
                mino_location = (mino_location[0] + 1, mino_location[1] + 0)
                move_to.append(mino_location)
            elif "left" in move_options and player_location[0] < mino_location[0]:
                mino_location = (mino_location[0] - 1, mino_location[1] + 0)
                move_to.append(mino_location)
            elif "up" in move_options and player_location[1] < mino_location[1]:
                mino_location = (mino_location[0] + 0, mino_location[1] - 1)
                move_to.append(mino_location)
            elif "down" in move_options and player_location[1] > mino_location[1]:
                mino_location = (mino_location[0] + 0, mino_location[1] + 1)
                move_to.append(mino_location)
            else:
                move_to.append(mino_location)

            remaining_moves -= 1
            self.maze.graph.graph["mino_location"] = mino_location

        self.location = mino_location
        return mino_location, move_to

class Player:
    def __init__(self, maze):
        """
        Initialize the player with the maze.
        """
        self.maze = maze
        self.location = maze.graph.graph["player_location"]

    def move(self, direction):
        """
        Move the player in the specified direction.
        """
        if direction not in self.maze.get_move_options()["player"]:
            raise ValueError(f"{direction} is not a valid direction.")
        else:
            player_location = self.maze.graph.graph["player_location"]

            if direction == "skip":
                pass
            elif direction == "right":
                player_location = (self.location[0] + 1, self.location[1] + 0)
            elif direction == "left":
                player_location = (self.location[0] - 1, self.location[1] + 0)
            elif direction == "up":
                player_location = (self.location[0] + 0, self.location[1] - 1)
            elif direction == "down":
                player_location = (self.location[0] + 0, self.location[1] + 1)

        self.maze.graph.graph["player_location"] = player_location
        self.location = player_location
        return player_location



