
"use client";

import React, { useState, useEffect, useRef } from "react";

interface Message {
  from: "user" | "bot";
  text: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendQuestion(question: string) {
    setLoading(true);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      if (data.answer) {
        setMessages((prev) => [...prev, { from: "bot", text: data.answer }]);
      } else {
        setMessages((prev) => [...prev, { from: "bot", text: "No answer :(" }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { from: "bot", text: "Error fetching answer" }]);
    }
    setLoading(false);
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { from: "user", text: input }]);
    sendQuestion(input);
    setInput("");
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#121212",
        boxShadow: "0 0 15px rgba(255,0,0,0.8)",
      }}
    >
   
      <header
        style={{
          display: "flex",
          alignItems: "center",
          padding: "15px 25px",
          backgroundColor: "#afafafff", 
          gap: 5,
        }}
      >
        <img
          src="/f1gpt.png"
          alt="F1 GPT Logo"
          style={{
            height: 70,
            width: 320,
           //* objectFit:"contain",*/
            userSelect: "none",
          }}
        />
      </header>

  
      <main
        style={{
          flexGrow: 1,
          padding: 20,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 12,
          backgroundColor: "#181818",
        }}
      >
        {messages.length === 0 && (
          <p style={{ color: "#bbb", textAlign: "center", marginTop: 50 }}>
            Ask me anything about Formula 1!
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              alignSelf: msg.from === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.from === "user" ? "#E10600" : "#333",
              color: "#fff",
              padding: "10px 16px",
              borderRadius: 20,
              maxWidth: "70%",
              fontSize: 16,
              whiteSpace: "pre-wrap",
              boxShadow: msg.from === "user" ? "0 0 8px rgba(225,16,0,0.8)" : "none",
            }}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </main>

      <form
        onSubmit={handleSubmit}
        style={{
        display: "flex",
        padding: "15px 20px",
        borderTop: "1px solid #333",
        backgroundColor: "#121212",
        gap: 10,
        boxSizing: "border-box",
  }}
      >
        <input
          type="text"
          placeholder="Ask your F1 question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          style={{
            flexGrow: 1,
            padding: "12px 20px",
            borderRadius: 25,
            border: "none",
            fontSize: 16,
            outline: "none",
            backgroundColor: "#222",
            color: "#fff",
            boxSizing: "border-box",
            marginLeft:"40px",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            backgroundColor: "#E10600",
            color: "#fff",
            border: "none",
            borderRadius: 25,
            padding: "0 20px",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: 16,
          }}
        >
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}
