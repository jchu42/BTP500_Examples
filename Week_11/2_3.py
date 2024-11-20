'''
2-3 trees are funky trees. They're also note fantastically
recursively defined like my favourite BST and AVL bois.
Still, interesting data structure!
'''

class Node:
    def __init__(self, key=None, is_leaf=False):
        # Each node can hold either 1 or 2 keys and has 2 or 3 children
        if key is not None:
            self.keys = [key]
        else:
            self.keys = []
        self.children = [] 
        # Setting a flag for whether or not this is a leaf
        self.is_leaf = is_leaf

    def display(self, node, indent, last):
        '''We keep coming back to this function! So useful'''
        print(indent, end="")
        if last:
            print("└── ", end="")
            indent += "    "
        else:
            print("├── ", end="")
            indent += "|   "
        print(node.keys)
        for child in node.children:
            self.display(child, indent, False)
    
    def insert_key(self, key):
        if self.is_leaf:
            self.keys.append(key)
            self.keys.sort()
            if len(self.keys) == 3:
                # make self the left node, return a tuple with the value to push up and
                # the new sibling
                to_return = (self.keys[1], Node(self.keys[2], is_leaf=True))
                self.keys = [self.keys[0]]
                return to_return
            return None
        else:
            for i in range(len(self.keys) + 1):
                if i == len(self.keys) or key < self.keys[i]:
                    returned = self.children[i].insert_key(key)
                    if returned is not None:
                        # this should insert into correct positions?
                        self.keys.insert(i, returned[0])
                        self.children.insert(i+1, returned[1])
                        if len(self.keys) == 3:
                            # make self the left node, return a tuple with the value to push
                            # up and the new sibling
                            to_return = (self.keys[1], Node(self.keys[2], is_leaf=False))
                            self.keys = [self.keys[0]]
                            to_return[1].children = self.children[2:]
                            self.children = self.children[:2]
                            return to_return
                    break
        return None

class TwoThreeTree:
    def __init__(self):
        '''Initialize the tree with a single empty root node'''
        self.root = Node(is_leaf=True)

    def search(self, key):
        '''Search starting from the root node.'''
        return self.search_recursive(self.root, key)

    def search_recursive(self, node, key):
        '''Helper function! Recursively searches the 2-3 tree'''
        # If the node is a leaf, just check if the key is here
        if node.is_leaf:
            return key in node.keys
        # Otherwise, we need to traverse down the tree
        for i, k in enumerate(node.keys):
            if key < k:
                return self.search_recursive(node.children[i], key)
        # If the key is greater than all keys in this node, go to the last child
        return self.search_recursive(node.children[-1], key)
    
    def insert_key(self, key):
        returned = self.root.insert_key(key)
        if returned:
            # split and set new root node
            new_root = Node(returned[0])
            new_root.children.append(self.root)
            new_root.children.append(returned[1])
            self.root = new_root

    def display(self):
        # Helper function to print the tree (for debugging purposes)
        self.root.display(self.root, "", True)


if __name__ == "__main__":
    tree = TwoThreeTree()

    # Insert some keys into the 2-3 tree
    keys_to_insert = [10, 20, 5, 6, 15, 30, 25]
    for key in keys_to_insert:
        tree.insert_key(key)
        tree.display()

    print("Search 15:", tree.search(15))
    print("Search 100:", tree.search(100))
