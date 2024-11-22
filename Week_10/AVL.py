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
        '''Initialize the node with data and set left/right children to None'''
        self.data = data
        self.left = None
        self.right = None
        # Initial balance factor of the node (0 means balanced)
        self.balance = 0 

    def rebalance_helper(self):
        '''Helper function to handle rebalancing of the tree'''
        # Left-heavy subtree (balance < -1)
        if self.balance < -1:
            # Check for Left-Right case: If left child is right-heavy, we perform a left rotation on it first
            if self.left and self.left.balance > 0:
                # Left-rotate the left child
                self.left.left_rotate() 
            # Perform a right rotation on the current node (this handles the Left-Left or Left-Right case)
            self.right_rotate()

        # Right-heavy subtree (balance > 1)
        elif self.balance > 1:
            # Check for Right-Left case: If right child is left-heavy, 
            # we perform a right rotation on it first
            if self.right and self.right.balance < 0:
                # Right-rotate the right child
                self.right.right_rotate()  
            # Perform a left rotation on the current node (this handles the Right-Right or Right-Left case)
            self.left_rotate()

    #----- Problems with the rotation functions ------

    def left_rotate(self):
        '''Perform left rotation on the current node to balance the tree'''
        # The current node's right child becomes the new root, if it exists
        if self.right:
            tempdata = self.right.data
            tempbalance = self.right.balance
            self.right.data = self.data
            self.right.balance = self.balance
            self.data = tempdata
            self.balance = tempbalance

            old_right = self.right
            self.right = self.right.right
            old_right.right = old_right.left
            old_right.left = self.left
            self.left = old_right

            
            # Update the balance factors for the current node and the new root
            # The current node’s balance decreases by 1 (it’s shifted one level down)
            self.left.balance = self.left.balance - 1 - max(self.balance, 0)
            
            # The new root's balance factor is adjusted based on the current node’s balance
            self.balance = self.balance - 1 + min(self.left.balance, 0)
        
        # Return the new root of the subtree
        #return new_root

    def right_rotate(self):
        '''Perform right rotation on the current node to balance the tree'''
        # The current node's left child becomes the new root, if it exists
        if self.left:
            tempdata = self.left.data
            tempbalance = self.left.balance
            self.left.data = self.data
            self.left.balance = self.balance
            self.data = tempdata
            self.balance = tempbalance

            old_left = self.left
            self.left = self.left.left
            old_left.left = old_left.right
            old_left.right = self.right
            self.right = old_left

            
            # Update the balance factors for the current node and the new root
            # The current node’s balance decreases by 1 (it’s shifted one level down)
            self.right.balance = self.right.balance - 1 - max(self.balance, 0)
            
            # The new root's balance factor is adjusted based on the current node’s balance
            self.balance = self.balance - 1 + min(self.right.balance, 0)
        
        # Return the new root of the subtree
        #return new_root

    def insert(self, data):
        '''Insert a node into the AVL tree and rebalance if necessary'''
        # If there is no data at the root (this is the first insertion)
        if not self.data:
            self.data = data  # Set the current node's data
            return
        
        # Insert data in the left subtree if the data is smaller than the current node's data
        if data < self.data:
            if not self.left: 
                self.left = AVL_Tree(data)
                # Left insertion makes the node more left-heavy
                self.balance -= 1  
            else:
                # Recursively insert in the left subtree
                self.left.insert(data) 

        # Insert data in the right subtree if the data is larger than the current node's data
        elif data > self.data:
            if not self.right:
                self.right = AVL_Tree(data)
                # Right insertion makes the node more right-heavy
                self.balance += 1  
            else:
                # Recursively insert in the right subtree
                self.right.insert(data)  

        # After insertion, update the balance factor of the current node
        self.balance = self.find_balance()

        # Check the balance, rebalance if necessary
        if self.balance > 1 or self.balance < -1:
            self.rebalance_helper()

    def find_balance(self):
        '''Calculate the balance factor of the node (difference between left and right heights)'''
        # The height of the left subtree, or 0 if there’s no left child
        left_height = self.left.find_height() if self.left else 0
        
        # The height of the right subtree, or 0 if there’s no right child
        right_height = self.right.find_height() if self.right else 0
        
        # Return the difference: left height - right height
        return right_height - left_height

    def search(self, data):
        '''Search for a value in the AVL tree'''
        found = False
        if self.data:
            # If the current node’s data matches the search value, return True
            if self.data == data:
                found = True
            # If the search value is larger, continue searching in the right subtree
            elif data > self.data and self.right:
                return self.right.search(data)
            # If the search value is smaller, continue searching in the left subtree
            elif data < self.data and self.left:
                return self.left.search(data)
        return found 
    
    def find_height(self):
        '''Find the maximum depth (height) of the tree'''
        height = 0
        if self.data:
            # Get the height of the left and right subtrees
            left_height = self.left.find_height() if self.left else 0
            right_height = self.right.find_height() if self.right else 0
            
            # The height of the current tree is the max of its left and right subtrees + 1
            height = 1 + max(left_height, right_height)
        
        return height

    def min_value_node(self):
        '''Return the node with the minimum value found in the tree'''
        current = self
        while current.left:
            current = current.left
        return current
    
    # Deletion method for AVL tree
    def delete(self, data):
        '''Delete a node from the AVL tree and rebalance if necessary'''
        if not self:
            return  # If the tree is empty, terminate early

        if data == self.data:
            if not self.left and not self.right:
                self.data = None
                return
            if not self.left and self.right:
                return self.right
            elif not self.right and self.left:
                return self.left
            else:
                # Case 2: Node has two children, get the inorder successor (smallest in the right subtree)
                temp = self.right._min_value_node()
                self.data = temp.data  # Copy the inorder successor's value to this node
                self.right = self.right.delete(temp.data)  # Delete the inorder successor
        elif data < self.data:
            if self.left:
                self.left = self.left.delete(data)
        elif data > self.data:
            if self.right:
                self.right = self.right.delete(data)
        else:
            return

        # Step 2: Update height and balance factor of this node
        self.balance = self.find_balance()

        # Step 3: Rebalance the tree if necessary
        if self.balance > 1 or self.balance < -1:
            self.rebalance_helper()

        return self

        
    #-----Printing Functions------
    def inorder_print(self):
        '''Prints values from smallest to largest.'''
        # Will only print things if something's there
        if self.data:
            if self.left:
                self.left.inorder_print()
            print(self.data, end = " ")
            if self.right:
                self.right.inorder_print()

    def pre_order_print(self):
        '''Prints values from smallest to largest, node data is first.'''
        # Will only print things if something's there
        if self.data:
            print(self.data, end = " ")
            if self.left:
                self.left.inorder_print()
            if self.right:
                self.right.inorder_print()

    def post_order_print(self):
        '''Prints values from smallest to largest, node data is last.'''
        # Will only print things if something's there
        if self.data:
            if self.left:
                self.left.inorder_print()
            if self.right:
                self.right.inorder_print()
            print(self.data, end = " ")
    
    def breadth_first_print(self):
        '''Cathy's implementation, modified for this data structure.'''
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

    def print_tree(self, prefix, is_left=False):
        '''Prints a string representation of the tree structure'''
        if self.data:
            # Print the current node’s value with its appropriate prefix
            print(prefix, end="")
            print("|__" if is_left else "|---", end="")
            print(self.data, self.balance)
            
            # Recursively print the left and right subtrees
            if self.left:
                self.left.print_tree(prefix + ("|   " if is_left else "    "), True)
            if self.right:
                self.right.print_tree(prefix + ("|   " if is_left else "    "))


if __name__ == "__main__":
    avl = AVL_Tree(1)
    avl.insert(2)
    avl.insert(3)
    avl.insert(4)
    avl.print_tree("")
    avl.insert(5)
    avl.insert(6)
    avl.insert(7)
    avl.insert(8)
    avl.insert(9)

    avl.print_tree("")

    print(f"Is 10 in the our AVL Tree? {avl.search(10)}")
    print(f"Is -1 in the our AVL Tree? {avl.search(-1)}")

    print(f"The height (max depth) of this tree is: {avl.find_height()}")

    print(f"The balance for our AVL tree is: {avl.find_balance()}")

    print("Deleting 3...")
    avl.delete(3)
    avl.print_tree("")

    print(f"The balance for the tree is: {avl.find_balance()}")