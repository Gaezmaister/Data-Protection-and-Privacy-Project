import pandas as pd
from utils import *
import itertools as it
import numpy as np

class Incognito:

    def __init__(self, gen_trees):
        self.gen_trees = gen_trees

    def __check_exists_tree__(self, features_name: list):
        if self.gen_trees is None:
            raise Exception("[!!] Generalization trees not defined!")
        for name in features_name:
            if name not in self.gen_trees:
                raise Exception("[!!] Generalization tree for {} not found!".format(name))

    def __check_generalization__(self, data, node, k):
        generalized_data = node.apply(data.copy(), self.gen_trees)
        for i in range(len(generalized_data.values)):
            count = 0
            for j in range(len(generalized_data.values)):
                if np.all(generalized_data.values[i] == generalized_data.values[j]):
                    count+=1
            if count < k:
                return False
        return True

    def __build_graphs__(self, i, quasi_ids):
        quasi_ids_combinations = list(it.combinations(quasi_ids, i))
        graphs = []
        for combination in quasi_ids_combinations:
            graphs.append(GenGraph(combination, self.gen_trees))
        return graphs

    def __is_visited__(self, node, visited):
        for v in visited:
            for i in range(len(node.qids)):
                if node.qids[i] in v and node.value[i] >= v[node.qids[i]]:
                    return True
        return False

    def __apply_kanonymous_generalization__(self, data, kanon_gen):
        for qid in data.columns.values:
            if qid not in kanon_gen:
                kanon_gen[qid] = 0
        kanon_config = GNode(data.columns.values,[kanon_gen[qid] for qid in data.columns.values], self.gen_trees)
        return kanon_config.apply(data,self.gen_trees)

    def max_generalization(self,data):
        max_gen = {}
        for qid in data.columns.values:
            max_gen[qid] = self.gen_trees[qid].height()
        return max_gen

    def __is_in_queue__(self, dgen, queue):
        for config in queue:
            if np.all(dgen.value == config.value):
                return True
        return False

    def __num_of_gen__(self, config):
        ris = 0
        for c in config:
            ris+=c
        return ris

    def __call__(self, data: pd.DataFrame, k: int, features_to_erase: list = None):
        data = remove_features(data, features_to_erase)
        self.__check_exists_tree__(data.columns.values.tolist())
        capped_qid = []
        best = {}
        for i in range(0, len(data.columns.values)):
            graphs = self.__build_graphs__(i+1, data.columns.values)
            queue = [elem.root for elem in graphs]
            queue.sort(key=lambda elem: elem.get_height(self.gen_trees), reverse=False)
            #print("[>>] Iteration: %d" % i)
            while len(queue) > 0:
                node = queue.pop(0) # GNode
                if not self.__is_visited__(node,capped_qid):#node.is_marked():
                    #print("[++] {} {}".format(node, capped_qid))
                    if(self.__check_generalization__(data, node, k)):
                        #print("[>>] It is {}-anonymous: {}".format(k, node.value))
                        observed = {}
                        for i in range(len(node.qids)):
                            observed[node.qids[i]] = node.value[i]
                        capped_qid.append(observed)
                        if len(best.values()) == 0 or (self.__num_of_gen__(list(best.values())) > self.__num_of_gen__(node.value)):
                            best=observed
                        #return self.__apply_kanonymous_generalization__(data, capped_qid)
                    else:
                        direct_generalizations = node.get_direct_generalization(self.gen_trees, capped_qid)
                        for dgen in direct_generalizations:
                            if not self.__is_in_queue__(dgen, queue):
                                queue.append(dgen)
                        queue.sort(key=lambda elem: elem.get_height(self.gen_trees), reverse=False)
        if len(best.values()) == 0:
            best = self.max_generalization(data)
        return self.__apply_kanonymous_generalization__(data, best)
