"use client";

import React, { useState, useEffect, useRef } from "react";

interface Message {
  id: string;
  sender: "user" | "system";
  text: string;
}

function generateSessionId() {
  return `session-${Math.random().toString(36).substr(2, 9)}`;
}

export function ChatInterface({ initialSessionId }: { initialSessionId?: string }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string>(initialSessionId || "");

  // Scroll chat to bottom on new message
  const chatEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Load or create session ID and load message history on mount
  useEffect(() => {
    let storedSessionId = initialSessionId || localStorage.getItem("chatSessionId");
    if (!storedSessionId) {
      storedSessionId = generateSessionId();
      localStorage.setItem("chatSessionId", storedSessionId);
    }
    setSessionId(storedSessionId);

    // Load message history from backend
    async function loadHistory() {
      try {
        const response = await fetch(`http://localhost:8000/api/chat/${storedSessionId}`, {
          method: "GET",
          mode: "cors",
        });
        if (response.ok) {
          const data = await response.json();
          // Expecting data.history as array of {role, content}
          if (Array.isArray(data.history)) {
            const loadedMessages = data.history.map((msg: any, idx: number) => ({
              id: `msg-${idx}`,
              sender: msg.role === "user" ? "user" : "system",
              text: msg.content,
            }));
            setMessages(loadedMessages);
          }
        }
      } catch (err) {
        // Ignore load errors
      }
    }
    loadHistory();
  }, [initialSessionId]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setError(null);

    // Add user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: input.trim(),
    };
    setMessages((msgs) => [...msgs, userMessage]);

    setIsSending(true);
    setInput("");

    try {
      // Prepare chat history for context
      const chatHistory = messages
        .concat(userMessage)
        .map((msg) => ({ role: msg.sender, content: msg.text }));

      // Send POST request with JSON body {task: message, context: {chat_history}, session_id}
      const response = await fetch("http://localhost:8000/api/task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ task: userMessage.text, context: { chat_history: chatHistory }, session_id: sessionId }),
        mode: "cors",
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();

      // Add system message with the output from the orchestrator
      const output = data?.result?.output || data?.result || JSON.stringify(data);
      const systemMessage: Message = {
        id: `system-${Date.now()}`,
        sender: "system",
        text: typeof output === "string" ? output : JSON.stringify(output, null, 2),
      };
      setMessages((msgs) => [...msgs, systemMessage]);
    } catch (err) {
      setError("Failed to send task request.");
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!isSending) {
        handleSend();
      }
    }
  };

  const handleNewSession = async () => {
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
    localStorage.setItem("chatSessionId", newSessionId);
    setMessages([]);
    setError(null);

    // Clear backend chat history for new session
    try {
      const response = await fetch(`http://localhost:8000/api/chat/${newSessionId}/clear`, {
        method: "POST",
        mode: "cors",
      });
      if (!response.ok) {
        throw new Error(`Failed to clear chat history: ${response.statusText}`);
      }
    } catch (err) {
      // Ignore clear errors
    }
  };

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto bg-gray-900 rounded-lg shadow-lg p-4">
      <h2 className="text-2xl font-semibold mb-4 text-white">Describe Your Build Task</h2>

      <div className="flex-1 overflow-y-auto mb-4 p-2 bg-gray-800 rounded">
        {messages.length === 0 && (
          <p className="text-gray-400">Type what you want to build and press Enter.</p>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`mb-2 max-w-[80%] whitespace-pre-wrap rounded px-3 py-2 ${
              msg.sender === "user"
                ? "bg-blue-600 text-white self-end"
                : "bg-gray-700 text-gray-200 self-start"
            }`}
            style={{ alignSelf: msg.sender === "user" ? "flex-end" : "flex-start" }}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {error && <div className="text-red-500 mb-2">Error: {error}</div>}

      <textarea
        className="w-full rounded p-2 resize-none bg-gray-700 text-white placeholder-gray-400"
        rows={3}
        placeholder="Describe what you want to build..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isSending}
        aria-label="Build task input"
      />

      <div className="flex justify-between mt-2">
        <button
          onClick={handleSend}
          disabled={isSending || !input.trim()}
          className={`px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold`}
          aria-label="Send build task"
        >
          {isSending ? "Building..." : "Send"}
        </button>

        <button
          onClick={handleNewSession}
          disabled={isSending}
          className="px-4 py-2 rounded bg-red-600 hover:bg-red-700 text-white font-semibold"
          aria-label="Start new session"
          title="Start a new chat session and clear history"
        >
          New Session
        </button>
      </div>
    </div>
  );
}
