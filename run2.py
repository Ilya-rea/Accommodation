import sys

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


class Robot:
    pos_x: int
    pos_y: int
    id: int

    def __init__(self, pos_x, pos_y, id):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = id

    def __repr__(self):
        return f'Robot_{self.id}({self.pos_x}, {self.pos_y})'


def get_input():
    return [list(line.strip()) for line in sys.stdin]


def get_nearest_key(
        curr_robot: Robot,
        curr_x: int,
        curr_y: int,
        path: dict[int, list[int]],
        steps: int,

        grid: list[list[str]],
        opened_doors: list[str],
) -> (int, int, int, str):

    solutions = []
    cell = grid[curr_x][curr_y]

    if cell in keys_char:
        return steps, curr_x, curr_y, cell.upper()

    for i in range(curr_x - 1, curr_x + 2):
        for j in range(curr_y - 1, curr_y + 2):
            diff_x = curr_x - i
            diff_y = curr_y - j

            if abs(diff_x + diff_y) != 1:
                continue

            cell = grid[i][j]
            next_x = i
            next_y = j

            if cell in keys_char:
                return steps + 1, next_x, next_y, cell.upper()

            elif cell == '.' or cell in opened_doors:

                if next_x in path.keys():
                    if next_y in path[next_x]:
                        continue

                if next_x in path.keys():
                    path[next_x].append(next_y)
                else:
                    path[next_x] = [next_y]

                solution = get_nearest_key(curr_robot, next_x, next_y, path, steps + 1, grid, opened_doors)

                if solution:
                    solutions.append(solution)

    if solutions:
        solutions.sort(key=lambda x: x[0])
        chosen_solution = solutions[0]

        return chosen_solution

    return None


def find_robots_and_keys(grid: list[list[str]]) -> (list[Robot], list[str]):
    temp_keys = []
    temp_robots = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                temp_robots.append(Robot(pos_x=i, pos_y=j, id=len(temp_robots) + 1))
            elif cell in keys_char:
                temp_keys.append(cell)

    return temp_robots, temp_keys


def solve(grid):
    opened_doors: list[str] = []
    all_steps = 0

    robots, keys = find_robots_and_keys(grid)

    while len(opened_doors) < len(keys):
        for robot in robots:
            path = {robot.pos_x: [robot.pos_y], }
            step_solution = get_nearest_key(
                curr_robot=robot,
                curr_x=robot.pos_x,
                curr_y=robot.pos_y,
                path=path,
                steps=0,
                grid=grid,
                opened_doors=opened_doors
            )

            if step_solution:
                steps, chosen_x, chosen_y, opened_door = step_solution

                grid[chosen_x][chosen_y] = '.'
                grid[robot.pos_x][robot.pos_y] = '.'

                robot.pos_x = chosen_x
                robot.pos_y = chosen_y

                opened_doors.append(opened_door)

                all_steps += steps

    return all_steps


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()