import { useMemo, useState } from 'react';
import { Search, Play, CheckCircle2 } from 'lucide-react';
import { CATEGORY_LIST } from '../data/cheatSheet';
import type { ScenarioItem } from '../types';

interface CurriculumBrowserProps {
  scenarios: ScenarioItem[];
  categoryCounts: Record<string, number>;
  completedIds: Set<string>;
  onLaunchSingle: (scenario: ScenarioItem) => void;
  onStartFilteredSession: (category: string, difficulty: string) => void;
}

export function CurriculumBrowser({
  scenarios,
  categoryCounts,
  completedIds,
  onLaunchSingle,
  onStartFilteredSession,
}: CurriculumBrowserProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [query, setQuery] = useState<string>('');

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return scenarios.filter((s) => {
      if (selectedCategory !== 'All' && s.category !== selectedCategory) return false;
      if (selectedDifficulty !== 'All' && s.difficulty !== selectedDifficulty) return false;
      if (q) {
        return (
          s.id.toLowerCase().includes(q) ||
          s.title.toLowerCase().includes(q) ||
          s.description.toLowerCase().includes(q) ||
          s.objective.toLowerCase().includes(q) ||
          s.category.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [scenarios, selectedCategory, selectedDifficulty, query]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="space-y-1">
          <h1 className="text-xl sm:text-2xl font-semibold text-white tracking-tight">
            RHEL 9/10 Scenario Curriculum
          </h1>
          <p className="text-sm text-slate-400">
            Browse all {scenarios.length} hands-on drills across seven Linux administration domains.
          </p>
        </div>

        <button
          type="button"
          onClick={() => onStartFilteredSession(selectedCategory, selectedDifficulty)}
          disabled={filtered.length === 0}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-[#E02424] hover:bg-[#C81E1E] disabled:opacity-40 text-xs font-semibold text-white transition-colors whitespace-nowrap shrink-0 self-start sm:self-auto"
        >
          <Play className="w-3.5 h-3.5" />
          <span>Drill Matching ({filtered.length})</span>
        </button>
      </div>

      {/* Filters Toolbar */}
      <div className="space-y-3">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by ID, command, flag, or keyword (e.g., firewall-cmd, awk, sed, perm)..."
              aria-label="Search curriculum scenarios"
              className="w-full rounded-md border border-slate-800 bg-[#111622] pl-9 pr-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:border-[#E02424] focus:outline-none"
            />
          </div>

          <div className="flex items-center gap-1 p-1 rounded-md bg-[#111622] border border-slate-800 shrink-0">
            {['All', 'Easy', 'Intermediate', 'Advanced'].map((diff) => (
              <button
                key={diff}
                type="button"
                onClick={() => setSelectedDifficulty(diff)}
                className={`px-3 py-1.5 rounded text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
                  selectedDifficulty === diff
                    ? 'bg-[#1D2537] text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {diff}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          <button
            type="button"
            onClick={() => setSelectedCategory('All')}
            className={`px-3 py-1.5 rounded-md border text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
              selectedCategory === 'All'
                ? 'border-[#E02424] bg-[#E02424]/15 text-white'
                : 'border-slate-800 bg-[#111622] text-slate-400 hover:text-slate-200'
            }`}
          >
            All ({scenarios.length})
          </button>
          {CATEGORY_LIST.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-md border text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
                selectedCategory === cat
                  ? 'border-[#E02424] bg-[#E02424]/15 text-white'
                  : 'border-slate-800 bg-[#111622] text-slate-400 hover:text-slate-200'
              }`}
            >
              {cat} ({categoryCounts[cat] ?? 0})
            </button>
          ))}
        </div>
      </div>

      {/* Scenarios Table */}
      <div className="rounded-lg border border-slate-800 bg-[#111622] overflow-hidden">
        {filtered.length === 0 ? (
          <div className="p-10 text-center space-y-3">
            <p className="text-sm font-medium text-slate-200">No scenarios match your current filters.</p>
            <button
              type="button"
              onClick={() => {
                setSelectedCategory('All');
                setSelectedDifficulty('All');
                setQuery('');
              }}
              className="px-4 py-2 rounded-md border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-[#0E131D] text-xs font-semibold text-slate-400">
                  <th className="py-3 px-4 w-24">ID</th>
                  <th className="py-3 px-4">Scenario</th>
                  <th className="py-3 px-4 w-48 hidden md:table-cell">Category</th>
                  <th className="py-3 px-4 w-32 hidden sm:table-cell">Difficulty</th>
                  <th className="py-3 px-4 w-28 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/70 text-xs">
                {filtered.map((s) => {
                  const isDone = completedIds.has(s.id);
                  return (
                    <tr
                      key={s.id}
                      className="hover:bg-[#151B2B] transition-colors"
                    >
                      <td className="py-3 px-4 font-mono tabular-nums text-slate-400 align-top">
                        {s.id}
                      </td>
                      <td className="py-3 px-4 align-top">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-slate-100 text-sm">{s.title}</span>
                          {isDone && (
                            <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-400 shrink-0">
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Passed</span>
                            </span>
                          )}
                        </div>
                        <p className="text-slate-400 mt-0.5 line-clamp-1 max-w-2xl">
                          {s.description}
                        </p>
                      </td>
                      <td className="py-3 px-4 text-slate-300 hidden md:table-cell align-top whitespace-nowrap">
                        {s.category}
                      </td>
                      <td className="py-3 px-4 text-slate-300 hidden sm:table-cell align-top whitespace-nowrap">
                        {s.difficulty}
                      </td>
                      <td className="py-3 px-4 text-right align-top">
                        <button
                          type="button"
                          onClick={() => onLaunchSingle(s)}
                          className="px-3 py-1.5 rounded border border-slate-700 hover:border-[#E02424] hover:bg-[#E02424]/15 text-xs font-medium text-slate-200 hover:text-white transition-colors whitespace-nowrap"
                        >
                          Practice
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
