from db_api import *
reverse_typedict={"仲裁":2,"教练":3,"负责人":1}

class MakeAllTypesToBeArbiter(CustomOperation):
    def __init__(self,ChangedUserId:int):
        super().__init__()
        self.ArbiterId=ChangedUserId
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.ArbiterId)
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
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.SupTeacherId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such SupTeacher!")
        if len(result) > 1:
            raise Exception("More than one SupTeacher!")
        if result[0][-3] != 1:
            raise Exception("This is not a SupTeacher!")
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.SubCoachId)
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
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.Id)
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
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.Id)
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

class ChangeAllTypesMarkingSubject(CustomOperation):
    def __init__(self,ChangedUserId:int, ItsNewMarkingSubject:int):
        self.Id=ChangedUserId
        self.NewMarkingSubject=ItsNewMarkingSubject
        assert self.NewMarkingSubject in [1,2,3,4,5,6,7,8,9,10], "Marking subject must be in [1,2,3,4,5,6,7,8,9,10]"

    def execute(self,cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
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
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.Id))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                if returned[0][0] > 0:
                    raise Exception("The SubCoach has not finished correcting the test papers !")
        
        cursor.execute("update cmf_tp_member set subject = %i where id = %i;" % (self.NewMarkingSubject, self.Id))
        cursor.fetchall()
        
class ChangeAllTypesSchool(CustomOperation):
    def __init__(self,ChangedUserId:int, NewSchoolId:int):
        self.Id=ChangedUserId
        self.NewSchoolId=NewSchoolId
    def execute(self,cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such TeacherId!")
        if len(result) > 1:
            raise Exception("More than one TeacherId!")
        cursor.execute("select * from cmf_tp_school where id = %i" % self.NewSchoolId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such SchoolId!")
        if len(result) > 1:
            raise Exception("More than one SchoolId!")
        cursor.execute("update cmf_tp_member set school_id = %i where id = %i;" % (self.NewSchoolId, self.Id))
        cursor.fetchall()

class ChangeAllTypesUploadLimit(CustomOperation):
    def __init__(self,ChangedUserId:int, NewUploadLimit:int):
        self.Id=ChangedUserId
        self.NewUploadLimit = NewUploadLimit
        assert (NewUploadLimit >=0 and NewUploadLimit<=60000), 'UploadLimit must be non-negative and <= 60000!'
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such TeacherId!")
        if len(result) > 1:
            raise Exception("More than one TeacherId!")
        cursor.execute("update cmf_tp_member set `limit` = %i where id = %i;" % (self.NewUploadLimit, self.Id))
        cursor.fetchall()
        
class VerifyTeacherUserToBeSupTeacher(CustomOperation):
    def __init__(self,ToBeVerifiedId:int,Name:str,SchoolId:int,ViewProblem:int=1, UploadLimit:int=1):
        self.Id = ToBeVerifiedId
        self.Name = Name
        self.SchoolId = SchoolId
        self.ViewProblem = ViewProblem
        self.UploadLimit = UploadLimit
    def execute(self,cursor:pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0 :
            raise Exception("待审核与已审核的老师用户中，均没有该id")
        if len(result) > 1:
            raise Exception("待审核与已审核的老师用户中，存在多个这种id")
        if result[0][-4] == 1:
            print("注意！userid为{}，姓名为{}的老师用户已经审核完毕，不做任何更改！".format(self.Id,result[0][-7]))
        else:
            cursor.execute("update cmf_tp_member set `user_name` = \'{}\', `school_id` = {}, `subject`={}, `limit`={}, `status`=1 where id = {}".format(self.Name,self.SchoolId,self.ViewProblem,self.UploadLimit,self.Id))
            cursor.fetchall()
            print("userid为{}，姓名为{}的老师用户审核完毕")
    



