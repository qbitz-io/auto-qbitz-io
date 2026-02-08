"use client";

import { useState, useEffect } from "react";

interface Approval {
  id: string;
  file_path: string;
  reason: string;
  requested_at: string;
  status: string;
  content: string;
}

const API_BASE = "http://localhost:8000";

export function ApprovalsPanel() {
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [acting, setActing] = useState<string | null>(null);

  const fetchApprovals = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/approvals?status=all`, {
        mode: "cors",
      });
      if (res.ok) {
        const data = await res.json();
        setApprovals(data.approvals);
      }
    } catch {
      // silently retry on next poll
    }
  };

  useEffect(() => {
    fetchApprovals();
    const interval = setInterval(fetchApprovals, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleApprove = async (id: string) => {
    setActing(id);
    try {
      const res = await fetch(`${API_BASE}/api/approvals/${id}/approve`, {
        method: "POST",
        mode: "cors",
      });
      if (res.ok) {
        await fetchApprovals();
      }
    } catch {
      alert("Failed to approve change.");
    } finally {
      setActing(null);
    }
  };

  const handleDeny = async (id: string) => {
    setActing(id);
    try {
      const res = await fetch(`${API_BASE}/api/approvals/${id}/deny`, {
        method: "POST",
        mode: "cors",
      });
      if (res.ok) {
        await fetchApprovals();
      }
    } catch {
      alert("Failed to deny change.");
    } finally {
      setActing(null);
    }
  };

  const pending = approvals.filter((a) => a.status === "pending");
  const resolved = approvals.filter((a) => a.status !== "pending");

  const statusBadge = (status: string) => {
    switch (status) {
      case "pending":
        return "bg-yellow-600 text-yellow-100";
      case "approved":
        return "bg-green-700 text-green-100";
      case "denied":
        return "bg-red-700 text-red-100";
      default:
        return "bg-gray-600 text-gray-100";
    }
  };

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    return `${hours}h ago`;
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold">
          Approvals
          {pending.length > 0 && (
            <span className="ml-2 text-sm bg-yellow-600 text-yellow-100 px-2 py-0.5 rounded-full">
              {pending.length} pending
            </span>
          )}
        </h2>
      </div>

      {approvals.length === 0 && (
        <p className="text-gray-500 text-sm">
          No approval requests yet. When Auto tries to modify a protected core
          file, it will appear here for your review.
        </p>
      )}

      {/* Pending approvals first */}
      {pending.map((a) => (
        <div
          key={a.id}
          className="mb-3 border border-yellow-700 rounded-lg p-4 bg-gray-800"
        >
          <div className="flex items-center justify-between mb-2">
            <div>
              <span
                className={`text-xs px-2 py-0.5 rounded ${statusBadge(a.status)}`}
              >
                {a.status.toUpperCase()}
              </span>
              <span className="ml-2 text-sm text-gray-400">
                {timeAgo(a.requested_at)}
              </span>
            </div>
            <span className="text-xs text-gray-500 font-mono">{a.id}</span>
          </div>

          <p className="text-sm font-mono text-blue-400 mb-1">{a.file_path}</p>
          <p className="text-sm text-gray-400 mb-3">{a.reason}</p>

          {/* Toggle to show proposed content */}
          <button
            onClick={() => setExpanded(expanded === a.id ? null : a.id)}
            className="text-xs text-blue-400 hover:text-blue-300 mb-3 block"
          >
            {expanded === a.id ? "Hide proposed changes" : "View proposed changes"}
          </button>

          {expanded === a.id && (
            <pre className="text-xs bg-gray-950 text-gray-300 p-3 rounded mb-3 max-h-64 overflow-auto whitespace-pre-wrap">
              {a.content}
            </pre>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => handleApprove(a.id)}
              disabled={acting === a.id}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded text-sm font-medium"
            >
              {acting === a.id ? "..." : "Approve"}
            </button>
            <button
              onClick={() => handleDeny(a.id)}
              disabled={acting === a.id}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white rounded text-sm font-medium"
            >
              {acting === a.id ? "..." : "Deny"}
            </button>
          </div>
        </div>
      ))}

      {/* Resolved approvals (collapsed) */}
      {resolved.length > 0 && (
        <div className="mt-4">
          <p className="text-xs text-gray-500 mb-2">
            Recent ({resolved.length})
          </p>
          {resolved.slice(-5).reverse().map((a) => (
            <div
              key={a.id}
              className="flex items-center justify-between py-1.5 text-sm border-b border-gray-800 last:border-0"
            >
              <span className="font-mono text-gray-400 text-xs truncate mr-2">
                {a.file_path}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded ${statusBadge(a.status)}`}
              >
                {a.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
