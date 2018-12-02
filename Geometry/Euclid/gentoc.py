#!/usr/bin/env python3
#
#  This program generates the detailed TOC in Contents.ipynb by slurping
#  pretty JSON from .ipynb files, changing headings '##' to lists '  *',
#  and writing result to stdout.
#
#  Program uses numpy because author wanted to learn numpy.  So don't do
#  that.  Seriously though, a bit of a learning curve, result would read
#  better if operators like '+' were supported on strings, but a fun shift
#  from thinking in terms of one line at a time.
#
####-####+####-####+####-####+####-####+####-####+####-####+####-####+####-###
import numpy as np
from glob import glob
import re

####-####+
#
#  Match pretty JSON markdown heading strings in Jupyter .ipynb files.  E.g.,
#
#        "## Postulate 1 - Points & Real Numbers\n",
#
regex = re.compile(r"""
  "(\#+)                  # /"#/ or /"##/ or /"###/, etc.
  \s+                     # Space.
  (\w+(?:\s+\d[-.\d]*)?)  # /Postulate 1/ or /Theorem 3.2-2/ or /Proof/.
  (.*)?                   # None or / - Points & Real Numbers/, etc.
  \\n                     # End of JSON string, drop embedded newline.
                          # The remainder, /",/, is ignored.
""", re.VERBOSE)

####-####+
#
#  Links grow large and numpy quietly truncates them if you did not reserve
#  enough space...
#
dtype = [("heading", "S8"), ("link", "S128"), ("title", "S128")]

####-####+####-####+####-####+####-####+####-####+####-####+####-####+####-###

for fname in sorted(glob('Chapter*')):

  # Slurp lines into ndarray.

  a_line = np.fromregex(fname, regex, dtype)

  # Change Markdown headings "#" or "##" to lists "*" or "  *", etc.

  a_depth = np.char.str_len(a_line['heading'])
  a_line['heading'] = np.char.add(np.char.multiply('  ', (a_depth - 1)), '*')

  # Build links from TOC entry to notebook:
  #  "Theorem 2 - Hot Arcs" -> "[Theorem 2](URL)"
  #   where URL = "{fname}#Theorem-2---Hot-Arcs".

  def spaceout(man): return np.char.replace(man, b' ', b'-')
  a_url = np.char.add(fname.encode('utf-8') + b'#',
                      np.char.add(spaceout(a_line['link']),
                                  spaceout(a_line['title'])))
  a_line['link'] = np.char.add(b' [',
                               np.char.add(a_line['link'],
                                           np.char.add(b'](',
                                                       np.char.add(a_url,
                                                                   b')'))))

  # Dump result to stdout.  Why doesn't a_line.decode work?

  for row in a_line:
    print(''.join([x.decode('utf-8') for x in row]))

####-####+####-####+####-####+####-####+####-####+####-####+####-####+####-###
