import { useEffect, useState } from "react";

function App() {
  const [isReady, setIsReady] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const checkBackend = async () => {
      try {
        const response = await fetch("/health");
        if (!response.ok) throw new Error("Backend not ready");

        if (!cancelled) {
          setIsReady(true);
          setHasError(false);
        }
      } catch {
        if (!cancelled) {
          setHasError(true);
        }
      }
    };

    checkBackend();
  }, []);

  if (!isReady) {
    return (
      <div style={{ padding: 24 }}>
        {hasError ? "Server is unavailable!" : "Connecting to server..."}
      </div>
    );
  }

  return (
    <div>
      {/* основное приложение */}
      <h1>App is ready</h1>
    </div>
  );
}

export default App;
