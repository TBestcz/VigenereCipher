# LINKS
# http://www.dcode.fr/vigenere-cipher
# https://akela.mendelu.cz/~foltynek/KAS/historie/vigenere2.php
# https://regex101.com/
# https://repl.it/

# IMPORTS
import re

# VARIABLES
#cipher_text = "MOYONCTCJKXOIKXIVGTSYIGOFIHOHQNLECIWFPKSAQLNWNCNEJRLEWICOHYYDJJEWTMAWKJVULZIFEDDVSUFALICICAEFEJIKJAZIEPGHZQORCOEKXLESZYGKGRPQSZPQTAQQEWYNQNQWVQSXIMMWVZXYEGUVQWCJJOFBODEIIWNIWRSXJDGTCLILSQFHKLAUZSIIWTUOHEECDQQIBOKPLXVGWUPDCEPAOMFTAQMFCTWQVQDBPATYLAKEYGOSUEOTIKMWSCXISVUTJEEKVMEEJAGMWOLRZHNSCZUBIZLOROUTMSSMOFYWSDSMVQQYTLGYSXSFGQNSQZFCSYZTSVVPQOLWUDETDAUTZEMVRYMPXQGDEUDOZIDAFEQQOTSZEBZVOGOYGREMUGSVILOJETVGAOXOVRZXSRYYZSQVNHTUZCAMJXVGTQJADRKZGPKJADUPIXOWYNCGMOBOZEHVRQRKJADGFEZRGFEIEEDPHAINERRR"
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
input_raw = ""
input_converted = ""
repetitive_parts = []
distances = {}
key_length = []

# FUNCTIONS
def load_input():
  print("Vigenere Cipher Decoder")
  print("Kamil Poruba, Jan Hudec, Patrik Burda")
  print("TAKR Project II")
  print("Brno University of Technology, 2017")

  return input("\r\nEnter cipher text to decode:\r\n")

def convert_input(text):
  """Replaces Czech accents, converts all lowercase characters to uppercase, and removes all invalid character from input.
  """
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
  """Finds all repetitive parts in input.
  """
  index = 0
  length = len(text)
  output = []

  # searches for repetitive parts from the longest to the shortes substrings
  while length > 2:
    index = 0

    # shifts the starting position of substring by one until reaches the end of text
    while index + length < len(text):
      temp = text[index:index+length]

      # adds found repetitive part to list if not already present
      if text.count(temp) > 1 and temp not in output:
        output.append(temp)

      index += 1

    length -= 1

  return output

def calculate_distances(parts):
  """Calculates distances between repetitive parts in input.
  """
  output = {}

  # takes each repetitive part and finds all characters between them using regex
  for part in parts:
    pattern = "(?<=" + part + ")(.+?)?(?=" + part + ")"
    matched = re.findall(pattern, input_converted)

    # counts the length of matched characters
    for match in matched:
      match_length = len(match) + len(part)

      # calculates the divisors and adds them to the dictionary, incrementing the entry by one if already present
      for i in range(2,31):
        if match_length % i == 0:
          if i in output:
            output[i] += 1
          else:
            output[i] = 1

  return output

def find_key_length(dictionary):
  """Calculates the expected key length from common divisors of individual repetitive parts.
  Most represented divisor is probably the key length.
  """
  value_temp = 0
  output = []

  # iterates over calculated divisors, finds the most represented one
  for key, value in dictionary.items():
    if value > value_temp:
      most_common_divisor_value = value
      value_temp = value

  # checks if the most represented divisor is the only one, adds them to list
  for key, value in dictionary.items():
    if value == most_common_divisor_value:
      output.append(key)

  return output

# MAIN
input_raw = load_input()
input_converted = convert_input(input_raw)
print("\r\nEdited cipher text (in case of accented or illegal characters):\r\n %s" % (input_converted))

repetitive_parts = find_repetitive_parts(input_converted)
print("\r\nFound repetitive parts in cipher text:\r\n ", end='')
print(*repetitive_parts, sep=', ')

distances = calculate_distances(repetitive_parts)

key_length = find_key_length(distances)
print("\r\nFound key length(s):\r\n ", end='')
print(*key_length, sep=', ')
