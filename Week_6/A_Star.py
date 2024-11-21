import time

# well... it feels like there's some strange behavior, but I think it works?
# good luck reading it

allow_diagonals = True
fps = 10
testno = 6
def main():
    if testno == 0:
        # test sorted linked list
        ll = LinkedList()
        ll.add_sorted(1, lambda val:val)
        ll.add_sorted(0, lambda val:val)
        ll.add_sorted(5, lambda val:val)
        ll.add_sorted(8, lambda val:val)
        ll.add_sorted(3, lambda val:val)
        start = ll.sentinel_start.next
        while start is not None:
            print(start.data)
            start = start.next
        ll = LinkedList()
        ll.add_sorted(1, lambda val:-val)
        ll.add_sorted(0, lambda val:-val)
        ll.add_sorted(5, lambda val:-val)
        ll.add_sorted(8, lambda val:-val)
        ll.add_sorted(3, lambda val:-val)
        start = ll.sentinel_start.next
        while start is not None:
            print(start.data)
            start = start.next
    elif testno == 1:
        world = ["                         ",
                 "              #          ",
                 "      a       #          ",
                 "              #          ",
                 "              #          ",
                 "              #          ",
                 "   #### #######          ",
                 "                         ",
                 "                        b",
                 ]
        astar = AStar(world)
        astar.pathfind('a', 'b')
    elif testno == 2:
        world = ["              #          ",
                 "              #          ",
                 "              #          ",
                 "          a   #          ",
                 "       ##     #          ",
                 "        #     #          ",
                 "   #### #######          ",
                 "                         ",
                 "                        b",
                 ]
        astar = AStar(world)
        astar.pathfind('a', 'b')
    elif testno == 3:
        world = ["                         ",
                 "                         ",
                 " a #          ##         ",
                 "   #    #    ##          ",
                 "   #    #   ##         b ",
                 "        #  ##            ",
                 "        #                ",
                 "                         ",
                 "                         ",
                 ]
        astar = AStar(world)
        astar.pathfind('a', 'b')
    elif testno == 4:
        world = ["   #                 #   ",
                 "   # #######  ###    #   ",
                 " a #  #       # ###  #   ",
                 "   #  # #  #### # #  #   ",
                 "   # d  #   c   # #  # b ",
                 "   ######  ###### #  #   ",
                 "   ## #           #  #   ",
                 "   ## ########### #      ",
                 "                  #      ",
                 ]
        astar = AStar(world)
        astar.pathfind('a', 'b')
    elif testno == 5:
        world = ["   #                 #   ",
                 "   # #######  ###    #   ",
                 " a #  #       # ###  #   ",
                 "   #  # #  #### # #  #   ",
                 "   # d  #   c   # #  # b ",
                 "   ######  ###### #  #   ",
                 "   ## #           #  #   ",
                 "   ## ########### #      ",
                 "                  #      ",
                 ]
        astar = AStar(world)
        astar.pathfind('c', 'd')
    elif testno == 6:
        world = ["   #                 #   ",
                 "   # #######  ###    #   ",
                 " a #  #       # ###  #   ",
                 "   #  # #  #### # #  #   ",
                 "   # d  #   c   # #  # b ",
                 "   ######  ###### #  #   ",
                 "   ## #           #  #   ",
                 "   ## ########### #      ",
                 "                  #      ",
                 ]
        astar = AStar(world)
        astar.pathfind('b', 'a')
    elif testno == 7:
        world = ["   #                 #   ",
                 "   # #######  ###    #   ",
                 " a #  #       # ###  #   ",
                 "   #  # #  #### # #  #   ",
                 "   # d  #   c   # #  # b ",
                 "   ######  ###### #  #   ",
                 "   ## #           #  #   ",
                 "   ## ########### #      ",
                 "                  #      ",
                 ]
        astar = AStar(world)
        astar.pathfind('d', 'c')

class Node:
    def __init__(self, data, cost, next=None):
        self.data = data
        self.cost = cost
        self.next = next
