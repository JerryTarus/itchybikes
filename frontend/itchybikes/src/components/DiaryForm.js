import React, { useState } from 'react';

const DiaryForm = ({ handleAddDiary }) => {
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [summary, setSummary] = useState('');
  const [image, setImage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Call the prop function handleAddDiary with the diary data
      await handleAddDiary({ title, date, summary, image });

      // Logic to send data to the server
      const formData = new FormData();
      formData.append('title', title);
      formData.append('date', date);
      formData.append('summary', summary);
      formData.append('image', image);

      const response = await fetch('http://localhost:5000/api/diaries', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to create diary');
      }

      const data = await response.json();
      console.log('Diary created successfully:', data);

      // Reset form fields after successfully adding the diary
      setTitle('');
      setDate('');
      setSummary('');
      setImage(null);
    } catch (error) {
      console.error('Error creating diary:', error);
    }
  };

  return (
    <div>
      <h2>Create Diary</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Title:
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
        </label>
        <label>
          Date:
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </label>
        <label>
          Summary:
          <textarea value={summary} onChange={(e) => setSummary(e.target.value)} />
        </label>
        <label>
          Image:
          <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files[0])} />
        </label>
        <button type="submit">Create Diary</button>
      </form>
    </div>
  );
};

export default DiaryForm;
