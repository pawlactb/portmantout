from queue import PriorityQueue, Queue, LifoQueue

from Node import expand_node


def a_star(root, heuristic_fn, cost_fn, node_count_max=None):
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
            node.register_child(child)
            fringe.put(child)
        if node.goal_test():
            return node, nodes_examined
    return None, nodes_examined


def DFS(root, node_count_max=None):
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
