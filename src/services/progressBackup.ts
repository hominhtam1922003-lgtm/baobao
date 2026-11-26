import { getDb, type ProgressRecord, type ReviewLogRecord, type SettingsRecord, type SrsCardRecord } from './db';

const AUTO_BACKUP_KEY = 'baobao-auto-backup';
let memoryAutoBackup: string | null = null;

export interface BackupPayload {
  version: 1;
  exportedAt: string;
  stores: {
    cards: SrsCardRecord[];
    reviewLog: ReviewLogRecord[];
    progress: ProgressRecord[];
    settings: SettingsRecord[];
  };
}

export async function exportBackupJson(): Promise<string> {
  const db = await getDb();
  const [cards, reviewLog, progress, settings] = await Promise.all([
    db.getAll('cards'),
    db.getAll('reviewLog'),
    db.getAll('progress'),
    db.getAll('settings'),
  ]);
  const payload: BackupPayload = {
    version: 1,
    exportedAt: new Date().toISOString(),
    stores: { cards, reviewLog, progress, settings },
  };
  return JSON.stringify(payload, null, 2);
}

export function getAutoBackup(): string | null {
  try {
    if (typeof localStorage !== 'undefined' && typeof localStorage.getItem === 'function') {
      return localStorage.getItem(AUTO_BACKUP_KEY) ?? memoryAutoBackup;
    }
  } catch {
    // ignore storage errors
  }
  return memoryAutoBackup;
}

function validateBackup(data: unknown): data is BackupPayload {
  if (!data || typeof data !== 'object') return false;
  const obj = data as Record<string, unknown>;
  if (obj.version !== 1) return false;
  if (!obj.stores || typeof obj.stores !== 'object') return false;
  const stores = obj.stores as Record<string, unknown>;
  return (
    Array.isArray(stores.cards) &&
    Array.isArray(stores.reviewLog) &&
    Array.isArray(stores.progress) &&
    Array.isArray(stores.settings)
  );
}

export async function importBackupJson(rawJson: string): Promise<{ ok: boolean; error?: string }> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(rawJson);
  } catch {
    return { ok: false, error: 'File sao lưu không phải JSON hợp lệ.' };
  }

  if (!validateBackup(parsed)) {
    return { ok: false, error: 'Cấu trúc file sao lưu không đúng định dạng BaoBao v1.' };
  }

  // Save current state as automatic safety snapshot before overwriting
  const currentSnapshot = await exportBackupJson();
  memoryAutoBackup = currentSnapshot;
  try {
    if (typeof localStorage !== 'undefined' && typeof localStorage.setItem === 'function') {
      localStorage.setItem(AUTO_BACKUP_KEY, currentSnapshot);
    }
  } catch {
    // ignore quota error on localStorage fallback
  }

  const db = await getDb();
  const tx = db.transaction(['cards', 'reviewLog', 'progress', 'settings'], 'readwrite');
  await Promise.all([
    tx.objectStore('cards').clear(),
    tx.objectStore('reviewLog').clear(),
    tx.objectStore('progress').clear(),
    tx.objectStore('settings').clear(),
  ]);

  for (const c of parsed.stores.cards) {
    if (c && typeof c.key === 'string') await tx.objectStore('cards').put(c);
  }
  for (const r of parsed.stores.reviewLog) {
    if (r && typeof r.key === 'string') await tx.objectStore('reviewLog').put(r);
  }
  for (const p of parsed.stores.progress) {
    if (
      p &&
      p.id === 'main' &&
      Number.isFinite(p.xp) &&
      Number.isFinite(p.streak) &&
      Number.isFinite(p.bestStreak) &&
      Number.isFinite(p.freezesLeft) &&
      p.skillXp &&
      Number.isFinite(p.skillXp.giaoTiep) &&
      Number.isFinite(p.skillXp.doc) &&
      Number.isFinite(p.skillXp.nghe) &&
      Number.isFinite(p.skillXp.viet)
    ) {
      await tx.objectStore('progress').put(p);
    } else {
      tx.abort();
      return { ok: false, error: 'Dữ liệu tiến độ trong file bị hỏng hoặc sai kiểu số.' };
    }
  }
  for (const s of parsed.stores.settings) {
    if (s && s.id === 'user') await tx.objectStore('settings').put(s);
  }

  await tx.done;
  return { ok: true };
}
