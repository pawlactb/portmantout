from cs451.Node import Node
import re


def read_word_list(path, dest, ignoreRegExp=None):
    f = open(path, r"r")
    print("Opened: %s" % (str(path)))
    for line in iter(f.readlines()):
        if ignoreRegExp is not None:
            if re.match(ignoreRegExp, line):
                continue
        dest.append(line.strip())
    print("Successfully Loaded %d words." % (len(dest)))


def split_word_into_syllables(word):
    ret_val = []
    ex = r'([^aeiou]*[aeiou]*)|[aeiou]*[^aeiou]*[aeiou]*'
    #ex = r'[^aeiou]*[aeiou]*[^aeiou]*|[aeiou]*[^aeiou]'
    ret_val = list(re.findall(ex, word))
    return ret_val


def append_word_to_syllable_dict(word, dict):
    dict[word] = split_word_into_syllables(word)


def main():
    words = []
    word_file = '/usr/share/dict/american-english'

    # read words, ignore possessives
    read_word_list(word_file, words, ignoreRegExp=r""".*["'].*""")
    syllables = {}
    for word in words:
        append_word_to_syllable_dict(word, syllables)

    for key, val in syllables.items():
        print("%s: %s" % (key, str(val)))
    # pick random word
    # generate table of portmanteaus to go from letter-to-letter
    # join words with easiest to manufacture letter-to-letter startings/endings
    pass


if __name__ == "__main__":
    main()
