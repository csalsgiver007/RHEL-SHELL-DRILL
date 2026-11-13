export interface ScenarioItem {
  id: string;
  category: string;
  title: string;
  difficulty: 'Easy' | 'Intermediate' | 'Advanced' | string;
  description: string;
  objective: string;
  hints: string[];
  setup_files: Record<string, string>;
  setup_perms: Record<string, number>;
}

export interface SandboxFile {
  path: string;
  mode: string;
  size: number;
  isSparse: boolean;
  content: string;
}

export interface TerminalEntry {
  id: string;
  command: string;
  mode: 'grade' | 'sandbox';
  passed: boolean | null;
  stdout: string;
  stderr: string;
  exitCode: number;
  feedback: string;
  timestamp: string;
}

export interface SessionConfig {
  category: string;
  difficulty: string;
  count: number | null; // null means all matching scenarios
  shuffled: boolean;
}

export interface QuestionOutcome {
  scenarioId: string;
  title: string;
  category: string;
  difficulty: string;
  status: 'passed' | 'skipped' | 'revealed' | 'pending';
  attempts: number;
}

export type ActiveView = 'trainer' | 'curriculum' | 'cli';
