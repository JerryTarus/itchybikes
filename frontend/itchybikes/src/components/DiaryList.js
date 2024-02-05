// components/DiaryList.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const DiaryList = () => {
  const [diaries, setDiaries] = useState([]);

  useEffect(() => {

    // Fetch diaries from the server
    fetch('http://localhost:5000/api/diaries')
      .then((response) => response.json())
      .then((data) => setDiaries(data))
      .catch((error) => console.error('Error fetching diaries:', error));
  }, []);

  return (
    <div>
      <h2>Diary List</h2>
      {diaries.map((diary) => (
        <div key={diary.diary_id}>
          <h3>{diary.title}</h3>
          <p>{diary.summary}</p>
          {/* Usisahau like and comment functionality */}


        </div>
      ))}
      <Link to="/create-diary">Create a New Diary</Link>
    </div>
  );
};

export default DiaryList;
