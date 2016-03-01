# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
 Name:          <MiddleSample.py> 
 Model:         A model for a lamp with some basic strategy
 Authors:       Raed Chammam
 Organization:  unice Polytech Sophia
 Date:          <1992-02-20>
 License:       GPL
-------------------------------------------------------------------------------
"""

### Specific import ------------------------------------------------------------
from DomainInterface.DomainBehavior import DomainBehavior
from DomainInterface.Object import Message
from transitions import Machine
from transitions import State

### Model class ----------------------------------------------------------------
class MiddleSample(DomainBehavior):
	''' DEVS Class for MiddleSample model
	'''

	def __init__(self):
		''' Constructor.
		'''
		DomainBehavior.__init__(self)

		self.state = {	'status': 'IDLE', 'sigma':INFINITY}
		self.proc = 0
		self.x = {}
		self.y = {}
		self.pos = [-1]*100
		''' The object '''
		self.lump = Lamp()
		# The states
		self.states = [
    		State(name='on', on_enter=['say_im_turned_on']),
    		State(name='off', on_enter=['say_im_turned_off'])
			]

		self.transitions = [
			{'trigger': 'illuminate', 'source': 'off', 'dest': 'on'},
			{'trigger': 'darken', 'source': 'on', 'dest': 'off'}
		]
		
		# Initialize
		self.machine = Machine(self.lump, states=self.states, transitions=self.transitions, initial='off')

	def extTransition(self):
		''' DEVS external transition function.
		'''
		for i in xrange(len(self.IPorts)):
			msg = self.peek(self.IPorts[i])
			if msg:
				print "---- EXTERNAL "+ str(msg) +" ----"
				self.x[i] = msg
				if self.state['status'] == 'ACTIVE':
					self.state['sigma'] = 0
				else:
					self.state = {  'status': 'ACTIVE', 'sigma':self.proc}

		self.y = self.x
		#print "STATUS : " , str(self.state['status'])
		#print "SIGMA : " , str(self.state['sigma'])


	def outputFnc(self):
		''' DEVS output function.
		'''
		print "---- OUTPUT ----"
		n = len(self.y)
		print "N : "+ str(n)
		print "TIME !!!!!!!!! : " + str(self.y[0].time)
		
		in0 = int(self.y[0].value[0])
		in1 = int(self.y[1].value[0])
		in2 = int(self.y[2].value[0])
		
		'''INSERT strategy here [Change the state of the FMS (self.lump)]'''
		if in0 == 1 and in1 == 1:
			if self.lump.state == "off":
				self.lump.illuminate()
		else:
			if self.lump.state == "on":
				self.lump.darken()
		
		''' End of strategy '''
		print "LAMP STATE :" , self.lump.state
		
		self.poke(self.OPorts[0],Message(str(int(self.lump.is_on())),str(self.y[0].time)))
		print "---- END OUTPUT ----"
		

	def intTransition(self):
		''' DEVS internal transition function.
		'''
		print "---- INTERNAL | Status "+str(self.state['status'])+" ----"
		if self.state['status'] == 'ACTIVE':
			self.state = {	'status': 'IDLE', 'sigma':INFINITY}

	def timeAdvance(self):
		''' DEVS Time Advance function.
		'''
		#print "---- TIME "+ str(self.state['sigma'])+" ----"
		return self.state['sigma']

	def finish(self, msg):
		''' Additional function which is lunched just before the end of the simulation.
		'''
		print "---- FINISH ----"



## Lamp class
class Lamp(object):
    def say_im_turned_on(self): print("Let there be LIGHT !")

    def say_im_turned_off(self): print("Hello darkness, my old friend !")
