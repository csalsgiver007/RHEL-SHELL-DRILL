import express from 'express';
import type { Request, Response } from 'express';
import { exec } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface Scenario {
  id: string;
  category: string;
  title: string;
  difficulty: string;
  description: string;
  objective: string;
  hints: string[];
  solution: string;
  accepted_regex: string[];
  setup_files?: Record<string, string>;
  setup_perms?: Record<string, number>;
  verify_cmd?: string;
}

interface SandboxFile {
  path: string;
  mode: string;
  size: number;
  isSparse: boolean;
  content: string;
}

interface SessionWorkspace {
  dir: string;
  scenarioId: string | null;
  lastActive: number;
}

const PORT = Number(process.env.PORT) || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');
const DIST_DIR = path.join(__dirname, 'dist');
const SCENARIOS_PATH = path.join(PUBLIC_DIR, 'all_scenarios.json');

let scenarios: Scenario[] = [];
const scenarioMap = new Map<string, Scenario>();

function loadScenarios() {
  const raw = fs.readFileSync(SCENARIOS_PATH, 'utf-8');
  scenarios = JSON.parse(raw) as Scenario[];
  scenarioMap.clear();
  for (const s of scenarios) {
    scenarioMap.set(s.id, s);
  }
}

loadScenarios();

const workspaces = new Map<string, SessionWorkspace>();
const SESSION_TTL_MS = 30 * 60 * 1000;

setInterval(() => {
  const now = Date.now();
  for (const [sid, ws] of workspaces.entries()) {
    if (now - ws.lastActive > SESSION_TTL_MS) {
      fs.rmSync(ws.dir, { recursive: true, force: true });
      workspaces.delete(sid);
    }
  }
}, 5 * 60 * 1000).unref();

function sanitizeSessionId(raw: unknown): string {
  if (typeof raw !== 'string' || !/^[a-zA-Z0-9_-]{4,64}$/.test(raw)) {
    return 'default-session';
  }
  return raw;
}

function getOrCreateWorkspace(sessionId: string): SessionWorkspace {
  let ws = workspaces.get(sessionId);
  if (!ws || !fs.existsSync(ws.dir)) {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), `shell-drill-${sessionId}-`));
    ws = { dir, scenarioId: null, lastActive: Date.now() };
    workspaces.set(sessionId, ws);
  } else {
    ws.lastActive = Date.now();
  }
  return ws;
}

function clearDirectory(targetDir: string) {
  for (const entry of fs.readdirSync(targetDir)) {
    fs.rmSync(path.join(targetDir, entry), { recursive: true, force: true });
  }
}

function populateWorkspace(targetDir: string, scenario: Scenario) {
  clearDirectory(targetDir);
  const setupFiles = scenario.setup_files ?? {};
  for (const [relPath, fileData] of Object.entries(setupFiles)) {
    const resolved = path.resolve(targetDir, relPath);
    if (!resolved.startsWith(targetDir + path.sep)) {
      continue;
    }
    fs.mkdirSync(path.dirname(resolved), { recursive: true });
    if (typeof fileData === 'string' && fileData.startsWith('__SPARSE_BYTES:')) {
      const sparseSize = Number.parseInt(fileData.split(':')[1] || '0', 10);
      const fd = fs.openSync(resolved, 'w');
      fs.ftruncateSync(fd, Number.isFinite(sparseSize) ? sparseSize : 0);
      fs.closeSync(fd);
    } else {
      fs.writeFileSync(resolved, fileData ?? '', 'utf-8');
    }
  }

  const setupPerms = scenario.setup_perms ?? {};
  for (const [relPath, mode] of Object.entries(setupPerms)) {
    const resolved = path.resolve(targetDir, relPath);
    if (!resolved.startsWith(targetDir + path.sep)) {
      continue;
    }
    if (fs.existsSync(resolved) && typeof mode === 'number') {
      try {
        fs.chmodSync(resolved, mode);
      } catch {
        // Ignore chmod failure if unsupported
      }
    }
  }
}

