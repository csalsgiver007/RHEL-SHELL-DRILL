import type { SandboxFile, ScenarioItem } from '../types';

export interface SandboxExecutionResult {
  passed: boolean | null;
  stdout: string;
  stderr: string;
  exitCode: number;
  feedback: string;
  files: SandboxFile[];
}

export function buildVirtualFiles(scenario: ScenarioItem): SandboxFile[] {
  const setupFiles = scenario.setup_files ?? {};
  const setupPerms = scenario.setup_perms ?? {};

  return Object.entries(setupFiles)
    .map(([relPath, rawData]) => {
      const numMode = setupPerms[relPath] ?? 0o644;
      const modeOctal = '0' + (numMode & 0o7777).toString(8).padStart(3, '0');

      if (typeof rawData === 'string' && rawData.startsWith('__SPARSE_BYTES:')) {
        const sparseSize = Number.parseInt(rawData.split(':')[1] || '0', 10);
        const safeSize = Number.isFinite(sparseSize) ? sparseSize : 0;
        return {
          path: relPath,
          mode: modeOctal,
          size: safeSize,
          isSparse: true,
          content: `[Sparse binary file: ${safeSize.toLocaleString()} bytes (${Math.round(safeSize / (1024 * 1024))} MiB)]`,
        };
      }

      const content = typeof rawData === 'string' ? rawData : '';
      return {
        path: relPath,
        mode: modeOctal,
        size: new TextEncoder().encode(content).length,
        isSparse: false,
        content,
      };
    })
    .sort((a, b) => a.path.localeCompare(b.path));
}

