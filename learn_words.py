# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 23:58:25 2024

@author: ville
"""

import numpy as np
import random as rnd
from termcolor import colored
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)


def lobby():
    command = input("To make changes to word sets, type 'input'. " +
                    "To play, type 'play'. To display the words in a set, " +
                    "type 'display'. ")
    print()

    if (command == "input"):
        input_procedure()
        lobby()
    elif (command == "play"):
        word_set = input("Input the name of the word set "
                         + "you want to play. ")
        print()
        translation_direction = int(input("If you want to translate finnish to " +
                                      "german, type '1'. If you want to " +
                                      "translate german to finnish, type '2'. "))
        print(translation_direction)
        if (translation_direction != 1 and translation_direction != 2):
            print()
            print("Invalid input.")
            print()
            lobby()
        game(word_set, translation_direction)
        lobby()
    elif (command == "display"):
        word_set = input("Input the name of the word set "
                         + "you want to be displayed. ")
        display(word_set)
        lobby()
    else:
        print("Invalid input.")
        lobby()


def input_procedure():
    command = input("To write a new word set, type 'new'. To cut an " +
                    "existing set into multiple sets, type 'cut'. ")

    if (command == "new"):
        language1 = np.array([])
        language2 = np.array([])

        language1_input = ""

        while (language1_input != "done"):
            language1_input = input("Input a word "
                                    + "(if you are done, type 'done'): ")
            if (language1_input != "done"):
                language2_input = input("Translation: ")

                language1 = np.append(language1, language1_input)
                language2 = np.append(language2, language2_input)

        file_name = input("Name of this word set: ")

        f = open(file_name + ".txt", "x")

        for i in range(len(language1)):
            f.write(language1[i])
            if (i != len(language1) - 1):
                f.write(",")
        f.write("\n")
        f.write("\n")
        for i in range(len(language2)):
            f.write(language2[i])
            if (i != len(language2) - 1):
                f.write(",")

        f.close()
    elif (command == "cut"):
        word_set = input("Type the name of the word set. ")

        language1 = np.loadtxt(word_set + ".txt", dtype=str,
                               max_rows=1, delimiter=",")
        language2 = np.loadtxt(word_set + ".txt", dtype=str, max_rows=1,
                               delimiter=",", skiprows=2)

        indices = np.arange(0, len(language1), 1, dtype=int)
        rnd.shuffle(indices)
        language1 = language1[indices]
        language2 = language2[indices]

        number_of_sets = int(input("How many sets do you want to cut" +
                                   " this set into? "))

        number_of_words = int(np.ceil(len(language1) / (number_of_sets * 1.)))

        for i in range(number_of_sets):
            file_name = word_set + "_" + str(i + 1) + ".txt"

            f = open(file_name, "x")

            for j in range(number_of_words):
                if (i * number_of_words + j == len(language1)):
                    break
                f.write(language1[i * number_of_words + j])
                if (j != number_of_words - 1 and
                        i * number_of_words + j != len(language1) - 1):
                    f.write(",")
            f.write("\n")
            f.write("\n")
            for j in range(number_of_words):
                if (i * number_of_words + j == len(language2)):
                    break
                f.write(language2[i * number_of_words + j])
                if (j != number_of_words - 1 and
                        i * number_of_words + j != len(language2) - 1):
                    f.write(",")


def game(word_set, translation_direction):
    try:
        language1 = np.loadtxt(word_set + ".txt", dtype=str,
                               max_rows=1, delimiter=",")
        language2 = np.loadtxt(word_set + ".txt", dtype=str, max_rows=1,
                               delimiter=",", skiprows=2)
    except:
        print()
        print("Word set not found.")
        print()
        return
    if (translation_direction == 2):
        memory = language1
        language1 = language2
        language2 = memory

    if (len(language1) != len(language2)):
        print("The amount of words doesn't match the amount of translations.")
        print(len(language1))
        print(len(language2))

    print()
    print("You will be given a word and you have to translate it. If at any " +
          "point you want to quit, just type 'quit'.")
    print()

    while (len(language1) > 0):
        random_index = rnd.randint(0, len(language1) - 1)

        ans = input(language1[random_index] + " - ")

        if (ans == "quit"):
            print()
            return

        if (ans == language2[random_index]):
            print(colored("Correct!", "green"))
            language1 = np.delete(language1, random_index)
            language2 = np.delete(language2, random_index)
        else:
            print(colored("Incorrect. Correct answer: " +
                          language2[random_index], "red"))

    print()
    print("You cleared the word set!")
    print()


def display(word_set):
    language1 = np.loadtxt(word_set + ".txt", dtype=str,
                           max_rows=1, delimiter=",")
    language2 = np.loadtxt(word_set + ".txt", dtype=str, max_rows=1,
                           delimiter=",", skiprows=2)

    print()
    for i in range(len(language1)):
        print(language1[i] + " - " + language2[i])
        if (i != len(language1) - 1):
            print()

    input()


lobby()
