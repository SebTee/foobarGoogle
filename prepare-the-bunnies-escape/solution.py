directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_pos_in_maze(maze, (x, y)):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])


def is_valid(maze, visited, pos):
    x, y = pos
    return is_pos_in_maze(maze, pos) and maze[x][y] == 0 and pos not in visited


def get_next_positions(maze, visited, (cur_x, cur_y)):
    new_positions = []
    for (i, j) in directions:
        new_pos = (cur_x + i, cur_y + j)
        if is_valid(maze, visited, new_pos):
            new_positions.append(new_pos)
    return new_positions


def get_adjacent_walls(maze, (cur_x, cur_y), ignore_walls):
    walls_to_remove = []
    for (i, j) in directions:
        x, y = cur_x + i, cur_y + j
        if is_pos_in_maze(maze, (x, y)) and maze[x][y] == 1 and (x, y) not in ignore_walls:
            walls_to_remove.append((x, y))
    return walls_to_remove


def shortest_path_len(maze, end, visited, queue):
    while queue:
        distance, cur_pos = queue.pop(0)
        if cur_pos == end:
            return distance
        for new_pos in get_next_positions(maze, visited, cur_pos):
            queue.append((distance + 1, new_pos))
            visited[new_pos] = None
    return -1


def shortest_path_len_remove_wall(maze, start, end):
    distances = []
    queue = [(1, start)]
    visited = {start: None}
    removed_walls = {}
    while queue:
        distance, cur_pos = queue.pop(0)
        distance += 1
        for new_pos in get_next_positions(maze, visited, cur_pos):
            queue.append((distance, new_pos))
            visited[new_pos] = None
        for wall_pos in get_adjacent_walls(maze, cur_pos, removed_walls):
            new_queue = queue[:]
            new_queue.append((distance, wall_pos))
            distance = shortest_path_len(maze, end, visited.copy(), new_queue)
            distances.append(distance)
    return min(filter(lambda x: x > 0, distances))


def solution(maze):
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)
    return shortest_path_len_remove_wall(maze, start, end)


print(solution([[0, 1, 1, 0],
                [0, 0, 0, 1],
                [1, 1, 0, 0],
                [1, 1, 1, 0]]))
# 7

print(solution([[0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0]]))
# 11
