import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

function TimeSlotsInput({ timeSlots, setTimeSlots }) {
  const addSlot = () => setTimeSlots([...timeSlots, ""]);
  const updateSlot = (index, value) => {
    const newSlots = [...timeSlots];
    newSlots[index] = value;
    setTimeSlots(newSlots);
  };
  const removeSlot = (index) => {
    const newSlots = [...timeSlots];
    newSlots.splice(index, 1);
    setTimeSlots(newSlots);
  };

  return (
    <div>
      <label className="font-semibold">Interview Time Slots</label>
      {timeSlots.map((slot, i) => (
        <div key={i} className="flex gap-2 my-1">
          <input
            type="datetime-local"
            value={slot}
            onChange={(e) => updateSlot(i, e.target.value)}
            className="border p-1 rounded"
          />
          <button onClick={() => removeSlot(i)} className="text-red-500">✖</button>
        </div>
      ))}
      <button onClick={addSlot} className="mt-2 text-blue-500">+ Add Slot</button>
    </div>
  );
}

export default function RecruiterDashboard() {
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [weights, setWeights] = useState({});
  const [timeSlotsMap, setTimeSlotsMap] = useState({});

  useEffect(() => {
    axios.get("/api/job_descriptions").then((res) => {
      setJobDescriptions(res.data);
    });
  }, []);

  const handleWeightChange = (jdId, key, value) => {
    setWeights({
      ...weights,
      [jdId]: {
        ...weights[jdId],
        [key]: Number(value),
      },
    });
  };

  const handleSave = (jdId) => {
    const payload = {
      jd_id: jdId,
      weights: weights[jdId] || {},
      time_slots: timeSlotsMap[jdId] || [],
    };
    axios.post("/api/set_weights_and_slots", payload).then((res) => {
      console.log("Saved:", res.data);
    });
  };

  const handleFindCandidates = (jdId) => {
    axios.post("/api/match_candidates", { jd_id: jdId }).then((res) => {
      console.log("Matching triggered:", res.data);
    });
  };

  return (
    <div className="p-4 grid gap-6">
      <h1 className="text-2xl font-bold mb-4">Recruiter Dashboard</h1>
      {jobDescriptions.map((jd) => (
        <Card key={jd.id} className="p-4 shadow-md">
          <CardContent>
            <h2 className="text-xl font-semibold mb-2">{jd.title}</h2>
            <div className="grid grid-cols-2 gap-4">
              {['skills', 'experience', 'education', 'location'].map((field) => (
                <div key={field}>
                  <label className="block font-medium">{field} weight</label>
                  <input
                    type="number"
                    className="border p-1 rounded w-full"
                    value={weights[jd.id]?.[field] || ""}
                    onChange={(e) => handleWeightChange(jd.id, field, e.target.value)}
                  />
                </div>
              ))}
            </div>
            <div className="mt-4">
              <TimeSlotsInput
                timeSlots={timeSlotsMap[jd.id] || []}
                setTimeSlots={(newSlots) => setTimeSlotsMap({ ...timeSlotsMap, [jd.id]: newSlots })}
              />
            </div>
            <div className="flex gap-4 mt-4">
              <Button onClick={() => handleSave(jd.id)}>Save</Button>
              <Button onClick={() => handleFindCandidates(jd.id)} variant="secondary">Find Candidates</Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
