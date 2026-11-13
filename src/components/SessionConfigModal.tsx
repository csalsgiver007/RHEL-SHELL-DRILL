import { useState } from 'react';
import { X, Shuffle, ListOrdered } from 'lucide-react';
import { CATEGORY_LIST } from '../data/cheatSheet';
import type { SessionConfig } from '../types';

interface SessionConfigModalProps {
  isOpen: boolean;
  currentConfig: SessionConfig;
  categoryCounts: Record<string, number>;
  totalCount: number;
  onClose: () => void;
  onStartSession: (config: SessionConfig) => void;
}

const PRESET_COUNTS: (number | null)[] = [10, 25, 50, null];

export function SessionConfigModal({
  isOpen,
  currentConfig,
  categoryCounts,
  totalCount,
  onClose,
  onStartSession,
}: SessionConfigModalProps) {
  const [category, setCategory] = useState(currentConfig.category);
  const [difficulty, setDifficulty] = useState(currentConfig.difficulty);
  const [count, setCount] = useState<number | null>(currentConfig.count);
  const [customCount, setCustomCount] = useState(
    currentConfig.count && !PRESET_COUNTS.includes(currentConfig.count)
      ? String(currentConfig.count)
      : '',
  );
  const [shuffled, setShuffled] = useState(currentConfig.shuffled);

  if (!isOpen) return null;

  const availableInCat = category === 'All' ? totalCount : categoryCounts[category] ?? 0;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const parsedCustom = Number.parseInt(customCount.trim(), 10);
    const resolvedCount =
      customCount.trim() !== '' && Number.isFinite(parsedCustom) && parsedCustom > 0
        ? parsedCustom
        : count;

    onStartSession({
      category,
      difficulty,
      count: resolvedCount,
      shuffled,
    });
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="session-modal-title"
    >
      <div className="w-full max-w-lg rounded-lg border border-slate-800 bg-[#111622] shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h2 id="session-modal-title" className="text-base font-semibold text-white">
            Configure Practice Session
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close session settings"
            className="p-1.5 text-slate-400 hover:text-white rounded-md hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div className="space-y-2">
            <label htmlFor="session-category" className="block text-xs font-semibold text-slate-300">
              Topic Category
            </label>
            <select
              id="session-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full rounded-md border border-slate-700 bg-[#0B0E14] px-3 py-2.5 text-sm text-slate-100 focus:border-[#E02424] focus:outline-none"
            >
              <option value="All">All Categories ({totalCount} scenarios)</option>
              {CATEGORY_LIST.map((cat) => (
                <option key={cat} value={cat}>
                  {cat} ({categoryCounts[cat] ?? 0})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <span className="block text-xs font-semibold text-slate-300">Difficulty Filter</span>
            <div className="grid grid-cols-4 gap-1.5 p-1 rounded-md bg-[#0B0E14] border border-slate-800">
              {['All', 'Easy', 'Intermediate', 'Advanced'].map((diff) => (
                <button
                  key={diff}
                  type="button"
                  onClick={() => setDifficulty(diff)}
                  className={`px-3 py-2 text-xs font-medium rounded transition-colors whitespace-nowrap ${
                    difficulty === diff
                      ? 'bg-[#1D2537] text-white'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300">Questions per Session</span>
              <span className="text-xs text-slate-400 tabular-nums">
                {availableInCat} available in topic
              </span>
            </div>
            <div className="grid grid-cols-4 gap-2">
              {PRESET_COUNTS.map((preset) => {
                const isSelected = customCount.trim() === '' && count === preset;
                return (
                  <button
                    key={String(preset)}
                    type="button"
                    onClick={() => {
                      setCount(preset);
                      setCustomCount('');
                    }}
                    className={`py-2 px-3 rounded-md border text-xs font-semibold tabular-nums transition-colors ${
                      isSelected
                        ? 'border-[#E02424] bg-[#E02424]/15 text-white'
                        : 'border-slate-800 bg-[#0B0E14] text-slate-300 hover:border-slate-700'
                    }`}
                  >
                    {preset === null ? 'All' : `${preset} Drills`}
                  </button>
                );
              })}
            </div>
            <div className="pt-1">
              <input
                type="number"
                min={1}
                max={460}
                value={customCount}
                onChange={(e) => setCustomCount(e.target.value)}
                placeholder="Or enter custom question count (e.g., 15)"
                className="w-full rounded-md border border-slate-800 bg-[#0B0E14] px-3 py-2 text-xs text-slate-100 placeholder:text-slate-500 focus:border-[#E02424] focus:outline-none tabular-nums"
              />
            </div>
          </div>

          <div className="space-y-2">
            <span className="block text-xs font-semibold text-slate-300">Question Order</span>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setShuffled(false)}
                className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-md border text-xs font-medium transition-colors ${
                  !shuffled
                    ? 'border-[#E02424] bg-[#E02424]/15 text-white'
                    : 'border-slate-800 bg-[#0B0E14] text-slate-400 hover:text-slate-200'
                }`}
              >
                <ListOrdered className="w-3.5 h-3.5" />
                <span>Sequential</span>
              </button>
              <button
                type="button"
                onClick={() => setShuffled(true)}
                className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-md border text-xs font-medium transition-colors ${
                  shuffled
                    ? 'border-[#E02424] bg-[#E02424]/15 text-white'
                    : 'border-slate-800 bg-[#0B0E14] text-slate-400 hover:text-slate-200'
                }`}
              >
                <Shuffle className="w-3.5 h-3.5" />
                <span>Randomized</span>
              </button>
            </div>
          </div>

          <div className="pt-3 border-t border-slate-800 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-300 hover:text-white rounded-md border border-slate-700 hover:border-slate-600 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-xs font-semibold text-white bg-[#E02424] hover:bg-[#C81E1E] rounded-md transition-colors"
            >
              Start Session
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
