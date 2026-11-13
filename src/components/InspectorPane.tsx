import { useEffect, useState } from 'react';
import { FileText, BookOpen, ListChecks, CheckCircle2, SkipForward, Eye } from 'lucide-react';
import { CHEAT_SHEETS } from '../data/cheatSheet';
import type { QuestionOutcome, SandboxFile, ScenarioItem } from '../types';

interface InspectorPaneProps {
  scenario: ScenarioItem;
  files: SandboxFile[];
  queue: QuestionOutcome[];
  currentQueueIndex: number;
  onSelectQueueIndex: (idx: number) => void;
}

type InspectorTab = 'files' | 'reference' | 'queue';

export function InspectorPane({
  scenario,
  files,
  queue,
  currentQueueIndex,
  onSelectQueueIndex,
}: InspectorPaneProps) {
  const [activeTab, setActiveTab] = useState<InspectorTab>('files');
  const [selectedFilePath, setSelectedFilePath] = useState<string>('');

  useEffect(() => {
    if (files.length > 0) {
      const stillExists = files.some((f) => f.path === selectedFilePath);
      if (!stillExists) {
        setSelectedFilePath(files[0].path);
      }
    } else {
      setSelectedFilePath('');
    }
  }, [files, selectedFilePath]);

  const activeFile = files.find((f) => f.path === selectedFilePath) ?? files[0] ?? null;
  const refItems = CHEAT_SHEETS[scenario.category] ?? [];

  return (
    <aside className="flex flex-col rounded-lg border border-slate-800 bg-[#111622] overflow-hidden h-full">
      {/* Segmented Control Tab Bar */}
      <div className="p-2 border-b border-slate-800 bg-[#0E131D]">
        <div className="grid grid-cols-3 gap-1 p-1 rounded-md bg-[#0B0E14]">
          <button
            type="button"
            onClick={() => setActiveTab('files')}
            className={`flex items-center justify-center gap-1.5 px-2.5 py-2 rounded text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'files'
                ? 'bg-[#1D2537] text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText className="w-3.5 h-3.5 shrink-0" />
            <span>Files ({files.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('reference')}
            className={`flex items-center justify-center gap-1.5 px-2.5 py-2 rounded text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'reference'
                ? 'bg-[#1D2537] text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 shrink-0" />
            <span>Reference</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('queue')}
            className={`flex items-center justify-center gap-1.5 px-2.5 py-2 rounded text-xs font-medium transition-colors whitespace-nowrap shrink-0 ${
              activeTab === 'queue'
                ? 'bg-[#1D2537] text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <ListChecks className="w-3.5 h-3.5 shrink-0" />
            <span>Queue ({queue.length})</span>
          </button>
        </div>
      </div>

      {/* Tab Body */}
      <div className="flex-1 overflow-y-auto terminal-scroll min-h-[380px] max-h-[580px]">
        {activeTab === 'files' && (
          <div className="flex flex-col h-full">
            {files.length === 0 ? (
              <div className="p-6 text-sm text-slate-400 space-y-2">
                <p className="font-medium text-slate-200">No scratch files provisioned</p>
                <p className="text-xs leading-relaxed text-slate-400">
                  This {scenario.category} drill validates RHEL 9/10 administrative commands and flags directly rather than operating on local scratch files.
                </p>
              </div>
            ) : (
              <>
                <div className="border-b border-slate-800 divide-y divide-slate-800/70">
                  {files.map((file) => {
                    const isSelected = activeFile?.path === file.path;
                    return (
                      <button
                        key={file.path}
                        type="button"
                        onClick={() => setSelectedFilePath(file.path)}
                        className={`w-full px-4 py-2.5 flex items-center justify-between gap-3 text-left text-xs transition-colors ${
                          isSelected
                            ? 'bg-[#161E2E] text-white'
                            : 'text-slate-300 hover:bg-[#141A28]'
                        }`}
                      >
                        <span className="font-mono truncate">{file.path}</span>
                        <span className="font-mono text-[11px] text-slate-400 tabular-nums shrink-0">
                          {file.mode} · {file.size} B
                        </span>
                      </button>
                    );
                  })}
                </div>

                {activeFile && (
                  <div className="flex-1 bg-[#090C11] p-4 font-mono text-xs overflow-auto terminal-scroll">
                    <div className="pb-2 mb-3 border-b border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                      <span>{activeFile.path}</span>
                      <span className="tabular-nums">mode {activeFile.mode}</span>
                    </div>
                    {activeFile.content ? (
                      <div className="space-y-0.5">
                        {activeFile.content.split('\n').map((line, i) => (
                          <div key={i} className="flex gap-3 leading-relaxed">
                            <span className="w-7 text-right text-slate-600 select-none tabular-nums shrink-0">
                              {i + 1}
                            </span>
                            <span className="text-slate-200 whitespace-pre-wrap break-all">
                              {line || ' '}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-slate-500 italic">[Empty file]</p>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {activeTab === 'reference' && (
          <div className="p-4 space-y-3">
            <div className="pb-2 border-b border-slate-800">
              <h3 className="text-xs font-semibold text-white">{scenario.category} Quick Reference</h3>
              <p className="text-xs text-slate-400 mt-0.5">Common RHEL 9/10 patterns and flags</p>
            </div>
            <div className="divide-y divide-slate-800/70">
              {refItems.map((item, idx) => (
                <div key={idx} className="py-2.5 space-y-1">
                  <code className="block font-mono text-xs text-emerald-300 break-all">
                    {item.command}
                  </code>
                  <p className="text-xs text-slate-400">{item.summary}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'queue' && (
          <div className="divide-y divide-slate-800/70">
            {queue.map((item, idx) => {
              const isCurrent = idx === currentQueueIndex;
              return (
                <button
                  key={`${item.scenarioId}-${idx}`}
                  type="button"
                  onClick={() => onSelectQueueIndex(idx)}
                  className={`w-full px-4 py-3 flex items-center justify-between gap-3 text-left transition-colors ${
                    isCurrent
                      ? 'bg-[#172033] text-white'
                      : 'hover:bg-[#141A28] text-slate-300'
                  }`}
                >
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 text-xs text-slate-400">
                      <span className="font-mono tabular-nums">
                        {String(idx + 1).padStart(2, '0')}
                      </span>
                      <span aria-hidden="true">·</span>
                      <span className="truncate">{item.category}</span>
                    </div>
                    <p className="text-xs font-medium text-slate-100 truncate mt-0.5">
                      {item.title}
                    </p>
                  </div>

                  <div className="shrink-0 text-xs font-medium">
                    {item.status === 'passed' && (
                      <span className="inline-flex items-center gap-1 text-emerald-400">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Pass</span>
                      </span>
                    )}
                    {item.status === 'skipped' && (
                      <span className="inline-flex items-center gap-1 text-slate-400">
                        <SkipForward className="w-3.5 h-3.5" />
                        <span>Skipped</span>
                      </span>
                    )}
                    {item.status === 'revealed' && (
                      <span className="inline-flex items-center gap-1 text-amber-400">
                        <Eye className="w-3.5 h-3.5" />
                        <span>Viewed</span>
                      </span>
                    )}
                    {item.status === 'pending' && (
                      <span className={isCurrent ? 'text-[#F87171]' : 'text-slate-500'}>
                        {isCurrent ? 'Active' : 'Queued'}
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
}
