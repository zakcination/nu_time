// components/SemesterCards.tsx
import React, { useEffect, useState } from 'react';
import { ISemester } from '../interfaces/ISemester';

const SemesterCards: React.FC = () => {
    const [semesters, setSemesters] = useState<ISemester[]>([]);

    useEffect(() => {
        fetch('http://0.0.0.0:8000/api/semesters/')
            .then(response => response.json())
            .then((data: ISemester[]) => setSemesters(data))
            .catch(error => console.error("Failed to fetch semesters", error));
    }, []);

    return (
        <div className="semester-cards-container">
            {semesters.map(semester => (
                <div key={semester.id} className="semester-card">
                    <h3>{semester.name}</h3>
                    <p>Starts: {new Date(semester.startFrom).toLocaleDateString()}</p>
                    <p>Ends: {new Date(semester.endAt).toLocaleDateString()}</p>
                </div>
            ))}
        </div>
    );
};

export default SemesterCards;


// Add this style tag inside your SemesterCards.tsx file, ideally at the top or bottom of the file
<style>
    {`
  .semester-cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  .semester-card {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: 0.3s;
    width: 300px;
    border-radius: 5px;
    padding: 15px;
    background-color: white;
  }
  .semester-card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  }
  .semester-card h3 {
    margin-top: 0;
  }
`}
</style>
