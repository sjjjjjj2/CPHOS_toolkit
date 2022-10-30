from db_api import customTransaction
from db_api.DataQueryApis.GetTeacherInfoApis import *
from db_api.DataManagingApis.ChangeTeacherInfoApis import *

returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆"))
print(returned)



sjzid = returned[0]['id']
returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号"))
# print(returned)
sjzxhid = returned[0]['id']
testreturned = customTransaction.executeOperation(MakeAllTypesToBeSubCoach(sjzxhid,sjzid))

returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号"))

returned = customTransaction.executeOperation(GetTeacherInfoByName("史景喆的小号"))
print(returned)
customTransaction.commit()