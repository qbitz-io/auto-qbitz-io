interface BuildStepsPanelProps {
  buildSteps: any;
}

export function BuildStepsPanel({ buildSteps }: BuildStepsPanelProps) {
  if (!buildSteps) return null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-900/20 border-green-800 text-green-200";
      case "running":
        return "bg-blue-900/20 border-blue-800 text-blue-200";
      case "failed":
        return "bg-red-900/20 border-red-800 text-red-200";
      default:
        return "bg-gray-800 border-gray-700 text-gray-300";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return "✓";
      case "running":
        return "⟳";
      case "failed":
        return "✗";
      default:
        return "○";
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <h2 className="text-2xl font-semibold mb-4">Recent Build Steps</h2>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {buildSteps.steps.map((step: any, idx: number) => (
          <div
            key={idx}
            className={`p-3 rounded border ${getStatusColor(step.status)}`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm">
                    {getStatusIcon(step.status)}
                  </span>
                  <span className="font-medium text-sm">{step.agent}</span>
                  <span className="text-xs text-gray-500">
                    {new Date(step.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="text-sm mt-1">{step.action}</div>
                {step.result && (
                  <div className="text-xs text-gray-400 mt-1 truncate">
                    {step.result.substring(0, 100)}
                    {step.result.length > 100 ? "..." : ""}
                  </div>
                )}
                {step.error && (
                  <div className="text-xs text-red-400 mt-1">{step.error}</div>
                )}
              </div>
              <div
                className={`text-xs px-2 py-1 rounded ${
                  step.status === "completed"
                    ? "bg-green-800"
                    : step.status === "running"
                    ? "bg-blue-800"
                    : step.status === "failed"
                    ? "bg-red-800"
                    : "bg-gray-700"
                }`}
              >
                {step.status}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-800 text-sm text-gray-400">
        Showing {buildSteps.steps.length} of {buildSteps.total} total steps
      </div>
    </div>
  );
}
