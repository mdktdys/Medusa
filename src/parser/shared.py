from typing import List

from src.parser.models.cabinet_model import Cabinet
from src.parser.models.course_model import Course
from src.parser.models.data_model import Data
from src.parser.models.group_model import Group
from src.parser.models.loadlinker_model import LoadLinker
from src.parser.models.teacher_model import Teacher


def clean_dirty_string(string: str):
    return (
        string.replace(" ", "")
        .replace(".", "")
        .replace(",", "")
        .replace("-", "")
        .replace("_", "")
        .replace("\n", " ")
        .replace("\t", "")
        .replace("—", "")
        .replace("—", "")
    ).lower().replace(' ','')


def get_group_from_string(string: str, groups: List[Group]) -> Group | None:
    string = clean_dirty_string(string)
    founded_groups_by_name = [
        group for group in groups if string == clean_dirty_string(group.name)
    ]
    try:
        return founded_groups_by_name[0]
    except:
        return None


def get_course_from_string(string: str, courses: List[Course]) -> Course:
    string = clean_dirty_string(string)
    founded_courses_by_name = [course for course in courses if string == clean_dirty_string(course.name)]
    if len(founded_courses_by_name) > 0:
        return founded_courses_by_name[0]
    founded_courses_by_fullname = [course for course in courses if string == clean_dirty_string(course.fullname)]
    if len(founded_courses_by_fullname) > 0:
        return founded_courses_by_fullname[0]
    else:
        founded_courses_by_synonyms = []
        for course in courses:
            for syn in course.synonyms:
                if string.__contains__(clean_dirty_string(syn)):
                    founded_courses_by_synonyms.append(course)
                    break
        try:
            return founded_courses_by_synonyms[0]
        except:
            raise Exception(f"Not found course in string {string}")


def get_align_course_by_group(group: Group, course_name: str, data_model: Data) -> Course:
    group_links: List[LoadLinker] = [link for link in data_model.LINKERS if link.group == group.id]
    links_courses_ids = [link.course for link in group_links]
    courses = [course for course in data_model.COURSES if course.id in links_courses_ids]
    try:
        course = get_course_from_string(courses=courses, string=course_name)
    except Exception as e:
        print(f"{e} group {group.name}")
        course = None
    return course


def get_teacher_from_string(string: str, teachers: List[Teacher]) -> Teacher | None:
    string = clean_dirty_string(string)
    founded_teachers_by_name = [
        teacher for teacher in teachers if string == clean_dirty_string(teacher.name)
    ]
    if len(founded_teachers_by_name) > 1:
        # if string != "" and founded_teachers_by_name[0].name == "":
        #     pass
        # else:
        return founded_teachers_by_name[0]
    else:
        founded_teachers_by_synonyms = []
        for teacher in teachers:
            for syn in teacher.synonyms:
                if string == clean_dirty_string(syn):
                    # print("found")
                    founded_teachers_by_synonyms.append(teacher)
                    break
        try:
            return founded_teachers_by_synonyms[0]
        except:
            return None


def get_cabinet_from_string(string: str, cabinets: List[Cabinet]) -> Cabinet | None:
    string = clean_dirty_string(string)
    founded_cabinets_by_name = [
        cabinet for cabinet in cabinets if string == clean_dirty_string(cabinet.name)
    ]
    if len(founded_cabinets_by_name) > 0:
        return founded_cabinets_by_name[0]
    else:
        founded_cabinets_by_synonyms = []
        for cabinet in cabinets:
            for syn in cabinet.synonyms:
                if string == clean_dirty_string(syn):
                    founded_cabinets_by_synonyms.append(cabinet)
                    break
        try:
            return founded_cabinets_by_synonyms[0]
        except:
            return None


def get_empty_course(data_model: Data) -> Course:
    return [course for course in data_model.COURSES if course.name == " "][0]


def is_empty_course(string: str, empty_course: Course) -> bool:
    string = clean_dirty_string(string=string)
    if (
        string in empty_course.synonyms
        or string == empty_course.name
        or string == empty_course.fullname
    ):
        return True
    return False
