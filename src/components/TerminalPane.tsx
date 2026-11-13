import { useEffect, useRef } from 'react';
import {
  CheckCircle2,
  XCircle,
  Terminal as TerminalIcon,
  Lightbulb,
  Eye,
  RotateCcw,
  SkipForward,
  Play,
  ArrowRight,
} from 'lucide-react';
import type { ScenarioItem, TerminalEntry } from '../types';

interface TerminalPaneProps {
  scenario: ScenarioItem;
  command: string;
  onCommandChange: (val: string) => void;
  onSubmitGrade: () => void;
  onRunSandbox: () => void;
  onCycleHint: () => void;
  onRevealSolution: () => void;
  onResetScenario: () => void;
  onNextScenario: () => void;
  onClearTerminal: () => void;
  history: string[];
  historyIndex: number;
  onHistoryNavigate: (nextIndex: number, value: string) => void;
  entries: TerminalEntry[];
  hintLevel: number;
  revealedSolution: string | null;
  isExecuting: boolean;
  isCurrentPassed: boolean;
}

export function TerminalPane({
  scenario,
  command,
  onCommandChange,
  onSubmitGrade,
  onRunSandbox,
  onCycleHint,
  onRevealSolution,
  onResetScenario,
  onNextScenario,
  onClearTerminal,
  history,
  historyIndex,
  onHistoryNavigate,
  entries,
  hintLevel,
  revealedSolution,
  isExecuting,
  isCurrentPassed,
}: TerminalPaneProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [entries, hintLevel, revealedSolution]);

  useEffect(() => {
    inputRef.current?.focus();
  }, [scenario.id]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && e.shiftKey) {
      e.preventDefault();
      if (!isExecuting) onRunSandbox();
      return;
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      if (!isExecuting) onSubmitGrade();
      return;
    }
    if (e.key === 'Tab') {
      e.preventDefault();
      onCycleHint();
      return;
    }
    if (e.key.toLowerCase() === 'l' && e.ctrlKey) {
      e.preventDefault();
      onClearTerminal();
      return;
    }
    if (e.key === 'ArrowUp') {
      if (history.length === 0) return;
      e.preventDefault();
      const nextIdx = historyIndex > 0 ? historyIndex - 1 : 0;
      onHistoryNavigate(nextIdx, history[nextIdx] ?? '');
      return;
    }
    if (e.key === 'ArrowDown') {
      if (history.length === 0) return;
      e.preventDefault();
      if (historyIndex < history.length - 1) {
        const nextIdx = historyIndex + 1;
        onHistoryNavigate(nextIdx, history[nextIdx] ?? '');
      } else {
        onHistoryNavigate(history.length, '');
      }
    }
  };

  const hints = scenario.hints ?? [];
  const activeHint = hintLevel > 0 && hints.length > 0 ? hints[Math.min(hintLevel - 1, hints.length - 1)] : null;
  const setupFileNames = Object.keys(scenario.setup_files ?? {});

  return (
    <div className="flex flex-col rounded-lg border border-slate-800 bg-[#111622] overflow-hidden h-full">
      {/* Scenario Brief Header */}
      <div className="p-5 sm:p-6 border-b border-slate-800 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <span className="font-medium text-slate-200">{scenario.category}</span>
            <span aria-hidden="true">·</span>
            <span>{scenario.difficulty}</span>
            <span aria-hidden="true">·</span>
            <span className="font-mono tabular-nums text-slate-400">{scenario.id}</span>
          </div>
          {isCurrentPassed && (
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
              <span>Completed</span>
            </div>
          )}
        </div>

        <h1 className="text-lg sm:text-xl font-semibold text-white tracking-tight text-balance">
          {scenario.title}
        </h1>

        <p className="text-sm text-slate-300 leading-relaxed max-w-[75ch]">
          {scenario.description}
        </p>

        {setupFileNames.length > 0 && (
          <div className="pt-1 text-xs text-slate-400 font-mono">
            Workspace files: <span className="text-slate-200">{setupFileNames.join(', ')}</span>
          </div>
        )}

        {(activeHint || revealedSolution) && (
          <div className="pt-2 space-y-2">
            {activeHint && (
              <div className="rounded-md border border-amber-500/30 bg-amber-950/20 px-3.5 py-2.5 text-xs text-amber-200 flex items-start gap-2.5">
                <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-amber-300 mr-2 tabular-nums">
                    Hint {hintLevel}/{hints.length}:
                  </span>
                  <span className="font-mono">{activeHint}</span>
                </div>
              </div>
            )}
            {revealedSolution && (
              <div className="rounded-md border border-[#E02424]/40 bg-[#E02424]/10 px-3.5 py-2.5 text-xs text-slate-100 flex items-start justify-between gap-3">
                <div className="flex items-start gap-2.5 min-w-0">
                  <Eye className="w-4 h-4 text-[#F87171] shrink-0 mt-0.5" />
                  <div className="min-w-0">
                    <span className="font-semibold text-[#FCA5A5] mr-2">Solution:</span>
                    <code className="font-mono text-white break-all">{revealedSolution}</code>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    onCommandChange(revealedSolution);
                    inputRef.current?.focus();
                  }}
                  className="text-xs font-medium text-slate-200 hover:text-white underline underline-offset-2 shrink-0"
                >
                  Copy to prompt
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Interactive Terminal Output */}
      <div
        ref={scrollRef}
        onClick={() => inputRef.current?.focus()}
        className="flex-1 min-h-[290px] max-h-[440px] overflow-y-auto bg-[#090C11] p-4 sm:p-5 font-mono text-xs sm:text-[13px] leading-relaxed space-y-4 terminal-scroll cursor-text"
      >
        {entries.length === 0 ? (
          <div className="text-slate-500 space-y-1.5">
            <p>RHEL 9/10 sandbox ready. Type your command below and press Enter to submit.</p>
            <p className="text-slate-600">
              Shortcuts: Enter to grade · Shift+Enter to test in sandbox · Tab for hint · Up/Down for history · Ctrl+L to clear
            </p>
          </div>
        ) : (
          entries.map((entry) => (
            <div key={entry.id} className="space-y-1.5">
              <div className="flex items-baseline gap-2 text-slate-100 break-all">
                <span className="text-emerald-400 font-semibold shrink-0 select-none">
                  [root@rhel-sandbox scratch]$
                </span>
                <span className="text-white">{entry.command}</span>
              </div>

              {entry.stdout && (
                <pre className="text-slate-300 whitespace-pre-wrap break-words pl-3 border-l border-slate-800">
                  {entry.stdout}
                </pre>
              )}

              {entry.stderr && (
                <pre className="text-rose-300 whitespace-pre-wrap break-words pl-3 border-l border-rose-900/60">
                  {entry.stderr}
                </pre>
              )}

              <div className="flex items-center gap-2 pt-0.5">
                {entry.mode === 'sandbox' ? (
                  <span className="inline-flex items-center gap-1.5 text-xs font-medium text-sky-300">
                    <TerminalIcon className="w-3.5 h-3.5" />
                    <span>SANDBOX · {entry.feedback}</span>
                  </span>
                ) : entry.passed ? (
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>PASS · {entry.feedback}</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-rose-400">
                    <XCircle className="w-3.5 h-3.5" />
                    <span>FAIL · {entry.feedback}</span>
                  </span>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Active Bash Command Input Prompt */}
      <div className="border-t border-slate-800 bg-[#0B0E14] px-4 sm:px-5 py-3 flex items-center gap-2 font-mono text-xs sm:text-[13px]">
        <span className="text-emerald-400 font-semibold shrink-0 select-none">
          [root@rhel-sandbox scratch]$
        </span>
        <input
          ref={inputRef}
          type="text"
          value={command}
          onChange={(e) => onCommandChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isExecuting}
          placeholder="Type RHEL command here..."
          aria-label="Linux command input"
          autoComplete="off"
          autoCapitalize="off"
          spellCheck={false}
          className="flex-1 bg-transparent text-white placeholder:text-slate-600 focus:outline-none min-w-0"
        />
      </div>

      {/* Workbench Action Bar */}
      <div className="border-t border-slate-800 bg-[#111622] px-4 sm:px-5 py-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={onSubmitGrade}
            disabled={isExecuting || !command.trim()}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-[#E02424] hover:bg-[#C81E1E] disabled:opacity-40 disabled:pointer-events-none text-xs font-semibold text-white transition-colors whitespace-nowrap shrink-0"
          >
            <Play className="w-3.5 h-3.5" />
            <span>{isExecuting ? 'Running...' : 'Submit Command'}</span>
          </button>

          <button
            type="button"
            onClick={onRunSandbox}
            disabled={isExecuting || !command.trim()}
            title="Run command inside the scratch directory without affecting score or streak (Shift+Enter)"
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-md border border-slate-700 hover:border-slate-600 bg-[#161D2C] hover:bg-[#1D2537] disabled:opacity-40 disabled:pointer-events-none text-xs font-medium text-slate-200 transition-colors whitespace-nowrap shrink-0"
          >
            <TerminalIcon className="w-3.5 h-3.5" />
            <span>Test in Sandbox</span>
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={onCycleHint}
            disabled={hints.length === 0}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-md border border-slate-800 hover:border-slate-700 text-xs font-medium text-slate-300 hover:text-white disabled:opacity-40 transition-colors whitespace-nowrap shrink-0"
          >
            <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
            <span>Hint{hints.length > 0 ? ` (${hintLevel}/${hints.length})` : ''}</span>
          </button>

          <button
            type="button"
            onClick={onRevealSolution}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-md border border-slate-800 hover:border-slate-700 text-xs font-medium text-slate-300 hover:text-white transition-colors whitespace-nowrap shrink-0"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>{revealedSolution ? 'Hide Solution' : 'Show Solution'}</span>
          </button>

          <button
            type="button"
            onClick={onResetScenario}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-md border border-slate-800 hover:border-slate-700 text-xs font-medium text-slate-300 hover:text-white transition-colors whitespace-nowrap shrink-0"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>

          <button
            type="button"
            onClick={onNextScenario}
            className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-md text-xs font-semibold transition-colors whitespace-nowrap shrink-0 ${
              isCurrentPassed
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white'
                : 'border border-slate-700 hover:border-slate-600 text-slate-200 hover:text-white'
            }`}
          >
            <span>{isCurrentPassed ? 'Next Drill' : 'Skip'}</span>
            {isCurrentPassed ? <ArrowRight className="w-3.5 h-3.5" /> : <SkipForward className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>
    </div>
  );
}
