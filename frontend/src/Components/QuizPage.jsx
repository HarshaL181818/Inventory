import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function QuizPage() {
  const { email, job_id } = useParams();
  const [quiz, setQuiz] = useState([]);

  useEffect(() => {
    axios.get(`/api/get_candidate_quiz/${email}/${job_id}`).then(res => {
      if (res.data.success) setQuiz(res.data.quiz);
    });
  }, [email, job_id]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Quiz for {email}</h2>
      {quiz.map((q, idx) => (
        <div key={idx} className="mb-4">
          <p className="font-semibold">{idx + 1}. {q.question}</p>
          <ul>
            {q.options.map((opt, i) => (
              <li key={i}><input type="radio" name={`q${idx}`} /> {opt}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
