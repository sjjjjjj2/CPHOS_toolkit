from db_api import customTransaction
from db_api.DataQueryApis.GetTeacherInfoApis import *
from db_api.DataManagingApis.ChangeTeacherInfoApis import *

returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆"))
print('customTransaction.executeOperation(GetTeacherInfoByName("史景喆")) returned: ', returned)
sjzid = returned[0]['id']
returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号"))
print('customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号")) returned: ', returned)
sjzxhid = returned[0]['id']



testreturned = customTransaction.executeOperation(MakeAllTypesToBeSubCoach(sjzxhid,sjzid))
print("customTransaction.executeOperation(MakeAllTypesToBeSubCoach(sjzxhid,sjzid)) returned:", testreturned)


returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号"))
print("now customTransaction.executeOperation(GetTeacherInfoByName('史景喆的小号')) returned:", returned)


customTransaction.rollBack() #rollBack, not making any change to the database.