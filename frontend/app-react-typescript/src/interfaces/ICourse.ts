export interface ICourse {
    id: number;
    name: string;
    description: string;
    departmentId: number; // Assuming department ID is used as a reference
    instructorIds: number[]; // Assuming a list of instructor IDs
    semesterId: number | null;
    credits: number;
}
