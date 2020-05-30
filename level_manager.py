#A Singleton object
#http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

#The LevelManager's job is to keep a stack of the currently executing screens
class LevelManager():
    #Inner class - This is where the implementation goes!
    class __LevelManager:
        def __init__(self):
            self._level_stack = []

        def load_level(self, level):
            self._level_stack.append(level)

        def leave_level(self):
            self._level_stack.pop()

        def get_current_level(self):
            if not self._level_stack:
                return None
            else:
                return self._level_stack[-1]

        
            
    #Instance variable!
    instance = None
    def __init__(self):
        #Create an object if one does not exist
        #Note that if two constructors are called, only one object is created!
        if not LevelManager.instance:
            LevelManager.instance = LevelManager.__LevelManager()

    #Pass attribute retrieval to the instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
