'''
2-3 trees are funky trees. They're also note fantastically
recursively defined like my favourite BST and AVL bois.
Still, interesting data structure!
'''
import random

class TwoThreeTree:
    def __init__(self, key=None, is_leaf=True, is_root=True):
        # Each node can hold either 1 or 2 keys and has 2 or 3 children
        if key is not None:
            self.keys = [key]
        else:
            self.keys = []
        self.children = [] 
        # Setting a flag for whether or not this is a leaf
        self.is_leaf = is_leaf
        # Setting a flag for whether or not this is the root
        self.is_root = is_root

    def display(self, indent="", pos="─── "):
        '''We keep coming back to this function! So useful'''
        if self.is_leaf:
            print(indent, end="")
            print(pos, end="")
            print (self.keys)
        else:
            for i in range(len(self.keys) + 1):
                if i == 0:
                    self.children[i].display(indent + "    ", pos="┌── ")
                elif i == len(self.keys):
                    self.children[i].display(indent + "    ", pos="└── ")
                else:
                    self.children[i].display(indent + "    ", pos="├── ")

                if i < len(self.keys):
                    print(indent, end="")
                    print(pos, end="")
                    print (self.keys[i])
    
    def insert_key(self, key):
        if self.is_leaf:
            # values are only ever initially inserted in leaf nodes
            if key not in self.keys:
                self.keys.append(key)
                self.keys.sort()
                # if turns into a 4-node
                if len(self.keys) == 3:
                    if not self.is_root:
                        # make self the left node, return a tuple with the value to push up and
                        # the new sibling
                        to_return = (self.keys[1], TwoThreeTree(self.keys[2], is_leaf=True, is_root=False))
                        self.keys = [self.keys[0]]
                        return to_return
                    else:
                        # slightly funkier to keep self as the root
                        left = TwoThreeTree(self.keys[0], is_leaf=True, is_root=False)
                        right = TwoThreeTree(self.keys[2], is_leaf=True, is_root=False)
                        self.keys = [self.keys[1]]
                        self.children = [left, right]
                        self.is_leaf = False
            return None
        else:
            for i in range(len(self.keys) + 1):
                # insert into correct child node
                if i == len(self.keys) or key < self.keys[i]:
                    returned = self.children[i].insert_key(key)
                    # if child was a 4-node
                    if returned is not None:
                        # insert key and child into correct positions
                        self.keys.insert(i, returned[0])
                        self.children.insert(i+1, returned[1])
                        # if self has become a 4-node
                        if len(self.keys) == 3:
                            if not self.is_root:
                                # make self the left node, return a tuple with the value to push
                                # up and the new sibling
                                to_return = (self.keys[1], TwoThreeTree(self.keys[2], is_leaf=False, is_root=False))
                                self.keys = [self.keys[0]]
                                to_return[1].children = self.children[2:]
                                self.children = self.children[:2]
                                return to_return
                            else:
                                # slightly funkier to keep self as the root
                                left = TwoThreeTree(self.keys[0], is_leaf=False, is_root=False)
                                left.children = self.children[:2]
                                right = TwoThreeTree(self.keys[2], is_leaf=False, is_root=False)
                                right.children = self.children[2:]
                                self.keys = [self.keys[1]]
                                self.children = [left, right]
                                return None
                    break
        return None
    
    def search_recursive(self, key):
        '''Helper function! Recursively searches the 2-3 tree'''
        # If the node is a leaf, just check if the key is here
        if key in self.keys:
            return True
        if not self.is_leaf:
        # Otherwise, we need to traverse down the tree
            for i, k in enumerate(self.keys):
                if key < k:
                    return self.children[i].search_recursive(key)
            # If the key is greater than all keys in this node, go to the last child
            return self.children[-1].search_recursive(key)
        return False

if __name__ == "__main__":
    tree = TwoThreeTree()

    # Insert some keys into the 2-3 tree
    keys_to_insert = [10, 20, 5, 6, 15, 30, 25]
    for key in keys_to_insert:
        tree.insert_key(key)
    tree.display()

    print("Search 10:", tree.search_recursive(10))
    print("Search 15:", tree.search_recursive(15))
    print("Search 100:", tree.search_recursive(100))

    tree = TwoThreeTree()
    keys_to_insert = [i for i in range(100)]
    random.shuffle(keys_to_insert)
    for key in keys_to_insert:
        tree.insert_key(key)
    tree.display()
    for i in range(100):
        if not tree.search_recursive(i):
            print ("error: couldn't find ", i)
    if tree.search_recursive (-1):
        print ("error: shouldn't have been able to find -1")
    if tree.search_recursive (100):
        print ("error: shouldn't have been able to find 100")