import { renderDesignScreen } from './screens/DesignScreen';
import { renderDialogueScreen } from './screens/DialogueScreen';
import { renderListeningScreen } from './screens/ListeningScreen';
import { renderMapScreen } from './screens/MapScreen';
import { applySettingsToDocument, renderProfileScreen } from './screens/ProfileScreen';
import { renderReadingScreen } from './screens/ReadingScreen';
import { renderReviewScreen } from './screens/ReviewScreen';
import { renderVocabLessonScreen } from './screens/VocabLessonScreen';
import { renderWritingScreen } from './screens/WritingScreen';
import { ensureSettings } from './services/srsEngine';
import { escapeHtml } from './utils/html';

let currentCleanup: (() => void) | null = null;

export async function startRouter(root: HTMLElement): Promise<void> {
  const settings = await ensureSettings();
  applySettingsToDocument(settings);

  const navigate = async () => {
    if (currentCleanup) {
      currentCleanup();
      currentCleanup = null;
    }

    const raw = (window.location.hash || '#/').replace(/^#/, '');
    const parts = raw.split('/').filter(Boolean);

    try {
      if (parts.length === 0) {
        currentCleanup = await renderMapScreen(root);
      } else if (parts[0] === 'lesson' && parts[1]) {
        currentCleanup = await renderVocabLessonScreen(root, parts[1]);
      } else if (parts[0] === 'dialogue' && parts[1]) {
        currentCleanup = await renderDialogueScreen(root, parts[1]);
      } else if (parts[0] === 'reading') {
        currentCleanup = await renderReadingScreen(root, parts[1] ?? 'r-t1');
      } else if (parts[0] === 'listening') {
        currentCleanup = await renderListeningScreen(root, parts[1] ?? 't1-nghe');
      } else if (parts[0] === 'writing') {
        currentCleanup = await renderWritingScreen(root, parts[1] ?? 't1-viet');
      } else if (parts[0] === 'review') {
        currentCleanup = await renderReviewScreen(root);
      } else if (parts[0] === 'profile') {
        currentCleanup = await renderProfileScreen(root);
      } else if (parts[0] === 'design') {
        renderDesignScreen(root);
      } else {
        currentCleanup = await renderMapScreen(root);
      }
    } catch (err) {
      root.innerHTML = `
        <div style="max-width:520px;margin:48px auto;padding:24px;" class="clay-card">
          <h2 style="margin:0 0 8px;">Không tải được màn hình</h2>
          <p style="color:var(--ink-muted);margin:0 0 16px;">${escapeHtml(err instanceof Error ? err.message : 'Lỗi không xác định')}</p>
          <a href="#/" class="btn btn-comm">Về trang chủ</a>
        </div>
      `;
    }
  };

  window.addEventListener('hashchange', navigate);
  await navigate();
}
