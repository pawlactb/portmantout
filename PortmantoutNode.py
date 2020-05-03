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
        added_syllables = []
        current_word_syllables = []
        last_word_syllables = []
        for word in words:
            if len(last_word_syllables) == 0:
                # first iteration
                last_word_syllables = PortmantoutNode.syllables[word]
                continue
            else:
                current_word_syllables = PortmantoutNode.syllables[word]

                # syllables shared between last word and current word
                syllables_shared = [
                    x for x in current_word_syllables if x in last_word_syllables]
                if len(syllables_shared) == 0:
                    # if no syllables are shared, then we can say a portmanteau doesn't exist
                    return False, None
                else:
                    old_word_pos = last_word_syllables.index(
                        syllables_shared[0]) + 1
                    new_word_pos = current_word_syllables.index(
                        syllables_shared[0]) + 1
                    new_syllables = list()
                    new_syllables.extend(last_word_syllables[0:old_word_pos])
                    new_syllables.extend(
                        current_word_syllables[new_word_pos:])
                    added_syllables.extend(new_syllables)
                    last_word_syllables = current_word_syllables[current_word_syllables.index(
                        syllables_shared[0]):]
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

        if self.path.len()==1000:
            return True
        else:
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
        if self.path.len()==1000 & is_portmanteau(self.path):
            return True
        else:
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
    return list(filter(lambda x: x != '', ret_val))


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
