import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { SlidersHorizontal, RotateCcw } from 'lucide-react';
import { TopBar } from './components/TopBar';
import { TerminalPane } from './components/TerminalPane';
import { InspectorPane } from './components/InspectorPane';
import { SessionConfigModal } from './components/SessionConfigModal';
import { SessionSummary } from './components/SessionSummary';
import { CurriculumBrowser } from './components/CurriculumBrowser';
import { CliPackageView } from './components/CliPackageView';
import { buildVirtualFiles, executeInBrowserSandbox } from './utils/browserSandbox';
import type {
  ActiveView,
  QuestionOutcome,
  SandboxFile,
  ScenarioItem,
  SessionConfig,
  TerminalEntry,
} from './types';

function createSessionId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID().replace(/-/g, '').slice(0, 16);
  }
  return Math.random().toString(36).slice(2, 14);
}

function shuffleArray<T>(items: T[]): T[] {
  const arr = [...items];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export default function App() {
  const [sessionId] = useState<string>(() => createSessionId());
  const [activeView, setActiveView] = useState<ActiveView>('trainer');

  const [allScenarios, setAllScenarios] = useState<ScenarioItem[]>([]);
  const [categoryCounts, setCategoryCounts] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [sessionConfig, setSessionConfig] = useState<SessionConfig>({
    category: 'All',
    difficulty: 'All',
    count: 10,
    shuffled: false,
  });
  const [isConfigOpen, setIsConfigOpen] = useState<boolean>(false);

  const [queue, setQueue] = useState<ScenarioItem[]>([]);
  const [outcomes, setOutcomes] = useState<QuestionOutcome[]>([]);
  const [currentIdx, setCurrentIdx] = useState<number>(0);
  const [sessionComplete, setSessionComplete] = useState<boolean>(false);

  const [score, setScore] = useState<number>(0);
  const [streak, setStreak] = useState<number>(0);
  const [maxStreak, setMaxStreak] = useState<number>(0);
  const [attempts, setAttempts] = useState<number>(0);
  const [successes, setSuccesses] = useState<number>(0);
  const [completedIds, setCompletedIds] = useState<Set<string>>(() => new Set());

  const [command, setCommand] = useState<string>('');
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState<number>(0);
  const [entries, setEntries] = useState<TerminalEntry[]>([]);
  const [files, setFiles] = useState<SandboxFile[]>([]);
  const [hintLevel, setHintLevel] = useState<number>(0);
  const [revealedSolution, setRevealedSolution] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState<boolean>(false);

  const staticModeRef = useRef<boolean>(false);
  const scenariosByIdRef = useRef<Map<string, ScenarioItem>>(new Map());
  const filesRef = useRef<SandboxFile[]>([]);
  filesRef.current = files;

  const setupSandboxForScenario = useCallback(
    async (scenarioId: string) => {
      if (staticModeRef.current) {
        const sc = scenariosByIdRef.current.get(scenarioId);
        setFiles(sc ? buildVirtualFiles(sc) : []);
        return;
      }
      try {
        const res = await fetch('/api/sandbox/setup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sessionId, scenarioId }),
        });
        const contentType = res.headers.get('content-type') || '';
        if (!res.ok || !contentType.includes('application/json')) {
          staticModeRef.current = true;
          const sc = scenariosByIdRef.current.get(scenarioId);
          setFiles(sc ? buildVirtualFiles(sc) : []);
          return;
        }
        const data = (await res.json()) as { files?: SandboxFile[] };
        setFiles(data.files ?? []);
      } catch {
        const sc = scenariosByIdRef.current.get(scenarioId);
        setFiles(sc ? buildVirtualFiles(sc) : []);
      }
    },
    [sessionId],
  );

  const startNewSession = useCallback(
    (config: SessionConfig, sourceScenarios: ScenarioItem[], focusScenario?: ScenarioItem) => {
      let pool = sourceScenarios.filter((s) => {
        if (config.category !== 'All' && s.category !== config.category) return false;
        if (config.difficulty !== 'All' && s.difficulty !== config.difficulty) return false;
        return true;
      });

      if (pool.length === 0) {
        pool = sourceScenarios;
      }

      if (focusScenario) {
        pool = [focusScenario, ...pool.filter((s) => s.id !== focusScenario.id)];
      } else if (config.shuffled) {
        pool = shuffleArray(pool);
      }

      if (config.count && config.count > 0 && pool.length > config.count) {
        pool = pool.slice(0, config.count);
      }

      const initialOutcomes: QuestionOutcome[] = pool.map((s) => ({
        scenarioId: s.id,
        title: s.title,
        category: s.category,
        difficulty: s.difficulty,
        status: 'pending',
        attempts: 0,
      }));

      setSessionConfig(config);
      setQueue(pool);
      setOutcomes(initialOutcomes);
      setCurrentIdx(0);
      setSessionComplete(false);
      setScore(0);
      setStreak(0);
      setMaxStreak(0);
      setAttempts(0);
      setSuccesses(0);
      setCommand('');
      setEntries([]);
      setHintLevel(0);
      setRevealedSolution(null);

      if (pool[0]) {
        void setupSandboxForScenario(pool[0].id);
      }
    },
    [setupSandboxForScenario],
  );

  useEffect(() => {
    let cancelled = false;
    async function fetchScenarios() {
      setLoading(true);
      setLoadError(null);
      try {
        let loadedScenarios: ScenarioItem[] = [];
        let counts: Record<string, number> = {};
        let usedBackend = false;

        try {
          const res = await fetch('/api/scenarios');
          const contentType = res.headers.get('content-type') || '';
          if (res.ok && contentType.includes('application/json')) {
            const data = (await res.json()) as {
              scenarios: ScenarioItem[];
              categoryCounts: Record<string, number>;
            };
            loadedScenarios = data.scenarios;
            counts = data.categoryCounts;
            usedBackend = true;
          }
        } catch {
          // Fall back to static scenario JSON bundle
        }

        if (!usedBackend) {
          staticModeRef.current = true;
          const staticRes = await fetch('/all_scenarios.json');
          if (!staticRes.ok) {
            throw new Error(`Failed to fetch scenario bundle (${staticRes.status})`);
          }
          const rawList = (await staticRes.json()) as ScenarioItem[];
          loadedScenarios = rawList;
          for (const s of rawList) {
            counts[s.category] = (counts[s.category] || 0) + 1;
          }
        }

        if (cancelled) return;
        scenariosByIdRef.current = new Map(loadedScenarios.map((s) => [s.id, s]));
        setAllScenarios(loadedScenarios);
        setCategoryCounts(counts);
        startNewSession(
          { category: 'All', difficulty: 'All', count: 10, shuffled: false },
          loadedScenarios,
        );
      } catch (err) {
        if (!cancelled) {
          setLoadError(err instanceof Error ? err.message : 'Failed to load scenarios');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }
    void fetchScenarios();
    return () => {
      cancelled = true;
    };
  }, [startNewSession]);

  const currentScenario = queue[currentIdx] ?? null;
  const currentOutcome = outcomes[currentIdx] ?? null;
  const accuracy = attempts > 0 ? Math.round((successes / attempts) * 100) : 100;

  const switchToQueueIndex = useCallback(
    (idx: number) => {
      if (idx < 0 || idx >= queue.length) return;
      setCurrentIdx(idx);
      setSessionComplete(false);
      setCommand('');
      setEntries([]);
      setHintLevel(0);
      setRevealedSolution(null);
      void setupSandboxForScenario(queue[idx].id);
    },
    [queue, setupSandboxForScenario],
  );

  const executeCommand = async (grade: boolean) => {
    const trimmed = command.trim();
    if (!trimmed || !currentScenario || isExecuting) return;

    if (trimmed === 'clear') {
      setEntries([]);
      setCommand('');
      return;
    }

    setHistory((prev) => [...prev, trimmed]);
    setHistoryIndex(history.length + 1);
    setCommand('');
    setIsExecuting(true);

    if (grade) {
      setAttempts((a) => a + 1);
    }

    try {
      let data: {
        passed: boolean | null;
        stdout: string;
        stderr: string;
        exitCode: number;
        feedback: string;
        files?: SandboxFile[];
      };

      if (staticModeRef.current) {
        data = executeInBrowserSandbox(trimmed, currentScenario, filesRef.current, grade);
      } else {
        const res = await fetch('/api/sandbox/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sessionId,
            scenarioId: currentScenario.id,
            command: trimmed,
            grade,
          }),
        });
        const contentType = res.headers.get('content-type') || '';
        if (!res.ok || !contentType.includes('application/json')) {
          staticModeRef.current = true;
          data = executeInBrowserSandbox(trimmed, currentScenario, filesRef.current, grade);
        } else {
          data = (await res.json()) as typeof data;
        }
      }

      if (data.files) {
        setFiles(data.files);
      }

      const newEntry: TerminalEntry = {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        command: trimmed,
        mode: grade ? 'grade' : 'sandbox',
        passed: data.passed,
        stdout: data.stdout ?? '',
        stderr: data.stderr ?? '',
        exitCode: data.exitCode ?? 0,
        feedback: data.feedback ?? '',
        timestamp: new Date().toLocaleTimeString(),
      };
      setEntries((prev) => [...prev, newEntry]);

      if (grade) {
        setOutcomes((prev) =>
          prev.map((o, i) => {
            if (i !== currentIdx) return o;
            const nextStatus = data.passed ? 'passed' : o.status;
            return { ...o, attempts: o.attempts + 1, status: nextStatus };
          }),
        );

        if (data.passed) {
          setSuccesses((s) => s + 1);
          const nextStreak = streak + 1;
          setStreak(nextStreak);
          setMaxStreak((m) => Math.max(m, nextStreak));
          setScore((sc) => sc + 100 + nextStreak * 25);
          setCompletedIds((prev) => {
            const next = new Set(prev);
            next.add(currentScenario.id);
            return next;
          });
        } else {
          setStreak(0);
        }
      }
    } catch (err) {
      setEntries((prev) => [
        ...prev,
        {
          id: `${Date.now()}`,
          command: trimmed,
          mode: grade ? 'grade' : 'sandbox',
          passed: grade ? false : null,
          stdout: '',
          stderr: err instanceof Error ? err.message : 'Execution request failed',
          exitCode: 1,
          feedback: 'Unable to reach execution sandbox.',
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleCycleHint = () => {
    if (!currentScenario || currentScenario.hints.length === 0) return;
    setHintLevel((prev) => (prev + 1) % (currentScenario.hints.length + 1));
  };

  const handleRevealSolution = async () => {
    if (!currentScenario) return;
    if (revealedSolution) {
      setRevealedSolution(null);
      return;
    }
    try {
      let solutionText = currentScenario.solution ?? '';
      if (!staticModeRef.current) {
        const res = await fetch(`/api/scenarios/${encodeURIComponent(currentScenario.id)}/reveal`, {
          method: 'POST',
        });
        const contentType = res.headers.get('content-type') || '';
        if (res.ok && contentType.includes('application/json')) {
          const data = (await res.json()) as { solution: string };
          solutionText = data.solution;
        }
      }
      if (!solutionText) return;
      setRevealedSolution(solutionText);
      setStreak(0);
      setOutcomes((prev) =>
        prev.map((o, i) =>
          i === currentIdx && o.status === 'pending' ? { ...o, status: 'revealed' } : o,
        ),
      );
    } catch {
      // Ignore error
    }
  };

  const handleResetScenario = () => {
    if (!currentScenario) return;
    setEntries([]);
    setCommand('');
    setHintLevel(0);
    setRevealedSolution(null);
    void setupSandboxForScenario(currentScenario.id);
  };

  const handleNextScenario = () => {
    if (currentOutcome?.status === 'pending') {
      setOutcomes((prev) =>
        prev.map((o, i) => (i === currentIdx ? { ...o, status: 'skipped' } : o)),
      );
      setStreak(0);
    }

    if (currentIdx + 1 >= queue.length) {
      setSessionComplete(true);
      return;
    }
    switchToQueueIndex(currentIdx + 1);
  };

  const passedInSession = useMemo(
    () => outcomes.filter((o) => o.status === 'passed').length,
    [outcomes],
  );

  return (
    <div className="min-h-screen bg-[#0B0E14] text-slate-100 flex flex-col">
      <TopBar
        activeView={activeView}
        onNavigate={setActiveView}
        onOpenNewSession={() => setIsConfigOpen(true)}
      />

      <main className="flex-1 max-w-[1380px] w-full mx-auto px-4 sm:px-6 py-6">
        {loading ? (
          <div className="rounded-lg border border-slate-800 bg-[#111622] p-8 space-y-4">
            <div className="h-5 w-48 bg-slate-800 rounded animate-pulse" />
            <div className="h-4 w-96 max-w-full bg-slate-800/70 rounded animate-pulse" />
            <div className="h-64 w-full bg-[#090C11] rounded border border-slate-800/80 animate-pulse" />
          </div>
        ) : loadError ? (
          <div className="rounded-lg border border-rose-800/60 bg-[#111622] p-8 space-y-4">
            <h1 className="text-lg font-semibold text-white">Unable to Load Scenario Library</h1>
            <p className="text-sm text-rose-300">{loadError}</p>
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-[#E02424] hover:bg-[#C81E1E] text-xs font-semibold text-white"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        ) : activeView === 'curriculum' ? (
          <CurriculumBrowser
            scenarios={allScenarios}
            categoryCounts={categoryCounts}
            completedIds={completedIds}
            onLaunchSingle={(scenario) => {
              startNewSession(
                {
                  category: scenario.category,
                  difficulty: 'All',
                  count: 10,
                  shuffled: false,
                },
                allScenarios,
                scenario,
              );
              setActiveView('trainer');
            }}
            onStartFilteredSession={(category, difficulty) => {
              startNewSession(
                { category, difficulty, count: 25, shuffled: false },
                allScenarios,
              );
              setActiveView('trainer');
            }}
          />
        ) : activeView === 'cli' ? (
          <CliPackageView />
        ) : sessionComplete ? (
          <SessionSummary
            score={score}
            accuracy={accuracy}
            maxStreak={maxStreak}
            outcomes={outcomes}
            onRestartSame={() => startNewSession(sessionConfig, allScenarios)}
            onConfigureNew={() => setIsConfigOpen(true)}
            onReviewQuestion={(idx) => switchToQueueIndex(idx)}
          />
        ) : currentScenario ? (
          <div className="space-y-5">
            {/* Compact Session Metrics & Filter Strip */}
            <div className="rounded-lg border border-slate-800 bg-[#111622] px-4 sm:px-5 py-3 flex flex-wrap items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-xs">
                <div>
                  <span className="text-slate-400 mr-2">Drill</span>
                  <span className="font-mono font-semibold text-white tabular-nums">
                    {currentIdx + 1} / {queue.length}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 mr-2">Passed</span>
                  <span className="font-mono font-semibold text-emerald-400 tabular-nums">
                    {passedInSession} / {queue.length}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 mr-2">Score</span>
                  <span className="font-mono font-semibold text-white tabular-nums">
                    {score.toLocaleString()}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 mr-2">Streak</span>
                  <span className="font-mono font-semibold text-amber-400 tabular-nums">
                    {streak}
                  </span>
                  <span className="text-slate-500 font-mono tabular-nums ml-1">
                    (best {maxStreak})
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 mr-2">Accuracy</span>
                  <span className="font-mono font-semibold text-slate-200 tabular-nums">
                    {accuracy}%
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3 text-xs">
                <span className="text-slate-400 hidden sm:inline">
                  {sessionConfig.category} · {sessionConfig.difficulty}
                </span>
                <button
                  type="button"
                  onClick={() => setIsConfigOpen(true)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 hover:text-white transition-colors whitespace-nowrap"
                >
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Session Options</span>
                </button>
              </div>
            </div>

            {/* Two-Zone Workbench Split */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
              <div className="lg:col-span-8 flex flex-col">
                <TerminalPane
                  scenario={currentScenario}
                  command={command}
                  onCommandChange={setCommand}
                  onSubmitGrade={() => void executeCommand(true)}
                  onRunSandbox={() => void executeCommand(false)}
                  onCycleHint={handleCycleHint}
                  onRevealSolution={() => void handleRevealSolution()}
                  onResetScenario={handleResetScenario}
                  onNextScenario={handleNextScenario}
                  onClearTerminal={() => setEntries([])}
                  history={history}
                  historyIndex={historyIndex}
                  onHistoryNavigate={(nextIdx, value) => {
                    setHistoryIndex(nextIdx);
                    setCommand(value);
                  }}
                  entries={entries}
                  hintLevel={hintLevel}
                  revealedSolution={revealedSolution}
                  isExecuting={isExecuting}
                  isCurrentPassed={currentOutcome?.status === 'passed'}
                />
              </div>

              <div className="lg:col-span-4 flex flex-col">
                <InspectorPane
                  scenario={currentScenario}
                  files={files}
                  queue={outcomes}
                  currentQueueIndex={currentIdx}
                  onSelectQueueIndex={switchToQueueIndex}
                />
              </div>
            </div>
          </div>
        ) : null}
      </main>

      <SessionConfigModal
        isOpen={isConfigOpen}
        currentConfig={sessionConfig}
        categoryCounts={categoryCounts}
        totalCount={allScenarios.length}
        onClose={() => setIsConfigOpen(false)}
        onStartSession={(nextConfig) => {
          startNewSession(nextConfig, allScenarios);
          setActiveView('trainer');
        }}
      />
    </div>
  );
}
