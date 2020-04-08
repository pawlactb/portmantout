from cs451.Node import Node
from cs451.Search import BFS
from PortmantoutNode import PortmantoutNode
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

    # read words, ignore words with ' (possessives)
    read_word_list(word_file, words, ignoreRegExp=r""".*["'].*""")
    syllables = {}
    for word in words:
        append_word_to_syllable_dict(word, syllables)

    root_node = PortmantoutNode(state='', name='root')
    goal_node, nodes_examined = BFS(root_node, node_count_max=10)

    print("Found Solution: %s (%s), after examining %d nodes." %
          (str(goal_node), str(goal_node.path), nodes_examined))


if __name__ == "__main__":
    main()
