class World:
    def __init__(self, width: int = 320, height: int = 180):
        self.grid = [[1] * width for _ in range(height)]

    def __repr__(self):
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

            