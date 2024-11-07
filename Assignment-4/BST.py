class BSTNode:
    def __init__(self, key):
        self.key: int = key
        self.left: BSTNode = None
        self.right: BSTNode = None
        self.parent: BSTNode = None

    def __str__(self):
        return f'Key: {self.key}'


class BinarySearchTree:
    def __init__(self):
        self.root: BSTNode = None
    
    def __get_node__(self, key: int) -> BSTNode|None:
        ptr: BSTNode = self.root

        while ptr is not None:
            if key > ptr.key:
                ptr = ptr.right
            elif key < ptr.key:
                ptr = ptr.left
            else:
                break
        
        return ptr
    
    def insert(self, key: int):
        newNode: BSTNode = BSTNode(key)

        if self.root is None:
            self.root = newNode
            return
        
        ptr: BSTNode = self.root
        while True:
            if key >= ptr.key:
                if ptr.right is None:
                    ptr.right = newNode
                    newNode.parent = ptr
                    break
                else:
                    ptr = ptr.right
            else:
                if ptr.left is None:
                    ptr.left = newNode
                    newNode.parent = ptr
                    break
                else:
                    ptr = ptr.left
    
    def search(self, key: int) -> bool:
        ptr = self.__get_node__(key=key)
        return ptr is not None
    
    def delete(self, key: int):
        node = self.__get_node__(key=key)
        if node is None:
            print('Key not found!')
            return
        
        self.__delete_node__(node)
    
    def __delete_node__(self, node: BSTNode):
        # Case 1: Node is a leaf
        if node.left is None and node.right is None:
            if node == self.root:
                self.root = None
            else:
                parent = node.parent
                if parent.left == node:
                    parent.left = None
                else:
                    parent.right = None
            return

        # Case 2: Node has only one child
        if node.left is None:
            child = node.right
        elif node.right is None:
            child = node.left
        else:
            # Case 3: Node has two children
            successor = self.__find_minimum__(node.right)
            node.key = successor.key
            self.__delete_node__(successor)
            return

        # Handle Case 2
        if node == self.root:
            self.root = child
            if child:
                child.parent = None
        else:
            parent = node.parent
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
            if child:
                child.parent = parent

    def __find_minimum__(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder_traversal(self, node=None) -> list[int]:
        traversal = []

        # stack = []
        # node: BSTNode|None = self.root
        # stack.append(node)

        # while node or stack:
        #     if node:
        #         stack.append(node)
        #         node = node.left
        #     else:
        #         node = stack.pop()
        #         traversal.append(node.key)
        #         node = node.right

        if node is None:
            node = self.root

        if node.left:
            traversal += self.inorder_traversal(node=node.left)
        
        traversal.append(node.key)

        if node.right:
            traversal += self.inorder_traversal(node=node.right)
        
        return traversal
    
    def find_maximum(self) -> int|None:
        if self.root is None:
            return None
        ptr = self.root

        while ptr.right:
            ptr = ptr.right

        return ptr.key
    
    def find_minimum(self) -> int|None:
        if self.root is None:
            return None
        ptr = self.root

        while ptr.left:
            ptr = ptr.left

        return ptr.key
    
    def find_successor(self, key: int) -> int|None:
        ptr = self.__get_node__(key=key)

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
        ptr = self.__get_node__(key=key)

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

if __name__ == '__main__':
    bst = BinarySearchTree()
    bst.insert(30)
    bst.insert(80)
    bst.insert(20)
    bst.insert(40)
    bst.insert(50)
    bst.insert(70)
    bst.insert(60)

    print("Inorder traversal of the given tree")
    print(bst.inorder_traversal())

    key = 50
    print(f"\nDeleting {key} from the tree")
    bst.delete(key)
    print("Inorder traversal of the modified tree")
    print(bst.inorder_traversal())

    print('Root: ', bst.root)

