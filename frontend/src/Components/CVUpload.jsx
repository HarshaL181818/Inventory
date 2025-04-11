import React, { useState } from 'react';

const CVUpload = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('cv', file);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/upload_cv', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error("Error uploading CV:", err);
    }
  };

  return (
    <div>
      <h2>Upload CV</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="application/pdf" />
        <button type="submit">Upload</button>
      </form>

      {response && (
        <div>
          <h3>Parsed CV Data</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default CVUpload;
