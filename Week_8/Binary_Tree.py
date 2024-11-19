'''
This is a binary tree implementation. Nodes
can have zero, one or two children.
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.children = [] # Cannot be more than two elements

    def add_node(self, data):
        if len(self.children) < 2:
            self.children.append(Node(data))
            self.children.sort(key=lambda n: n.data) # Just so they're in order
        else:
            if data < self.data:
                self.children[0].add_node(data)
            elif data > self.data:
                self.children[1].add_node(data)
            else:
                return # do nothing as the node already exists in the tree

    def print_tree(self, prefix, is_left=False):
        '''Prints a string representation of the actual tree.'''
        if self.data:
            print(prefix, end="")
            print("|__" if is_left else "|---", end="")
            print(self.data)
            # Enter the next tree level - left and right branch
            if self.children:
                self.children[0].print_tree(prefix + ("|   " if is_left else "    "), True)
                if len(self.children) == 2:
                    self.children[1].print_tree(prefix + ("|   " if is_left else "    "), False)


class BinaryTree:
    def __init__(self, data):
        self.root = Node(data)

    def add_node(self, data):
        self.root.add_node(data)

    def display(self):
        self.root.print_tree("")

    #TODO: Add height calculation

if __name__ == "__main__":
    tree = BinaryTree(5)
    tree.add_node(8)
    tree.add_node(7)
    tree.add_node(9)
    tree.add_node(4)
    tree.add_node(-1)
    tree.add_node(10)
    tree.add_node(11)
    tree.display()