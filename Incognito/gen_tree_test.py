#!/usr/bin/env python3

from utils import GeneralizationTreeNode

test = GeneralizationTreeNode("****")
test.add_son("****","a***")
test.add_son("a***","aa**")
test.add_son("aa**","aaa*")
test.add_son("aaa*","aaaa")
test.add_son("a***","ab**")
test.add_son("aaa*","aaab")

test.print_tree()

print("[--] Generalization of 'a***' is {}".format(test.generalize("a***")))
print("[--] Generalization of 'aa**' is {}".format(test.generalize("aa**")))
print("[--] Generalization of 'ab**' is {}".format(test.generalize("ab**")))
print("[--] Generalization of 'aaab' is {}".format(test.generalize("aaab")))
print("[--] Generalization of '****' is {}".format(test.generalize("****")))
print("[--] Generalization of 'aaa*' is {}".format(test.generalize("aaa*")))

print("[--] Height of test tree: {}".format(test.height()))
