export type PipelineStage = 'idle' | 'profiling' | 'identifying_gaps' | 'matching_courses' | 'pathway_built' | 'complete' | 'error';

export interface PipelineState {
  stage: PipelineStage;
  progress: number;
  logs: string[];
  results: {
    profile?: any;
    pathway?: any;
    assessment?: any;
  };
  error?: string;
}

export type PipelineAction =
  | { type: 'START' }
  | { type: 'SET_STAGE'; payload: PipelineStage }
  | { type: 'UPDATE_PROGRESS'; payload: number }
  | { type: 'ADD_LOG'; payload: string }
  | { type: 'SET_RESULT'; payload: { key: keyof PipelineState['results']; data: any } }
  | { type: 'COMPLETE' }
  | { type: 'ERROR'; payload: string }
  | { type: 'RESET' };
