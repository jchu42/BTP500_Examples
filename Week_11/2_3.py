'''
2-3 trees are funky trees. They're also note fantastically
recursively defined like my favourite BST and AVL bois.
Still, interesting data structure!
'''

class Node:
    def __init__(self, is_leaf=False):
        # Each node can hold either 1 or 2 keys and has 2 or 3 children
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

class TwoThreeTree:
    def __init__(self):
        '''Initialize the tree with a single empty root node'''
        self.root = Node(True)

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

    def insert(self, key):
        '''Start inserting at the root, and handle splits if necessary'''
        root = self.root
        # If root is full, we need to split it
        if len(root.keys) == 2:  
            new_root = Node()
            new_root.children.append(root)
            self.split(new_root, 0)  # Split the old root
            self.root = new_root  # The new root becomes the root
        self.insert_non_full(self.root, key)

    def insert_non_full(self, node, key):
        # This is where we insert the key when the node is not full
        if node.is_leaf:
            # Just insert the key in the correct place in this leaf node
            node.keys.append(key)
            node.keys.sort()  # Keep keys sorted in ascending order
        else:
            # If not a leaf, we need to decide which child to go to
            for i, k in enumerate(node.keys):
                if key < k:
                    self.insert_non_full(node.children[i], key)
                    return
            # If the key is greater than all keys, go to the last child
            self.insert_non_full(node.children[-1], key)

    def split(self, node, index):
        # Split the child at node.children[index]
        child = node.children[index]
        # The middle key to push up to the parent node
        mid_key = child.keys[1]  
        new_child = Node(is_leaf=child.is_leaf)
        if len(child.keys) == 3:
            # Move the larger key and child references to the new child
            new_child.keys.append(child.keys[2])
        if not child.is_leaf:
            new_child.children.append(child.children[2])
            new_child.children.append(child.children[3])

        # Now, split the original child
        child.keys = child.keys[:1]
        child.children = child.children[:2]

        # Push the middle key up to the parent node
        node.keys.insert(index, mid_key)
        node.children.insert(index + 1, new_child)

    def display(self):
        # Helper function to print the tree (for debugging purposes)
        self.root.display(self.root, "", True)


if __name__ == "__main__":
    tree = TwoThreeTree()

    # Insert some keys into the 2-3 tree
    keys_to_insert = [10, 20, 5, 6, 15, 30, 25]
    for key in keys_to_insert:
        tree.insert(key)

    tree.display()

    print("Search 15:", tree.search(15))
    print("Search 100:", tree.search(100))
