from db_api import customTransaction
from db_api.DataQueryApis.GetTeacherInfoApis import *
from db_api.DataManagingApis.ChangeTeacherInfoApis import *
from db_api.DataManagingApis.ChangeSchoolInfoApis import *
from db_api.DataQueryApis.GetSchoolInfoApis import *
from db_api.DataQueryApis.GetStudentInfoApis import *
from db_api.DataQueryApis.GetAreaInfoApis import *

returned = customTransaction.executeOperation(GetAllAreaNamesAndAreaIdsAsDict())

print(returned.keys())

customTransaction.rollBack() #rollBack, not making any change to the database. This can be omitted.
#That is, customTransaction.rollBack() will be executed at the end of the program unless you use customTransaction.commit().
