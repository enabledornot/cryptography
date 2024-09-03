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
def v_decode(codeword, e_message, cesar=0, word_off=0):
    d_message = ""
    for i in range(len(e_message)):
        new_num = (char_to_num(e_message[i]) - char_to_num(codeword[(i + word_off) % len(codeword)]) + cesar) % 26
        d_message+=num_to_chr(new_num)
    return d_message
def v_encode(codeword, d_message, cesar=0, word_off=0):
    e_message = ""
    for i in range(len(d_message)):
        new_num = (char_to_num(codeword[(i + word_off) % len(codeword)]) + char_to_num(d_message[i]) + cesar) % 26
        e_message+=num_to_chr(new_num)
    return e_message
def v_guess_length(message):
    cycles = [0]
    for offset in range(1,len(message)):
        cycles.append(0)
        for ii in range(0, len(message) - offset):
            if message[ii] == message[offset+ii]:
                cycles[-1] += 1
    return cycles.index(max(cycles)), cycles
if __name__ == "__main__":
    if len(sys.argv) == 4:
        message = handle_input(sys.argv[2])
        codeword = handle_input(sys.argv[3])
        if sys.argv[1] == 'encode':
            # for i in range(26):
            #     print(v_encode(codeword,message,cesar=i))
            result = v_encode(codeword,message)
            print("encoded message: {}".format(result))
        elif sys.argv[1] == 'decode':
            # for i in range(19):
            #     print(v_decode(codeword,message,word_off=i))
            result = v_decode(codeword,message)
            print("decoded message: {}".format(result))
        else:
            print("invalid command action")
            print("python vigenere.py <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>")
    elif len(sys.argv) == 3:
        message = handle_input(sys.argv[2])
        if sys.argv[1] == 'cw_len':
            keyword_len, cycles = v_guess_length(message)
            print("guessed codeword length: {}".format(keyword_len))
            print("offset - duplicate count")
            for i, cycle in enumerate(cycles):
                if i == 0:
                    continue
                if max(cycles) == cycle:
                    print("\033[1m",end="")
                print("{:2} - {}".format(i,cycle))
                if max(cycles) == cycle:
                    print("\033[0m",end="")
    else:
        print("invalid command format")
        print("python vigenere.py <encode:decode> <message_or_filename_of_message> <codeword_or_filename_of_codeword>")
