import sys
import re
from pyfiglet import Figlet
from tabulate import tabulate


#Custom error for empty string
class EmptyStringError(Exception):
    pass


#Custom error for decryption validation
class IncorrectDigitEncryptionError(Exception):
    pass


def main():

    #Intro
    figlet = Figlet()
    figlet.setFont(font='rectangles')
    print(figlet.renderText("Welcome to the Encryption and Decryption tool"))

    while True:

        #Prompting the user for choice
        while True:
            try:
                choice = validate_choice(input("Enter 1 to encrypt, 2 to decrypt or 3 to exit: "))
                break
            except ValueError:
                print("Incorrect input")
                pass
            except EOFError:
                    sys.exit("\nProgram terminated")

        #Choice target 1, prompting the user for the text to be encrypted and the encryption key
        if choice == "1":

            #Acquiring and validating the text to be encrypted
            while True:
                try:
                    text = input("Enter the text you want to encrypt: ")
                    if text == "":
                        raise EmptyStringError
                    break
                except EmptyStringError:
                    print("Invalid input: Nothing was entered")
                    pass
                except EOFError:
                    sys.exit("\nProgram terminated")

            #Acquiring and validating the encryption key
            while True:
                try:
                    encryption_key = input("Enter the encryption key: ")
                    if encryption_key == "":
                        raise EmptyStringError
                    break
                except EmptyStringError:
                    print("Invalid input: Nothing was entered")
                    pass
                except EOFError:
                    sys.exit("\nProgram terminated")

            #Printing the encrypted text
            encrypted_text = encrypt(text, encryption_key)
            encryption_table = [["Text", text], ["Encryption key", encryption_key], ["Encrypted text", encrypted_text]]
            print(tabulate(encryption_table, tablefmt="double_grid"))

        #Choice target 2, prompting the user for the text to be decrypted and the encryption phrase
        elif choice == "2":
            #Acquiring and validating the text to be decrypted
            while True:
                try:
                    text = input("Enter the text you want to decrypt: ")
                    if text == "":
                        raise EmptyStringError
                    if  decryption_text_valdiation(text):
                        break
                except EmptyStringError:
                    print("Invalid input: Nothing was entered")
                    pass
                except IncorrectDigitEncryptionError:
                    print("Invalid input: Incorrect digit encryption")
                    pass
                except EOFError:
                    sys.exit("\nProgram terminated")

            #Acquiring and validating the encryption key
            while True:
                try:
                    encryption_key = input("Enter the encryption key: ")
                    if encryption_key == "":
                        raise EmptyStringError
                    break
                except EmptyStringError:
                    print("Invalid input: Nothing was entered")
                    pass
                except EOFError:
                    sys.exit("\nProgram terminated")
            
            #Printing the decrypted text
            decryption = decrypt(text, encryption_key)
            decryption_table = [["Encrypted text", text], ["Encryption key", encryption_key], ["Original text", decryption]]
            print(tabulate(decryption_table, tablefmt="double_grid"))

        #Choice target 3, exiting the program
        else:
            sys.exit("Program terminated")


#Used to validate the choice
def validate_choice(choice):
    if choice not in ["1", "2", "3"]:
        raise ValueError
    else:
        return choice


#Encryption function, the encryption process is described in README.md
def encrypt(text, encryption_key):
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    zero_to_three = {"0": "#7#", "1": "#8#", "2": "#9#", "3": "#0#"}
    special = {"@": "(@)", "#": "(#)"}
    encrypted_text = []
    en_key_counter = 0
    text = text.split()
    for word in text:
        new_word = ""
        left = ""
        right = ""
        for char in word:
            en_key_index = 0
            if char.isalpha():
                if char.islower():
                    index = alphabet_lower.index(char)
                    if encryption_key[en_key_counter].isalpha():
                        if encryption_key[en_key_counter].islower():
                            en_key_index = alphabet_lower.index(encryption_key[en_key_counter])
                        else:
                            en_key_index = alphabet_upper.index(encryption_key[en_key_counter])
                    elif encryption_key[en_key_counter].isdigit():
                        en_key_index = int(encryption_key[en_key_counter])
                    else:
                        en_key_index = 13
                    new_index = (index + en_key_index) % 26
                    new_word += alphabet_upper[new_index]
                    en_key_counter += 1
                    if en_key_counter == len(encryption_key):
                        en_key_counter = 0
                elif char.isupper():
                    index = alphabet_upper.index(char)
                    if encryption_key[en_key_counter].isalpha():
                        if encryption_key[en_key_counter].islower():
                            en_key_index = alphabet_lower.index(encryption_key[en_key_counter])
                        else:
                            en_key_index = alphabet_upper.index(encryption_key[en_key_counter])
                    elif encryption_key[en_key_counter].isdigit():
                        en_key_index = int(encryption_key[en_key_counter])
                    else:
                        en_key_index = 13
                    new_index = (index + en_key_index) % 26
                    new_word += alphabet_lower[new_index]
                    en_key_counter += 1
                    if en_key_counter == len(encryption_key):
                        en_key_counter = 0
            elif char.isdigit():
                if char in zero_to_three:
                    new_word += zero_to_three[char]
                else:
                    square = int(char) ** 2
                    squares = str(square)
                    left += squares[0]
                    right += squares[1]
                    new_word += "@"
            elif char in special:
                new_word += special[char]
            else:
                new_word += char
        left = left [::-1]
        encrypted_word = left + new_word + right
        encrypted_text.append(encrypted_word[::-1])

    return " ".join(encrypted_text)


