#!/usr/bin/env python3
# coding=utf-8

from rich.pretty import pprint  # noqa: F401
from ast import literal_eval
import utils
import conf
from time import sleep
#  from iselect import iselect
import data
import json
import render
import textwrap

#  vari = bytes('CHRISTMAS POGGIES!!! later\ud83d\udc49 PoE ATLAS INVASION EVENT (UBER ELDER ON THE BEACH) | \"!interview\" with Leslie AKA SILVER FOX')
#  vari = 'CHRISTMAS POGGIES!!! later\ud83d\udc49 PoE ATLAS INVASION EVENT (UBER ELDER ON THE BEACH) | \"!interview\" with Leslie AKA SILVER FOX'
#  vari = '\u2b50\u3010\u8eb2\u8c93\u8c93\ud83e\udddf\u85cf\u5728\u79ae\u7269\u88e1\u2764\ufe0f\u3011\ud83c\udf81\u4eca\u665a\u9001\u8056\u8a95\u5927\u79ae\u5305 !\u8056\u8a95\u3010\ud83c\udf81\u9001\u65b0\u578b Switch OLED - \u53c3\u52a0\u8f38\u5165 !\u62bd\u734e\u3011\u3010FW\ud83c\udf4a\u8766\u611b\u6a58\u5b50\u3011\u904a\u6232\u540d\u7a31'

# very shitty! still brakes something!
vari = '\u3010 Stanley \u301112/26   \u7830\u7830\u6cd5\u5e2b\u5927\u6539\u7248  \u5c08\u5c6c\u514c\u63db\u78bc pbstanley666  \u8d85\u4f5b\u5fc3\u5927\u6539\u7248 \u770b\u6211\u80fd\u6253\u5230\u5e7eCombo'

#  string = vari.encode('raw_unicode_escape').decode('utf8')
#  string = str(vari).encode('raw_unicode_escape').decode()

#  string = vari.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
#  string = vari.encode('utf-16', 'surrogatepass').decode('unicode-escape').encode('latin1').decode('utf-16', 'surrogatepass')

#  string = vari.encode('utf-16', 'surrogatepass').decode('utf-16')
#  string = vari.encode('utf-8', 'surrogatepass').decode("utf-8", "ignore")

#  vari = "blyaaa"

string = vari
if not string.isprintable():
    try:
        string = string.encode('utf-16', 'surrogatepass').decode("utf-16", "ignore")
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        string = str(e)



#  string = json.loads(vari.encode('raw_unicode_escape').decode())
#  string = json.loads(vari.encode('raw_unicode_escape'))
#  out = utils.word_wrap_for_box(string, 40, 40 * 3)
#  print(vari)
#  print()
print(string)
#  print(out)


text = textwrap.fill(
    string, 40, max_lines=3,
    expand_tabs=False, replace_whitespace=True,
    break_long_words=True, break_on_hyphens=True, drop_whitespace=True
)
print(text)
print(len(string))
print(string)
