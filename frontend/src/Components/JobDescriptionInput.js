import React, { useState } from 'react';

const JobDescriptionInput = ({ fetchAllJDs }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDesc, setJobDesc] = useState('');
  const [output, setOutput] = useState('');

  async function submitJD() {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: jobTitle,
          description: jobDesc,
        }),
      });

      const data = await res.json();
      if (data.error) {
        setOutput("❌ " + data.error);
      } else {
        const out = `
🎓 Education: ${data.education.required_degree}, ${data.education.field}
🛠 Skills:
  Programming: ${data.skills.programming_languages.join(', ')}
  Tools: ${data.skills.tools_and_technologies.join(', ')}
  Soft Skills: ${data.skills.soft_skills.join(', ') || 'None'}
📋 Responsibilities:\n  - ${data.responsibilities.join('\n  - ')}
📅 Experience: ${data.experience.years} years in ${data.experience.preferred_domains.join(', ')}
🆔 Job ID: ${data.job_id}
        `;
        setOutput(out);
      }

      // Fetch all stored job descriptions from the database
      fetchAllJDs();

    } catch (err) {
      console.error("Error:", err);
      setOutput("❌ Something went wrong. Please try again!");
    }
  }

  return (
    <div>
      <h1>Job Description Analyzer</h1>
      <input
        type="text"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
        placeholder="Enter job title"
      />
      <br />
      <textarea
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
        placeholder="Paste job description here..."
      />
      <br />
      <button onClick={submitJD}>Analyze</button>

      <pre>{output}</pre>
    </div>
  );
};

export default JobDescriptionInput;
