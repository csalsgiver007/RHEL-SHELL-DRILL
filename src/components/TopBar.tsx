import type { ActiveView } from '../types';

interface TopBarProps {
  activeView: ActiveView;
  onNavigate: (view: ActiveView) => void;
  onOpenNewSession: () => void;
}

export function TopBar({ activeView, onNavigate, onOpenNewSession }: TopBarProps) {
  const navItems: { id: ActiveView; label: string }[] = [
    { id: 'trainer', label: 'Trainer' },
    { id: 'curriculum', label: 'Curriculum' },
    { id: 'cli', label: 'CLI Package' },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-[#0B0E14]">
      <div className="max-w-[1380px] mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-8">
        <button
          type="button"
          onClick={() => onNavigate('trainer')}
          className="text-lg font-bold tracking-tight text-white whitespace-nowrap shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#E02424] rounded px-1 -ml-1"
        >
          shell-drill
        </button>

        <nav className="flex items-center gap-6 sm:gap-8" aria-label="Primary Navigation">
          {navItems.map((item) => {
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onNavigate(item.id)}
                className={`relative py-2 text-sm font-medium whitespace-nowrap shrink-0 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#E02424] rounded px-1 ${
                  isActive
                    ? 'text-white'
                    : 'text-slate-400 hover:text-slate-100'
                }`}
              >
                {item.label}
                {isActive && (
                  <span
                    aria-hidden="true"
                    className="absolute left-0 right-0 -bottom-[17px] h-[2px] bg-[#E02424]"
                  />
                )}
              </button>
            );
          })}
        </nav>

        <div className="flex items-center shrink-0">
          <button
            type="button"
            onClick={onOpenNewSession}
            className="px-4 py-2 text-xs sm:text-sm font-semibold text-white bg-[#E02424] hover:bg-[#C81E1E] rounded-md transition-colors whitespace-nowrap shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-white/80"
          >
            New Session
          </button>
        </div>
      </div>
    </header>
  );
}
