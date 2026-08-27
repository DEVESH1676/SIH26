import { describe, it, expect } from 'vitest';
import type { PipelineState, PipelineAction } from '../src/types/pipeline';

// Copying reducer logic for testing if not exported, or we can export it from usePipeline.tsx
// For now, I'll assume we want to test the one in the file.
// Since it's not exported, I'll have to either export it or copy it.
// Exporting it is better for testing.

import { pipelineReducer } from '../src/hooks/usePipeline';

const initialState: PipelineState = {
  stage: 'idle',
  progress: 0,
  logs: [],
  results: {},
};

describe('pipelineReducer', () => {
  it('should transition to classification on START', () => {
    const action: PipelineAction = { type: 'START' };
    const state = pipelineReducer(initialState, action);
    expect(state.stage).toBe('classification');
  });

  it('should transition from classification to triage on SET_RESULT classification', () => {
    const startState = pipelineReducer(initialState, { type: 'START' });
    const action: PipelineAction = { 
      type: 'SET_RESULT', 
      payload: { key: 'classification', data: { category: 'test' } } 
    };
    const state = pipelineReducer(startState, action);
    expect(state.stage).toBe('triage');
    expect(state.results.classification).toEqual({ category: 'test' });
  });

  it('should transition from rag to resolution on SET_RESULT rag', () => {
    const prevState: PipelineState = {
      ...initialState,
      stage: 'rag'
    };
    const action: PipelineAction = { 
      type: 'SET_RESULT', 
      payload: { key: 'rag', data: { docs: [] } } 
    };
    const state = pipelineReducer(prevState, action);
    expect(state.stage).toBe('resolution');
  });
});
