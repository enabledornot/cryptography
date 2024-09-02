from tools import *
import sys
from collections import OrderedDict
def count_freq(src_code):
    freq_count = OrderedDict()
    for word in src_code:
        for letter in word:
            if letter not in freq_count:
                freq_count[letter] = 0
            freq_count[letter]+=1
    return OrderedDict(sorted(freq_count.items(), key=lambda x: x[1], reverse=True))
def perform_precalc():
    global msg_freq_count
    global en_letter_freq
    global prev_deductions
    src_filename = sys.argv[1]
    en_word_freq = loadWords()
    en_word_by_len = words_by_length(en_word_freq)
    for i,word_list in enumerate(en_word_by_len):
        if sum(word_list.values()) == 0:
            continue
        prev_deductions["?"*i] = (word_list,sum(word_list.values()),next(iter(word_list.values()),0) / sum(word_list.values()))
    en_letter_freq = loadLetters()
    src_codeing = readCodefile(src_filename)
    msg_freq_count = count_freq(src_codeing)
    return src_codeing
def pick_freqa_guesses(src_encoded, guessed_dl,guessed_el):
    global msg_freq_count
    global en_letter_freq
    guess_priority = []
    e_hit = 0
    for encoded_letter in msg_freq_count.keys():
        if encoded_letter not in guessed_el:
            e_hit += 1
            d_hit = 0
            for decoded_letter in en_letter_freq:
                if decoded_letter not in guessed_dl:
                    d_hit += 1
                    guess_priority.append((encoded_letter,decoded_letter))
                if d_hit == 5:
                    break
        if e_hit == 5:
            break
    return guess_priority
def apply_sub(src_encoded, map_guesses):
    new_src_encoded = []
    updated_words = []
    for i, e_word in enumerate(src_encoded):
        if any(item in e_word for item in map_guesses.keys()):
            updated_words.append(i)
            new_src_encoded.append([map_guesses[item] if item in map_guesses else item for item in e_word])
        else:
            new_src_encoded.append(e_word)
    return new_src_encoded, updated_words
def encoded_to_key(encoded):
    key = ""
    for e_letter in encoded:
        if len(e_letter) == 1:
            key += e_letter
        else:
            key += "?"
    return key
def get_word_ifcf(original_word, updated_word):
    global prev_deductions
    if not encoded_to_key(original_word) in prev_deductions:
        return 0, 0
    if encoded_to_key(updated_word) in prev_deductions:
        if prev_deductions[encoded_to_key(original_word)][1] == 0:
            return 0, 0
        rel_ded = prev_deductions[encoded_to_key(updated_word)]
        return  prev_deductions[encoded_to_key(updated_word)][1] / prev_deductions[encoded_to_key(original_word)][1], rel_ded[2]
        # return prev_deductions[encoded_to_key(updated_word)][1] / prev_deductions[encoded_to_key(original_word)][1]
    e_word_poss, e_word_cnt, _ = prev_deductions[encoded_to_key(original_word)]
    if e_word_cnt == 0:
        return 0, 0
    new_e_word_poss = OrderedDict()
    new_e_word_poss_cnt = 0
    for e_word in e_word_poss:
        if all(len(p_letter) > 1 or p_letter == c_letter for p_letter,c_letter in zip(updated_word, e_word)):
            new_e_word_poss[e_word] = e_word_poss[e_word]
            new_e_word_poss_cnt += e_word_poss[e_word]
    if new_e_word_poss_cnt == 0:
        new_e_word_poss_cnt = -1
    prev_deductions[encoded_to_key(updated_word)] = (new_e_word_poss, new_e_word_poss_cnt, next(iter(new_e_word_poss.values()),0) / new_e_word_poss_cnt)
    # return new_e_word_poss_cnt / e_word_cnt
    return new_e_word_poss_cnt / e_word_cnt, prev_deductions[encoded_to_key(updated_word)][2]
def avg(ls):
    return sum(ls) / len(ls)
# if = improvement factor (how much the additional letter narrowed down the word)
# cf = certainty factor (how certain it is that the word is the top choice)
def score_updated(src_encoded, p_src_encoded, updated_words):
    updated_word_if_list = []
    updated_word_cf_list = []
    # for updated_word_id in updated_words:
    #     original_word = src_encoded[updated_word_id]
    #     updated_word = p_src_encoded[updated_word_id]
    #     updated_word_if, updated_word_cf = get_word_ifcf(original_word,updated_word)
    #     updated_word_if_list.append(updated_word_if)
    #     updated_word_cf_list.append(updated_word_cf)
    for i, (original_word, updated_word) in enumerate(zip(src_encoded, p_src_encoded)):
        updated_word_if, updated_word_cf = get_word_ifcf(original_word,updated_word)
        if i in updated_words:
            updated_word_if_list.append(updated_word_if)
        updated_word_cf_list.append(updated_word_cf)
    return avg(updated_word_if_list), updated_word_cf_list
def decode_rec(src_encoded, guessed_dl, guessed_el,itr=0):
    global freq_count
    global en_letter_freq
    frequa_guesses = pick_freqa_guesses(src_encoded, guessed_dl, guessed_el)
    scored_guesses = []
    for frequa_guess in frequa_guesses:
        p_src_encoded, updated_words = apply_sub(src_encoded, {frequa_guess[0]:frequa_guess[1]})
        if len(updated_words) != 0:
            score = score_updated(src_encoded,p_src_encoded,updated_words)
        else:
            score = (0,0)
        scored_guesses.append((frequa_guess, score, p_src_encoded))
    scored_guesses.sort(key=lambda x: x[1][0], reverse=True)
    rec_rslts = []
    if itr < 1:
        for sg in scored_guesses[:5]:
            frequa_guess, score, p_src_encoded = sg
            if score[0] == 0:
                break
            rec_rslt = decode_rec(p_src_encoded, guessed_dl + [frequa_guess[1]], guessed_el + [frequa_guess[0]],itr=itr+1)
            rec_rslts.append((rec_rslt, frequa_guess))
    if len(rec_rslts) == 0:
        frequa_guess, score, p_src_encoded = scored_guesses[0]
        return score, {frequa_guess[0]:frequa_guess[1]}
    rec_rslt = max(rec_rslts, key=lambda x: x[0][0][0])
    (rec_score, rec_key), frequa_guess = rec_rslt
    rec_key[frequa_guess[0]] = frequa_guess[1]
    return rec_score, rec_key
def display_preview(encoded_message,rec_score, rec_key):
    print(rec_score[0])
    print(rec_key)
    print("")
    for word, word_score in zip(apply_sub(encoded_message,rec_key)[0],rec_score[1]):
        # subfil_word = encoded_to_key(apply_sub(word,rec_key)[0])
        print("{:16.6f}-{}".format(word_score,encoded_to_key(word)))
    # print(frequa_guesses)
global prev_deductions
prev_deductions = {}
encoded_message = perform_precalc()
rec_score, rec_key = decode_rec(encoded_message, [], [])
display_preview(encoded_message,rec_score,rec_key)
# print(rec_score)
# print(rec_key)
# print()