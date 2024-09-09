import string
def clean_text(text):
    return ''.join(char for char in text.lower() if char.isalpha()).replace('j','i')
def handle_input(input):
    try:
        with open(input, "r") as f:
            return f.read()
    except:
        return input
class Polybius:
    def __init__(self, codeword):
        codeword = clean_text(codeword)
        self.grid = []
        for c in codeword:
            if c not in self.grid:
                self.grid.append(c)
        for c in string.ascii_lowercase:
            if c == 'j':
                continue
            if c not in self.grid:
                self.grid.append(c)
    def row_column(self,letter):
        letter_index = self.grid.index(letter)
        return letter_index // 5, letter_index % 5
    def get(self, row, column):
            row = row % 5
            column = column % 5
            return self.grid[row*5 + column]