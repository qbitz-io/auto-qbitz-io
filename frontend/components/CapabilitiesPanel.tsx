interface CapabilitiesPanelProps {
  capabilities: any;
}

export function CapabilitiesPanel({ capabilities }: CapabilitiesPanelProps) {
  if (!capabilities) return null;

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <h2 className="text-2xl font-semibold mb-4">System Capabilities</h2>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {capabilities.capabilities.map((cap: any, idx: number) => (
          <div
            key={idx}
            className={`p-3 rounded border ${
              cap.implemented
                ? "bg-green-900/20 border-green-800"
                : "bg-yellow-900/20 border-yellow-800"
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      cap.implemented ? "bg-green-500" : "bg-yellow-500"
                    }`}
                  ></div>
                  <div className="font-medium">{cap.name}</div>
                </div>
                <div className="text-sm text-gray-400 mt-1">
                  {cap.description}
                </div>
                {cap.file_path && (
                  <div className="text-xs text-gray-500 mt-1 font-mono">
                    {cap.file_path}
                  </div>
                )}
              </div>
              <div
                className={`text-xs px-2 py-1 rounded ${
                  cap.implemented
                    ? "bg-green-800 text-green-200"
                    : "bg-yellow-800 text-yellow-200"
                }`}
              >
                {cap.implemented ? "✓ Done" : "Pending"}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-800 text-sm text-gray-400">
        {capabilities.implemented} of {capabilities.total} capabilities
        implemented
      </div>
    </div>
  );
}
