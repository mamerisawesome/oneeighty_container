#!/usr/bin/env python
import time
import random as rand
import json
import numpy

class Point:
  def __init__ (self, x=None, y=None, id=None):
    self.id = id
    if isinstance (x, int) and y != None:
      self.x = x
      self.y = y
    elif isinstance (x, list):
      self.x = x[0]
      self.y = x[1]
    elif isinstance (x, Point):
      self.x = point.x
      self.y = point.y
    else:
      return None

  def get_x (self):
    return self.x

  def get_y (self):
    return self.y

  def get_id (self):
    return self.id

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

  def in_graph (self, point, subgraph):
    for p in subgraph:
      if point == p:
        return True

    return False

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

  def get_siblings (self, point):
    points = []
    for edge in self.edges:
      if point.get_coords() in edge.get_coords():
        if not edge.get_coords() \
          .index(point.get_coords()):
            ni = 1 # if 0
        else:
          ni = 0 # el 1
        points += [Point(edge.get_coords()[ni])]

    return points

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

def generate_graph (n):
  edges = []
  z = 0
  for i in range(0, n):
    for j in range(0, n):
      edges += [Line(Point(i, j), Point(i, j+1))]
      edges += [Line(Point(i, j), Point(i+1, j))]
      edges += [Line(Point(i+1, j), Point(i+1, j+1))]
      edges += [Line(Point(i, j+1), Point(i+1, j+1))]
      # edges += [Line(Point(i, j), Point(i+1, j+1))]
      # edges += [Line(Point(i+1, j), Point(i, j+1))]

      z += 1

  return Graph(edges)

def chunks(l, n):
  return numpy.array_split(l, n)

def flatten(l, counter=2):
  if counter == 0:
    out = []
    for i in range(0, len(l)):
      if l[i] not in out:
        out += [l[i]]

    return out
  else:
    return flatten(sum(l, []), counter=counter-1)

def get_resistance_distance (g):
  output = 0
  graph = g.get_coords()
  res = {}

  # get serial
  for i in range(0, len(g.edges)):
    semi_out = 0
    pid1 = g.edges[i].get_p1().get_coords()
    pid2 = g.edges[i].get_p2().get_coords()
    
    try: 
      res[g.edges[i].get_p1().to_str()]    
    except KeyError:
      res[g.edges[i].get_p1().to_str()] = 0

    if pid1[0] == pid2[0] and pid1[1] < pid2[1]:
      semi_out += 1
    elif pid1[1] == pid2[1] and pid1[0] < pid2[0]:
      semi_out += 1

    res[g.edges[i].get_p1().to_str()] += semi_out
    output += semi_out

  # get parallel
  another_output = []
  for key, value in res.iteritems():
    key = key.split("(")[1]
    key = key.split(")")[0]
    key = key.split(", ")

    key[0] = int(key[0])
    key[1] = int(key[1])

    try:
      another_output[key[0]] += value
    except IndexError:
      another_output += [value]

  truly_final = 0
  for val in another_output:
    truly_final += val ** -1

  return truly_final

from mpi4py import MPI
import sys

graph = generate_graph(1000)
print get_resistance_distance(graph)
