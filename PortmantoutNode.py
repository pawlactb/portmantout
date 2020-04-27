from cs451.Node import Node
import re


class PortmantoutNode(Node):
    syllables = {}

    @staticmethod
    def get_syllables(word):
        """Query the generated list of syllables for a word's syllables.

        :param word: word to return syllables of
        :type word: str
        :return: List of syllables
        :rtype: [str]
        """
        return PortmantoutNode.syllables[word]

    @staticmethod
    def is_portmanteau(words):
        """Determine if a portmanteau can be made along words (in current order).

        :param words: words to see if portmanteau exists along
        :type words: [str]
        :return: True iff portmanteau exists along words, False otherwise.
        :rtype: Boolean
        """
        if words is None:
            return False

        added_syllables = []
        last_word_syllables = None
        for word in words:
            if len(added_syllables) == 0:
                # first iteration
                added_syllables.append(PortmantoutNode.get_syllables(word))
                last_word_syllables = PortmantoutNode.get_syllables(word)
                continue
            current_word_syllables = PortmantoutNode.get_syllables(word)
            for syllable_num, syllable in enumerate(current_word_syllables):
                print()
                if syllable not in added_syllables[:-len(last_word_syllables)]:
                    # there is no portmanteau along this path
                    return False, None
                else:
                    # portmanteau exists between added_syllables and syllable
                    added_syllables.append(
                        current_word_syllables[:syllable_num])
                    last_word_syllables = current_word_syllables[:syllable_num]

        # if we make it here, we had no issues adding all the words.
        return True, added_syllables

    @staticmethod
    def generate_portmanteau(words):
        """Generate a portmanteau from words (in order).

         :return: The rendered portmanteaus.
         :rtype: [str]
         """
        portmanteau = PortmantoutNode.is_portmanteau(words)
        if not PortmantoutNode.is_portmanteau(words)[0]:
            return False
        else:
            return "".join(portmanteau[1])

    def __init__(self, *args, **kwargs):
        self.portmanteau = ''
        Node.__init__(self, args, kwargs)

    def __str__(self):
        return "%s (%d words)" % (PortmantoutNode.generate_portmanteau(self.path), len(self.path))

    def is_valid(self):
        """Check if a valid portmantaeu is made from the words in self.path.
        (Might only need to check most recent word added? Since we don't generate successors in invalid portmanteaus.)

        :return: True iff self.path can be a portmanteau, False otherwise.
        :rtype: Boolean
        """
        return PortmantoutNode.is_portmanteau(self.path)

    # TODO: RH
    def is_complete(self):
        """Check if node is at a terminal depth in search.

        :return: True iff node is at terminal depth.
        :rtype: Boolean
        """

        return False

    # TODO: RH
    def goal_test(self):
        """Check if the node met the goal requirements.

        :return: True iff node is at terminal depth, and node meets goal requirements.
        :rtype: Boolean
        """
        if not self.is_complete():
            return False

        # Change this:
        return False

    # TODO: AD
    def successors(self):
        """This function should return a list of PortmantoutNode s each with one of the remaining words appended to the successor's path.

            :return: If not self.valid(), returns [], else, returns a List of PortmantoutNodes (that may not be valid).
            :rtype: List
        """
        return []

    def cost(self):
        """Return the number of words added to the PortmantoutNode.

        :return: Number of words on path
        :rtype: int
        """
        return len(self.path)


def read_word_list(path, ignoreRegExp=None):
    words = []
    f = open(path, r"r")
    print("Opened: %s" % (str(path)))
    for line in iter(f.readlines()):
        if ignoreRegExp is not None:
            if re.match(ignoreRegExp, line):
                continue
        words.append(line.strip())
    print("Successfully Loaded %d words." % (len(words)))
    return words


def split_word_into_syllables(word):
    ret_val = []
    ex = r'[^aeiou]*[aeiou]*[^aeiou]*|[aeiou]*[^aeiou]'
    # ex = r'([^aeiou]*[aeiou]*)|[aeiou]*[^aeiou]*[aeiou]*'
    # ex = r"[aiouy]+e*|e(?!d$| ly). | [td]ed | le"
    ret_val = list(re.findall(ex, word))
    # ret_val.remove('')
    return ret_val


def append_word_to_syllables(word, dict):
    dict[word] = split_word_into_syllables(word)


def load_syllables(path):
    # read words, ignore words with ' (possessives)
    words = read_word_list(path, ignoreRegExp=r""".*["'].*""")
    #words = read_word_list_no_proper_nouns(path, ignoreRegExp=r""".*["'].*""")
    syllables = {}
    for word in words:
        append_word_to_syllables(
            word, syllables)
    return syllables


if __name__ == "__main__":
    word_file = './american-english'
    syllables = load_syllables(word_file)

    PortmantoutNode.syllables = syllables

    words = ["Afrikaners", "Afrikaner", ]
    for word in words:
        print("Word: %s, syllables %s" %
              (word, str(PortmantoutNode.get_syllables(word))))
    print(PortmantoutNode.generate_portmanteau(words))
