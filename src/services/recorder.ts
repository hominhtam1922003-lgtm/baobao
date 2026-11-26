export interface ShadowRecorder {
  supported: boolean;
  start: () => Promise<boolean>;
  stop: () => Promise<string | null>;
}

export function createShadowRecorder(): ShadowRecorder {
  const supported =
    typeof navigator !== 'undefined' &&
    Boolean(navigator.mediaDevices?.getUserMedia) &&
    typeof MediaRecorder !== 'undefined';

  let recorder: MediaRecorder | null = null;
  let stream: MediaStream | null = null;
  let chunks: BlobPart[] = [];

  return {
    supported,
    async start() {
      if (!supported) return false;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        chunks = [];
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = (ev) => {
          if (ev.data.size > 0) chunks.push(ev.data);
        };
        recorder.start();
        return true;
      } catch {
        return false;
      }
    },
    stop() {
      return new Promise((resolve) => {
        if (!recorder) {
          resolve(null);
          return;
        }
        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' });
          stream?.getTracks().forEach((t) => t.stop());
          stream = null;
          recorder = null;
          resolve(URL.createObjectURL(blob));
        };
        recorder.stop();
      });
    },
  };
}
