#!/usr/bin/env python

#  validator.py (Python2.3 or higher required) [oct. 14 2004]

#  [Original] by Yusuke Shinyama (yusuke at cs dot nyu dot edu)

#  modified to accomodate new format and rules, fall 2013
#  by Akshay Kumar [oct. 3 2013] (ak4126 at nyu dot edu)

import sys, re, copy

##  Person object
##
PID = 0
AMBCAPACITY = 4
class Person:

  def __init__(self, x, y, st):
    global PID
    self.pid = PID
    self.x = x
    self.y = y
    self.st = st
    self.rescued = False
    self.rescTime = -1
    self.rescAmbid = -1
    self.rescLoc = (-1,-1)
    self.picked = False
    PID += 1
    return
  
  def pick(self):
    self.picked = True
    return
  def rescue(self,time,ambid,loc):
    self.rescued = True
    self.rescTime = time
    self.rescLoc = loc
    self.rescAmbid = ambid
    return
  
## Ambulance object
AMBID = 0
class Ambulance:
  def __init__(self,hid,x,y):
    global AMBID
    self.id = AMBID
    self.hid = hid
    self.x = x
    self.y = y
    self.time = 0
    self.path = []
    self.pers = []
    
    AMBID += 1
    return

  def updateLocation(self,x,y):
    self.x = x
    self.y = y
    return
  def pick(self,pid):
    if len(self.pers) == AMBCAPACITY:
      raise IllegalPlanError('Cannot rescue more than %d people at once: %d' % (AMBCAPACITY, pid))
    else:
      self.pers.append(pid)
    return
      
  def drop(self):
    self.pers = []
    return  
  def inctime(self,t):
    self.time += t
    return

##  Hostpital object
##
HID = 0
class Hospital:
  
  def __init__(self, x, y, namb):
    global HID
    self.hid = HID
    self.x = x
    self.y = y
    self.ambids = []
    self.setLoc = False
    HID += 1
    return
    
  def updateLocation(self,x,y):
    self.x = x
    self.y = y
    self.setLoc = True
    return
  
  def addAmbu(self,ambid):
    self.ambids.append(ambid)
    return
  

# readdata
def readdata(fname):
  persons = []
  hospitals = []
  ambulances = []
  mode = 0
  with open(fname) as file_:
    for line in file_:
      line = line.strip().lower()
      if line.startswith("person") or line.startswith("people"):
        mode = 1
      elif line.startswith("hospital"):
        mode = 2
<<<<<<< HEAD
      elif line.startswith('<'):
        mode = 0    
=======
>>>>>>> f2da8660fcc2857eb2c91f988b5d53989b6820c4
      elif line:
        (a,b,c) = (0,0,0)
        if mode == 1:
          (a,b,c) = map(int, line.split(","))
          persons.append(Person(a,b,c))
        elif mode == 2:
          a = int(line)
          hospitals.append(Hospital(0,0,a))
          for i in range(a):
            ambulances.append(Ambulance(HID-1,0,0))
            hospitals[HID-1].addAmbu(AMBID-1)
  return (persons, hospitals, ambulances)

# read_results
def readresults(persons, hospitals, ambulances,result):
  hp1 = re.compile(r'\d+\s*\(\s*\d+\s*,\s*\d+\s*\)')
  hp2 = re.compile('\d+')
  #input(result)
  
  for line in result.split('\n'):
    line = line.strip().lower()
    if not line: continue
    if line.startswith('hospital'):
      line = line.strip('hospital').strip()
      hos = hp1.findall(line)
      
      for i in range(len(hos)):
        (hid,x,y) = map(int,hp2.findall(hos[i]))
        if hid<0 or hid>len(hospitals):
          return
        else:
          h = hospitals[hid]
          h.updateLocation(x,y)
          for j in h.ambids:
            ambulances[j].updateLocation(x,y)
      continue

    if line.startswith('ambulance'):
      line = line.strip('ambulance').strip()
      (ambid,path) = line.split(None,1)
      ambid = int(ambid)
      for s in path.split(';'):
        move = [int(a) for a in hp2.findall(s)]
        if len(move) == 0:
          continue # blank move, or line
        if len(move) == 4:
          # pick up a person (id, x, y, time)
          ambulances[ambid].path.append((move[0],move[1],move[2],move[3]))
        if len(move) == 2:
          # drop off at hospital  (-1,x,y) , -1 means its drop off move
          ambulances[ambid].path.append((-1,move[0],move[1]))
      continue
  return

