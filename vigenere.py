# IMPORTS
import re
import os

# VARIABLES
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
czech_accents = {
  'á': 'A', 'Á': 'A',
  'č': 'C', 'Č': 'C',
  'ď': 'D', 'Ď': 'D',
  'é': 'E', 'É': 'E',
  'ě': 'E', 'Ě': 'E',
  'í': 'I', 'Í': 'I',
  'ň': 'N', 'Ň': 'N',
  'ó': 'O', 'Ó': 'O',
  'ř': 'R', 'Ř': 'R',
  'š': 'S', 'Š': 'S',
  'ť': 'T', 'Ť': 'T',
  'ú': 'U', 'Ú': 'U',
  'ů': 'U', 'Ů': 'U',
  'ý': 'Y', 'Ý': 'Y',
  'ž': 'Z', 'Ž': 'Z'
}
frequency_czech = {
  'A': 7.3749,  'B': 1.8477,
  'C': 1.9052,  'D': 4.2712,
  'E': 9.1251,  'F': 0.3240,
  'G': 0.3236,  'H': 1.5074,
  'I': 5.1616,  'J': 2.5132,
  'K': 4.4310,  'L': 4.5564,
  'M': 3.8263,  'N': 7.7496,
  'O': 10.2767, 'P': 4.0468,
  'Q': 0.0015,  'R': 4.3840,
  'S': 5.3551,  'T': 6.7909,
  'U': 3.7286,  'V': 5.5278,
  'W': 0.0104,  'X': 0.0895,
  'Y': 2.2641,  'Z': 2.6072
}
input_raw = ""
input_converted = ""
input_split = []
input_split_decoded = []
input_decoded = []
repetitive_parts = []
distances = {}
key_lengths = []
run = True

# FUNCTIONS
def print_head():
    """Prints information text about this program."""
    print("This code is intended to be run under Python 3. No backward compatibility!\r\n")
    print("Vigenere Cipher Decoder")
    print("Kamil Poruba, Jan Hudec, Patrik Burda")
    print("TAKR Project II")
    print("Brno University of Technology, 2017\r\n")

def load_input():
    """Loads the cipher text from user."""
    return input("\r\nEnter cipher text to decode or type \"quit\" to exit:\r\n ")

def convert_input(text):
    """Replaces Czech accents, converts all lowercase characters to uppercase, and removes all invalid character from input."""
    output = []

    for char in text:
        # czech accents replacement
        if char in czech_accents:
            output.append(czech_accents.get(char))
        # other regular letters
        elif char.upper() in alphabet:
            output.append(alphabet[alphabet.index(char.upper())])
        # omit invalid characters

    return ''.join(output)

def find_repetitive_parts(text):
    """Finds all repetitive parts in input. """
    index = 0
    length = len(text)
    output = []

    # search for repetitive parts from the longest to the shortest substrings
    while length > 2:
        index = 0

        # shift the starting position of substring by one until the end of text
        while index + length < len(text):
            temp = text[index:index+length]

            # add found repetitive part to list if not already present
            if text.count(temp) > 1 and temp not in output:
                output.append(temp)

            index += 1

        length -= 1

    return output

def calculate_distances(parts):
    """Calculates distances between repetitive parts in input."""
    output = {}

    # take each repetitive part and find all characters between them using regex
    for part in parts:
        pattern = "(?<=" + part + ")(.+?)?(?=" + part + ")"
        matched = re.findall(pattern, input_converted)

        # count the length of matched characters
        for match in matched:
            match_length = len(match) + len(part)

            # calculate the divisors and add them to the dictionary, incrementing the entry by one if already present
            for i in range(2,31):
                if match_length % i == 0:
                    if i in output:
                        output[i] += 1
                    else:
                        output[i] = 1

    return output

def find_key_lengths(dictionary):
    """Calculates the expected key length from common divisors of individual repetitive parts.
    Most represented divisor is probably the key length."""
    value_temp = 0
    output = []

    # iterate over calculated divisors, find the most represented one
    for key, value in dictionary.items():
        if value > value_temp:
            most_common_divisor_value = value
            value_temp = value

    # check if the most represented divisor is the only one, add them to list
    for key, value in dictionary.items():
        if value == most_common_divisor_value:
            output.append(key)

    return output

