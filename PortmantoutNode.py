from cs451.Node import Node
from cs451.Search import DFS
import re
from copy import deepcopy
from random import shuffle
from threading import Lock
import concurrent.futures
import traceback


class PortmanteauNode(Node):
    """A PortmanteauNode is a portmanteau of specified word length.
    """
    syllables = {}

    @staticmethod
    def get_syllables(word):
        """Query the generated list of syllables for a word's syllables.

        :param word: word to return syllables of
        :type word: str
        :return: List of syllables
        :rtype: [str]
        """
        return PortmanteauNode.syllables[word]

    @staticmethod
    def is_portmanteau(words):
        """Determine if a portmanteau can be made along words (in current order).

        :param words: words to see if portmanteau exists along
        :type words: [str]
        :return: True iff portmanteau exists along words, False otherwise.
        :rtype: Boolean
        """
        if len(words) == 0:
            return False, None

        added_syllables = []
        current_word_syllables = []
        last_word_syllables = []
        for word in words:
            if len(last_word_syllables) == 0:
                # first iteration
                last_word_syllables = PortmanteauNode.syllables[word]
                added_syllables.extend(last_word_syllables)
                continue
            else:
                current_word_syllables = PortmanteauNode.syllables[word]

                # syllables shared between last word and current word
                syllables_shared = [
                    x for x in current_word_syllables if x in last_word_syllables]
                if len(syllables_shared) == 0:
                    # if no syllables are shared, then we can say a portmanteau doesn't exist
                    return False, None

                current_shared_index = current_word_syllables.index(
                    syllables_shared[0])
                last_shared_index = last_word_syllables.index(
                    syllables_shared[0])
                if current_shared_index == len(current_word_syllables)-1:
                    return False, None
                if last_shared_index == 0:
                    return False, None

                # old_word_pos = last_word_syllables.index(
                #     syllables_shared[0]) + 1
                new_word_pos = current_word_syllables.index(
                    syllables_shared[0]) + 1
                new_syllables = list()
                # new_syllables.extend(last_word_syllables[0:old_word_pos])
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
        good, to_render = PortmanteauNode.is_portmanteau(words)
        if good:
            return "".join(to_render)
        else:
            return None

    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

    def __str__(self):
        _, to_render = PortmanteauNode.is_portmanteau(self.path)
        if _ == True:
            return "%s (%d words) %s" % ("".join(to_render), len(self.path), str(self.path))
        else:
            return "BAD PORTMANTOUT (%d depth) " % (len(self.path))

    def is_valid(self):
        """Check if a valid portmantaeu is made from the words in self.path.
        (Might only need to check most recent word added? Since we don't generate successors in invalid portmanteaus.)

        :return: True iff self.path can be a portmanteau, False otherwise.
        :rtype: Boolean
        """
        if len(self.path) == 0:
            return True
        else:
            return PortmanteauNode.is_portmanteau(self.path)

    def is_complete(self):
        """Check if node is at a terminal depth in search.

        :return: True iff node is at terminal depth.
        :rtype: Boolean
        """

        if len(self.path) >= 4:
            return True
        else:
            return False

    def goal_test(self):
        """Check if the node met the goal requirements.

        :return: True iff node is at terminal depth, and node meets goal requirements.
        :rtype: Boolean
        """
        if self.is_valid() and self.is_complete():
            return True
        else:
            return False

    def successors(self):
        """This function should return a list of PortmantoutNode s each with one of the remaining words appended to the successor's path.

            :return: If not self.valid(), returns [], else, returns a List of PortmantoutNodes (that may not be valid).
            :rtype: List
        """
        if not self.is_valid():
            return []
        successors = []
        child_path = []
        words_left = list(PortmanteauNode.syllables.keys())
        shuffle(words_left)
        for word in words_left:
            if not word in self.path:
                child_path = deepcopy(self.path)
                child_path.append(word)
                kid = PortmanteauNode(path=child_path, parent=self)
                successors.append(kid)

        return successors

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


class PortmanteauNodeGenerator(object):
    def __init__(self, syllables, portmanteau_length=4):
        self.syllables = syllables
        self._mapping = dict()
        self._state_lock = Lock()

    def add_portmanteau(self, portmantaeu_node):
        start_syllable = PortmanteauNode.get_syllables(
            portmantaeu_node.path[0])
        end_syllable = PortmanteauNode.get_syllables(
            portmantaeu_node.path[-1])
        with self._state_lock:
            if (start_syllable, end_syllable) in self._mapping.keys():
                self._mapping[(start_syllable, end_syllable)
                              ].append(portmantaeu_node)
            else:
                self._mapping[(start_syllable, end_syllable)
                              ] = list()
                self._mapping[(start_syllable, end_syllable)
                              ].append(portmantaeu_node)

            for word in portmantaeu_node.path:
                del self.syllables[word]

    def get_portmanteau(self, start_syllable, end_syllable):
        portmanteau_node = None
        if (start_syllable, end_syllable) in self._mapping.keys():
            with self._state_lock:
                portmanteau_node = self._mapping[(
                    start_syllable, end_syllable)].pop()
            return portmanteau_node
        else:
            return None

    def generate(self, num_searches=1):
        nodes = []
        for _ in range(num_searches):
            nodes.append(PortmanteauNode())

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_node = {executor.submit(
                DFS, node, 1000): node for node in nodes}
            for future in concurrent.futures.as_completed(future_to_node):
                node = future_to_node[future]
                try:
                    print(node.path)
                    # self.add_portmanteau(node)
                except Exception as exc:
                    tb = traceback.format_exc(exc)
                    print(tb)

    def __len__(self):
        length = 0
        for _, val in self._mapping.values():
            length += len(val)
        return length


class PortmantoutNode(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
