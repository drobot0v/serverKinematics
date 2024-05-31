import roboticstoolbox as rtb
from spatialmath import SE3
import numpy as np


""" Вспомогательный функционал """

def nonNumericProd(lst__):
  res_ = lst__[0] if len(lst__) > 0 else None
  for i in range(1, len(lst__)):
    res_ *= lst__[i]
  return res_

""" Определение робота """

def buildRobot(robo__): # robo__ = {'robo_id': 'm2RR', 'dim': 2, 'args': [{'name': 'l0', 'parent': None, 'ETS': [('R', None), ('tx', 15)]}, etc] }
  # Составление композиции элементарных преобразований для конкретного сочленения:
  ETS_ = lambda ETS: nonNumericProd([getattr(rtb.ET, e[0])(e[1]) for e in ETS])
  # Создание сочленений:
  links_ = [rtb.Link(ETS_(l['ETS']), name=l['name'], parent=l['parent']) for l in robo__['links']]
  return rtb.ERobot(links_, name=robo__['robo_id'])

""" Основные функции """

def fkine(robo_, qs_):
  robot_ = buildRobot(robo_)
  sol_ = robot_.fkine(qs_)
  return list(sol_.t)


def ikine(robo__, 
          position__, 
          orientationEul__ = ([0, 0, 0], 'ZYX'), 
          q0__ = None):

  robot_ = buildRobot(robo__)
  orientationEul_ = SE3(orientationEul__[0], 'eul', orientationEul__[1])
  Tep_ = SE3(position__) * orientationEul_

  sol_ = robot_.ikine_LM(Tep=Tep_, q0=q0__)
  return list(sol_.q)