#Used to validate the encrypted text for decryption, the process is described in README.md
def decryption_text_valdiation(text):
    text = text.split()
    for word in text:
        
        #Checks if 'word' contains digits only, which is incorrect
        if word.isdigit():
            raise IncorrectDigitEncryptionError

        #Returns 'word' to its original order
        word = word[::-1]

        #Splits 'word' into 'left', 'word' and 'right'
        left = ""
        right = ""
        j = 0
        for char in word:
            if char.isdigit():
                continue
            elif not char.isdigit():
                left = word[:(word.index(char))]
                word = word[(word.index(char)):]
                left = left[::-1]
                word = word[::-1]
                break
        for char in word:
            if char.isdigit():
                continue
            elif not char.isdigit():
                right = word[:(word.index(char))]
                word = word[(word.index(char)):]
                right = right[::-1]
                word = word[::-1]
                break

        #Checks if the encryption of digits from 0 to 3 is correct
        if len(re.findall(r"(7|8|9|0)", word)) == len(re.findall(r"#(7|8|9|0)#", word)):
            pass
        else:
            raise IncorrectDigitEncryptionError

        #Checks if the character "#" follows the encryption rules
        if len(re.findall(r"#", word)) == (len(re.findall(r"#(7|8|9|0)#", word)) * 2 + len(re.findall(r"\(#\)", word))):
            pass
        else:
            raise IncorrectDigitEncryptionError

        #Checks if the length of digits' encryption matches the character "@" rules
        if len(left) == len(right) == (len(re.findall(r"@", word)) - len(re.findall(r"\(@\)", word))):
            pass
        else:
            raise IncorrectDigitEncryptionError

        #Checks if the digits on both ends form perfect squares from 4 to 9
        for j in range(len(left)):
            sqr_num = left[j] + right[j]
            if sqr_num in ["16", "25", "36", "49", "64", "81"]:
                pass
            else:
                raise IncorrectDigitEncryptionError

    return True


#Decryption function, the decryption process is described in README.md
def decrypt(text, encryption_key):
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    zero_to_three_rev = {"#7#": "0", "#8#": "1", "#9#": "2", "#0#": "3"}
    unspecial = {"(@)": "@", "(#)": "#"}
    decrypted_text = []
    en_key_counter = 0
    text = text.split()
    for word in text:

        #Returns 'word' to its original order
        word = word[::-1]

        original_word = ""
        left = ""
        right = ""
        i = 0
        j = 0
        en_key_index = 0
        for char in word:
            if char.isdigit():
                continue
            elif not char.isdigit():
                left = word[:(word.index(char))]
                word = word[(word.index(char)):]
                left = left[::-1]
                word = word[::-1]
                break
        for char in word:
            if char.isdigit():
                continue
            elif not char.isdigit():
                right = word[:(word.index(char))]
                word = word[(word.index(char)):]
                right = right[::-1]
                word = word[::-1]
                break
        while i <= len(word) - 1:
            if word[i].isalpha():
                if word[i].isupper():
                    index = alphabet_upper.index(word[i])
                    if encryption_key[en_key_counter].isalpha():
                        if encryption_key[en_key_counter].islower():
                            en_key_index = alphabet_lower.index(encryption_key[en_key_counter])
                        else:
                            en_key_index = alphabet_upper.index(encryption_key[en_key_counter])
                    elif encryption_key[en_key_counter].isdigit():
                        en_key_index = int(encryption_key[en_key_counter])
                    else:
                        en_key_index = 13
                    old_index = (index - en_key_index + 26) % 26
                    original_word += alphabet_lower[old_index]
                    en_key_counter += 1
                    if en_key_counter == len(encryption_key):
                        en_key_counter = 0
                    i += 1
                elif word[i].islower():
                    index = alphabet_lower.index(word[i])
                    if encryption_key[en_key_counter].isalpha():
                        if encryption_key[en_key_counter].islower():
                            en_key_index = alphabet_lower.index(encryption_key[en_key_counter])
                        else:
                            en_key_index = alphabet_upper.index(encryption_key[en_key_counter])
                    elif encryption_key[en_key_counter].isdigit():
                        en_key_index = int(encryption_key[en_key_counter])
                    else:
                        en_key_index = 13
                    old_index = (index - en_key_index + 26) % 26
                    original_word += alphabet_lower[old_index]
                    en_key_counter += 1
                    if en_key_counter == len(encryption_key):
                        en_key_counter = 0
                    i += 1
            elif word[i] == "@":
                square = int(left[j] + right[j])
                num, _ = str(square ** 0.5).split(".")
                original_word += num
                j += 1
                i += 1
            elif i + 2 <= len(word) - 1:
                if word[i] == "#":
                    if (word[i] + word[i+1] + word[i+2]) in zero_to_three_rev:
                        original_word += zero_to_three_rev[(word[i] + word[i+1] + word[i+2])]
                        i += 3
                    else:
                        original_word += word[i]
                        i += 1
                elif word[i] == "(":
                    if (word[i] + word[i+1] + word[i+2]) in unspecial:
                        original_word += unspecial[(word[i] + word[i+1] + word[i+2])]
                        i += 3
                    else:
                        original_word += word[i]
                        i += 1
                else:
                    original_word += word[i]
                    i += 1
            else:
                original_word += word[i]
                i += 1
        decrypted_text.append(original_word)

    return " ".join(decrypted_text)


if __name__ == "__main__":
    main()
