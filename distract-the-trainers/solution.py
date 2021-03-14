from fractions import gcd


def is_infinite_thumb_wrestling_loop(banana_vals):
    while True:
        smaller_bananas, larger_bananas = min(banana_vals), max(banana_vals)
        cd = gcd(smaller_bananas, larger_bananas)
        smaller_bananas, larger_bananas = int(smaller_bananas / cd), int(larger_bananas / cd)
        if smaller_bananas == larger_bananas:
            return False
        elif (smaller_bananas + larger_bananas) % 2 == 1:
            return True
        else:
            banana_vals = smaller_bananas * 2, larger_bananas - smaller_bananas


def make_graph(banana_list):
    num_trainers = len(banana_list)
    graph = {i: set() for i in range(num_trainers)}
    for i in range(num_trainers):
        for j in range(i + 1, num_trainers):
            if is_infinite_thumb_wrestling_loop((banana_list[i], banana_list[j])):
                graph[i].add(j)
                graph[j].add(i)
    return graph


def update_matching(matching, augmenting_path):
    for i in range(0, len(augmenting_path) - 1, 2):
        new_matching_v, new_matching_w = augmenting_path[i], augmenting_path[i + 1]
        matching[new_matching_v], matching[new_matching_w] = new_matching_w, new_matching_v


def get_min_unmatched(graph):
    matching = get_initial_matching(graph)
    augmenting_path, graph, matching = find_augmenting_path(graph, matching)
    while augmenting_path:
        update_matching(matching, augmenting_path)
        augmenting_path, graph, matching = find_augmenting_path(graph, matching)
    return len(graph) - len(matching)


def contract_blossom(blossom, graph, matching):
    contracted_node = blossom[0]
    nodes_to_contract = set(blossom[1:])
    for node_to_contract in nodes_to_contract:
        for adjacent_node in graph[node_to_contract]:
            graph[adjacent_node].remove(node_to_contract)
            if adjacent_node != contracted_node:
                graph[adjacent_node].add(contracted_node)
        del graph[node_to_contract]
        if node_to_contract in matching:
            matched_node_to_contract = matching[node_to_contract]
            del matching[node_to_contract]
            if matched_node_to_contract in nodes_to_contract:
                del matching[matched_node_to_contract]
            else:
                matching[matched_node_to_contract] = contracted_node
    return graph, matching


def construct_blossom(path_to_node, path_from_node):
    path_from_node.reverse()
    blossom = path_to_node + path_from_node
    last_shared = None
    x, y = blossom.pop(0), blossom.pop()
    while x == y:
        last_shared = x
        x, y = blossom.pop(0), blossom.pop()
    return [last_shared, x] + blossom + [y]


# Use a modified version of the blossom algorithm.
# The blossom is never expanded after being contracted
# since we aren't concerned with the matching itself; just the number of unmatched nodes.
def find_augmenting_path(graph, initial_matching):
    marked_edge = set()
    marked_node = set()
    exposed_nodes = get_exposed_nodes(graph, initial_matching)
    unmarked_nodes = exposed_nodes[:]
    forest = {i: [i] for i in exposed_nodes}
    while unmarked_nodes:
        from_node = unmarked_nodes.pop()
        unmarked_edges = [i for i in graph[from_node] if (from_node, i) not in marked_edge]
        while unmarked_edges:
            to_node = unmarked_edges.pop(0)
            if to_node not in forest:  # add to node to forest
                to_node_initial_matching = initial_matching[to_node]
                path = forest[from_node] + [to_node]
                forest[to_node] = path
                forest[to_node_initial_matching] = path + [to_node_initial_matching]
                if len(path) % 2 == 0:
                    unmarked_nodes += [to_node_initial_matching]
                else:
                    unmarked_nodes += [to_node]
            else:
                to_node_path = forest[to_node]
                if len(to_node_path) % 2 == 1:
                    path_to_node, path_from_node = forest[to_node], forest[from_node]
                    root_to_node, root_from_node = path_to_node[0], path_from_node[0]
                    if root_from_node == root_to_node:
                        # contract blossom
                        blossom = construct_blossom(path_to_node, path_from_node)
                        contracted_graph, contracted_matching = contract_blossom(blossom, graph, initial_matching)
                        return find_augmenting_path(contracted_graph, contracted_matching)
                    else:
                        # return augmenting path
                        path_to_node.reverse()
                        augmenting_path = path_from_node + path_to_node
                        return augmenting_path, graph, initial_matching
            # mark edge
            marked_edge.add((from_node, to_node))
            marked_edge.add((to_node, from_node))
        # mark node
        marked_node.add(from_node)
    return [], graph, initial_matching


def get_exposed_nodes(graph, matching):
    exposed_nodes = []
    for node in graph:
        if node not in matching:
            exposed_nodes.append(node)
    return exposed_nodes


def get_initial_matching(graph):  # greedy matching algorithm
    num_nodes = len(graph)
    matchings = {}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if i not in matchings and j not in matchings and i in graph[j]:
                matchings[i], matchings[j] = j, i
    return matchings


def solution(banana_list):
    graph = make_graph(banana_list)
    return get_min_unmatched(graph)


print(solution([1, 1]))
# 2

print(solution([1, 7, 3, 21, 13, 19]))
# 0
