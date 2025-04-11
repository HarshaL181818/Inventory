import React, { useState, useEffect } from 'react';

const AllCVs = () => {
  const [candidates, setCandidates] = useState([]);
  const [error, setError] = useState(null);

  const fetchCandidates = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/get_all_candidates');
      const data = await res.json();
      if (res.ok) {
        setCandidates(data);
      } else {
        setError(data.error || 'Failed to fetch candidates');
      }
    } catch (err) {
      setError('An error occurred while fetching candidates');
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">All Candidate CVs</h2>
      {error && <p className="text-red-600">{error}</p>}

      {candidates.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {candidates.map((candidate) => (
            <div
              key={candidate.candidate_id}
              className="bg-gray-100 p-5 rounded-xl shadow-sm mb-4"
            >
              <h3 className="text-xl font-semibold mb-2">
                {candidate.name} ({candidate.candidate_id})
              </h3>
              <p className="mb-1"><strong>Email:</strong> {candidate.email}</p>
              <p className="mb-1">
                <strong>Education:</strong> {candidate.education_degree} from {candidate.education_university} ({candidate.education_year})
              </p>
              <p className="mb-2"><strong>Skills:</strong> {candidate.skills}</p>

              {/* Work Experience */}
              {candidate.work_experience && (
                <div className="mb-2">
                  <p className="font-semibold">Work Experience:</p>
                  {(() => {
                    try {
                      const experienceList = JSON.parse(candidate.work_experience);
                      return experienceList.map((exp, idx) => (
                        <div key={idx} className="ml-2 mb-1">
                          <p>
                            <strong>{exp.role}</strong> at <strong>{exp.company}</strong> ({exp.duration})
                          </p>
                          {exp.responsibilities && (
                            <ul className="list-disc list-inside text-sm text-gray-700">
                              {exp.responsibilities.map((resp, i) => (
                                <li key={i}>{resp}</li>
                              ))}
                            </ul>
                          )}
                        </div>
                      ));
                    } catch {
                      return <p className="text-gray-500">Invalid format</p>;
                    }
                  })()}
                </div>
              )}

              {/* Certifications */}
              {candidate.certifications && (
                <div className="mb-2">
                  <p className="font-semibold">Certifications:</p>
                  {(() => {
                    try {
                      const certs = JSON.parse(candidate.certifications);
                      return (
                        <ul className="list-disc list-inside text-sm text-gray-700">
                          {certs.map((cert, i) => (
                            <li key={i}>{cert}</li>
                          ))}
                        </ul>
                      );
                    } catch {
                      return <p className="text-gray-500">{candidate.certifications}</p>;
                    }
                  })()}
                </div>
              )}

              {/* Achievements */}
              {candidate.achievements && (
                <div>
                  <p className="font-semibold">Achievements:</p>
                  {(() => {
                    try {
                      const achs = JSON.parse(candidate.achievements);
                      return (
                        <ul className="list-disc list-inside text-sm text-gray-700">
                          {achs.map((ach, i) => (
                            <li key={i}>{ach}</li>
                          ))}
                        </ul>
                      );
                    } catch {
                      return <p className="text-gray-500">{candidate.achievements}</p>;
                    }
                  })()}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p>No candidates found.</p>
      )}
    </div>
  );
};

export default AllCVs;