def split_input_by_key(text, index = 0):
    """Splits the converted input into separate parts based on found key length(s)."""
    output = []

    # take each n-th character from text with n as step being the length of key
    for i in range(key_lengths[index]):
        output.append(text[i::key_lengths[index]])

    return output

def count_frequency_diff(text):
    """Counts the frequency analysis of cipher text."""
    alphabet_tuple = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    output = dict.fromkeys(alphabet_tuple)
    text_length = len(text)
    difference = 0

    # count occurences of individual letters and save them in dictionary
    for key in alphabet_tuple:
        occurences = text.count(key)

        # compute respective occurences in percentage
        if occurences > 0:
            output[key] = (text.count(key) / text_length) * 100
        else:
            output[key] = 0

    # count total sum
    for key, value in output.items():
        difference += abs(frequency_czech[key] - value)

    return difference

def decode_by_key(text, key):
    """Decodes part of cipher text by respective char from found key."""
    part_decoded = []
    decoded_char_index = 0

    # decode each character by key
    for char in text:
        decoded_char_index = alphabet.find(char)
        decoded_char_index -= alphabet.find(key)
        decoded_char_index %= len(alphabet)
        part_decoded.append(alphabet[decoded_char_index])

    return part_decoded

def decode_parts(keys):
    """Splits input, counts frequency analysis of each part, finds key(s) and decodes input."""
    output = []
    frequency_temp = {}
    key_value = 0
    key_char = ''
    key = ""

    # repeat process for each found key
    for i in range(len(keys)):
        print("\r\nDecoding message for key length of %i characters:\r\n" % keys[i], end='')

        # split input into parts
        print(" Split input into parts based on key length:")
        input_split = split_input_by_key(input_converted, 0)
        for i, part in enumerate(input_split):
            print("  %i. part: %s" % (i + 1, part))

            # decode parts by each character in alphabet
            for i in range(len(alphabet)):
                input_shifted = []
                decoded_char_index = 0

                for char in part:
                    decoded_char_index = alphabet.find(char)
                    decoded_char_index -= i
                    decoded_char_index %= len(alphabet)
                    input_shifted.append(alphabet[decoded_char_index])

                # compute frequency analysis
                frequency_temp[i] = count_frequency_diff(input_shifted)

            # find the lowest deviation from frequency analysis of czech text
            key_value = min(frequency_temp.values())
            for i in frequency_temp.keys():
                if frequency_temp[i] == key_value:
                    key_char = alphabet[i]

            # add the character with the lowest deviation to key string
            key += str(key_char)

            # decode each part with corresponding character of the key
            output.append(decode_by_key(part, key_char))

        print("\r\n Found key is: %s" % key)

        return output

def compose_decoded_parts(parts):
    """Composes final decoded message from separate decoded parts."""
    output = []
    run = True

    # take the first character from each part and append it to output
    while run:
        for i in range(len(parts)):
            if parts[i]:
                output.append(parts[i].pop(0))

        # repeat until the first part is empty
        if not parts[0]:
            run = False

    return output

# MAIN
while run:
    os.system('cls' if os.name == 'nt' else 'clear')

    print_head()
    input_raw = load_input()

    if input_raw.lower() != "quit":
        if len(input_raw) > 0:
            input_converted = convert_input(input_raw)

            if len(input_converted):
                print("\r\nEdited cipher text (in case of accented or illegal characters):\r\n %s" % (input_converted))

                repetitive_parts = find_repetitive_parts(input_converted)

                if len(repetitive_parts):
                    print("\r\nFound repetitive parts in cipher text:\r\n ", end='')
                    print(*repetitive_parts, sep=', ')

                    distances = calculate_distances(repetitive_parts)
                    key_lengths = find_key_lengths(distances)

                    print("\r\nFound key length(s):\r\n ", end='')
                    print(*key_lengths, sep=', ')

                    input_split_decoded = decode_parts(key_lengths)
                    input_decoded = compose_decoded_parts(input_split_decoded)

                    print("\r\n Decrypted message is:\r\n  ", end='')
                    print(*input_decoded, sep='')
                else:
                    print("\r\nNo repetitive parts have been found, decode is not possible.")
            else:
                print("\r\nEdited input does not contain any characters to decode.")
        else:
            print("No input")

        input("\r\n\r\nPress Enter to continue. ")
    else:
        print("\r\nExiting...\r\n")
        run = False
