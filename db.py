import sqlite3
 
class ConnectDb(object):
    def __enter__(self) :
        print(self.__class__.__name__ + ".__enter__():Start")
 
        try :
            self.db = sqlite3.connect("database.db")
        except Exception as e:
            self.db = None
 
        print(self.__class__.__name__ + ".__enter__():End")
 
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.__class__.__name__ + ".__exit__():Start")
        if self.db != None :
            self.db.commit()
            self.db.close()
 
        print(self.__class__.__name__ + ".__exit__():End")
 
    def execute(self, sql):
        return self.db.execute(sql)
