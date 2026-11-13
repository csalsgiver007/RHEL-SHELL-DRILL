import { useState } from 'react';
import { Copy, Check, Download } from 'lucide-react';

export function CliPackageView() {
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const origin = typeof window !== 'undefined' ? window.location.origin : '';

  const curlRun = `curl -sSL "${origin}/shell-drill" -o shell-drill && chmod +x shell-drill && ./shell-drill`;
  const curlCount = `./shell-drill --count 15 --category "Firewall & Network"`;

  const copyText = async (key: string, text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedKey(key);
      setTimeout(() => setCopiedKey(null), 1800);
    } catch {
      // Clipboard blocked in non-HTTPS contexts
    }
  };

  return (
    <div className="max-w-4xl space-y-6">
      <div className="space-y-1.5 border-b border-slate-800 pb-5">
        <h1 className="text-xl sm:text-2xl font-semibold text-white tracking-tight">
          Offline RHEL 9/10 CLI Package
        </h1>
        <p className="text-sm text-slate-400">
          Prefer practicing directly inside a disposable RHEL virtual machine or SSH console? Download the standalone zero-dependency Python curses executable.
        </p>
      </div>

      <div className="rounded-lg border border-slate-800 bg-[#111622] p-6 space-y-4">
        <div className="space-y-1">
          <h2 className="text-sm font-semibold text-white">Direct Install via curl</h2>
          <p className="text-xs text-slate-400">
            Requires Python 3.6+ and standard system curses (included by default on RHEL 9 and 10).
          </p>
        </div>

        <div className="flex items-center justify-between gap-3 rounded-md border border-slate-800 bg-[#090C11] px-4 py-3">
          <code className="font-mono text-xs text-emerald-300 break-all">{curlRun}</code>
          <button
            type="button"
            onClick={() => copyText('curl', curlRun)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 shrink-0 transition-colors"
          >
            {copiedKey === 'curl' ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <a
            href="/shell-drill"
            download="shell-drill"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-[#E02424] hover:bg-[#C81E1E] text-xs font-semibold text-white transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Standalone Script</span>
          </a>

          <a
            href="/shell-drill.tar.gz"
            download="shell-drill.tar.gz"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-md border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Tarball (.tar.gz)</span>
          </a>

          <a
            href="/shell-drill.zip"
            download="shell-drill.zip"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-md border border-slate-700 hover:border-slate-600 text-xs font-medium text-slate-200 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Archive (.zip)</span>
          </a>
        </div>
      </div>

      <div className="rounded-lg border border-slate-800 bg-[#111622] p-6 space-y-3">
        <h2 className="text-sm font-semibold text-white">CLI Flags</h2>
        <div className="rounded-md border border-slate-800 bg-[#090C11] p-4 font-mono text-xs text-slate-300 space-y-1.5 overflow-x-auto">
          <p>./shell-drill                                    # Launch interactive curses TUI</p>
          <p>{curlCount}  # Practice 15 networking drills</p>
          <p>./shell-drill --list                             # List all 460 scenarios</p>
          <p>./shell-drill --export-library scenarios.json    # Export scenario JSON pack</p>
        </div>
      </div>
    </div>
  );
}
