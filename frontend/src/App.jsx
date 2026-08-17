import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  async function uploadFile() {
    if (!file) {
      setUploadMessage("Please select a PDF or DOCX file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadMessage("Uploading and indexing...");

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setUploadMessage(
        `✅ ${data.filename} indexed successfully — ${data.chunks} chunks`
      );
    } catch (error) {
      setUploadMessage(`❌ ${error.message}`);
    }
  }

  async function askQuestion() {
    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);
      setAnswer("");
      setSources([]);

      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setAnswer(`❌ ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-slate-800">
        <div className="mx-auto max-w-5xl px-6 py-8">
          <h1 className="text-3xl font-bold">
            🎓 AI University Knowledge Assistant
          </h1>

          <p className="mt-2 text-slate-400">
            Upload university documents and ask questions using RAG + Ollama.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10">
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-xl font-semibold">📄 Upload Document</h2>

          <p className="mt-2 text-sm text-slate-400">
            Supported formats: PDF and DOCX
          </p>

          <div className="mt-6 flex flex-col gap-4 md:flex-row">
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm"
            />

            <button
              onClick={uploadFile}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-500"
            >
              Upload & Index
            </button>
          </div>

          {uploadMessage && (
            <p className="mt-4 text-sm text-slate-300">
              {uploadMessage}
            </p>
          )}
        </section>

        <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-xl font-semibold">💬 Ask a Question</h2>

          <div className="mt-6 flex flex-col gap-4 md:flex-row">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askQuestion();
                }
              }}
              placeholder="What is machine learning?"
              className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-blue-500"
            />

            <button
              onClick={askQuestion}
              disabled={loading}
              className="rounded-lg bg-green-600 px-8 py-3 font-semibold hover:bg-green-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
        </section>

        {answer && (
          <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">🤖 Answer</h2>

            <div className="mt-4 whitespace-pre-wrap rounded-xl bg-slate-950 p-5 leading-7 text-slate-200">
              {answer}
            </div>
          </section>
        )}

        {sources.length > 0 && (
          <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">📚 Sources</h2>

            <div className="mt-4 space-y-3">
              {sources.map((source, index) => (
                <div
                  key={index}
                  className="rounded-lg bg-slate-950 p-4 text-sm text-slate-300"
                >
                  <span className="font-semibold">
                    Source {index + 1}:
                  </span>{" "}
                  {source.source || JSON.stringify(source)}
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;