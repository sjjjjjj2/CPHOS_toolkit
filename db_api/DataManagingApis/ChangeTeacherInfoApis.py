from db_api import *
reverse_typedict={"仲裁":2,"教练":3,"负责人":1}

class MakeAllTypesToBeArbiter(CustomOperation):
    def __init__(self,ChangedUserId:int):
        super().__init__()
        self.ArbiterId=ChangedUserId
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i" % self.ArbiterId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such User!")
        if len(result) > 1:
            raise Exception("More than one User!")
        if result[0][-3] == 1:
            #Then it is currently a 负责人。
            #Firstly check: 是否有尚未批改的题目，作为负责人
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                if len(exam_id)>1:
                    raise Exception("What is happening? Two Tests are happening!")
                #存在未批改的考试
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.ArbiterId))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                if returned[0][0] > 0:
                    raise Exception("The SubCoach has not finished correcting the test papers !")
        cursor.execute("update cmf_tp_member set type = 2 where id = %i;" % self.ArbiterId)
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;"% self.ArbiterId)
        cursor.fetchall()
        







import openpyxl
class MakeAllTypesToBeSubCoach(CustomOperation):
    def __init__(self,ChangedUserId:int, ItsNewSupId:int):
        '''
            This api takes into ChangedUserId and ItsNewSupId.
            After being executed, it will make the subcoachid to be the subcoach of the supteacherid.
            Notice that this will raise an exception when the one becoming the subcoach is a arbiter.
        '''
        super().__init__()
        self.SupTeacherId = ItsNewSupId
        self.SubCoachId = ChangedUserId
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i" % self.SupTeacherId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such SupTeacher!")
        if len(result) > 1:
            raise Exception("More than one SupTeacher!")
        if result[0][-3] != 1:
            raise Exception("This is not a SupTeacher!")
        cursor.execute("select * from cmf_tp_member where id = %i" % self.SubCoachId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such SubCoach!")
        if len(result) > 1:
            raise Exception("More than one SubCoach!")
        if result[0][-3] == 1:
            #Then it is currently a 负责人。
            #Firstly check: 是否有尚未批改的题目，作为负责人
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                if len(exam_id)>1:
                    raise Exception("What is happening? Two Tests are happening!")
                #存在未批改的考试
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.SubCoachId))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                if returned[0][0] > 0:
                    raise Exception("The SubCoach has not finished correcting the test papers !")
        
        cursor.execute("update cmf_tp_member set type = 3 where id = %i;" % self.SubCoachId)
        cursor.fetchall()
        cursor.execute("update cmf_tp_member set p_id = %i where id = %i;" % (self.SupTeacherId, self.SubCoachId))
        cursor.fetchall()
        
                
class MakeAllTypesToBeSupTeacher(CustomOperation):
    def __init__(self,Id:int):
        super().__init__()
        self.Id = Id
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
        cursor.execute("update cmf_tp_member set type = 1 where id = %i;" % self.Id)
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;" % self.Id)
        cursor.fetchall()
        

class MakeArbiterToBeSupTeacher(CustomOperation):
    def __init__(self,Id:int):
        super().__init__()
        self.Id = Id
    def execute(self,cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
        if result[0][-3] != 2:
            raise Exception("This is not a arbiter!")
        cursor.execute("update cmf_tp_member set type = 1 where id = %i;" % self.Id)
        
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;" % self.Id)
        cursor.fetchall()