function listWorkspaceFiles(targetDir: string, baseDir = targetDir): SandboxFile[] {
  const results: SandboxFile[] = [];
  if (!fs.existsSync(targetDir)) {
    return results;
  }
  const entries = fs.readdirSync(targetDir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  for (const entry of entries) {
    const fullPath = path.join(targetDir, entry.name);
    const relPath = path.relative(baseDir, fullPath);
    if (entry.isDirectory()) {
      results.push(...listWorkspaceFiles(fullPath, baseDir));
    } else if (entry.isFile()) {
      const stat = fs.statSync(fullPath);
      const modeOctal = '0' + (stat.mode & 0o7777).toString(8).padStart(3, '0');
      const isSparse = stat.size > 1024 * 1024;
      let content = '';
      if (isSparse) {
        content = `[Sparse binary file: ${stat.size.toLocaleString()} bytes (${Math.round(stat.size / (1024 * 1024))} MiB)]`;
      } else {
        try {
          const buf = fs.readFileSync(fullPath);
          content = buf.subarray(0, 32768).toString('utf-8');
          if (buf.length > 32768) {
            content += '\n... [truncated preview]';
          }
        } catch {
          content = '[Unreadable file]';
        }
      }
      results.push({
        path: relPath,
        mode: modeOctal,
        size: stat.size,
        isSparse,
        content,
      });
    }
  }
  return results;
}

function snapshotDirForCompare(targetDir: string): Record<string, string> {
  const snap: Record<string, string> = {};
  const files = listWorkspaceFiles(targetDir);
  for (const f of files) {
    snap[f.path] = `${f.mode}|${f.size}|${f.isSparse ? 'sparse' : f.content}`;
  }
  return snap;
}

function snapshotsEqual(a: Record<string, string>, b: Record<string, string>): boolean {
  const keysA = Object.keys(a).sort();
  const keysB = Object.keys(b).sort();
  if (keysA.length !== keysB.length) return false;
  for (let i = 0; i < keysA.length; i++) {
    if (keysA[i] !== keysB[i]) return false;
    if (a[keysA[i]] !== b[keysB[i]]) return false;
  }
  return true;
}

const BLOCKED_COMMAND_PATTERNS: RegExp[] = [
  /rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive.*--force|-[a-zA-Z]*f[a-zA-Z]*r)\s+\/(\s|$|\*)/,
  /:\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:/,
  /\b(mkfs|shutdown|reboot|halt|poweroff|init\s+0|init\s+6)\b/,
  />\s*\/dev\/(sd|nvme|vd|hd|loop)/,
  /\bdd\b.*\bof=\/dev\//,
];

function isCommandSafe(cmd: string): string | null {
  for (const pattern of BLOCKED_COMMAND_PATTERNS) {
    if (pattern.test(cmd)) {
      return 'Command blocked by sandbox safety policy.';
    }
  }
  return null;
}

function runBash(
  cmd: string,
  cwd: string,
  timeoutMs = 5000,
): Promise<{ stdout: string; stderr: string; exitCode: number; timedOut: boolean }> {
  return new Promise((resolve) => {
    exec(
      cmd,
      {
        cwd,
        shell: '/bin/bash',
        timeout: timeoutMs,
        maxBuffer: 256 * 1024,
        env: {
          PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
          HOME: cwd,
          LANG: 'C.UTF-8',
          LC_ALL: 'C.UTF-8',
          TERM: 'xterm-256color',
        },
      },
      (error, stdout, stderr) => {
        if (error) {
          const timedOut = Boolean((error as { killed?: boolean }).killed);
          const code = typeof error.code === 'number' ? error.code : 1;
          resolve({
            stdout: stdout ?? '',
            stderr: stderr ?? (timedOut ? 'Execution timed out (5.0s limit).' : error.message),
            exitCode: code,
            timedOut,
          });
          return;
        }
        resolve({
          stdout: stdout ?? '',
          stderr: stderr ?? '',
          exitCode: 0,
          timedOut: false,
        });
      },
    );
  });
}

