class RBNode:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


class RedBlackTree:
    def __init__(self):
        self.root = None

    def __getNode__(self, key: int) -> RBNode|None:
        ptr: RBNode = self.root

        while ptr is not None:
            if key > ptr.key:
                ptr = ptr.right
            elif key < ptr.key:
                ptr = ptr.left
            else:
                break
        
        return ptr

    def search(self, key):
        curr_node = self.root
        while curr_node is not None:
            if key == curr_node.key:
                return curr_node
            elif key < curr_node.key:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    def insert(self, key):
        new_node = RBNode(key)
        if self.root is None:
            new_node.color = 'black'
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if key < curr_node.key:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    def delete(self, key):
        node_to_remove = self.search(key)

        if node_to_remove is None:
            return

        if node_to_remove.left is None or node_to_remove.right is None:
            self._replace_node(
                node_to_remove, node_to_remove.left or node_to_remove.right)
        else:
            successor = self._find_min(node_to_remove.right)
            node_to_remove.key = successor.key
            self._replace_node(successor, successor.right)

        self.delete_fix(node_to_remove)

    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_left(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.right is None or sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.right:
                        sibling.right.color = 'black'
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_right(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left is None or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.rotate_left(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.left:
                        sibling.left.color = 'black'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'black'

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def _find_max(self, node):
        while node.right is not None:
            node = node.right
        return node

    def inorder_traversal(self, node=None) -> list[int]:
        traversal = []

        if node is None:
            node = self.root
            if node is None: 
                return []

        if node.left:
            traversal += self.inorder_traversal(node=node.left)
        
        traversal.append(node.key)

        if node.right:
            traversal += self.inorder_traversal(node=node.right)
        
        return traversal

    def find_successor(self, key: int) -> int|None:
        ptr = self.__getNode__(key=key)

        if ptr is None:
            print('Key not found!')
            return

        if ptr.right is not None:
            ptr = ptr.right
            while ptr.left is not None:
                ptr = ptr.left
            return ptr.key
        else:
            while ptr.parent is not None and ptr.parent.key < key:
                ptr = ptr.parent
            if ptr.parent is None:
                return None
            else:
                return ptr.parent.key
    
    def find_predecessor(self, key: int) -> int|None:
        ptr = self.__getNode__(key=key)

        if ptr is None:
            print('Key not found!')
            return

        if ptr.left is not None:
            ptr = ptr.left
            while ptr.right is not None:
                ptr = ptr.right
            return ptr.key
        else:
            while ptr.parent is not None and ptr.parent.key > key:
                ptr = ptr.parent
            if ptr.parent is None:
                return None
            else:
                return ptr.parent.key
    
    def select(self, k: int):
        return self.inorder_traversal()[k-1]

    def rank(self, key: int):
        return self.inorder_traversal().index(key)
    
if __name__ == "__main__":
    tree = RedBlackTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    tree.insert(25)

    print("Inorder traversal of the Red-Black Tree:")
    tree.inorder_traversal(tree.root)
    print()

    tree.delete(20)

    print("Inorder traversal of the Red-Black Tree after deleting 20")
    tree.inorder_traversal(tree.root)
    print()
