import React, { createContext, useContext, useState } from "react";

export const PipelineContext = createContext<any>(null);

export const PipelineProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [pipelineState, setPipelineState] = useState<any>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [loading, setLoading] = useState(false);

  const initializePipeline = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/pipeline/initialize");
      const data = await response.json();
      setPipelineState(data);
      setIsInitialized(true);
    } catch (error) {
      console.error("Pipeline initialization error:", error);
    } finally {
      setLoading(false);
    }
  };

  const resetPipeline = () => {
    setPipelineState(null);
    setIsInitialized(false);
  };

  return (
    <PipelineContext.Provider
      value={{
        pipelineState,
        isInitialized,
        loading,
        initializePipeline,
        resetPipeline,
      }}
    >
      {children}
    </PipelineContext.Provider>
  );
};

export default PipelineProvider;
