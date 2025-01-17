# -*- coding: utf-8 -*-
"""
BSD 2-Clause License

Copyright (c) 2020, The FreeBSD Project
Copyright (c) 2020, Sergio Carlavilla

This script will convert the releases.adoc file to releases.toml
in this way we can share the releases variables between AsciiDoctor and Hugo
"""
#!/usr/bin/env python3

import sys, getopt
import re

# Global
variables = {}

def getValueByKey(key):
  return variables[key.replace("{", "").replace("}", "")].replace("\"", "")

def loadVariables(path):
  with open(path, 'r', encoding = 'utf-8') as releasesFile:
    line = releasesFile.readline()

    while line:
      if (re.match(r"^:{1}[^\n]+", line)):
        variable = re.sub(':', '', line.strip(), 1)
        variable = re.sub(': ', '="', variable)
        variable += "\""
        data = variable.split("=")

        if (len(data) == 2):
          variables.update( {data[0] : data[1]} )

      line = releasesFile.readline()

def main(argv):
  path = ''

  try:
    opts, args = getopt.getopt(argv,"hp:",["path="])
  except getopt.GetoptError:
    print('releases-toml.py -p <path>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('releases-toml.py -p <path>')
      sys.exit()
    elif opt in ("-p", "--path"):
      path = arg

  releasesTOML =  "# Code generated by the FreeBSD Documentation toolchain. DO NOT EDIT.\n"
  releasesTOML += "# Please don't change this file manually but run `make` to update it.\n"
  releasesTOML += "# For more information, please read the FreeBSD Documentation Project Primer\n"
  releasesTOML += '\n'

  loadVariables(path)

  for key in variables:
    foundBraces = re.search(r"\{.*?\}", variables[key])

    if (foundBraces):
      braces = foundBraces.group(0)
      releasesTOML += key + "=" + variables[key].replace(braces, getValueByKey(braces)) + "\n"
    else:
      releasesTOML += key + "=" + variables[key] + "\n"

  with open('./data/releases.toml', 'w', encoding = 'utf-8') as releasesTOMLFile:
    releasesTOMLFile.write(releasesTOML)

if __name__ == "__main__":
  main(sys.argv[1:])
