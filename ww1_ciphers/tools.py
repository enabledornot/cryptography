def clean_text(text):
    return ''.join(char for char in text.lower() if char.isalpha()).replace('j','i')
def handle_input(input):
    try:
        with open(input, "r") as f:
            return f.read()
    except:
        return input