
class SymTable(object, Entry):
	
	def __init__(self, entry):
		self.entry = Entry
		self.symTable = {}
		
	def initEntry(self.entry.symName, self.entry()):
		symTable[self.entry.symName] = self.entry;
	
	def searchTable (self.entry.symName):
		return self.symTable.has_key(self.entry.symName);
	
	def getEntry (self.entry.symName):
		return self.symTable.get(symName);
	
	def modifyEntry(self.entry.symName):
		self.symTable[self.entry.symName].symValue = self.entry.symValue;
	
	def removeEntry(self.entry.symName):
		del self.symTable[self.entry.symName];
	
	def getParams(self.entry.symName):
		return self.symTable.get(self.entry.symName).symParamList;
	
	def getReturnType(self.entry.symName):
		return self.symTable.get(self.entry.symName).symReturnType;
	
	def getEntryValue(self.entry.symName):
		return self.symTable.get(self.entry.symName).symValue;
