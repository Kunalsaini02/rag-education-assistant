import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: question }),
      });

      const data = await response.json();
      setAnswer(data.answer || "No answer returned.");
    } catch (err) {
      setError("Unable to reach backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">📘 RAG Education Assistant</h1>

      <textarea
        className="textarea"
        placeholder="Ask a question from your notes..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        className="button"
        onClick={askQuestion}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && <p className="error">{error}</p>}

      {answer && (
        <div className="answer-box">
          <h3>Answer</h3>

          {answer.split("\n").map((line, index) => {
            // bullet points (1., 2., -, *)
            if (/^\d+\./.test(line) || line.startsWith("-")) {
              return (
                <li key={index} className="answer-bullet">
                  {line.replace(/^\d+\.\s*/, "")}
                </li>
              );
            }

            // headings
            if (line.length < 60 && line.endsWith(":")) {
              return (
                <h4 key={index} className="answer-heading">
                  {line}
                </h4>
              );
            }

            // normal text
            return (
              <p key={index} className="answer-text">
                {line}
              </p>
            );
          })}
        </div>
      )}



      
    </div>
  );
}

export default App;