function tokenizeCommand(input: string): string[] {
  const tokens: string[] = [];
  let current = '';
  let quote: '"' | "'" | null = null;
  let escapeNext = false;

  for (let i = 0; i < input.length; i++) {
    const ch = input[i];
    if (escapeNext) {
      current += ch;
      escapeNext = false;
      continue;
    }
    if (ch === '\\' && quote !== "'") {
      escapeNext = true;
      continue;
    }
    if (quote) {
      if (ch === quote) {
        quote = null;
      } else {
        current += ch;
      }
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (/\s/.test(ch)) {
      if (current.length > 0) {
        tokens.push(current);
        current = '';
      }
      continue;
    }
    current += ch;
  }

  if (current.length > 0) {
    tokens.push(current);
  }
  return tokens;
}

function splitPipeline(cmd: string): string[] {
  const segments: string[] = [];
  let current = '';
  let quote: '"' | "'" | null = null;
  let escapeNext = false;

  for (let i = 0; i < cmd.length; i++) {
    const ch = cmd[i];
    if (escapeNext) {
      current += ch;
      escapeNext = false;
      continue;
    }
    if (ch === '\\' && quote !== "'") {
      current += ch;
      escapeNext = true;
      continue;
    }
    if (quote) {
      current += ch;
      if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      current += ch;
      continue;
    }
    if (ch === '|') {
      segments.push(current.trim());
      current = '';
      continue;
    }
    current += ch;
  }
  if (current.trim()) {
    segments.push(current.trim());
  }
  return segments;
}

function findFile(files: SandboxFile[], target: string): SandboxFile | undefined {
  const normalized = target.replace(/^\.\//, '');
  return files.find((f) => f.path === normalized || f.path === target);
}

function globToRegex(glob: string): RegExp {
  const escaped = glob
    .replace(/[.+^${}()|[\]\\]/g, '\\$&')
    .replace(/\*/g, '.*')
    .replace(/\?/g, '.');
  return new RegExp(`^${escaped}$`);
}

function simulateRhelOutput(cmd: string, scenario: ScenarioItem): string {
  const trimmed = cmd.trim();
  if (trimmed.startsWith('systemctl enable')) {
    const unit = trimmed.split(/\s+/).pop() || 'service';
    const unitName = unit.endsWith('.service') ? unit : `${unit}.service`;
    return `Created symlink /etc/systemd/system/multi-user.target.wants/${unitName} -> /usr/lib/systemd/system/${unitName}.`;
  }
  if (trimmed.startsWith('systemctl disable')) {
    const unit = trimmed.split(/\s+/).pop() || 'service';
    const unitName = unit.endsWith('.service') ? unit : `${unit}.service`;
    return `Removed "/etc/systemd/system/multi-user.target.wants/${unitName}".`;
  }
  if (trimmed.startsWith('systemctl mask')) {
    const unit = trimmed.split(/\s+/).pop() || 'service';
    const unitName = unit.endsWith('.service') ? unit : `${unit}.service`;
    return `Created symlink /etc/systemd/system/${unitName} -> /dev/null.`;
  }
  if (trimmed.startsWith('systemctl unmask')) {
    const unit = trimmed.split(/\s+/).pop() || 'service';
    const unitName = unit.endsWith('.service') ? unit : `${unit}.service`;
    return `Removed "/etc/systemd/system/${unitName}".`;
  }
  if (trimmed.startsWith('firewall-cmd')) {
    if (trimmed.includes('--list') || trimmed.includes('--get')) {
      return `public (active)\n  target: default\n  services: cockpit dhcpv6-client ssh\n  ports: \n  forward-ports: \n  rich rules: `;
    }
    return 'success';
  }
  if (trimmed.startsWith('nmcli')) {
    return `Connection operation applied cleanly on RHEL NetworkManager.`;
  }
  if (trimmed.startsWith('semanage')) {
    return `SELinux policy updated.`;
  }
  if (trimmed.startsWith('journalctl')) {
    return `-- Logs begin at Fri 2026-11-13 08:00:00 UTC, end at Fri 2026-11-13 11:55:00 UTC. --\nNov 13 11:42:10 rhel-sandbox systemd[1]: Started ${scenario.title}.`;
  }
  return `[rhel-sandbox] Executed: ${trimmed}`;
}

function runSingleCommand(
  tokens: string[],
  stdin: string,
  files: SandboxFile[],
): { stdout: string; stderr: string; exitCode: number; files: SandboxFile[] } {
  if (tokens.length === 0) {
    return { stdout: '', stderr: '', exitCode: 0, files };
  }

  const cmd = tokens[0];
  const args = tokens.slice(1);
  let nextFiles = files.map((f) => ({ ...f }));

  if (cmd === 'pwd') {
    return { stdout: '/scratch\n', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'echo') {
    return { stdout: args.join(' ') + '\n', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'ls') {
    const longFmt = args.some((a) => a.startsWith('-') && a.includes('l'));
    const pathArg = args.find((a) => !a.startsWith('-'))?.replace(/^\.\//, '').replace(/\/$/, '');
    const matching = pathArg
      ? nextFiles.filter((f) => f.path === pathArg || f.path.startsWith(pathArg + '/'))
      : nextFiles;

    if (matching.length === 0 && pathArg) {
      return { stdout: '', stderr: `ls: cannot access '${pathArg}': No such file or directory\n`, exitCode: 2, files: nextFiles };
    }

    const lines = matching.map((f) =>
      longFmt ? `${f.mode} 1 root root ${String(f.size).padStart(7, ' ')} ${f.path}` : f.path,
    );
    return { stdout: lines.length ? lines.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'cat') {
    const fileArgs = args.filter((a) => !a.startsWith('-'));
    if (fileArgs.length === 0) {
      return { stdout: stdin, stderr: '', exitCode: 0, files: nextFiles };
    }
    let out = '';
    let err = '';
    let code = 0;
    for (const fa of fileArgs) {
      const f = findFile(nextFiles, fa);
      if (!f) {
        err += `cat: ${fa}: No such file or directory\n`;
        code = 1;
      } else {
        out += f.content;
      }
    }
    return { stdout: out, stderr: err, exitCode: code, files: nextFiles };
  }

  if (cmd === 'head' || cmd === 'tail') {
    let n = 10;
    const positional: string[] = [];
    for (let i = 0; i < args.length; i++) {
      if (args[i] === '-n' && args[i + 1]) {
        n = Number.parseInt(args[++i], 10) || 10;
      } else if (/^-\d+$/.test(args[i])) {
        n = Number.parseInt(args[i].slice(1), 10) || 10;
      } else if (!args[i].startsWith('-')) {
        positional.push(args[i]);
      }
    }
    let source = stdin;
    if (positional[0]) {
      const f = findFile(nextFiles, positional[0]);
      if (!f) {
        return { stdout: '', stderr: `${cmd}: cannot open '${positional[0]}': No such file or directory\n`, exitCode: 1, files: nextFiles };
      }
      source = f.content;
    }
    const lines = source.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    const sliced = cmd === 'head' ? lines.slice(0, n) : lines.slice(-n);
    return { stdout: sliced.length ? sliced.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'wc') {
    const countLines = args.includes('-l');
    const countWords = args.includes('-w');
    const countBytes = args.includes('-c');
    const fileArg = args.find((a) => !a.startsWith('-'));
    let source = stdin;
    if (fileArg) {
      const f = findFile(nextFiles, fileArg);
      if (!f) {
        return { stdout: '', stderr: `wc: ${fileArg}: No such file or directory\n`, exitCode: 1, files: nextFiles };
      }
      source = f.content;
    }
    const lines = source === '' ? 0 : source.split('\n').length - (source.endsWith('\n') ? 1 : 0);
    const words = source.trim() === '' ? 0 : source.trim().split(/\s+/).length;
    const bytes = new TextEncoder().encode(source).length;
    if (countLines && !countWords && !countBytes) {
      return { stdout: `${lines}${fileArg ? ' ' + fileArg : ''}\n`, stderr: '', exitCode: 0, files: nextFiles };
    }
    if (countWords && !countLines && !countBytes) {
      return { stdout: `${words}${fileArg ? ' ' + fileArg : ''}\n`, stderr: '', exitCode: 0, files: nextFiles };
    }
    if (countBytes && !countLines && !countWords) {
      return { stdout: `${bytes}${fileArg ? ' ' + fileArg : ''}\n`, stderr: '', exitCode: 0, files: nextFiles };
    }
    return { stdout: `${lines} ${words} ${bytes}${fileArg ? ' ' + fileArg : ''}\n`, stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'sort') {
    const reverse = args.includes('-r');
    const numeric = args.includes('-n') || args.includes('-rn') || args.includes('-nr');
    const unique = args.includes('-u');
    const fileArg = args.find((a) => !a.startsWith('-'));
    let source = stdin;
    if (fileArg) {
      const f = findFile(nextFiles, fileArg);
      if (!f) {
        return { stdout: '', stderr: `sort: cannot read: ${fileArg}: No such file or directory\n`, exitCode: 2, files: nextFiles };
      }
      source = f.content;
    }
    let lines = source.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    lines.sort((a, b) => {
      if (numeric) {
        const na = Number.parseFloat(a.trim()) || 0;
        const nb = Number.parseFloat(b.trim()) || 0;
        return na - nb;
      }
      return a.localeCompare(b);
    });
    if (reverse) lines.reverse();
    if (unique) lines = Array.from(new Set(lines));
    return { stdout: lines.length ? lines.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'uniq') {
    const countFlag = args.includes('-c');
    const lines = stdin.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    const out: string[] = [];
    for (let i = 0; i < lines.length; i++) {
      let count = 1;
      while (i + 1 < lines.length && lines[i + 1] === lines[i]) {
        count++;
        i++;
      }
      out.push(countFlag ? `${String(count).padStart(7, ' ')} ${lines[i]}` : lines[i]);
    }
    return { stdout: out.length ? out.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'grep') {
    let flags = '';
    const positional: string[] = [];
    let afterCtx = 0;
    let beforeCtx = 0;
    for (let i = 0; i < args.length; i++) {
      const a = args[i];
      if (a === '-A' && args[i + 1]) {
        afterCtx = Number.parseInt(args[++i], 10) || 0;
      } else if (a === '-B' && args[i + 1]) {
        beforeCtx = Number.parseInt(args[++i], 10) || 0;
      } else if (a === '-C' && args[i + 1]) {
        const c = Number.parseInt(args[++i], 10) || 0;
        afterCtx = c;
        beforeCtx = c;
      } else if (a === '-e' && args[i + 1]) {
        positional.push(args[++i]);
      } else if (a.startsWith('-') && a.length > 1 && !a.startsWith('--')) {
        flags += a.slice(1);
      } else if (a === '--extended-regexp') {
        flags += 'E';
      } else if (a === '--fixed-strings') {
        flags += 'F';
      } else if (a === '--ignore-case') {
        flags += 'i';
      } else if (a === '--invert-match') {
        flags += 'v';
      } else if (a === '--line-number') {
        flags += 'n';
      } else if (a === '--count') {
        flags += 'c';
      } else if (a === '--only-matching') {
        flags += 'o';
      } else if (a === '--word-regexp') {
        flags += 'w';
      } else {
        positional.push(a);
      }
    }

    const patternStr = positional[0] ?? '';
    const fileArgs = positional.slice(1);
    const ignoreCase = flags.includes('i');
    const invert = flags.includes('v');
    const showLineNum = flags.includes('n');
    const countOnly = flags.includes('c');
    const onlyMatching = flags.includes('o');
    const fixed = flags.includes('F');
    const word = flags.includes('w');

    let regexSource = fixed ? patternStr.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') : patternStr;
    if (word) {
      regexSource = `\\b(?:${regexSource})\\b`;
    }

    let re: RegExp;
    try {
      re = new RegExp(regexSource, ignoreCase ? 'i' : '');
    } catch {
      return { stdout: '', stderr: `grep: Invalid regular expression\n`, exitCode: 2, files: nextFiles };
    }

    const targets: { name: string | null; text: string }[] = [];
    if (fileArgs.length === 0) {
      targets.push({ name: null, text: stdin });
    } else {
      for (const fa of fileArgs) {
        const f = findFile(nextFiles, fa);
        if (!f) {
          return { stdout: '', stderr: `grep: ${fa}: No such file or directory\n`, exitCode: 2, files: nextFiles };
        }
        targets.push({ name: fileArgs.length > 1 ? fa : null, text: f.content });
      }
    }

    const outLines: string[] = [];
    let totalMatches = 0;

    for (const t of targets) {
      const lines = t.text.split('\n');
      if (lines[lines.length - 1] === '') lines.pop();
      const matchedLineIndices = new Set<number>();

      lines.forEach((line, idx) => {
        const isMatch = re.test(line);
        const keep = invert ? !isMatch : isMatch;
        if (keep) {
          totalMatches++;
          if (countOnly) return;
          if (onlyMatching && !invert) {
            const globalRe = new RegExp(re.source, ignoreCase ? 'gi' : 'g');
            let m: RegExpExecArray | null;
            while ((m = globalRe.exec(line)) !== null) {
              if (m[0] === '') break;
              const prefix = `${t.name ? t.name + ':' : ''}${showLineNum ? idx + 1 + ':' : ''}`;
              outLines.push(prefix + m[0]);
            }
          } else {
            for (let b = Math.max(0, idx - beforeCtx); b <= Math.min(lines.length - 1, idx + afterCtx); b++) {
              matchedLineIndices.add(b);
            }
          }
        }
      });

      if (countOnly) {
        outLines.push(`${t.name ? t.name + ':' : ''}${totalMatches}`);
      } else if (!onlyMatching) {
        Array.from(matchedLineIndices)
          .sort((a, b) => a - b)
          .forEach((idx) => {
            const prefix = `${t.name ? t.name + ':' : ''}${showLineNum ? idx + 1 + ':' : ''}`;
            outLines.push(prefix + lines[idx]);
          });
      }
    }

    return {
      stdout: outLines.length ? outLines.join('\n') + '\n' : '',
      stderr: '',
      exitCode: totalMatches > 0 ? 0 : 1,
      files: nextFiles,
    };
  }

  if (cmd === 'sed') {
    const suppress = args.includes('-n');
    const inPlace = args.some((a) => a === '-i' || a.startsWith('-i'));
    const positional = args.filter((a) => !a.startsWith('-'));
    const script = positional[0] ?? '';
    const fileArg = positional[1];

    let source = stdin;
    let targetFile: SandboxFile | undefined;
    if (fileArg) {
      targetFile = findFile(nextFiles, fileArg);
      if (!targetFile) {
        return { stdout: '', stderr: `sed: can't read ${fileArg}: No such file or directory\n`, exitCode: 2, files: nextFiles };
      }
      source = targetFile.content;
    }

    const lines = source.split('\n');
    const hadTrailingNewline = source.endsWith('\n');
    if (hadTrailingNewline) lines.pop();

    const subMatch = script.match(/^s(.)(.*?)\1(.*?)\1([gi]*)$/);
    const outLines: string[] = [];

    if (subMatch) {
      const [, , pat, rep, flags] = subMatch;
      const re = new RegExp(pat, flags.includes('g') ? (flags.includes('i') ? 'gi' : 'g') : flags.includes('i') ? 'i' : '');
      for (const line of lines) {
        const replaced = line.replace(re, rep);
        outLines.push(replaced);
      }
    } else if (/^\/.+\/d$/.test(script)) {
      const pat = script.slice(1, -2);
      const re = new RegExp(pat);
      for (const line of lines) {
        if (!re.test(line)) outLines.push(line);
      }
    } else if (/^\d+(,\d+)?p$/.test(script) && suppress) {
      const parts = script.slice(0, -1).split(',').map((v) => Number.parseInt(v, 10));
      const start = parts[0];
      const end = parts[1] ?? start;
      lines.forEach((line, idx) => {
        if (idx + 1 >= start && idx + 1 <= end) outLines.push(line);
      });
    } else {
      outLines.push(...lines);
    }

    const resultText = outLines.length ? outLines.join('\n') + (hadTrailingNewline ? '\n' : '') : '';
    if (inPlace && targetFile) {
      targetFile.content = resultText;
      targetFile.size = new TextEncoder().encode(resultText).length;
      return { stdout: '', stderr: '', exitCode: 0, files: nextFiles };
    }
    return { stdout: resultText, stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'find') {
    const startArg = args[0] && !args[0].startsWith('-') ? args[0].replace(/^\.\//, '').replace(/\/$/, '') : '.';
    let typeFilter: string | null = null;
    let nameRegex: RegExp | null = null;
    let permFilter: string | null = null;
    let minSizeBytes: number | null = null;

    for (let i = 0; i < args.length; i++) {
      if (args[i] === '-type' && args[i + 1]) {
        typeFilter = args[++i];
      } else if ((args[i] === '-name' || args[i] === '-iname') && args[i + 1]) {
        const isI = args[i] === '-iname';
        const pat = globToRegex(args[++i]);
        nameRegex = isI ? new RegExp(pat.source, 'i') : pat;
      } else if (args[i] === '-perm' && args[i + 1]) {
        permFilter = args[++i];
      } else if (args[i] === '-size' && args[i + 1]) {
        const sz = args[++i];
        const m = sz.match(/^([+-]?)(\d+)([ckMG]?)$/);
        if (m) {
          const val = Number.parseInt(m[2], 10);
          const unit = m[3];
          const mult = unit === 'M' ? 1024 * 1024 : unit === 'k' ? 1024 : unit === 'G' ? 1024 ** 3 : 1;
          if (m[1] === '+') minSizeBytes = val * mult;
        }
      }
    }

    if (typeFilter === 'd') {
      return { stdout: '', stderr: '', exitCode: 0, files: nextFiles };
    }

    const matched = nextFiles.filter((f) => {
      if (startArg !== '.' && f.path !== startArg && !f.path.startsWith(startArg + '/')) {
        return false;
      }
      if (nameRegex) {
        const base = f.path.split('/').pop() ?? f.path;
        if (!nameRegex.test(base)) return false;
      }
      if (permFilter) {
        const normalizedPerm = permFilter.replace(/^-/, '').padStart(4, '0');
        if (permFilter.startsWith('-')) {
          const req = Number.parseInt(normalizedPerm, 8);
          const actual = Number.parseInt(f.mode, 8);
          if ((actual & req) !== req) return false;
        } else if (f.mode !== normalizedPerm) {
          return false;
        }
      }
      if (minSizeBytes !== null && f.size <= minSizeBytes) {
        return false;
      }
      return true;
    });

    const prefix = args[0]?.startsWith('./') ? './' : '';
    const out = matched.map((f) => `${prefix}${f.path}`).join('\n');
    return { stdout: out ? out + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'chmod' && args.length >= 2) {
    const modeArg = args[0];
    const f = findFile(nextFiles, args[1]);
    if (!f) {
      return { stdout: '', stderr: `chmod: cannot access '${args[1]}': No such file or directory\n`, exitCode: 1, files: nextFiles };
    }
    if (/^[0-7]{3,4}$/.test(modeArg)) {
      f.mode = modeArg.padStart(4, '0');
    }
    return { stdout: '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'touch' && args[0]) {
    const target = args[0].replace(/^\.\//, '');
    if (!findFile(nextFiles, target)) {
      nextFiles.push({ path: target, mode: '0644', size: 0, isSparse: false, content: '' });
      nextFiles.sort((a, b) => a.path.localeCompare(b.path));
    }
    return { stdout: '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'cut') {
    let delim = '\t';
    let fieldsSpec = '';
    const positional: string[] = [];
    for (let i = 0; i < args.length; i++) {
      if (args[i] === '-d' && args[i + 1]) {
        delim = args[++i];
      } else if (args[i].startsWith('-d') && args[i].length > 2) {
        delim = args[i].slice(2);
      } else if (args[i] === '-f' && args[i + 1]) {
        fieldsSpec = args[++i];
      } else if (args[i].startsWith('-f') && args[i].length > 2) {
        fieldsSpec = args[i].slice(2);
      } else if (!args[i].startsWith('-')) {
        positional.push(args[i]);
      }
    }
    let source = stdin;
    if (positional[0]) {
      const f = findFile(nextFiles, positional[0]);
      if (!f) {
        return { stdout: '', stderr: `cut: ${positional[0]}: No such file or directory\n`, exitCode: 2, files: nextFiles };
      }
      source = f.content;
    }
    const indices = fieldsSpec
      .split(',')
      .map((n) => Number.parseInt(n, 10) - 1)
      .filter((n) => Number.isFinite(n) && n >= 0);
    const lines = source.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    const out = lines.map((line) => {
      const parts = line.split(delim);
      return indices.map((idx) => parts[idx] ?? '').join(delim);
    });
    return { stdout: out.length ? out.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
  }

  if (cmd === 'awk') {
    let fsRegex: RegExp = /\s+/;
    const positional: string[] = [];
    for (let i = 0; i < args.length; i++) {
      if (args[i] === '-F' && args[i + 1]) {
        const sep = args[++i];
        fsRegex = new RegExp(sep.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      } else if (args[i].startsWith('-F') && args[i].length > 2) {
        const sep = args[i].slice(2);
        fsRegex = new RegExp(sep.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      } else if (!args[i].startsWith('-')) {
        positional.push(args[i]);
      }
    }
    const prog = positional[0] ?? '';
    const fileArg = positional[1];
    let source = stdin;
    if (fileArg) {
      const f = findFile(nextFiles, fileArg);
      if (!f) {
        return { stdout: '', stderr: `awk: fatal: cannot open file \`${fileArg}' for reading (No such file or directory)\n`, exitCode: 2, files: nextFiles };
      }
      source = f.content;
    }
    const lines = source.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    const outLines: string[] = [];

    const eqMatch = prog.match(/^\s*\$(\d+)\s*==\s*["']([^"']+)["']\s*\{print\s+(.*?)\}\s*$/);
    const simplePrintMatch = prog.match(/^\s*\{print\s+(.*?)\}\s*$/);
    const expr = eqMatch ? eqMatch[3] : simplePrintMatch ? simplePrintMatch[1] : null;

    if (expr) {
      for (const line of lines) {
        const trimmed = line.trim();
        const cols = fsRegex.source === '\\s+' ? (trimmed ? trimmed.split(fsRegex) : []) : line.split(fsRegex);
        const getField = (idx: number) => (idx === 0 ? line : cols[idx - 1] ?? '');
        if (eqMatch) {
          const checkIdx = Number.parseInt(eqMatch[1], 10);
          if (getField(checkIdx) !== eqMatch[2]) continue;
        }
        const rendered = expr
          .replace(/\$(\d+)/g, (_, d) => getField(Number.parseInt(d, 10)))
          .replace(/["']([^"']*)["']/g, '$1')
          .replace(/,/g, ' ');
        outLines.push(rendered);
      }
      return { stdout: outLines.length ? outLines.join('\n') + '\n' : '', stderr: '', exitCode: 0, files: nextFiles };
    }
  }

  return {
    stdout: '',
    stderr: '',
    exitCode: 0,
    files: nextFiles,
  };
}

function runPipeline(
  rawCmd: string,
  initialFiles: SandboxFile[],
): { stdout: string; stderr: string; exitCode: number; files: SandboxFile[] } {
  let clean = rawCmd.trim();
  let redirectOut: string | null = null;
  let appendOut = false;

  const redirMatch = clean.match(/\s*(?:&>>?|>>?)\s*([^\s>&]+)(?:\s+2>&1)?$/);
  if (redirMatch && !clean.startsWith('firewall-cmd') && !clean.startsWith('nmcli')) {
    redirectOut = redirMatch[1].replace(/^\.\//, '');
    appendOut = redirMatch[0].includes('>>');
    clean = clean.slice(0, redirMatch.index).trim();
  }

  const segments = splitPipeline(clean);
  let stdin = '';
  let stderr = '';
  let exitCode = 0;
  let files = initialFiles.map((f) => ({ ...f }));

  for (const seg of segments) {
    const tokens = tokenizeCommand(seg);
    const res = runSingleCommand(tokens, stdin, files);
    stdin = res.stdout;
    if (res.stderr) stderr += res.stderr;
    exitCode = res.exitCode;
    files = res.files;
  }

  if (redirectOut) {
    const existing = findFile(files, redirectOut);
    if (existing) {
      existing.content = appendOut ? existing.content + stdin : stdin;
      existing.size = new TextEncoder().encode(existing.content).length;
    } else {
      files.push({
        path: redirectOut,
        mode: '0644',
        size: new TextEncoder().encode(stdin).length,
        isSparse: false,
        content: stdin,
      });
      files.sort((a, b) => a.path.localeCompare(b.path));
    }
    return { stdout: '', stderr, exitCode, files };
  }

  return { stdout: stdin, stderr, exitCode, files };
}

function isSystemAdminCommand(cmd: string, scenario: ScenarioItem): boolean {
  const hasFiles = Object.keys(scenario.setup_files ?? {}).length > 0;
  if (!hasFiles) return true;
  return /^(systemctl|journalctl|firewall-cmd|nmcli|semanage|restorecon|setsebool|getsebool|getenforce|setenforce|sestatus|tuned-adm|hostnamectl|timedatectl|chronyc|ip\s|ss\s|systemd-|loginctl|dig\s|tracepath|tcpdump|nc\s|ausearch)/.test(
    cmd.trim(),
  );
}

export function executeInBrowserSandbox(
  rawCommand: string,
  scenario: ScenarioItem,
  currentFiles: SandboxFile[],
  grade: boolean,
): SandboxExecutionResult {
  const cleanCmd = rawCommand.trim();
  if (!cleanCmd) {
    return {
      passed: grade ? false : null,
      stdout: '',
      stderr: 'Empty command entered.',
      exitCode: 1,
      feedback: 'Empty command entered.',
      files: currentFiles,
    };
  }

  if (!grade) {
    const res = runPipeline(cleanCmd, currentFiles);
    return {
      passed: null,
      stdout: res.stdout,
      stderr: res.stderr,
      exitCode: res.exitCode,
      feedback: `Sandbox run exited with code ${res.exitCode}.`,
      files: res.files,
    };
  }

  let regexMatched = false;
  for (const pattern of scenario.accepted_regex ?? []) {
    try {
      if (new RegExp(pattern).test(cleanCmd)) {
        regexMatched = true;
        break;
      }
    } catch {
      // Ignore malformed pattern
    }
  }

  if (isSystemAdminCommand(cleanCmd, scenario) && Object.keys(scenario.setup_files ?? {}).length === 0) {
    if (regexMatched) {
      return {
        passed: true,
        stdout: simulateRhelOutput(cleanCmd, scenario),
        stderr: '',
        exitCode: 0,
        feedback: 'Validated: RHEL 9/10 command syntax and flags satisfy the objective.',
        files: currentFiles,
      };
    }

    const isReadOnlyInspect = /^(ls|pwd|echo|cat|head|tail|whoami|uname)\b/.test(cleanCmd);
    if (isReadOnlyInspect) {
      const res = runPipeline(cleanCmd, currentFiles);
      return {
        passed: false,
        stdout: res.stdout,
        stderr: res.stderr,
        exitCode: res.exitCode,
        feedback: 'Command executed, but it does not solve the target RHEL objective.',
        files: res.files,
      };
    }

    return {
      passed: false,
      stdout: '',
      stderr: '',
      exitCode: 1,
      feedback: 'Syntax or required flags did not match the RHEL 9/10 objective. Use Hint or Quick Reference.',
      files: currentFiles,
    };
  }

  const userRes = runPipeline(cleanCmd, currentFiles);

  if (!regexMatched && scenario.solution) {
    const refFiles = buildVirtualFiles(scenario);
    const refRes = runPipeline(scenario.solution, refFiles);
    if (refRes.stdout.trim() !== '' && userRes.stdout.trim() === refRes.stdout.trim() && userRes.exitCode === 0) {
      return {
        passed: true,
        stdout: userRes.stdout,
        stderr: userRes.stderr,
        exitCode: userRes.exitCode,
        feedback: 'Exact match: output matches target result.',
        files: userRes.files,
      };
    }
  }

  if (regexMatched) {
    return {
      passed: true,
      stdout: userRes.stdout,
      stderr: userRes.stderr,
      exitCode: 0,
      feedback: 'Validated: command syntax and arguments satisfy the objective.',
      files: userRes.files,
    };
  }

  const failMsg =
    userRes.exitCode !== 0 && userRes.stderr.trim()
      ? `Command exited with code ${userRes.exitCode}: ${userRes.stderr.trim().slice(0, 100)}`
      : 'Output or flags did not satisfy the target objective. Review Hint or Scratch Files.';

  return {
    passed: false,
    stdout: userRes.stdout,
    stderr: userRes.stderr,
    exitCode: userRes.exitCode,
    feedback: failMsg,
    files: userRes.files,
  };
}
