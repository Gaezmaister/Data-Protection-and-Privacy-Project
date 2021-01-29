
class GNode:
    def __init__(self, qids, value, gen_trees):
        self.qids = qids
        self.value = value
        self.marked = False
        self.gheight = None

    def is_marked(self):
        return self.marked

    def __get_height__(self, gen_trees):
        hmax = None
        for q in self.qids:
            h = gen_trees[q].height()
            if hmax is None or hmax < h:
                hmax = h
        return hmax

    def get_height(self, gen_trees):
        if self.gheight is None:
            self.gheight = self.__get_height__(gen_trees)
        return self.gheight

    def already_visited(self, id, val, visited):
        for v in visited:
            if (id in v and val >= v[id]):
                return True
        return False

    def get_direct_generalization(self, gen_forest, visited):
        direct_generalizations = []
        for i in range(len(self.qids)):

            if self.value[i] < gen_forest[self.qids[i]].height():
                if not self.already_visited(self.qids[i],self.value[i],visited):
                    value = list(self.value)
                    value[i] += 1
                    new_node = GNode(self.qids, value, gen_forest)
                    direct_generalizations.append(new_node)
        return direct_generalizations

    def apply(self, data, gen_forest):
        for i in range(len(self.qids)):
            for j in range(self.value[i]):
                data[self.qids[i]] = [gen_forest[self.qids[i]].generalize(row) for row in data[self.qids[i]].values]
        return data

    def __repr__(self):
        return "(qids: {} value: {})".format(self.qids, self.value)

class GenGraph:

    def __init__(self, quasi_ids, gen_forest):
        self.quasi_ids = quasi_ids
        self.root = GNode(quasi_ids,[0 for q in self.quasi_ids],gen_forest)
