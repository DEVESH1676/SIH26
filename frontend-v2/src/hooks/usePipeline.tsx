import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import type { PipelineState, PipelineAction, PipelineStage } from '../types/pipeline';

const initialState: PipelineState = {
  stage: 'idle',
  progress: 0,
  logs: [],
  results: {},
};

const PipelineContext = createContext<{
  state: PipelineState;
  startPipeline: (title: string, description: string) => Promise<any>;
  reset: () => void;
} | undefined>(undefined);

export function pipelineReducer(state: PipelineState, action: PipelineAction): PipelineState {
  switch (action.type) {
    case 'START':
      return { ...initialState, stage: 'classification', logs: ['Initiating pipeline...'] };
    case 'UPDATE_PROGRESS':
      return { ...state, progress: action.payload };
    case 'ADD_LOG':
      return { ...state, logs: [...state.logs, action.payload] };
    case 'SET_RESULT':
      const nextStageMap: Record<string, PipelineStage> = {
        classification: 'triage',
        triage: 'rag',
        rag: 'resolution',
        resolution: 'judge',
        judge: 'complete'
      };
      return {
        ...state,
        results: { ...state.results, [action.payload.key]: action.payload.data },
        stage: nextStageMap[action.payload.key] || state.stage
      };
    case 'COMPLETE':
      return { ...state, stage: 'complete', progress: 1 };
    case 'ERROR':
      return { ...state, stage: 'error', error: action.payload };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

export const PipelineProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(pipelineReducer, initialState);

  const startPipeline = useCallback(async (title: string, description: string) => {
    dispatch({ type: 'START' });

    const ctrl = new AbortController();
    
    try {
      await fetchEventSource('/api/pipeline/stream', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({ title, description, enable_resolution: true }),
        signal: ctrl.signal,
        async onopen(response) {
          if (response.ok && response.headers.get('content-type')?.includes('text/event-stream')) {
            return; // Everything is fine
          } else {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown backend error' }));
            const errorMessage = typeof errorData.detail === 'string' 
              ? errorData.detail 
              : JSON.stringify(errorData.detail);
            
            dispatch({ type: 'ERROR', payload: `Backend Error: ${errorMessage}` });
            throw new Error(`Expected stream, got ${response.status}: ${errorMessage}`);
          }
        },
        onmessage(msg) {
          if (msg.event === 'status') {
            let data = JSON.parse(msg.data);
            if (typeof data === 'string') data = JSON.parse(data);
            if (data.message) dispatch({ type: 'ADD_LOG', payload: data.message });
            if (data.progress) dispatch({ type: 'UPDATE_PROGRESS', payload: data.progress });
          } else if (msg.event === 'result') {
            let data = JSON.parse(msg.data);
            if (typeof data === 'string') data = JSON.parse(data);
            dispatch({ type: 'SET_RESULT', payload: { key: data.type, data: data.payload } });
          } else if (msg.event === 'done') {
            dispatch({ type: 'COMPLETE' });
          }
        },
        onerror(err) {
          dispatch({ type: 'ERROR', payload: 'Connection lost. Retrying...' });
          throw err;
        }
      });
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        dispatch({ type: 'ERROR', payload: err.message });
      }
    }

    return () => ctrl.abort();
  }, []);

  return (
    <PipelineContext.Provider value={{ state, startPipeline, reset: () => dispatch({ type: 'RESET' }) }}>
      {children}
    </PipelineContext.Provider>
  );
};

export const usePipeline = () => {
  const context = useContext(PipelineContext);
  if (context === undefined) {
    throw new Error('usePipeline must be used within a PipelineProvider');
  }
  return context;
};
