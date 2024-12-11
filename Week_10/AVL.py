import queue
'''
Augumenting last week's BST such that it will be height balanced,
thus becoming an AVL tree.

A tree is height balanced if for every node within the
tree, the height of its right and left subtrees differ by no
more than one.

In the case of the AVL tree, the balance of a node is calculated:

Node's balance = height of right - height of left
     of node        subtree          subtree
'''

class AVL_Tree:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.balance = 0    # Use to check the balance factor...

    def copy(self, other):
        self.data = other.data
        self.left = other.left
        self.right = other.right
        self.balance = other.balance

    def reBalance_helper(self):
        """Helper function to handle re-balancing of the tree"""
        if self.balance == -2:  # Left-heavy :- Need to rotate right.
            if self.left and self.left.balance == 1:  # Left-Right case :- left child is right heavy
                self.left.left_rotate()
            self.print_tree()
            return self.right_rotate()  # Rotate right
        elif self.balance == 2:  # Right-heavy :- need to rotate left.
            if self.right and self.right.balance == -1:  # Right-Left case :- right child is left heavy
                self.right.right_rotate()
            return self.left_rotate()   # Rotate Left
        return self

    def left_rotate(self):
        """Fixed left rotation implementation"""
        if not self.right:  # if there is no right child, rotation not possible
            return self
        new_left = AVL_Tree()
        new_left.copy(self)
        new_left.left = self.left
        new_left.right = self.right.left
        self.copy(self.right)
        self.left = new_left
        # new_root = self.right  # The new root of the subtree will be the right child
        # self.right = new_root.left  # The left child of the new root becomes the right child of the old root
        # new_root.left = self  # The current node becomes the left child of the new root

        # Update balance factors, after each rotation
        if self.left.balance == 1:
            self.left.balance = 0
        if self.left.balance == 2:
            self.left.balance = 0
        if self.balance == 0:
            self.balance = -1
        if self.balance == 1:
            self.balance = 0


    def right_rotate(self):
        """Fixed right rotation implementation"""
        if not self.left:  # If there is no left child, rotation is not possible
            return self
        new_right = AVL_Tree()
        new_right.copy(self)
        new_right.right = self.right
        new_right.left = self.left.right
        self.copy(self.left)
        self.right = new_right

        # Update balance factors, after each rotation
        if self.right.balance == -1:
            self.right.balance = 0
        if self.right.balance == -2:
            self.right.balance = 0
        if self.balance == 0:
            self.balance = 1
        if self.balance == -1:
            self.balance = 0


    def insert(self, data):
        """Fixed insert implementation with proper balancing"""
        if not self.data:  # If the current node is empty
            self.data = data
            return self

        # Insert the data into the left or right subtree depending on its value
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = AVL_Tree(data)
        elif data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.right = AVL_Tree(data)

        # Update balance factor
        self.balance = self.find_balance()

        print()
        self.print_tree()

        # Re-balance if necessary (the balance factor exceeds the limit)
        if abs(self.balance) > 1:
            self.reBalance_helper()

    def find_balance(self):
        """Calculate balance factor correctly"""
        # right_height = self.right.find_height() if self.right else 0
        # left_height = self.left.find_height() if self.left else 0
        # return right_height - left_height
        return (abs(self.right.balance) + 1 if self.right else 0) - (abs(self.left.balance) + 1 if self.left else 0)

    # def find_height(self):
    #     """Correctly calculate height"""
    #     if not self.data:
    #         return 0

    #     left_height = self.left.find_height() if self.left else 0
    #     right_height = self.right.find_height() if self.right else 0
    #     return 1 + max(left_height, right_height)

    def min_value_node(self):
        """Find minimum value node"""
        current = self
        while current.left:
            current = current.left
        return current

    def delete(self, data):
        """Fixed delete implementation with proper re-balancing"""
        if not self.data:
            return self

        if data < self.data:   # If the data is smaller than the current node, delete from the left subtree
            if self.left:
                self.left = self.left.delete(data)
        elif data > self.data:  # If the data is larger than the current node, delete from the right subtree
            if self.right:
                self.right = self.right.delete(data)
        else:
            # Node with one child or no child
            if not self.left:
                return self.right
            elif not self.right:
                return self.left

            # Node with two children
            temp = self.right.min_value_node()   # Find the inorder successor (min value node in right subtree)
            self.data = temp.data   # Replace the current node's data with the inorder successor's data
            self.right = self.right.delete(temp.data)   # Delete the inorder successor from the right subtree

        # Update balance
        self.balance = self.find_balance()

        # Re-balance if necessary
        if abs(self.balance) > 1:
            return self.reBalance_helper()

        return self

    def search(self, data):
        """Search implementation remains the same"""
        if not self.data:
            return False

        if self.data == data:
            return True
        elif data < self.data and self.left:
            return self.left.search(data)
        elif data > self.data and self.right:
            return self.right.search(data)
        return False

    # Your existing printing methods remain unchanged
    def inorder_print(self):
        if self.data:
            if self.left:
                self.left.inorder_print()
            print(self.data, end=" ")
            if self.right:
                self.right.inorder_print()

    def pre_order_print(self):
        if self.data:
            print(self.data, end=" ")
            if self.left:
                self.left.pre_order_print()
            if self.right:
                self.right.pre_order_print()

    def post_order_print(self):
        if self.data:
            if self.left:
                self.left.post_order_print()
            if self.right:
                self.right.post_order_print()
            print(self.data, end=" ")

    def breadth_first_print(self):
        the_nodes = queue.Queue()
        if self.data:
            the_nodes.put(self)
        while not the_nodes.empty():
            curr = the_nodes.get()
            if curr.left:
                the_nodes.put(curr.left)
            if curr.right:
                the_nodes.put(curr.right)
            print(curr.data, end=" ")

    def breadth_first_print_2(self):
        dummy = AVL_Tree(None)
        cur_row = queue.Queue()
        next_row = queue.Queue()
        print ('{:>5}'.format(self.data), '{:>2}'.format(self.balance))
        if self.data:
            cur_row.put(self)
        next_row_empty = False
        while not next_row_empty:
            next_row_empty = True
            while not cur_row.empty():
                element = cur_row.get()

                if element.left:
                    print ('{:>5}'.format(element.left.data), '{:>2}'.format(element.left.balance), end="  ")
                    next_row.put(element.left)
                    if element.left.left or element.left.right:
                        next_row_empty = False
                else:
                    print('{:>5}'.format("_"), '{:>2}'.format("_"), end="  ")
                    next_row.put(dummy)
                if element.right:
                    print ('{:>5}'.format(element.right.data), '{:>2}'.format(element.right.balance), end="  ")
                    next_row.put(element.right)
                    if element.right.left or element.right.right:
                        next_row_empty = False
                else:
                    print('{:>5}'.format("_"), '{:>2}'.format("_"), end="  ")
                    next_row.put(dummy)
            print()
            cur_row = next_row
            next_row = queue.Queue()



    def print_tree(self, prefix="", is_left=False):
        if self.data:
            print(prefix, end="")
            print("|__" if is_left else "|---", end="")
            print(f"{self.data} (b={self.balance})")
            if self.left:
                self.left.print_tree(prefix + ("|   " if is_left else "    "), True)
            if self.right:
                self.right.print_tree(prefix + ("|   " if is_left else "    "))


if __name__ == "__main__":
    # Create a new AVL tree
    avl = AVL_Tree(6)

    # Test multiple insertions
    values = [7, 10, 1, 3, -4, 8]
    for val in values:
        avl.print_tree()
        avl.insert(val)

    print("Initial tree:")
    avl.print_tree()
    avl.breadth_first_print_2()

    # Test search
    print(f"\nIs 10 in the AVL Tree? {avl.search(10)}")
    print(f"Is -1 in the AVL Tree? {avl.search(-1)}")

    # Test height and balance
    #print(f"\nTree height: {avl.find_height()}")
    print(f"Root balance: {avl.find_balance()}")

    # Test deletion
    print("\nDeleting 7...")
    avl.delete(7)
    avl.print_tree()

    print(f"\nNew root balance: {avl.find_balance()}")
