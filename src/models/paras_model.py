import datetime


class Paras:
    def __init__(self, id: int, group_id: int, number_para: int, course_id: int, teacher_id: int, cabinet_id: int,
                 date: datetime.date):
        self.id = id
        self.group_id = group_id
        self.number_para = number_para
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.cabinet_id = cabinet_id
        self.date = date

    def toDict(self) -> dict:
        return {'id':self.id,'group':self.group_id,'number':self.number_para,'course':self.course_id,'teacher':self.teacher_id,'cabinet':self.cabinet_id,'date':self.date.strftime("%Y-%m-%d")}
