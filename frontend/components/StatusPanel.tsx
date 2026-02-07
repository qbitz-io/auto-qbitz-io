interface StatusPanelProps {
  status: any;
}

export function StatusPanel({ status }: StatusPanelProps) {
  if (!status) return null;

  const implementedPercentage = status.total_capabilities
    ? Math.round(
        (status.implemented_capabilities / status.total_capabilities) * 100
      )
    : 0;

  return (
    <div className="lg:col-span-2 bg-gray-900 rounded-lg p-6 border border-gray-800">
      <h2 className="text-2xl font-semibold mb-4">System Status</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded p-4">
          <div className="text-gray-400 text-sm mb-1">Build Loop</div>
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                status.build_loop_running ? "bg-green-500" : "bg-gray-600"
              }`}
            ></div>
            <div className="text-xl font-semibold">
              {status.build_loop_running ? "Running" : "Idle"}
            </div>
          </div>
          {status.build_loop_running && (
            <div className="text-sm text-gray-400 mt-1">
              Iteration {status.build_loop_iteration}
            </div>
          )}
        </div>

        <div className="bg-gray-800 rounded p-4">
          <div className="text-gray-400 text-sm mb-1">Capabilities</div>
          <div className="text-2xl font-semibold">
            {status.implemented_capabilities}/{status.total_capabilities}
          </div>
          <div className="text-sm text-gray-400 mt-1">
            {implementedPercentage}% complete
          </div>
        </div>

        <div className="bg-gray-800 rounded p-4">
          <div className="text-gray-400 text-sm mb-1">Generated Files</div>
          <div className="text-2xl font-semibold">{status.total_files}</div>
        </div>

        <div className="bg-gray-800 rounded p-4">
          <div className="text-gray-400 text-sm mb-1">Build Steps</div>
          <div className="text-2xl font-semibold">{status.total_steps}</div>
        </div>
      </div>

      {status.last_updated && (
        <div className="mt-4 text-sm text-gray-400">
          Last updated: {new Date(status.last_updated).toLocaleString()}
        </div>
      )}
    </div>
  );
}
