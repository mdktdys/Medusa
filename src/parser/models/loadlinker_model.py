class LoadLinker:
    def __init__(
        self,
        id: int,
        load: int,
        group: int,
        course: int,
        codediscipline: int,
        teacher: int,
        certificationformFirst: int,
        certificationformSecond: int,
        firstSemesterHours: int,
        secondSemesterHours: int,
        totalHours: int,
        srsHours: int,
        konspectHours: int,
        LandPHours: int,
        lecturesHours: int,
        practicesHours: int,
        lab1Hours: int,
        lab2Hours: int,
        KandPHours: int,
        ExamHours: int,
    ):
        self.id = id
        self.load = load
        self.group = group
        self.course = course
        self.codediscipline = codediscipline
        self.teacher = teacher
        self.certificationformFirst = certificationformFirst
        self.certificationformSecond = certificationformSecond
        self.firstSemesterHours = firstSemesterHours
        self.secondSemesterHours = secondSemesterHours
        self.totalHours = totalHours
        self.srsHours = srsHours
        self.konspectHours = konspectHours
        self.LandPHours = LandPHours
        self.lecturesHours = lecturesHours
        self.practicesHours = practicesHours
        self.lab1Hours = lab1Hours
        self.lab2Hours = lab2Hours
        self.KandPHours = KandPHours
        self.ExamHours = ExamHours

    def __eq__(self, other):
        if isinstance(other, LoadLinker):
            return (
                self.id == other.id
                and self.load == other.load
                and self.group == other.group
                and self.course == other.course
                and self.codediscipline == other.codediscipline
                and self.teacher == other.teacher
                and self.certificationformFirst == other.certificationformFirst
                and self.certificationformSecond == other.certificationformSecond
                and self.firstSemesterHours == other.firstSemesterHours
                and self.secondSemesterHours == other.secondSemesterHours
                and self.totalHours == other.totalHours
                and self.srsHours == other.srsHours
                and self.konspectHours == other.konspectHours
                and self.LandPHours == other.LandPHours
                and self.lecturesHours == other.lecturesHours
                and self.practicesHours == other.practicesHours
                and self.lab1Hours == other.lab1Hours
                and self.lab2Hours == other.lab2Hours
                and self.KandPHours == other.KandPHours
                and self.ExamHours == other.ExamHours
            )
        return False

    def __hash__(self):
        return hash(
            (
                self.id,
                self.load,
                self.group,
                self.course,
                self.codediscipline,
                self.teacher,
                self.certificationformFirst,
                self.certificationformSecond,
                self.firstSemesterHours,
                self.secondSemesterHours,
                self.totalHours,
                self.srsHours,
                self.konspectHours,
                self.LandPHours,
                self.lecturesHours,
                self.practicesHours,
                self.lab1Hours,
                self.lab2Hours,
                self.KandPHours,
                self.ExamHours,
            )
        )

    def __repr__(self):
        return (
            f"LoadLinker(id={self.id}, load={self.load}, group={self.group}, course={self.course}, "
            f"codediscipline={self.codediscipline}, teacher={self.teacher}, certificationformFirst={self.certificationformFirst}, certificationformSecond={self.certificationformSecond} "
            f"firstSemesterHours={self.firstSemesterHours}, secondSemesterHours={self.secondSemesterHours}, "
            f"totalHours={self.totalHours}, srsHours={self.srsHours}, konspectHours={self.konspectHours}, "
            f"LandPHours={self.LandPHours}, lecturesHours={self.lecturesHours}, practicesHours={self.practicesHours}, "
            f"lab1Hours={self.lab1Hours}, lab2Hours={self.lab2Hours}, KandPHours={self.KandPHours}, "
            f"ExamHours={self.ExamHours})"
        )
