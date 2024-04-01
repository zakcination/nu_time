import React, { useEffect, useState } from 'react';
import { ICourse } from '../interfaces/ICourse';

const CourseDropdown: React.FC = () => {
    const [courses, setCourses] = useState<ICourse[]>([]);
    const [selectedCourse, setSelectedCourse] = useState<number | null>(null);

    useEffect(() => {
        fetch('http://0.0.0.0:8000/api/courses/')
            .then(response => response.json())
            .then((data: ICourse[]) => setCourses(data))
            .catch(error => console.error("Failed to fetch courses", error));
    }, []);

    return (
        <select value={selectedCourse || ''} onChange={e => setSelectedCourse(Number(e.target.value) || null)}>
            <option value="">Select a course</option>
            {courses.map(course => (
                <option key={course.id} value={course.id}>
                    {`${course.name} - ${course.credits} credits`}
                </option>
            ))}
        </select>
    );
};

export default CourseDropdown;