def dist(a,b):
 return abs(a[0]-b[0])+abs(a[1]-b[1])

def isValidDropLocation(loc,hos):
  flag = False
  (x,y) = loc
  for i in range(len(hos)):
    h = hos[i]
    if (h.x == x) and (h.y == y):
      flag = True
      break
  return flag
 
def validateAndScore(persons, hospitals, ambulances):
  score = 0
  died = 0
  errmsg = ''
  err = False
  for i in range(len(ambulances)):
    amb = ambulances[i]    
    plen = len(amb.path)
    if err == False and plen > 0:
      path = amb.path
      prev = loc = (amb.x,amb.y)
      pers = []
      for j in range(plen):
        move = path[j]
        pid = move[0]

        #Pick up
        if pid >= 0 and pid < len(persons):
          if len(pers) == AMBCAPACITY:
            errmsg = 'ERROR: Cannot carry more than %d people at once: persId = %d, ambuId = %d' % (AMBCAPACITY, move[0],i)
            break
          else:
            p = persons[pid]
            loc = (p.x,p.y)
            if p.rescued == False and p.picked == False:
              pers.append(pid)
              p.picked = True
              amb.inctime(1+dist(prev,loc))
              prev = loc
              
            else:
              p = persons[pid]
              errmsg = 'ERROR: Person gets picked or rescued on other path (persId, rescTime, ambuId, Loc) = (%d,%d,%d,(%d,%d))'  % (pid,p.rescTime,p.rescAmbid,p.rescLoc[0],p.rescLoc[1])
              break
        
        # Drop    
        elif pid == -1:
          loc = (move[1],move[2])
          if isValidDropLocation(loc,hospitals):
            
            amb.inctime(1+dist(prev,loc))
            for k in range(len(pers)):
              tmpid = pers[k]
              if persons[tmpid].st >= amb.time:
                if persons[tmpid].rescued == False:
                  persons[tmpid].rescue(amb.time,i,loc)
                  score += 1
                else:
                  p = persons[tmpid]
                  errmsg = 'ERROR: Person gets picked or rescued on other path (persId, rescTime, ambuId, Loc) = (%d,%d,%d,(%d,%d))'  % (tmpid,p.rescTime,p.rescAmbid,p.rescLoc[0],p.rescLoc[1])
                  break                  
              else:
                died += 1
                
            pers = []
            prev = loc           
            continue
          else:
            errmsg = 'ERROR: Invalid Drop Location: ambId =%d, loc = (%d,%d)' % (i,loc[0],loc[1])
            break
            
        else:
          errmsg = 'ERROR: Invalid person: (ambId,pid) = (%d,%d): ' %(i,pid)
          break
      if len(errmsg)>0:
        err = True
        break
          
  
  if len(errmsg)>0:
    score = 0
    died = 0
  return (score,died,errmsg)

def getScore(output, scoreHelper):
  #(persons, hospitals, ambulances) = readdata(inputFile)
  (persons, hospitals, ambulances) = scoreHelper
  persons = copy.deepcopy(persons)
  hospitals = copy.deepcopy(hospitals)
  ambulances = copy.deepcopy(ambulances)
  readresults(persons, hospitals, ambulances, output)
  (score,died,errmsg) = validateAndScore(persons,hospitals,ambulances)
  return score
