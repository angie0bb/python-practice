# Practice python, assignment 4
# trees

# Part 1: Implement functions of a BST class
# class Node, print, insert codes are from lecture note
class BST:
    class Node:
        def __init__(self, value):
            self.left = None
            self.right = None
            self.value = value

    def __init__(self):
        self.root = None

    def print(self):
        def printTree(n, indent = 0):
            if n.right is not None:
                printTree(n.right, indent + 4)
            print(" " * indent, end="")
            print(n.value)
            if n.left is not None:
                printTree(n.left, indent + 4)
        printTree(self.root)
        print()

    def insert(self, value):
        # special case: when tree is empty
        if self.root is None:
            self.root = self.Node(value)
            return
        # Search for value in the tree, but remember the parent of the last node visted
        p = self.root  # parent
        prev = None
        while p is not None:
            prev = p
            if value < p.value:
                p = p.left
            else:
                p = p.right
        # Insert a new node with the value into the parent
        if value < prev.value:
            prev.left = self.Node(value)
        else:
            prev.right = self.Node(value)

    # 1) maxBST: returns the maximum value in a tree
    def maxBST(self):
        root = self.root
        while root.right is not None:
            root = root.right
        return root.value

    # 2) minBST: returns the minimum value in a tree
    def minBST(self):
        root = self.root
        while root.left is not None:
            root = root.left
        return root.value

    # sumLowerBST(value): calculates the sum of all values in the tree lower than the given value
    def sumLowerBST(self, value):
        def sumLowerBSTHelper(n):
            # base
            if n is None:
                return 0
            # recursive
            if n.value < value:
                return n.value + sumLowerBSTHelper(n.left) + sumLowerBSTHelper(n.right)
            else:  # n.value >= value
                return sumLowerBSTHelper(n.left)
        return sumLowerBSTHelper(self.root)

    # 4) countBST: counts the number of nodes in a tree
    def countBST(self):
        def countHelper(n):
            if n is None:
                return 0
            return 1 + countHelper(n.left) + countHelper(n.right)
        return countHelper(self.root)


bst_example = BST()
bst_example.insert(20)
bst_example.insert(10)
bst_example.insert(30)
bst_example.insert(5)
bst_example.insert(7)
bst_example.insert(25)
bst_example.insert(35)
bst_example.insert(40)
bst_example.insert(8)
bst_example.insert(12)
bst_example.insert(16)
bst_example.insert(18)
bst_example.insert(42)
bst_example.insert(50)
bst_example.insert(-10)
bst_example.insert(-5)
bst_example.insert(-1)
bst_example.insert(1)
bst_example.insert(37)
bst_example.insert(70)


bst_example.print()
print(bst_example.maxBST()) # 70
print(bst_example.minBST()) # -10
print(bst_example.sumLowerBST(0)) # -10 -5 - 1 = -16
print(bst_example.countBST()) # 20


