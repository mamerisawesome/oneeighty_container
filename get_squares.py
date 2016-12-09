#!/usr/bin/env python
import time
import random as rand
import json

class Point:
  def __init__ (self, x=None, y=None, tup=None, point=None):
    if x != None and y != None:
      self.x = x
      self.y = y
    elif tup != None:
      self.x = tup[0]
      self.y = tup[1]
    elif point != None:
      self.x = point.x
      self.y = point.y

  def get_x (self):
    return self.x

  def get_y (self):
    return self.y

  def get_coords (self):
    return (self.x, self.y,)

  def to_str(self):
    return "".join(("(", str(self.x), ", ", str(self.y), ")"))

class Line:
  def __init__ (self, point1, point2):
    self.p1 = point1
    self.p2 = point2

  def get_p1 (self):
    return self.p1

  def get_p2 (self):
    return self.p2

  def get_points (self):
    return (self.p1, self.p2,)

  def get_coords (self):
    return [self.p1.get_coords(), self.p2.get_coords()]

  def to_str(self):
    return "".join(("(", self.p1.to_str(), ", ", self.p2.to_str(), ")"))

class Graph:
  def __init__ (self, edges):
    self.edges = edges

  def get_siblings (self, point):
    points = []
    for edge in self.edges:
      if point.get_coords() in edge.get_coords():
        if not edge.get_coords() \
          .index(point.get_coords()):
            ni = 1 # if 0
        else:
          ni = 0 # el 1
        points += [Point(tup=edge.get_coords()[ni])]

    return points

  def in_graph (self, point, graph):
    for p in graph:
      if point == p:
        return True

    return False

  def _get_squares (self, data, counter=5, output=[]):
    if counter == 0:
      return output
    elif isinstance(data, Point):
      sibs = self.get_siblings(data)
      return self._get_squares(sibs, counter=counter, output=output+[data])
    else:
      c = counter-1
      out = []
      for point in data:
        sq = self._get_squares(point, counter=c, output=output)
        out += sq
      return out

  def get_squares (self, data, counter=5, output=[]):
    point_list = self._get_squares(data, counter=counter)

    squares = []
    count = 0
    i = 0

    for vertex in point_list:
      try:
        if i == 0:
          square = []

        square += [vertex.to_str()]

        if square[0] == square[4] and \
          not (
            self.in_graph(square[0], [square[1], square[2], square[3]]) or \
            self.in_graph(square[1], [square[0], square[2], square[3]]) or \
            self.in_graph(square[2], [square[0], square[1], square[3]])
          ) and square not in squares:
            squares += [square]

        i += 1

        if i == 5:
          i = 0

      except IndexError:
        i += 1

    squares = str(squares) \
      .replace("(", "[") \
      .replace(")", "]") \
      .replace("'", "")
    return json.loads(squares)

  def get_coords (self):
    edge_list = []
    for edge in self.edges:
      edge_list += [edge.get_coords()]

    return edge_list

  def get_points (self):
    points = []

    for edge in self.edges:
      p1 = edge.get_p1().get_coords()
      p2 = edge.get_p2().get_coords()
      if (p1 not in points):
        points += [p1]
      if (p2 not in points):
        points += [p2]

    return points

def generate_testgraph ():
  # Points
  a = Point(0, 0)
  b = Point(0, 1)
  e = Point(0, 2)
  d = Point(1, 0)
  c = Point(1, 1)
  f = Point(1, 2)
  h = Point(2, 0)
  g = Point(2, 2)

  # Edges
  ab = Line(a, b)
  ac = Line(a, c)
  ad = Line(a, d)
  be = Line(b, e)
  bc = Line(b, c)
  ce = Line(c, e)
  cd = Line(c, d)
  ch = Line(c, h)
  cf = Line(c, f)
  dh = Line(d, h)
  ef = Line(e, f)
  fg = Line(f, g)
  gh = Line(g, h)

  # Graph
  return Graph([ab, ac, ad, be, bc, ce, cd, ch, cf, dh, ef, fg, gh])

def generate_graph (n):
  points = []
  for i in range(0, n):
    for j in range(0, n):
      points += [Point(i, j)]

  edges = []
  for i in range(0, len(points)):
    for j in range(0, len(points)):
      if (i != j):
        edges += [Line(points[i], points[j])]

  return Graph(edges)

def chunks(l, n):
  for i in xrange(0, len(l), n):
    yield l[i:i + n]

from mpi4py import MPI
import numpy
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = 2

grap = generate_graph(n)
points = None
if rank == 0:
  points = grap.get_points()

  new_list = []
  for p in points:
    new_list += [Point(tup=p)]

  points = new_list
  points = list(chunks(points, ((n * n) / size)))
  t = time.time()

data = comm.scatter(points, root=0)
olist = []
for point in data:
  olist += [grap.get_squares(point, counter=5)]

res = comm.gather(olist, root=0)
if rank == 0:
  print res
  print "[TIME] " + str(time.time() - t)
