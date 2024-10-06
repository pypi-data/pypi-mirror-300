#!/usr/bin/env python3
# coding=utf-8

import re
import data
import iselect
import render
from rich.pretty import pprint  # noqa: F401


#  JSON_DATA = data.read_live_streams()
#  user_list = data.get_entries(JSON_DATA, 'user_name')
#  title_list = data.get_entries(JSON_DATA, 'title')
#  category_list = data.get_entries(JSON_DATA, 'game_name')


#  grid = render.Grid()
#  grid.key_list = user_list
#  #  grid.key_start_index = 2
#  dictionary = grid.coordinates()
#  pprint(dictionary)

#  req = data.get_channels_terse_data("provod")
#  multilinestr = ""
#  for entry in req.values():
#      multilinestr += f"{str(entry)}\n"
#  multilinestr = data.get_channels_terse_mulstr("provod")
#  print(multilinestr)
#  exit()




#  multilinestr = data.get_channels_terse_mulstr("provod")
#  print(multilinestr)
#  exit()

multilinestr = """
provod          provod          [54621416]
provodn1k1      ProVodN1k1      [511212557]
provoda_club    provoda_club    [633274587]
"""
selection = iselect.iselect(multilinestr)
if selection == 130:
    # handle cancel of the command
    exit(selection)
# TODO: rewrite for channels
id_pattern = re.compile(r"\[(\d+)\]$")
sel_id = re.search(id_pattern, selection).group(1)
__sel_user = re.sub(id_pattern, "", selection).strip()
sel_user = re.sub(r"^.*\s", "", __sel_user).strip()

print(f"id:'{sel_id}'")
print(f"user:'{sel_user}'")
