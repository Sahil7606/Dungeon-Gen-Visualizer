class World:
    """
    Represents the map as a 2D integer grid.

    Attributes:
        width (int): the width of the world
        height (int): the height of the world
        grid (list[list[int]]): the 2D map grid where each integer represents a tile type
    """

    def __init__(self, width: int = 320, height: int = 180) -> None:
        """
        Initializes the world grid with default filled tiles.

        Args:
            width (int): the width of the map in tiles
            height (int): the height of the map in tiles
        """
        self.width = width
        self.height = height
        self.grid = [[1] * self.width for _ in range(self.height)]

    def __repr__(self) -> str:
        """
        Converts the world grid into a printable string.

        Returns:
            (str): a line-by-line string view of the world grid
        """
        if not self.grid:
            return ""

        cell_width = max(
            1,
            max(len(str(cell)) for row in self.grid for cell in row),
        )
        row_label_sep = " | "
        out_lines = []

        for row_index, row in enumerate(self.grid):
            cells = []
            for cell in row:
                cell_text = "-" if cell == 1 else str(cell)
                cells.append(cell_text.rjust(cell_width))
            out_lines.append(" ".join(cells) + f"{row_label_sep}{row_index}")


        return "\n".join(out_lines)
    
    def clear_world(self) -> None:
        self.grid = [[1] * self.width for _ in range(self.height)]
            