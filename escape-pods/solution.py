def consolidate_sink_source(entrances, exits, path, max_corridor_size):
    consolidated_source, consolidated_sink = [0] * (len(path) + 2), [0] * (len(path) + 2)
    for entrance in entrances:
        consolidated_source[entrance + 1] = max_corridor_size
    flow_graph = []
    for node_id in range(len(path)):
        sink_flow = 0
        if node_id in exits:
            sink_flow = max_corridor_size
        flow_graph.append([0] + path[node_id] + [sink_flow])
    flow_graph.append(consolidated_sink)
    flow_graph = [consolidated_source] + flow_graph
    return flow_graph, 0, len(flow_graph) - 1


def find_maximum_flow(residual_flow_graph, source, sink, max_corridor_size):  # Ford-Fulkerson Algorithm
    current_flow = 0
    augmenting_path, augmenting_path_flow = find_augmenting_path(residual_flow_graph, [source], max_corridor_size, sink)
    while augmenting_path:
        current_flow += augmenting_path_flow
        residual_flow_graph = update_residual_flow_graph(residual_flow_graph, augmenting_path, augmenting_path_flow)
        augmenting_path, augmenting_path_flow = find_augmenting_path(residual_flow_graph,
                                                                     [source],
                                                                     max_corridor_size,
                                                                     sink)
    return current_flow


def find_augmenting_path(residual_flow_graph, augmenting_path, augmenting_path_flow, sink):
    from_node = augmenting_path[-1]
    for to_node in [x for x in range(len(residual_flow_graph)) if x not in augmenting_path]:
        flow = residual_flow_graph[from_node][to_node]
        if flow > 0:
            new_augmenting_path, new_augmenting_path_flow = augmenting_path + [to_node], min(augmenting_path_flow, flow)
            if to_node == sink:
                return new_augmenting_path, new_augmenting_path_flow
            new_augmenting_path, new_augmenting_path_flow = find_augmenting_path(residual_flow_graph,
                                                                                 new_augmenting_path,
                                                                                 new_augmenting_path_flow,
                                                                                 sink)
            if new_augmenting_path_flow > 0:
                return new_augmenting_path, new_augmenting_path_flow
    return [], 0


def update_residual_flow_graph(residual_flow_graph, augmenting_path, augmenting_path_flow):
    for from_node, to_node in zip(augmenting_path[:-1], augmenting_path[1:]):
        residual_flow_graph[from_node][to_node] -= augmenting_path_flow
        residual_flow_graph[to_node][from_node] += augmenting_path_flow
    return residual_flow_graph


def solution(entrances, exits, path):
    max_corridor_size = 2000000
    residual_flow_graph, source, sink = consolidate_sink_source(entrances, exits, path, max_corridor_size)
    maximum_flow = find_maximum_flow(residual_flow_graph, source, sink, max_corridor_size)
    return maximum_flow


print(solution([0], [3],
               [[0, 7, 0, 0],
                [0, 0, 6, 0],
                [0, 0, 0, 8],
                [9, 0, 0, 0]]))
# 6

print(solution([0, 1], [4, 5],
               [[0, 0, 4, 6, 0, 0],
                [0, 0, 5, 2, 0, 0],
                [0, 0, 0, 0, 4, 4],
                [0, 0, 0, 0, 6, 6],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]))
# 16
