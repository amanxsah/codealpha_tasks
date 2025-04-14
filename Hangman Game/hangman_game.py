import random
import hangman_stages
from tkinter.colorchooser import Chooser
word_list=["apple","banana","grape","kiwi"]
lives=6
chosen_word=random.choice(word_list)
print(chosen_word)
display=[]
for letter in chosen_word:
    display += '-'
print(display)
game_over = False
while not game_over:
    guessed_letter=input("Guess a Letter: ").lower()
    for position in range(len(chosen_word)):
        letter = chosen_word[position]
        if letter==guessed_letter:
            display[position]=guessed_letter
    print(display)
    if guessed_letter not in chosen_word:
        lives -= 1
        if lives == 0:
            game_over = True
            print("You Loose !!")
    if '-' not in display:
        game_over = True
        print("You won !!")
    print(hangman_stages.stage[lives])
        