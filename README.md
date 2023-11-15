# Encryption/Decryption Tool with Key

This project is a version of an encryption/decryption tool combined with a key for an extra layer of protection. It consists of the following files:

- `project.py`: Contains the code for the encryption/decryption tool.
- `test_project.py`: Tests vital functions from `project.py` to avoid various errors.
- `requirements.txt`: Contains the pip-installable libraries used in `project.py` and `test_project.py`.
- `README.md`: Explains the project in detail and provides an overview of each file.

## Execution

Upon running the program, a welcome text is displayed using the `pyfiglet` library. The user is then prompted to choose from three options: encrypt, decrypt, or exit. The function `validate_choice(choice)` validates the input provided.

### Encryption

If the user chooses to encrypt, they will be prompted to enter a text to encrypt and an encryption key. Both inputs are validated to ensure they are not empty. A custom error, `emptystringerror`, has been created using a class that inherits from `exception`. All other characters are allowed.

The encryption process involves modifying the text based on its character type and combining alphabet characters with the encryption key to produce new characters. This approach increases the complexity of the encryption.

To ensure stronger encryption, each encryption key is made unique by looping through it for each alphabet character in the length of the given text by using (`en_key_counter`). This makes decrypting part of the encrypted text yield an incorrect result.

The following describes the encryption process for each character `char` in each `word` in the target text, after splitting it using `split()`:

- If `char` is a lowercase alphabet character, its index value is obtained from a given lowercase alphabet. Based on the character in the key:
   - If the character in the key is in the alphabet, its index value is obtained from a given alphabet string. This value is added to the index value of `char`.
   - If the character in the key is a digit, its integer value is added to the index value of `char`.
   - If the character in the key is anything else, half the length of the alphabet (13) is added to the index value of `char`.

The remainder of this value after dividing by 26 (the length of the alphabet) is used as the new index value, which is then replaced by an uppercase alphabet character from a given alphabet string.

- If `char` is an uppercase alphabet character, a similar process is applied but it will be replaced by a lowercase alphabet character.

- If `char` is a digit:
   - If `char` is "0", "1", "2", or "3", it is replaced with "#7#", "#8#", "#9#", or "#0#", respectively, using a given dictionary. This substitution adds chaotic nature to the encryption.
   - If `char` is larger than 3, it is squared and split in half. The left value is added to a 'left' string, the right value is added to a 'right' string, and `char` is replaced with "@". After processing the last character in the word, the order of 'left' is reversed. The final result is obtained by concatenating `left`, `word`, and `right`. This addition of extra characters to each word makes the encryption result harder to read.

- If `char` is "#" or "@", parentheses are added to differentiate it from digit encryption, which may cause errors in the decryption process.

- If `char` is anything else, it is kept as is.

After processing the last `char`, the `word` is reversed, and the total word result is added to a list. This adds more chaos to the final encrypted text.

Once all words are processed, they are joined with a space using `"".join()` and returned as the total encrypted text.

Using the `tabulate` library, a table is printed that displays the text, encryption key, and encrypted text.

### Decryption

Choosing the decrypt option will prompt the user for the following inputs:

- An encrypted text: The encrypted text provided will undergo thorough validation using regular expressions. Each `word` in the text must meet specific criteria:
  - If `word` contains "#", it must be between brackets as "(#)" or one of the following: "#7#", "#8#", "#9#", and/or "#0#".
  - If numbers are present on both the left and right sides of `word`, the length of the left side must be equal to the length of the right side, as well as the number of occurrences of "@" alone, as "(@)" with parenthesis is not associated with digits' encryption.
  - The numbers at both ends of `word` must form perfect squares of the numbers from 4 to 9.
  - In case of incorrect or invalid number encryption, a custom error is raised using the class 'IncorrectNumberEncryptionError' which inherits from the 'Exception' class.

- The encryption key: Note that while any key will produce any result, only the original key will decrypt the full encrypted text correctly.

Both the encrypted text and the encryption key are validated to ensure they are not empty.

To decrypt the encrypted text, the following process is applied:

- First, split the text into a list of words using the `.split()` function.
- Reverse each `word`, which will return each `word` to its original order.
- For each character `char` in each `word` in the list, perform the following steps:
  - If `char` is a digit, continue processing.
  - If `char` is not a digit, split `word` into `left` and `word` and reverse the order of `left` and `word`. Then, in the new `word`, if `char` is a digit, continue processing. If `char` is not a digit, split the `word` into `word` and `right` and reverse the order of `word` and `right`.
    - The reason for the mulitple use of reversals here is to ensure that the encryption of digits less than 4 is preserved in the middle part of the final `word`.
  - Now we have `left`, `word`, and `right`. If there were no matches for digits, `left` and `right` would be empty. Then, for each `char` in `word`, perform the following steps:
    - If `char` is in the alphabet:
      - If `char` is uppercase, apply the reverse process of lowercase encryption. Take the index value of the uppercase character from a given alphabet string, subtract the lowercase character value in the key from it, add 26, take the remainder after dividing by 26, and finally replace `char` with a lowercase character from a given lowercase alphabet string using the remainder as an index.
      - If `char` is lowercase, apply the reverse process of uppercase encryption. Take the index value of the lowercase character from a given alphabet string, subtract the uppercase character value in the key from it, add 26, take the remainder after dividing by 26, and finally replace `char` with an uppercase character from a given uppercase alphabet string using the remainder as an index.
    - If `char` is "(", check if `char` and the following 2 indices form either of the special symbols "@)" or "(#)". If they do, replace `char` with "@" or "#" accordingly. Otherwise, leave it as intended.
    - If `char` is "#", replace it and the following 2 indices with the corresponding original number from the encryption "#7#", "#8#", "#9#", "#0#" (i.e., "0", "1", "2", "3").
    - If `char` is "@", replace it with the square root of the combined same-index elements from 'left' and 'right'. A counter `j` is used for this purpose.
    - If `char` is anything else, keep it as is.

After processing the last character, add the resulting word to a list. Once all words are processed, join the word list with a space using the `join()` function and return it as the decrypted text.

Finally, using the `Tabulate` library, a table is printed containing the encrypted text, the encryption key, and the original text.