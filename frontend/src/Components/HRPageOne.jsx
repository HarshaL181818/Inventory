import React, { useState, useEffect } from 'react';

const HRPageOne = () => {
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [selectedJD, setSelectedJD] = useState(null);
  const [weights, setWeights] = useState({
    skills: 50,
    experience: 20,
    education: 15,
    certifications: 10,
    location: 5,
  });
  const [timeSlots, setTimeSlots] = useState(['']);
  const [candidates, setCandidates] = useState([]);
  const [jdConfigs, setJdConfigs] = useState([]);
  const [jds, setJDs] = useState([]);

  // Fetch all job descriptions
  useEffect(() => {
    const fetchJDs = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/get_all_jds');
        const data = await res.json();
        setJobDescriptions(data);
      } catch (err) {
        console.error('❌ Failed to fetch JDs', err);
      }
    };
    fetchJDs();
  }, []);

  // Fetch JD configs (weights + time slots)
  useEffect(() => {
    const fetchConfigs = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/get_all_configs');
        const data = await res.json();
        setJdConfigs(data);
      } catch (err) {
        console.error('❌ Failed to fetch configs', err);
      }
    };
    fetchConfigs();
  }, []);

  // Fetch JD candidate match results
  useEffect(() => {
    const fetchJDData = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/jd_candidates');
        const data = await res.json();
        console.log("Fetched JD data with candidates:", data);
        setJDs(data);  // [{ jd_id, title, candidates: [{ candidate_email, match_score }] }]
      } catch (err) {
        console.error("Error fetching JD candidates", err);
      }
    };
    fetchJDData();
  }, []);

  const handleWeightChange = (field, value) => {
    setWeights(prev => ({ ...prev, [field]: Number(value) }));
  };

  const handleAddTimeSlot = () => {
    setTimeSlots(prev => [...prev, '']);
  };

  const handleTimeSlotChange = (index, value) => {
    const updated = [...timeSlots];
    updated[index] = value;
    setTimeSlots(updated);
  };

  const handleSaveConfig = async () => {
    if (selectedJD === null || selectedJD === '') return alert('❗Select a JD first');
    try {
      await fetch('http://127.0.0.1:5000/api/save_weights_and_timeslots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jd_id: selectedJD,
          weights,
          time_slots: timeSlots,
        }),
      });
      alert('✅ Config saved');
    } catch (err) {
      console.error('❌ Error saving config', err);
    }
  };

  const handleFindCandidates = async (jdId) => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/match_candidates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jd_id: jdId }),
      });

      const data = await res.json();
      console.log("Matched Candidates:", data);
      setCandidates(data);
    } catch (err) {
      console.error("Error finding candidates:", err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold">HR Page 1: JD Config & Candidate Scores</h2>

      <label className="block mt-4">Select JD:</label>
      <select onChange={(e) => setSelectedJD(e.target.value)} className="border p-2">
        <option value="">-- Select JD --</option>
        {jobDescriptions.map((jd) => (
          <option key={jd.job_id} value={jd.job_id}>
            {jd.title} (ID: {jd.job_id})
          </option>
        ))}
      </select>

      <div className="mt-4">
        <h3 className="font-semibold">Assign Weights</h3>
        {Object.entries(weights).map(([key, val]) => (
          <div key={key}>
            <label>{key.charAt(0).toUpperCase() + key.slice(1)} (%): </label>
            <input
              type="number"
              value={val}
              onChange={(e) => handleWeightChange(key, e.target.value)}
              className="border px-2"
            />
          </div>
        ))}
      </div>

      <div className="mt-4">
        <h3 className="font-semibold">Interview Time Slots</h3>
        {timeSlots.map((slot, i) => (
          <input
            key={i}
            type="text"
            placeholder="e.g., 2025-04-14T15:00"
            value={slot}
            onChange={(e) => handleTimeSlotChange(i, e.target.value)}
            className="block border px-2 my-1"
          />
        ))}
        <button onClick={handleAddTimeSlot} className="mt-2 px-2 py-1 bg-blue-500 text-white rounded">Add Slot</button>
      </div>

      <div className="mt-4 flex gap-4">
        <button onClick={handleSaveConfig} className="px-3 py-1 bg-green-600 text-white rounded">Save Config</button>
      </div>

      {candidates.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-bold">Matched Candidates</h3>
          {candidates.map((c) => (
            <div key={c.candidate_id} className="border p-2 rounded mb-2">
              <strong>{c.name}</strong> - Score: {c.score}%, Tier: {c.tier}
              <pre className="text-sm text-gray-700">{JSON.stringify(c.breakdown, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}

      <div className="mt-6">
        <h3 className="text-lg font-bold mb-2">JDs with Configured Time Slots</h3>
        {jdConfigs.map((jd) => (
          <div key={jd.jd_id} className="border p-4 mb-2 rounded bg-gray-50">
            <h4 className="font-semibold">{jd.title}</h4>
            <p><strong>Time Slots:</strong> {jd.time_slots.join(', ')}</p>
            <button
              onClick={() => handleFindCandidates(jd.jd_id)}
              className="px-3 py-1 bg-purple-600 text-white rounded mt-2"
            >
              Find Candidates
            </button>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-bold">All JD Candidate Matches</h3>
        {jds.map((jd) => (
          <div key={jd.jd_id} className="border p-4 mb-4 rounded shadow">
            <h2 className="text-xl font-bold mb-2">{jd.title}</h2>
            {jd.candidates ? (
              <ul className="list-disc pl-6">
                {jd.candidates.map((candidate, index) => (
                  <li key={index}>
                    {candidate.candidate_email} - Match Score: {candidate.match_score}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No matches yet</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HRPageOne;
