"""
Binary Search Tree Traversal
"""

from enum import Enum


class DFSTraversalTypes(Enum):
    PREORDER = 1
    INORDER = 2
    POSTORDER = 3


class Node():
    def __init__ (self, val):
        self.value = val
        self.parent = None  # type: Node
        self.left = None  # type: Node
        self.right = None  # type: Node

    @property
    def has_left_child (self):
        return self.left is not None

    @property
    def has_right_child (self):
        return self.right is not None

    @property
    def has_child (self):
        return self.has_left_child or self.has_right_child

    @property
    def is_right_child (self):
        return self.value > self.parent.value

    @property
    def is_left_child (self):
        return self.value < self.parent.value

    @property
    def has_parent (self):
        return self.parent is not None

    def __eq__ (self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return self.value == other

    def __lt__ (self, other):
        if isinstance(other, Node):
            return self.value < other.value
        return self.value < other

    def __le__ (self, other):
        if isinstance(other, Node):
            return self.value <= other.value
        return self.value <= other

    def __gt__ (self, other):
        if isinstance(other, Node):
            return self.value > other.value
        return self.value > other

    def __ge__ (self, other):
        if isinstance(other, Node):
            return self.value >= other.value
        return self.value >= other


class BinaryTree():
    def __init__ (self):
        self.root = None
        self.__values = None  # Used to store results for function getValues

    def getValues (self, depth):
        if self.root is None:
            raise KeyError('Empty BinaryTree')

        # Init container for results.
        # Create empty list for each level of recursion.
        self.__values = []
        for i in range(depth + 1):
            self.__values.append([])

        self.__traverse_values(self.root, depth, 0)
        return self.__values

    def __traverse_values (self, node, depth, n):
        """Called recursively to store values at node number n."""
        # Append value for this node to results.
        if node is None:
            self.__values[n].append(None)
        else:
            self.__values[n].append(node.value)
        n += 1

        # Exit recursion if we've passed desired depth.
        if n > depth:
            return

        # Call recursively on children.
        if node is None:
            self.__traverse_values(None, depth, n)
            self.__traverse_values(None, depth, n)
            return

        self.__traverse_values(node.left, depth, n)
        self.__traverse_values(node.right, depth, n)

    def insert (self, val):
        """If val already is located in the tree, no new nodes are created."""
        if self.root is None:
            self.root = Node(val)
        else:
            self.__insert(val, self.root)

    def __insert (self, val, node: Node):
        """Calls itself recursively until an empty left or right node is
        found where val can be inserted.

        If a node with val already exists, no new (duplicate) node is created.
        """
        # Node placed to the left.
        if val < node:
            if not node.has_left_child:
                new_node = Node(val)
                new_node.parent = node
                node.left = new_node
            else:
                self.__insert(val, node.left)
        # Node placed to the right.
        elif val > node:
            if not node.has_right_child:
                new_node = Node(val)
                new_node.parent = node
                node.right = new_node
            else:
                self.__insert(val, node.right)

    def remove (self, val):
        if self.root is None:
            raise KeyError('Empty BinaryTree')
        self.__remove(val, self.root)

    def __remove (self, val, node: Node):
        """Calls itself recursively until node with this value is found and
        removed. Upon removal the left child will take the place of the node
        if it exists, otherwise the right child.
        """
        ##########################
        # Not the node we're looking for.
        ##########################
        if val < node:
            if node.has_left_child:
                self.__remove(val, node.left)
                return
            else:
                raise KeyError('Value not found in tree')
        elif val > node:
            if node.has_right_child:
                self.__remove(val, node.right)
                return
            else:
                raise KeyError('Value not found in tree')

        ##########################
        # Node is the one we're looking for.
        ##########################
        if node == self.root:
            # If this node is the root node, it has no parent so set it to root.
            parent_node = self.root
        else:
            parent_node = node.parent

        # ----------------------
        # No children.
        # ----------------------
        # Remove parent's left or right child (i.e., set it to None).
        if not node.has_child:
            if node == self.root:
                self.root = None
            elif node < parent_node:
                parent_node.left = None
            else:
                parent_node.right = None
            return

        # ----------------------
        # Only left child.
        # ----------------------
        if node.has_left_child and not node.has_right_child:
            if node == self.root:
                node.left.parent = None
                self.root = node.left
                return

            if node.left < parent_node:
                parent_node.left = node.left
            else:
                parent_node.right = node.left
            return

        # ----------------------
        # Only right child.
        # ----------------------
        if node.has_right_child and not node.has_left_child:
            if node == self.root:
                node.right.parent = None
                self.root = node.right
                return

            node.right.parent = parent_node
            if node.right < parent_node:
                parent_node.left = node.right
            else:
                parent_node.right = node.right
            return

        # ----------------------
        # Both children.
        # ----------------------
        # Find rightmost node in left child and set its right child to the
        # current node's right.
        rightmost_in_left = self.__find_rightmost_node(node.left)
        node.right.parent = rightmost_in_left
        rightmost_in_left.right = node.right

        # Replace this node with its left child in the hierarchy.
        if node == self.root:
            node.left.parent = None
            self.root = node.left
            return

        node.left.parent = parent_node
        if node < parent_node:
            parent_node.left = node.left
        else:
            parent_node.right = node.left

    def __find_rightmost_node (self, node):
        """Finds rightmost child in node hierarchy."""
        if node.has_right_child:
            return self.__find_rightmost_node(node.right)
        return node


class DFSTraversal():
    """Iterator utility class made for BinaryTree.

    Attributes
    ----------
        tree : BinaryTree
            The tree whose values we want to iterate over.
        traversal_type : DFSTraversalTypes
            Dictates the order with which tree's values are iterated over.
        values : list
            Stores all values in tree after traversing in order dictated by
            traversal_type.
        __index : int
            Used internally to keep track of where we are in self.values when
            iterating.
    """

    def __init__ (self, tree, traversalType):
        self.tree = tree
        self.traversal_type = traversalType
        self.values = None
        self.__index = None

    def changeTraversalType (self, traversalType):
        self.traversal_type = traversalType

    def __iter__ (self):
        self.values = []
        self.__index = 0
        self.__extract_values()
        return self

    def __next__ (self):
        if self.__index > len(self.values) - 1:
            raise StopIteration

        value = self.values[self.__index]
        self.__index += 1
        return value

    def __extract_values (self):
        if self.traversal_type == DFSTraversalTypes.INORDER:
            self.__traverse_in_order(self.tree.root)
        elif self.traversal_type == DFSTraversalTypes.PREORDER:
            self.__traverse_pre_order(self.tree.root)
        elif self.traversal_type == DFSTraversalTypes.POSTORDER:
            self.__traverse_post_order(self.tree.root)
        else:
            raise NotImplementedError('Unhandled DFSTraversalTypes value.')

    def __traverse_in_order (self, tree: Node):
        if tree is not None:
            self.__traverse_in_order(tree.left)
            self.values.append(tree.value)
            self.__traverse_in_order(tree.right)

    def __traverse_pre_order (self, tree: Node):
        if tree is not None:
            self.values.append(tree.value)
            self.__traverse_pre_order(tree.left)
            self.__traverse_pre_order(tree.right)

    def __traverse_post_order (self, tree: Node):
        if tree is not None:
            self.__traverse_post_order(tree.left)
            self.__traverse_post_order(tree.right)
            self.values.append(tree.value)


def test_INORDER ():
    """Test that results of iterating INORDER are in expected order."""
    tree = BinaryTree()
    values = [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]
    for val in values:
        tree.insert(val)

    traversal = DFSTraversal(tree, DFSTraversalTypes.INORDER)
    expected = [4, 10, 12, 15, 18, 22, 24, 25, 31, 35, 44, 50, 66, 70, 90]
    actual = [i for i in traversal]
    assert expected == actual


def test_PREORDER ():
    """Test that results of iterating PREORDER are in expected order."""
    tree = BinaryTree()
    values = [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]
    for val in values:
        tree.insert(val)

    traversal = DFSTraversal(tree, DFSTraversalTypes.PREORDER)
    expected = [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]
    actual = [i for i in traversal]
    assert expected == actual


def test_POSTORDER ():
    """Test that results of iterating POSTORDER are in expected order."""
    tree = BinaryTree()
    values = [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]
    for val in values:
        tree.insert(val)

    traversal = DFSTraversal(tree, DFSTraversalTypes.POSTORDER)
    expected = [4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 66, 90, 70, 50, 25]
    actual = [i for i in traversal]
    assert expected == actual


if __name__ == '__main__':
    test_INORDER()
    test_PREORDER()
    test_POSTORDER()
    print('DFSTraversal tests passed.')