class LinkedList:
    """Uses sorting_function on data to calculate cost. 
    Keeps list sorted in ascending cost. 
    """
    def __init__(self, sorting_function):
        self.sentinel_start = Node(None, None)
        self.size = 0
        self.sorting_function = sorting_function
    def add_sorted(self, data):
        self.size += 1
        prev = self.sentinel_start
        cur = prev.next
        cost = self.sorting_function(data)
        while cur is not None and cur.cost < cost:
            prev = cur
            cur = cur.next
        prev.next = Node(data, cost, cur)
    def pop_front(self):
        if self.sentinel_start.next is None:
            raise Exception("Tried to pop empty list!")
        self.size -= 1
        to_return = self.sentinel_start.next.data
        self.sentinel_start.next = self.sentinel_start.next.next
        return to_return
    def peek_front(self):
        if self.size == 0:
            return None
        return self.sentinel_start.next.data

class Data:
    def __init__(self, cur_pos, cost_so_far, path):
        self.cur_pos = cur_pos
        self.cost_so_far=cost_so_far
        self.path = path

class AStar:
    def __init__(self, world):
        self.world = world
    def get_heuristic_estimate(self, endpos):
        def heuristic_estimate(data):
            if allow_diagonals:
                # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
                # so I guess just having it as exact as possible is best
                return data.cost_so_far + max(abs(data.cur_pos[0] - endpos[0]), abs(data.cur_pos[1] - endpos[1]))
            else:
                return data.cost_so_far + abs(data.cur_pos[0] - endpos[0]) + abs(data.cur_pos[1] - endpos[1])
            #return pos[1] + 0.5*((pos[0][0] - endpos[0])**2 + (pos[0][1] - endpos[1])**2)**0.5
        return heuristic_estimate

    def pathfind(self, startchar, endchar):
        # find start and end points
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                if self.world[i][j] == startchar:
                    startpos = (i, j)
                if self.world[i][j] == endchar:
                    endpos = (i, j)
        if startpos is None or endpos is None:
            raise Exception ("start/end positions not found")
    
        # setup
        heuristic_estimate = self.get_heuristic_estimate(endpos)
        visited = [len(self.world[0])*[False] for _ in range(len(self.world))]
        ll = LinkedList(heuristic_estimate)
        ll.add_sorted(Data(cur_pos=startpos, 
                           cost_so_far=0, 
                           path=[startpos])) 

        while ll.size > 0 and ll.peek_front().cur_pos != endpos:
            # get next-lowest cost
            cur_node = ll.pop_front()
            if visited[cur_node.cur_pos[0]][cur_node.cur_pos[1]]:
                continue
            if fps > 0:
                time.sleep(1/fps)

            visited[cur_node.cur_pos[0]][cur_node.cur_pos[1]] = True 
            # get connected vertices
            connected = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            if allow_diagonals:
                connected.extend ([[1, 1], [1, -1],[-1, -1], [-1, 1]])
            for dx, dy in connected:
                next_pos = (cur_node.cur_pos[0] + dx, cur_node.cur_pos[1] + dy)
                # if in range
                if next_pos[0] >= 0 and next_pos[0] < len(self.world) and next_pos[1] >= 0 and next_pos[1] < len(self.world[0]):
                    # and has not been visited, and the space in the world at that point is not a wall
                    if not visited[next_pos[0]][next_pos[1]] and self.world[next_pos[0]][next_pos[1]] != '#':
                        # set as visited
                        #visited[next_pos[0]][next_pos[1]] = True
                        # add to list with heuristic function
                        ll.add_sorted(Data(cur_pos=next_pos, 
                                           cost_so_far=cur_node.cost_so_far + 1, 
                                           path=cur_node.path + [next_pos]))

            # print world and the resultant search space
            print("-" * len(self.world[0]))
            for i in range(len(self.world)):
                for j in range(len(self.world[0])):
                    if visited [i][j] and (i, j) != startpos:
                        print('.', end='')
                    else:
                        print(self.world[i][j], end='')
                print()
        path = ll.peek_front().path
        # print world and the resultant search space
        print("-" * len(self.world[0]))
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                if (i, j) in path and (i, j) != startpos and (i, j) != endpos:
                    print('!', end='')
                elif visited [i][j] and (i, j) != startpos and (i, j) != endpos:
                    print('.', end='')
                else:
                    print(self.world[i][j], end='')
            print()
        
if __name__ == "__main__":
    main()