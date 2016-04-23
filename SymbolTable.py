import Entry as ent


class SymTable(object):
    def __init__(self, prev):
        # self.entry = Entry
        self._symTable = {}
        self._previous = prev

    @property
    def PreviousSymbolTable(self):
        return self._previous

    def initEntry(self, symName, symEntry):
        # listEntry = []
        # listEntry.append(symEntry)
        self._symTable.__setitem__(symName, symEntry)

    def searchCurrentTable(self, symName):
        return self._symTable.has_key(symName)

    def searchTable (self, symName):
        bFound = self._symTable.has_key(symName)
        if not bFound:
            prevTable = self._previous
            while prevTable != None:
                bFound = prevTable.searchTable(symName)
                if bFound:
                    break
                else:
                    prevTable = prevTable.PreviousSymbolTable

        return bFound

    def getEntryFromCurrentTable(self, symName):
        if self._symTable.has_key(symName):
            return self._symTable[symName]
        return None

    def getEntry (self, symName):
        if self._symTable.has_key(symName):
            Entries = self._symTable[symName]
            if Entries is not None:
                return Entries
        else:
            prev = self._previous
            while prev != None:
                if prev._symTable.has_key(symName):
                    Entries = prev._symTable[symName]
                    return Entries
                else:
                    prev = prev._previous

        return None

'''
    def UpdateValueInTable(self, symName, symValue):
        if self._symTable.has_key(symName):
            listEntries = self._symTable[symName]
            if listEntries is not None and listEntries.__len__() > 0:
                listEntries[0].symValue = symValue

    def removeEntryfromTable(self, symName):
        if self._symTable.has_key(symName):
            listEntries = self._symTable[symName]
            if listEntries is not None and listEntries.__len__() > 0:
                listEntries.__delitem__(0)
                if listEntries.__len__() == 0:
                    self._symTable.__delitem__(symName)
                else:
                    self._symTable[symName] = listEntries

    def getParams(self, symName):
        if self._symTable.has_key(symName):
            listEntry = self._symTable[symName]
            if listEntry is not None and listEntry.__len__() > 0:
                return listEntry[0].symParamList
        return None

    def getReturnType(self, symName):
        if self._symTable.has_key(symName):
            listEntry = self._symTable[symName]
            if listEntry is not None and listEntry.__len__() > 0:
                return listEntry[0].symReturnType
        return None

    def setParams(self, symName, listParms):
        if self._symTable.has_key(symName):
            listEntry = self._symTable[symName]
            if listEntry is not None and listEntry.__len__() > 0:
                listEntry[0].symParamList = listParms
'''