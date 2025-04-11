import React, { useState, useEffect } from 'react';

const AllJobDescriptions = () => {
  const [jobDescriptions, setJobDescriptions] = useState([]);

  async function fetchAllJDs() {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/get_all_jds');
      const data = await res.json();
      console.log(data);
      setJobDescriptions(data);  // Set job descriptions into the state
    } catch (err) {
      console.error("Error fetching job descriptions:", err);
    }
  }

  useEffect(() => {
    fetchAllJDs();
  }, []);  // Fetch job descriptions on component mount

  return (
    <div>
      <h2>All Job Descriptions</h2>
      {jobDescriptions.length > 0 ? (
        jobDescriptions.map((jd) => {
          // Parse responsibilities if it's a stringified JSON array
          const responsibilities = jd.responsibilities ? JSON.parse(jd.responsibilities) : [];
          
          // Convert comma-separated strings to arrays
          const programmingLanguages = jd.programming_languages ? jd.programming_languages.split(', ') : [];
          const experienceDomains = jd.experience_domains ? jd.experience_domains.split(', ') : [];

          return (
            <div className="jd-card" key={jd.job_id}>
              <h3>
                {jd.title} ({jd.job_id})
              </h3>
              <p>
                <strong>Education:</strong> {jd.education_degree || 'N/A'}, {jd.education_field || 'N/A'}
              </p>
              <p>
                <strong>Skills:</strong> 
                Programming: {programmingLanguages.length > 0 ? programmingLanguages.join(', ') : 'N/A'}
              </p>
              <p>
                <strong>Experience:</strong> {jd.experience_years || 'N/A'} years in{' '}
                {experienceDomains.length > 0 ? experienceDomains.join(', ') : 'N/A'}
              </p>
              <p><strong>Responsibilities:</strong></p>
              <ul>
                {responsibilities.length > 0 
                  ? responsibilities.map((res, index) => (
                      <li key={index}>{res}</li>
                    ))
                  : <li>N/A</li>}
              </ul>
              <hr />
            </div>
          );
        })
      ) : (
        <p>❌ Could not fetch job descriptions.</p>
      )}
    </div>
  );
};

export default AllJobDescriptions;
