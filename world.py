class World:
    """
    Represents the map as a 2D integer grid.

    Attributes:
        grid (list[list[int]]): the 2D map grid where each integer represents a tile type
    """

    def __init__(self, width: int = 320, height: int = 180) -> None:
        """
        Initializes the world grid with default filled tiles.

        Args:
            width (int): the width of the map in tiles
            height (int): the height of the map in tiles
        """
        self.grid = [[1] * width for _ in range(height)]

    def __repr__(self) -> str:
        """
        Converts the world grid into a printable string.

        Returns:
            (str): a line-by-line string view of the world grid
        """
        out = ""

        for row in self.grid:
            string = ""
            for cell in row:
                if cell == 1:
                    string += "  "
                else:
                    string += (str(cell) + " ")

            out += string + "\n"

        return out

            