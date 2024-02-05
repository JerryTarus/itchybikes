import React, { useState, useEffect } from 'react';

const Home = () => {
  // State for handling diary input
  const [diaryTitle, setDiaryTitle] = useState('');
  const [diarySummary, setDiarySummary] = useState('');
  const [diaryDate, setDiaryDate] = useState('');
  const [diaryImage, setDiaryImage] = useState(null);

  // State for storing posted diaries
  const [diaries, setDiaries] = useState([]);

  // State for comments and likes
  const [commentInput, setCommentInput] = useState('');
  const [diaryLikes, setDiaryLikes] = useState({});
  const [diaryComments, setDiaryComments] = useState({});

  // Fetch diaries from the backend on component mount
  useEffect(() => {
    const fetchDiaries = async () => {
      try {
        const response = await fetch('http://localhost:5000/diaries?sort=-date');
        if (!response.ok) {
          throw new Error('Failed to fetch diaries');
        }
        const diariesData = await response.json();
        setDiaries(diariesData);
      } catch (error) {
        console.error('Error fetching diaries:', error);
      }
    };

    fetchDiaries();
  }, []);

  // Function to handle adding a new diary
  const handleAddDiary = async () => {
    try {
      // Check if the user is authenticated
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('User not authenticated');
      }

      // Check if required fields are not empty
      if (!diaryTitle || !diarySummary || !diaryDate || !diaryImage) {
        throw new Error('All fields are required');
      }

      const formData = new FormData();
      formData.append('title', diaryTitle);
      formData.append('summary', diarySummary);
      formData.append('date', diaryDate);
      formData.append('image', diaryImage);

      const response = await fetch('http://localhost:5000/diaries', {
        method: 'POST',
        mode: 'cors',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to post diary');
      }

      // After successfully posting the diary, fetch the updated diaries
      const updatedDiariesResponse = await fetch('http://localhost:5000/diaries', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!updatedDiariesResponse.ok) {
        throw new Error('Failed to fetch updated diaries');
      }

      const updatedDiariesData = await updatedDiariesResponse.json();
      setDiaries(updatedDiariesData);

      // Reset input fields
      setDiaryTitle('');
      setDiarySummary('');
      setDiaryDate('');
      setDiaryImage(null);
    } catch (error) {
      console.error('Error posting diary:', error.message);
    }
  };

  // Function to handle adding a comment
  const handleAddComment = async (diaryId) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`http://localhost:5000/diaries/${diaryId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ comment: commentInput }),
      });

      if (!response.ok) {
        throw new Error('Failed to add comment');
      }

      // After successfully adding the comment, fetch the updated diary
      const updatedDiaryResponse = await fetch(`http://localhost:5000/diaries/${diaryId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!updatedDiaryResponse.ok) {
        throw new Error('Failed to fetch updated diary');
      }

      const updatedDiaryData = await updatedDiaryResponse.json();
      setDiaries((prevDiaries) =>
        prevDiaries.map((diary) =>
          diary._id === diaryId ? { ...diary, comments: updatedDiaryData.comments } : diary
        )
      );

      // Reset comment input
      setCommentInput('');
    } catch (error) {
      console.error('Error adding comment:', error.message);
    }
  };

  // Function to handle liking or unliking a diary
  const handleLikeDiary = async (diaryId) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('User not authenticated');
      }

      // Check if the user has already liked the diary
      const isLiked = diaryLikes[diaryId];

      const method = isLiked ? 'DELETE' : 'POST';

      const response = await fetch(`http://localhost:5000/diaries/${diaryId}/${isLiked ? 'unlike' : 'like'}`, {
        method,
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!response.ok) {
        throw new Error('Error liking or unliking diary');
      }
      
      // After successfully liking or unliking the diary, fetch the updated diary
      const updatedDiaryResponse = await fetch(`http://localhost:5000/diaries/${diaryId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!updatedDiaryResponse.ok) {
        throw new Error('Failed to fetch updated diary');
      }

      const updatedDiaryData = await updatedDiaryResponse.json();
      setDiaries((prevDiaries) =>
        prevDiaries.map((diary) =>
          diary._id === diaryId ? { ...diary, likes: updatedDiaryData.likes } : diary
        )
      );

      // Update like state
      setDiaryLikes((prevLikes) => ({
        ...prevLikes,
        [diaryId]: !isLiked,
      }));
    } catch (error) {
      console.error('Error liking or unliking diary:', error.message);

    }
  };

  // Function to handle deleting a comment
  const handleDeleteComment = async (diaryId, commentId) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`http://localhost:5000/diaries/${diaryId}/comments/${commentId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete comment');
      }

      // After successfully deleting the comment, fetch the updated diary
      const updatedDiaryResponse = await fetch(`http://localhost:5000/diaries/${diaryId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!updatedDiaryResponse.ok) {
        throw new Error('Failed to fetch updated diary');
      }

      const updatedDiaryData = await updatedDiaryResponse.json();
      setDiaries((prevDiaries) =>
        prevDiaries.map((diary) =>
          diary._id === diaryId ? { ...diary, comments: updatedDiaryData.comments } : diary
        )
      );
    } catch (error) {
      console.error('Error deleting comment:', error.message);
    }
  };

  // Function to handle editing a comment
  const handleEditComment = async (diaryId, commentId, editedComment) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`http://localhost:5000/diaries/${diaryId}/comments/${commentId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ comment: editedComment }),
      });

      if (!response.ok) {
        throw new Error('Failed to edit comment');
      }

      // After successfully editing the comment, fetch the updated diary
      const updatedDiaryResponse = await fetch(`http://localhost:5000/diaries/${diaryId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!updatedDiaryResponse.ok) {
        throw new Error('Failed to fetch updated diary');
      }

      const updatedDiaryData = await updatedDiaryResponse.json();
      setDiaries((prevDiaries) =>
        prevDiaries.map((diary) =>
          diary._id === diaryId ? { ...diary, comments: updatedDiaryData.comments } : diary
        )
      );
    } catch (error) {
      console.error('Error editing comment:', error.message);
    }
  };

  return (
    <div>
      {/* Landing Page Section */}
      <div>
        <h1>Welcome to Itchy Bikes Diary</h1>
        <p>Explore and share your biking experiences with the community!</p>
      </div>

      {/* Diary Entry Section */}
      <div>
        <h2>Add Diary</h2>
        <div>
          <label>Title:</label>
          <input type="text" value={diaryTitle} onChange={(e) => setDiaryTitle(e.target.value)} />
        </div>
        <div>
          <label>Summary:</label>
          <textarea value={diarySummary} onChange={(e) => setDiarySummary(e.target.value)} />
        </div>
        <div>
          <label>Date:</label>
          <input type="date" value={diaryDate} onChange={(e) => setDiaryDate(e.target.value)} />
        </div>
        <div>
          <label>Image:</label>
          <input type="file" accept="image/*" onChange={(e) => setDiaryImage(e.target.files[0])} />
        </div>
        <button onClick={handleAddDiary}>Post Diary</button>
      </div>

      {/* Display Diaries Section */}
      <div>
        <h2>Diaries</h2>
        {diaries.map((diary, index) => (
          <div key={index}>
            {/* Displaying diary details */}
            <h3>{diary.title}</h3>
            <p>{diary.summary}</p>
            <p>{diary.date}</p>
            {diary.image && <img src={`http://localhost:5000/${diary.image}`} alt={`Diary ${index}`} />}
            {/* Add comment and like functionality here */}
            <div>
              {/* Comment input and button */}
              <input
                type="text"
                placeholder="Add a comment"
                value={commentInput}
                onChange={(e) => setCommentInput(e.target.value)}
              />
              <button onClick={() => handleAddComment(diary._id)}>Comment</button>
            </div>
            <div>
              {/* Like button and count */}
              <button onClick={() => handleLikeDiary(diary._id)}>
                {diaryLikes[diary._id] ? 'Unlike' : 'Like'}
              </button>
              <span>{diary.likes} Likes</span>
            </div>
            {/* Display comments */}
            <div>
              {diary.comments &&
                diary.comments.map((comment) => (
                  <div key={comment._id}>
                    <p>{comment.text}</p>
                    {/* Edit and delete comment buttons */}
                    <button onClick={() => handleEditComment(diary._id, comment._id, prompt('Edit your comment:', comment.text))}>Edit</button>
                    <button onClick={() => handleDeleteComment(diary._id, comment._id)}>Delete</button>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
