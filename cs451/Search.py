from queue import PriorityQueue, Queue, LifoQueue

from .Node import expand_node


def a_star(root, heuristic_fn, cost_fn, node_count_max=None):
    """Perform A* search starting from the root Node.

    :param root: Node to begin search.
    :type root: Node
    :param heuristic_fn: Function to estimate distance to goal.
    :type heuristic_fn: function returning int.
    :param cost_fn: function to calculate cost from root to current node.
    :type cost_fn: function returning int.
    :param node_count_max: Maximum number of nodes to examine, defaults to None
    :type node_count_max: int, optional
    :return: (First Node that satisfies goal_test(), # of nodes examined)
    :rtype: (Node, int)
    """
    fringe = PriorityQueue()
    fringe.put((cost_fn(root) + heuristic_fn(root), root))
    visited = []
    nodes_examined = 0
    while not fringe.empty() and nodes_examined < node_count_max:
        _, node = fringe.get()

        nodes_examined += 1

        if node.goal_test():
            # this is a solution.
            return node, nodes_examined

        visited.append(node)

        for successor in node.successors():
            # print("added successor!")
            if successor in visited:
                continue
            else:
                fringe.put(
                    (cost_fn(successor) + heuristic_fn(successor), successor))
        # print(str("#%d %s" % (nodes_examined, node.state)).ljust(50, " "), end='\r')
    return None, nodes_examined


def BFS(root, node_count_max=None):
    """Perform Breadth-First Search starting from root.

    :param root: Root Node to start BFS on.
    :type root: Node
    :param node_count_max: Maximum # of nodes to examine, defaults to None
    :type node_count_max: int, optional
    :return: First goal node found, and total number of nodes examined.
    :rtype: (Node, int)
    """
    nodes_examined = 0
    fringe = Queue()

    # put the root on the fringe
    fringe.put(root)

    # in BFS, we treat the fringe as a FIFO queue
    while not fringe.empty() and nodes_examined < node_count_max:
        node = fringe.get()
        nodes_examined += 1
        print("Examining Node #%d: %s" % (nodes_examined, node))
        for child in node.successors():
            print("Child: %s" % (str(child)))
            node.register_child(child)
            fringe.put(child)
        if node.goal_test():
            return node, nodes_examined
    return None, nodes_examined


def DFS(root, node_count_max=None):
    """Perform Depth-First Search starting at root.

    :param root: Node to begin search upon
    :type root: Node
    :param node_count_max: maximum number of nodes to examine, defaults to None
    :type node_count_max: int, optional
    :return: (First Node that satisfies goal_test(), # of nodes examined)
    :rtype: (Node, int)
    """
    nodes_examined = 0
    fringe = LifoQueue()

    # put the root on the fringe
    fringe.put(root)

    # in DFS, we treat the fringe as a LIFO queue
    while not fringe.empty() and nodes_examined < node_count_max:
        node = fringe.get()
        nodes_examined += 1
        print("Examining Node #%d: %s" % (nodes_examined, node))
        for child in node.children:
            fringe.put(child)
        if node.goal_test():
            return node, nodes_examined
    return None, nodes_examined
