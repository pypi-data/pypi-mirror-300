#!/usr/bin/env python3
# coding=utf-8

#  from configparser import ConfigParser, NoOptionError, DEFAULTSECT
#  import configparser
import conf


#  config = configparser.ConfigParser()
#  config.read(global_config)
#  config.read("config.conf")
#  print(config.options(configparser.DEFAULTSECT))
#  print(config.options("GENERAL"))
#  print(config.get("GENERAL", "container_box_height"))
#  config.sections()
print(conf.setting("container_box_height"))
print(conf.setting("container_box_width"))
