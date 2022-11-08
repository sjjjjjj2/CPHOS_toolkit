#CustomOperation is defined in db_api\CustomOperation.py
from db_api import *
typedict={2:'仲裁',3:'教练',1:'负责人'}
class GetTeacherInfoByName(CustomOperation):
    def __init__(self, Name:str):
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where user_name = '%s' and status != 0 " % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[3],'user_name':item[-7],'school_id':item[-6],'upload_limit':item[-2],'viewing_problem':item[-5],'type':typedict[item[-3]]})
            return returned_lst
        except Exception as e:
            print(e)
            raise e
        
class GetTeacherInfoByFlexibleName(CustomOperation):
    def __init__(self, Name:str):
        '''
        Name: str
        return: list, each element is a dictionary.
            item in list: dictionary with 
        '''
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where user_name like '%%%s%%'" % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[3],'user_name':item[-7],'school_id':item[-6],'upload_limit':item[-2],'viewing_problem':item[-5],'type':typedict[item[-3]]})
            return returned_lst
        except Exception as e:
            print(e)
            raise e

class GetTeacherInfoBySchoolId(CustomOperation):
    def __init__(self,SchoolId:int):
        self.MySQLCommand = "select * from cmf_tp_member where school_id = %d and status != 0" % SchoolId
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[3],'user_name':item[-7],'school_id':item[-6],'upload_limit':item[-2],'viewing_problem':item[-5],'type':typedict[item[-3]]})
            return returned_lst
        except Exception as e:
            print(e)
            raise e

class GetToBeVerifiedTeacherInfoByWechatName(CustomOperation):
    def __init__(self, WechatName:str):
        self.MySQLCommand = "select * from cmf_tp_member where `nickname` = \'{}\' and status = 0".format(WechatName)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'wechat_nickname':item[3]})
            return returned_lst
        except Exception as e:
            print(e)
            raise e

class GetToBeVerifiedTeacherInfoByFlexibleWechatName(CustomOperation):
    def __init__(self, WechatName:str):
        self.MySQLCommand = "select * from cmf_tp_member where `nickname` like \'%{}%\' and status = 0".format(WechatName)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'wechat_nickname':item[3]})
            return returned_lst
        except Exception as e:
            print(e)
            raise e