class GameLog():
	""" Keeps and supplies game log messages """
	
	def __init__(self):
		self.logEntries = []

	def _checkCurrentStateN(self, currentStateN):
		lastStateN = self.logEntries[-1][0] if len(self.logEntries) > 0 else 0
		if currentStateN < lastStateN:
			raise RuntimeError("gameLog received currentStateN={} but last log entry has stateN={}".format(currentStateN, lastStateN))

	def _findStateBeginIdx(self, stateN):
		endIdx = len(self.logEntries)
		firstIdx = endIdx
		for i in reversed(range(0, endIdx)):
			if self.logEntries[i][0] < stateN:
				break
			firstIdx = i
		return firstIdx

	def _findStateEndIdx(self, stateN):
		endIdx = len(self.logEntries)
		for i in reversed(range(0, endIdx)):
			if self.logEntries[i][0] <= stateN:
				break
			endIdx = i
		return endIdx

	def addLogEntry(self, currentStateN, text: str):
		""" Adds a single log entry, the log entry is given the next free number as logID """
		self._checkCurrentStateN(currentStateN)
		# The array position (index) in logEntries IS the logID
		self.logEntries.append((currentStateN, text))
	
	def addLogEntries(self, currentStateN, texts: list):
		""" Adds a list of log entries, each log entry is given the next free number as logID """
		self._checkCurrentStateN(currentStateN)
		# The array position (index) in logEntries IS the logID
		self.logEntries += [(currentStateN, t) for t in texts]

	def clearLogEntries(self, fromStateN):
		""" Removes all log entries including and after fromStateN """
		if len(self.logEntries) > 0:
			firstClearIdx = self._findStateBeginIdx(fromStateN)
			# apply clearing
			self.logEntries = self.logEntries[0:firstClearIdx]

	def getLogEntries(self, fromStateN, toStateN):
		""" Extracts log entries by fromStateN, toStateN where each log entry returned is on the form (logID, stateN, text)
		Note: fromStateN and toStateN is equivalent to iterators "begin" and "end" pointers
		"""
		if toStateN <= fromStateN:
			return []
		beginIdx = self._findStateBeginIdx(fromStateN)
		endIdx = self._findStateEndIdx(toStateN-1)
		logEntriesSubset = self.logEntries[beginIdx:endIdx]
		# extract log entries and prefixes each log entry with the log id
		return [(beginIdx + i,) + logEntry for i,logEntry in enumerate(logEntriesSubset)]

