from copy import deepcopy


class Node(object):
    def __init__(self, name=None, parent=None, path=None):
        self.parent = parent
        # self.fringe = []
        self.total_path_cost = 0
        self.name = name
        self.children = []

        if path is not None:
            self.path = deepcopy(path)
        else:
            self.path = []

    def register_child(self, child):
        self.children.append(child)

    def is_valid(self):
        pass

    def is_complete(self):
        pass

    def goal_test(self):
        pass

    def successors(self):
        pass

    def cost(self):
        return len(self.path)


def create_finite_tree(root):
    successors = root.successors()
    for node in successors:
        node.parent.register_child(node)
        create_finite_tree(node)


def expand_node(node):
    successors = node.successors()
    for s in successors:
        s.parent.register_child(s)
