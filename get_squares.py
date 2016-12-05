#!/usr/bin/env python
import time
import random as rand

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
           \
          .index(point.get_coords()): 
            ni = 1 # if 0
        else: 
          ni = 0 # el 1
        points += [Point(tup=edge.get_coords()[ni])]

    return points

  def get_squares (self, data, counter=5, output=[]):
    if counter == 0:
      print "BASE CASE"
      print data.to_str()
      return output
    elif isinstance(data, Point):
      # print "POINT CASE"
      print data.to_str()
      sibs = self.get_siblings(data)
      return self.get_squares(sibs, counter=counter, output=output)
    # elif isinstance(data, list):
    else:
      print "LIST CASE"
      c = counter-1
      out = []
      for point in data:
        # print point.to_str()
        sq = self.get_squares(point, counter=c, output=output+[point])
        out += sq
      return out

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
g = Graph([ab, ac, ad, be, bc, ce, cd, ch, cf, dh, ef, fg, gh])
point_list = g.get_squares(a, counter=5)

squares = []
count = 0
for vertex in point_list:
  if :
  vertex.to_str()

from mpi4py import MPI
import numpy
import sys
