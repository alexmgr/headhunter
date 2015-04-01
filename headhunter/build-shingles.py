#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import enum
import itertools
import logging
import json
import pickle
import sys

class Format(enum.Enum):
  JSON = "json"
  PICKLE = "pickle"

def prepare_parser():
  parser = argparse.ArgumentParser(description="Compiles the shingle list from a set of headers")
  parser.add_argument("headers", help="File containing one header per line. If not provided, stdin is assumed", type=str, default='-', nargs='?')
  parser.add_argument("-o", "--output", help="File where to store the data", required=True)
  parser.add_argument("-s", "--size", help="Shingle length to use when building the permutations", type=int, default=4)
  output_format_group = parser.add_mutually_exclusive_group()
  output_format_group.add_argument("-j", "--json", help="Output data in json format", dest="output_format", action="store_const", const=Format.JSON)
  output_format_group.add_argument("-p", "--pickle", help="Output data in binary pickle format. Default, more efficient", dest="output_format", action="store_const", const=Format.PICKLE)
  return parser

if __name__ == "__main__":
  parser = prepare_parser()
  parser.set_defaults(output_format=Format.PICKLE)
  args = parser.parse_args()

  if args.headers != "-":
    try:
      with open(args.headers, "r") as f:
        headers = f.readlines()
    except:
      logging.fatal("Cannot access file containing headers: %s" % args.headers)
  else:
    headers = sys.stdin.readlines()

  headers = [header.strip() for header in headers]

  shingles = tuple(itertools.permutations(headers, args.size))
  with open(args.output, "w+") as f:
    if args.output_format == Format.PICKLE:
      pickle.dump({"shingles":shingles}, f)
    else:
      json.dump({"shingles":shingles}, f)

  exit(0)
