"use client";
import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [claims, setClaims] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    setClaims(data.claims);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-100 p-10">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-4 text-center">
          AI Hallucination Checker
        </h1>

        <textarea
          className="w-full border p-3 rounded mb-4"
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste AI-generated text here..."
        />

        <button
          onClick={handleVerify}
          disabled={loading}
          className="w-full bg-black text-white py-2 rounded mb-6"
        >
          {loading ? "Analyzing..." : "Verify Claims"}
        </button>

        {claims.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold mb-3">Verification Results</h2>

            <ul className="space-y-3">
              {claims.map((item, index) => (
                <li
                  key={index}
                  className={`border p-3 rounded ${
                    item.status === "verified"
                      ? "bg-green-50 border-green-400"
                      : "bg-red-50 border-red-400"
                  }`}
                >
                  <p className="font-medium">{item.claim}</p>
                  <p className="text-sm mt-1">
                    Status:{" "}
                    <span className="font-semibold">
                      {item.status.toUpperCase()}
                    </span>
                  </p>
                  <p className="text-sm">
                    Confidence: {(item.confidence * 100).toFixed(0)}%
                  </p>

                  {item.citations && item.citations.length > 0 && (
                    <div className="mt-2">
                      <p className="text-sm font-semibold">Citations:</p>
                      <ul className="list-disc list-inside text-sm text-blue-600">
                        {item.citations.map((cite: any, i: number) => (
                          <li key={i}>
                            <a
                              href={cite.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="underline"
                            >
                              {cite.title}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}
