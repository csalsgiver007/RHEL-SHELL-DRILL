import { CheckCircle2, RotateCcw, SlidersHorizontal, SkipForward, Eye } from 'lucide-react';
import type { QuestionOutcome } from '../types';

interface SessionSummaryProps {
  score: number;
  accuracy: number;
  maxStreak: number;
  outcomes: QuestionOutcome[];
  onRestartSame: () => void;
  onConfigureNew: () => void;
  onReviewQuestion: (index: number) => void;
}

export function SessionSummary({
  score,
  accuracy,
  maxStreak,
  outcomes,
  onRestartSame,
  onConfigureNew,
  onReviewQuestion,
}: SessionSummaryProps) {
  const passedCount = outcomes.filter((o) => o.status === 'passed').length;

  return (
    <div className="max-w-3xl mx-auto rounded-lg border border-slate-800 bg-[#111622] p-6 sm:p-8 space-y-6">
      <div className="space-y-1.5 border-b border-slate-800 pb-5">
        <p className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
          <CheckCircle2 className="w-4 h-4" />
          <span>Session Complete</span>
        </p>
        <h1 className="text-2xl font-semibold text-white tracking-tight">
          Practice Session Summary
        </h1>
        <p className="text-sm text-slate-400">
          Completed {passedCount} of {outcomes.length} drills in this session.
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 border-b border-slate-800 pb-6">
        <div>
          <p className="text-xs text-slate-400">Final Score</p>
          <p className="text-2xl font-semibold text-white font-mono tabular-nums mt-1">
            {score.toLocaleString()}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Accuracy</p>
          <p className="text-2xl font-semibold text-emerald-400 font-mono tabular-nums mt-1">
            {accuracy}%
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Best Streak</p>
          <p className="text-2xl font-semibold text-amber-400 font-mono tabular-nums mt-1">
            {maxStreak}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Drills Passed</p>
          <p className="text-2xl font-semibold text-white font-mono tabular-nums mt-1">
            {passedCount}/{outcomes.length}
          </p>
        </div>
      </div>

      <div className="space-y-3">
        <h2 className="text-sm font-semibold text-white">Drill Breakdown</h2>
        <div className="max-h-72 overflow-y-auto divide-y divide-slate-800/70 border border-slate-800 rounded-md bg-[#0B0E14] terminal-scroll">
          {outcomes.map((o, idx) => (
            <button
              key={`${o.scenarioId}-${idx}`}
              type="button"
              onClick={() => onReviewQuestion(idx)}
              className="w-full px-4 py-2.5 flex items-center justify-between gap-4 text-left hover:bg-[#121826] transition-colors"
            >
              <div className="min-w-0">
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <span className="font-mono tabular-nums">{o.scenarioId}</span>
                  <span aria-hidden="true">·</span>
                  <span>{o.category}</span>
                </div>
                <p className="text-xs font-medium text-slate-200 truncate mt-0.5">{o.title}</p>
              </div>
              <div className="shrink-0 text-xs font-medium">
                {o.status === 'passed' && (
                  <span className="inline-flex items-center gap-1 text-emerald-400">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Pass</span>
                  </span>
                )}
                {o.status === 'skipped' && (
                  <span className="inline-flex items-center gap-1 text-slate-400">
                    <SkipForward className="w-3.5 h-3.5" />
                    <span>Skipped</span>
                  </span>
                )}
                {o.status === 'revealed' && (
                  <span className="inline-flex items-center gap-1 text-amber-400">
                    <Eye className="w-3.5 h-3.5" />
                    <span>Solution Viewed</span>
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3 pt-2">
        <button
          type="button"
          onClick={onRestartSame}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md bg-[#E02424] hover:bg-[#C81E1E] text-xs font-semibold text-white transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Start Another Session</span>
        </button>

        <button
          type="button"
          onClick={onConfigureNew}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 hover:text-white transition-colors"
        >
          <SlidersHorizontal className="w-3.5 h-3.5" />
          <span>Change Topic or Count</span>
        </button>
      </div>
    </div>
  );
}
