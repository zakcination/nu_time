interface IGradeDistribution {
    [grade: string]: number;
}

export interface ICourseGetting {
    courseId: number;
    sectionId: number | null;
    semesterId: number | null;
    instructorId: number | null;
    gradeDistribution: IGradeDistribution;
    averageGpa: number | null;
    grade: string;
    standardDeviation: number | null;
    medianGpa: number | null;
}
