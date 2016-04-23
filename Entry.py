

class Entry(object):
    def __init__ (self, symName, symLocation, symType, symValue, symReturnType, symGlobal):
        # self._token = token
        self._symName = symName
        self._symLocation = symLocation
        self._symType = symType
        self._symValue = symValue
        self._symReturnType = symReturnType
        self._symParamList = []
        self._symLocalOrGlobal = symGlobal

    '''
    @property
    def token(self):
        return self._token

    @token.deleter
    def token(self):
        del self._token
    '''

    @property
    def symGlobalOrLocal(self):
        return self._symLocalOrGlobal

    @symGlobalOrLocal.setter
    def symGlobalOrLocal(self, value):
        self._symLocalOrGlobal = value

    @property
    def symName(self):
        return self._symName

    @symName.setter
    def symName(self, value):
        self._symName = value

    @property
    def symLocation(self):
        return self._symLocation

    @symLocation.setter
    def symLocation(self, value):
        self._symLocation = value

    @property
    def symValue(self):
        return self.symValue

    @symValue.setter
    def symValue(self, value):
        self._symValue = value

    @property
    def symType(self):
        return self._symType

    @symType.setter
    def symType(self, value):
        self._symType = value

    @property
    def symReturnType(self):
        return self._symReturnType

    @symReturnType.setter
    def symReturnType(self, value):
        self._symReturnType = value

    @property
    def symParamList(self):
        return self._symParamList

    @symParamList.setter
    def symParamList(self, value):
        self._symParamList = value
