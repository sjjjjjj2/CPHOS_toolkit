from db_api import *
class AddNewSchoolByName(CustomOperation):
    def __init__(self,Name:str,AreaId:int):
        self.Name = Name
        self.AreaId = AreaId
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute("select * from cmf_tp_area where id = {}".format(self.AreaId))
            result = cursor.fetchall()
            if len(result) == 0:
                raise Exception("No such Id!")
            if len(result) > 1:
                raise Exception("More than one Id!")
            cursor.execute("select * from cmf_tp_school where `school_name` = '{}' and `area` = {}".format(self.Name,self.AreaId))
            result = cursor.fetchall()
            if len(result) > 0:
                print("School Named {} in Area id {} already exists!".format(self.Name,self.AreaId))
                print("Now just return the id of the school.")
                return result[0][0]
            
            
            cursor.execute("insert into cmf_tp_school (`school_name`,`area`) values ('{}',{})".format(self.Name,self.AreaId))
            cursor.execute("select * from cmf_tp_school where `school_name` = '{}' and `area` = {}".format(self.Name,self.AreaId))
            result = cursor.fetchall()
            return result[0][0]
        except Exception as e:
            print(e)
            raise e