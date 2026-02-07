interface ControlPanelProps {
  isRunning: boolean;
  onTriggerBuild: () => void;
  onStopBuild: () => void;
}

export function ControlPanel({
  isRunning,
  onTriggerBuild,
  onStopBuild,
}: ControlPanelProps) {
  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <h2 className="text-2xl font-semibold mb-4">Control</h2>

      <div className="space-y-3">
        <button
          onClick={onTriggerBuild}
          disabled={isRunning}
          className={`w-full py-3 px-4 rounded font-medium transition-colors ${
            isRunning
              ? "bg-gray-700 text-gray-500 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
        >
          {isRunning ? "Build Running..." : "Trigger Build"}
        </button>

        <button
          onClick={onStopBuild}
          disabled={!isRunning}
          className={`w-full py-3 px-4 rounded font-medium transition-colors ${
            !isRunning
              ? "bg-gray-700 text-gray-500 cursor-not-allowed"
              : "bg-red-600 hover:bg-red-700 text-white"
          }`}
        >
          Stop Build
        </button>
      </div>

      <div className="mt-6 p-4 bg-gray-800 rounded text-sm">
        <div className="font-medium mb-2">Build Loop</div>
        <p className="text-gray-400">
          The build loop continuously analyzes the system, identifies missing
          components, and generates code to fill gaps. It terminates when no
          more changes are needed.
        </p>
      </div>
    </div>
  );
}
