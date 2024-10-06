#!/usr/bin/env python3
# coding=utf-8

#Following lines are for assigning parent directory dynamically.
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

#  from .. import render
#  import render
from render import Hints
import re
from rich.pretty import pprint  # noqa: F401


def diff_lists(l1, l2):
    """Python code to get difference of two lists without using set()"""

    #  ldiff = [i for i in l1 + l2 if i not in l1 or i not in l2]
    #  return ldiff

    # Get elements which are in first_list but not in sec_list
    diff = []
    for elem in l1:
        if elem not in l2:
            diff.append(elem)
    return diff


#  hints = render.Hints()
hints = Hints()
hc = hints.hint_chars
#  items = [*range(45)]
#  items = [*range(13)]
items = [*range(15)]

total, hint_length = hints.total(items)

l1 = hints.gen_hint_seq(items)
l2 = l1
s1 = set(l1)
s2 = set(l2)

print(items)
# XXX БЛЯДЬ хули они одинаковые?
#  l2.insert(0, "nn")  # XXX

differ = diff_lists(l1, l2)
print("???")
print("".join(differ))
print("???")

string_l1 = " ".join(l1)
string_l2 = " ".join(l2)
string_s1 = " ".join(s1)

print(f"l1 len = {len(l1)}")
print(f"l2 len = {len(l2)}")
print(f"s1 len = {len(s1)}")

print(string_l1)
print(string_l2)
print(string_s1)

print()

#  square = len(hc) ** 2
#  print(f"({len(hc)}) hc:'{hc}'")
#  if len(l1[1]) == 2:
#      print(f"{len(hc)}^2 = {square}")
#  elif len(l1[1]) == 3:
#      print(f"{len(hc)}^2 * 2 - {len(hc)} = {square * 2 - len(hc)}")

print(f"hc:({len(hc)}) hl:{hint_length} total:[{total}] hc: '{hc}'")

# using re + search()
# to get string with substring
#  res = [x for x in test_list if re.search(subs, x)]

#  select = [s for s in l1 if re.search("^n", s)]
#  select = [s for s in l1 if re.search("^nn", s)]
#  select = [s for s in l1 if re.search("^nno", s)]

#  select = l1["n"]
#  print(select)

#  sseq = "en"
#  #  res = re.search(r"{0}.".format(sseq), string_l1)
#  res = re.search(r"\b{0}\w\b".format(sseq), string_l1)
#  print(str(res[0]))
