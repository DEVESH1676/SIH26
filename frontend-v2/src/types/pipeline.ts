export type PipelineStage = 'idle' | 'classification' | 'triage' | 'rag' | 'resolution' | 'judge' | 'complete' | 'error';

export interface PipelineState {
  stage: PipelineStage;
  progress: number;
  logs: string[];
  results: {
    classification?: any;
    triage?: any;
    rag?: any;
    resolution?: any;
    judge?: any;
  };
  error?: string;
}

export type PipelineAction =
  | { type: 'START' }
  | { type: 'UPDATE_PROGRESS'; payload: number }
  | { type: 'ADD_LOG'; payload: string }
  | { type: 'SET_RESULT'; payload: { key: keyof PipelineState['results']; data: any } }
  | { type: 'COMPLETE' }
  | { type: 'ERROR'; payload: string }
  | { type: 'RESET' };
