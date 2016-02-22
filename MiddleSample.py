# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
 Name:          <filename.py> 
 Model:         <describe model>
 Authors:       <your name>
 Organization:  <your organization>
 Date:          <yyyy-mm-dd>
 License:       <your license>
-------------------------------------------------------------------------------
"""

### Specific import ------------------------------------------------------------
from DomainInterface.DomainBehavior import DomainBehavior
from DomainInterface.Object import Message

### Model class ----------------------------------------------------------------
class MiddleSample(DomainBehavior):
	''' DEVS Class for MiddleSample model
	'''

	def __init__(self):
		''' Constructor.
		'''
		DomainBehavior.__init__(self)

		self.state = {	'status': 'IDLE', 'sigma':INFINITY}
		self.proc = 3
		self.x = None
		self.y = None

	def extTransition(self):
		''' DEVS external transition function.
		'''
		slef.x = self.peek(self.IPorts[0])
		if self['status'] == 'ACTIVE':
			self.state['sigma'] -= self.elapsed
		else:
			self.state = {	'status': 'ACTIVE', 'sigma':self.proc}
			self.y = self.x
		print "EXTERNAL"
		print "X : ", self.x
		print "Y : ", self.y


	def outputFnc(self):
		''' DEVS output function.
		'''
		print "OUTPUT "
		slef.poke(slef.OPorts[0],Message(self.y))

	def intTransition(self):
		''' DEVS internal transition function.
		'''
		if self['status'] == 'ACTIVE':
			self.state = {	'status': 'IDLE', 'sigma':INFINITY}

	def timeAdvance(self):
		''' DEVS Time Advance function.
		'''
		return self.state['sigma']

	def finish(self, msg):
		''' Additional function which is lunched just before the end of the simulation.
		'''
		pass
