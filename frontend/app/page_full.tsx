"use client";

import { useState, useEffect } from "react";
import { StatusPanel } from "@/components/StatusPanel";
import { CapabilitiesPanel } from "@/components/CapabilitiesPanel";
import { BuildStepsPanel } from "@/components/BuildStepsPanel";
import { ControlPanel } from "@/components/ControlPanel";

export default function Home() {
  const [status, setStatus] = useState<any>(null);
  const [capabilities, setCapabilities] = useState<any>(null);
  const [buildSteps, setBuildSteps] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE = typeof window !== 'undefined' && window.location.hostname.includes('manus.computer')
    ? window.location.protocol + '//' + window.location.hostname.replace('3000-', '8000-') + (window.location.port ? ':' + window.location.port : '')
    : "http://localhost:8000";

  const fetchData = async () => {
    try {
      const [statusRes, capRes, stepsRes] = await Promise.all([
        fetch(`${API_BASE}/api/status`),
        fetch(`${API_BASE}/api/capabilities`),
        fetch(`${API_BASE}/api/build-steps?limit=20`),
      ]);

      if (!statusRes.ok || !capRes.ok || !stepsRes.ok) {
        throw new Error("Failed to fetch data");
      }

      const statusData = await statusRes.json();
      const capData = await capRes.json();
      const stepsData = await stepsRes.json();

      setStatus(statusData);
      setCapabilities(capData);
      setBuildSteps(stepsData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleTriggerBuild = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/build`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ force: false }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to trigger build");
      }

      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to trigger build");
    }
  };

  const handleStopBuild = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/build/stop`, {
        method: "POST",
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to stop build");
      }

      await fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to stop build");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading system state...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
          <p className="text-gray-400">{error}</p>
          <button
            onClick={fetchData}
            className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">
            Self-Building LangChain System
          </h1>
          <p className="text-gray-400">
            Real-time monitoring and control dashboard
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <StatusPanel status={status} />
          <ControlPanel
            isRunning={status?.build_loop_running}
            onTriggerBuild={handleTriggerBuild}
            onStopBuild={handleStopBuild}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CapabilitiesPanel capabilities={capabilities} />
          <BuildStepsPanel buildSteps={buildSteps} />
        </div>
      </div>
    </main>
  );
}