function simulateRhelOutput(cmd: string, scenario: Scenario): string {
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

function isSystemAdminScenario(scenario: Scenario): boolean {
  const hasFiles = Object.keys(scenario.setup_files ?? {}).length > 0;
  if (hasFiles) return false;
  return (
    scenario.category === 'Service Management' ||
    scenario.category === 'Firewall & Network' ||
    /^(systemctl|journalctl|firewall-cmd|nmcli|semanage|restorecon|setsebool|tuned-adm|hostnamectl|timedatectl|chronyc|ip\s|ss\s|systemd-)/.test(
      scenario.solution.trim(),
    )
  );
}

async function startServer() {
  const app = express();
  app.use(express.json({ limit: '512kb' }));

  app.get('/api/health', (_req: Request, res: Response) => {
    res.json({ status: 'ok', scenarioCount: scenarios.length });
  });

  app.get('/api/scenarios', (req: Request, res: Response) => {
    const category = typeof req.query.category === 'string' ? req.query.category : '';
    const difficulty = typeof req.query.difficulty === 'string' ? req.query.difficulty : '';
    const search = typeof req.query.search === 'string' ? req.query.search.trim().toLowerCase() : '';

    const categoryCounts: Record<string, number> = {};
    for (const s of scenarios) {
      categoryCounts[s.category] = (categoryCounts[s.category] || 0) + 1;
    }

    let filtered = scenarios;
    if (category && category !== 'All') {
      filtered = filtered.filter((s) => s.category === category);
    }
    if (difficulty && difficulty !== 'All') {
      filtered = filtered.filter((s) => s.difficulty === difficulty);
    }
    if (search) {
      filtered = filtered.filter(
        (s) =>
          s.id.toLowerCase().includes(search) ||
          s.title.toLowerCase().includes(search) ||
          s.description.toLowerCase().includes(search) ||
          s.objective.toLowerCase().includes(search) ||
          s.category.toLowerCase().includes(search),
      );
    }

    const sanitized = filtered.map((s) => ({
      id: s.id,
      category: s.category,
      title: s.title,
      difficulty: s.difficulty,
      description: s.description,
      objective: s.objective,
      hints: s.hints ?? [],
      setup_files: s.setup_files ?? {},
      setup_perms: s.setup_perms ?? {},
    }));

    res.json({
      total: scenarios.length,
      categoryCounts,
      scenarios: sanitized,
    });
  });

  app.post('/api/scenarios/:id/reveal', (req: Request, res: Response) => {
    const scenario = scenarioMap.get(req.params.id);
    if (!scenario) {
      res.status(404).json({ error: 'Scenario not found' });
      return;
    }
    res.json({ id: scenario.id, solution: scenario.solution });
  });

  app.post('/api/sandbox/setup', (req: Request, res: Response) => {
    const sessionId = sanitizeSessionId(req.body?.sessionId);
    const scenarioId = typeof req.body?.scenarioId === 'string' ? req.body.scenarioId : '';
    const scenario = scenarioMap.get(scenarioId);
    if (!scenario) {
      res.status(404).json({ error: 'Scenario not found' });
      return;
    }

    const ws = getOrCreateWorkspace(sessionId);
    populateWorkspace(ws.dir, scenario);
    ws.scenarioId = scenario.id;

    res.json({
      scenarioId: scenario.id,
      files: listWorkspaceFiles(ws.dir),
    });
  });

  app.post('/api/sandbox/execute', async (req: Request, res: Response) => {
    const sessionId = sanitizeSessionId(req.body?.sessionId);
    const scenarioId = typeof req.body?.scenarioId === 'string' ? req.body.scenarioId : '';
    const rawCommand = typeof req.body?.command === 'string' ? req.body.command : '';
    const grade = req.body?.grade !== false;

    const scenario = scenarioMap.get(scenarioId);
    if (!scenario) {
      res.status(404).json({ error: 'Scenario not found' });
      return;
    }

    const cleanCmd = rawCommand.trim();
    if (!cleanCmd) {
      res.status(400).json({ error: 'Empty command entered.' });
      return;
    }

    const safetyError = isCommandSafe(cleanCmd);
    if (safetyError) {
      res.json({
        passed: grade ? false : null,
        stdout: '',
        stderr: safetyError,
        exitCode: 1,
        feedback: safetyError,
        files: [],
      });
      return;
    }

    const ws = getOrCreateWorkspace(sessionId);
    if (ws.scenarioId !== scenario.id) {
      populateWorkspace(ws.dir, scenario);
      ws.scenarioId = scenario.id;
    }

    // Explore-only run (does not grade attempt)
    if (!grade) {
      const result = await runBash(cleanCmd, ws.dir, 5000);
      res.json({
        passed: null,
        stdout: result.stdout,
        stderr: result.stderr,
        exitCode: result.exitCode,
        feedback: result.timedOut
          ? 'Command timed out (5.0s limit).'
          : `Sandbox run exited with code ${result.exitCode}.`,
        files: listWorkspaceFiles(ws.dir),
      });
      return;
    }

    // Grade mode
    let regexMatched = false;
    for (const pattern of scenario.accepted_regex ?? []) {
      try {
        if (new RegExp(pattern).test(cleanCmd)) {
          regexMatched = true;
          break;
        }
      } catch {
        // Ignore invalid regex
      }
    }

    // Handle RHEL system-state scenarios (systemd, firewalld, NetworkManager, SELinux, or system paths)
    if (isSystemAdminScenario(scenario)) {
      if (regexMatched) {
        res.json({
          passed: true,
          stdout: simulateRhelOutput(cleanCmd, scenario),
          stderr: '',
          exitCode: 0,
          feedback: 'Validated: RHEL 9/10 command syntax and flags satisfy the objective.',
          files: listWorkspaceFiles(ws.dir),
        });
        return;
      }

      // Allow harmless inspection commands inside scratch without passing
      const isReadOnlyInspect = /^(ls|pwd|echo|cat|head|tail|whoami|uname)\b/.test(cleanCmd);
      if (isReadOnlyInspect) {
        const inspectRes = await runBash(cleanCmd, ws.dir, 3000);
        res.json({
          passed: false,
          stdout: inspectRes.stdout,
          stderr: inspectRes.stderr,
          exitCode: inspectRes.exitCode,
          feedback: 'Command executed, but it does not solve the target RHEL objective.',
          files: listWorkspaceFiles(ws.dir),
        });
        return;
      }

      res.json({
        passed: false,
        stdout: '',
        stderr: '',
        exitCode: 1,
        feedback: 'Syntax or required flags did not match the RHEL 9/10 objective. Use Hint or Quick Reference.',
        files: listWorkspaceFiles(ws.dir),
      });
      return;
    }

    // Real bash execution inside isolated scratch workspace
    const hasSetupFiles = Object.keys(scenario.setup_files ?? {}).length > 0;
    const initialSnap = hasSetupFiles ? snapshotDirForCompare(ws.dir) : {};
    const userRes = await runBash(cleanCmd, ws.dir, 5000);

    if (userRes.timedOut) {
      res.json({
        passed: false,
        stdout: userRes.stdout,
        stderr: userRes.stderr,
        exitCode: userRes.exitCode,
        feedback: 'Execution timed out (5.0s limit).',
        files: listWorkspaceFiles(ws.dir),
      });
      return;
    }

    // 1. Check audit.log special case
    if (cleanCmd.includes('audit.log')) {
      const auditPath = path.join(ws.dir, 'audit.log');
      if (fs.existsSync(auditPath)) {
        const auditText = fs.readFileSync(auditPath, 'utf-8');
        if (auditText.includes('Missing database credentials') && auditText.includes('Deploying artifacts')) {
          res.json({
            passed: true,
            stdout: userRes.stdout,
            stderr: userRes.stderr,
            exitCode: userRes.exitCode,
            feedback: 'Exact match: stdout and stderr both captured in audit.log.',
            files: listWorkspaceFiles(ws.dir),
          });
          return;
        }
      }
    }

    // 2. Reference comparison when scenario has setup_files and regex didn't already match
    if (hasSetupFiles && !regexMatched && userRes.exitCode === 0) {
      const refDir = fs.mkdtempSync(path.join(os.tmpdir(), 'shell-drill-ref-'));
      try {
        populateWorkspace(refDir, scenario);
        const refRes = await runBash(scenario.solution, refDir, 5000);
        if (refRes.exitCode === 0) {
          if (refRes.stdout.trim() !== '' && userRes.stdout.trim() === refRes.stdout.trim()) {
            res.json({
              passed: true,
              stdout: userRes.stdout,
              stderr: userRes.stderr,
              exitCode: userRes.exitCode,
              feedback: 'Exact match: output matches target result.',
              files: listWorkspaceFiles(ws.dir),
            });
            return;
          }
          // Check file mutation equivalence (e.g., sed -i, redirection, chmod)
          if (refRes.stdout.trim() === '' && userRes.stdout.trim() === '') {
            const userSnap = snapshotDirForCompare(ws.dir);
            const refSnap = snapshotDirForCompare(refDir);
            if (!snapshotsEqual(userSnap, initialSnap) && snapshotsEqual(userSnap, refSnap)) {
              res.json({
                passed: true,
                stdout: userRes.stdout,
                stderr: userRes.stderr,
                exitCode: userRes.exitCode,
                feedback: 'Exact match: workspace files match expected target state.',
                files: listWorkspaceFiles(ws.dir),
              });
              return;
            }
          }
        }
      } finally {
        fs.rmSync(refDir, { recursive: true, force: true });
      }
    }

    // 3. Accepted regex fallback (handles pipelines/commands referencing external system paths like /var/log or /etc)
    if (regexMatched) {
      res.json({
        passed: true,
        stdout: userRes.stdout,
        stderr: hasSetupFiles ? userRes.stderr : '',
        exitCode: 0,
        feedback: 'Validated: command syntax and arguments satisfy the objective.',
        files: listWorkspaceFiles(ws.dir),
      });
      return;
    }

    const failMsg =
      userRes.exitCode !== 0 && userRes.stderr.trim()
        ? `Command exited with code ${userRes.exitCode}: ${userRes.stderr.trim().slice(0, 100)}`
        : 'Output or flags did not satisfy the target objective. Review Hint or Scratch Files.';

    res.json({
      passed: false,
      stdout: userRes.stdout,
      stderr: userRes.stderr,
      exitCode: userRes.exitCode,
      feedback: failMsg,
      files: listWorkspaceFiles(ws.dir),
    });
  });

  // Explicit download endpoints from public/
  for (const asset of ['shell-drill', 'shell_drill.py', 'shell-drill.zip', 'shell-drill.tar.gz', 'install.sh', 'all_scenarios.json']) {
    app.get(`/${asset}`, (_req: Request, res: Response) => {
      const filePath = path.join(PUBLIC_DIR, asset);
      if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
      } else {
        res.status(404).send('Not found');
      }
    });
  }

  if (process.env.NODE_ENV !== 'production') {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: {
        middlewareMode: true,
        hmr: false,
      },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(DIST_DIR));
    app.use(express.static(PUBLIC_DIR));
    app.get('*', (_req: Request, res: Response) => {
      res.sendFile(path.join(DIST_DIR, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`shell-drill web server listening on http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error('Failed to start server:', err);
  process.exit(1);
});
