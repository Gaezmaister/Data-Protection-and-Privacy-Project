
class GeneralizationTreeNode:

    def __init__(self, value):
        self.father = None
        self.level = 0
        self.value = value
        self.son = None
        self.bro = None
        self.tree_height = None

    def search_node_value(self, value):
        node = None
        if value == self.value:
            node = self
        if node is None and self.son is not None:
            node = self.son.search_node_value(value)
        if node is None and self.bro is not None:
            node = self.bro.search_node_value(value)
        return node

    def __add_son__(self, son_node):
        if self.son is None:
            self.son = son_node
            return
        if self.son.value == son_node.value:
            raise Exception("[!!] A node with value {} at this level already exists".format(node.value))
        node = self
        while node.bro is not None:
            if node.value == son_node.value or node.bro.value == son_node.value:
                raise Exception("[!!] A node with value {} at this level already exists".format(node.value))
            node = node.bro
        node.bro = son_node

    def add_son(self, father_value, value):
        father = self.search_node_value(father_value)
        if father is None:
            raise Exception("[--] Cannot use this node as father: a node with value {} doesn't exists".format(father_value))
        new_son = GeneralizationTreeNode(value)
        new_son.father = father
        new_son.level = father.level + 1
        father.__add_son__(new_son)

    def __height__(self):
        if self.son is None and self.bro is None:
            return 1
        if self.son is not None:
            return 1 + self.son.height()
        if self.bro is not None:
            return 1 + self.bro.height()

    def height(self):
        if self.tree_height is None:
            self.tree_height = self.__height__()
        return self.tree_height

    def __generalize__(self):
        if self.father is None:
            return self.value
        return self.father.value

    def generalize(self, value, level=None):
        result = None
        if self.value == value and (level is None or level == self.level):
            result = self.__generalize__()
        if result is None and self.son is not None:
            result = self.son.generalize(value,level)
        if result is None and self.bro is not None:
            result = self.bro.generalize(value,level)
        return result

    def print_tree(self):
        print("[--] (lvl: {}\t value: {})".format(self.level, self.value))
        if self.son is not None:
            self.son.print_tree()
        if self.bro is not None:
            self.bro.print_tree()
