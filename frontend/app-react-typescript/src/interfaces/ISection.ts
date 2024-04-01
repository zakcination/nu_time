export interface ISection {
    courseId: number;
    sectionNumber: number;
    instructorIds: number[];
    sectionType: string;
    enrolled: number;
    capacity: number;
}
