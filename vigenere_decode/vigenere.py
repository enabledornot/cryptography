import sys
def char_to_num(c):
    c = c.lower()
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    elif 'A' <= c <= 'Z':
        return ord(c) - ord('A')
    else:
        print("letter convert error")
def num_to_chr(n):
    return chr(n % 26 + ord('A'))
def handle_input(input):
    try:
        with open(input, "r") as f:
            return f.read()
    except:
        return input
# codeword - the word which the message was encoded with
# e_message - the message which has been encoded
def v_decode(codeword, e_message):
    d_message = ""
    for i in range(len(e_message)):
        new_num = (char_to_num(codeword[i % len(codeword)]) - char_to_num(e_message[i])) % 26
        d_message+=num_to_chr(new_num)
    return d_message
def v_encode(codeword, d_message):
    e_message = ""
    for i in range(len(d_message)):
        new_num = (char_to_num(codeword[i % len(codeword)]) + char_to_num(d_message[i])) % 26
        e_message+=num_to_chr(new_num)
    return e_message
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("invalid command format")
        print("python vigenere.py <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>")
    else:
        message = handle_input(sys.argv[2])
        codeword = handle_input(sys.argv[3])
        if sys.argv[1] == 'encode':
            result = v_encode(codeword,message)
            print("encoded message: {}".format(result))
        elif sys.argv[1] == 'decode':
            result = v_decode(codeword,message)
            print("decoded message: {}".format(result))
        else:
            print("invalid command action")
            print("python vigenere.py <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>")
