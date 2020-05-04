from cs451.Node import Node
from cs451.Search import BFS
from PortmantoutNode import PortmantoutNode
import re


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
    #ex = r'([^aeiou]*[aeiou]*)|[aeiou]*[^aeiou]*[aeiou]*'
    ex = r'[^aeiou]*[aeiou]*[^aeiou]*|[aeiou]*[^aeiou]'
    ret_val = list(re.findall(ex, word))
    return ret_val


def append_word_to_syllables(word, dict):
    dict[word] = split_word_into_syllables(word)


def load_syllables(path):
    # read words, ignore words with ' (possessives)
    words = read_word_list(path, ignoreRegExp=r""".*["'].*""")
    #words = read_word_list_no_proper_nouns(path, ignoreRegExp=r""".*["'].*""")
    syllables = {}
    for word in words:
        append_word_to_syllables(word, syllables)
    return syllables


def main():
    word_file = './american-english'
    syllables = load_syllables(word_file)

    PortmantoutNode.syllables = syllables

    root_node = PortmantoutNode(path=["apple"], name='root')
    for succ in root_node.successors():
        print(str(succ))
    # goal_node, nodes_examined = BFS(root_node, node_count_max=10)

    # print("Found Solution: %s (%s), after examining %d nodes." %
        #   (str(goal_node if goal_node else ""), str(goal_node.path if goal_node else ""), nodes_examined))


if __name__ == "__main__":
    main()
