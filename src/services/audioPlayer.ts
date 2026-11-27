const base = import.meta.env.BASE_URL;

class AudioService {
  private current: HTMLAudioElement | null = null;
  private audioCtx: AudioContext | null = null;
  private sfxEnabled = true;

  setSfxEnabled(enabled: boolean) {
    this.sfxEnabled = enabled;
  }

  resolveUrl(relPath: string): string {
    return `${base}${relPath.replace(/^\//, '')}`;
  }

  preload(relPaths: (string | undefined)[]) {
    for (const rel of relPaths) {
      if (!rel) continue;
      const audio = new Audio();
      audio.preload = 'auto';
      audio.src = this.resolveUrl(rel);
    }
  }

  stop() {
    if (this.current) {
      this.current.pause();
      this.current.currentTime = 0;
      this.current = null;
    }
  }

  async play(relPath: string, rate = 1, onEnd?: () => void): Promise<void> {
    this.stop();
    const audio = new Audio(this.resolveUrl(relPath));
    audio.playbackRate = rate;
    this.current = audio;
    audio.addEventListener('ended', () => {
      if (this.current === audio) this.current = null;
      onEnd?.();
    });
    try {
      await audio.play();
    } catch {
      onEnd?.();
    }
  }

  private getCtx(): AudioContext | null {
    if (!this.sfxEnabled || typeof window === 'undefined') return null;
    const Ctor = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Ctor) return null;
    if (!this.audioCtx) this.audioCtx = new Ctor();
    return this.audioCtx;
  }

  playSfx(kind: 'pop' | 'ok' | 'err' | 'coin' | 'cheer') {
    const ctx = this.getCtx();
    if (!ctx) return;
    if (ctx.state === 'suspended') {
      ctx.resume().catch(() => {});
    }
    const now = ctx.currentTime;

    if (kind === 'coin') {
      [987.77, 1318.51].forEach((freq, i) => {
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.connect(g);
        g.connect(ctx.destination);
        o.type = 'sine';
        o.frequency.setValueAtTime(freq, now + i * 0.075);
        g.gain.setValueAtTime(0.11, now + i * 0.075);
        g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.075 + 0.18);
        o.start(now + i * 0.075);
        o.stop(now + i * 0.075 + 0.19);
      });
      return;
    }

    if (kind === 'cheer') {
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, i) => {
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.connect(g);
        g.connect(ctx.destination);
        o.type = 'triangle';
        o.frequency.setValueAtTime(freq, now + i * 0.07);
        g.gain.setValueAtTime(0.1, now + i * 0.07);
        g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.25);
        o.start(now + i * 0.07);
        o.stop(now + i * 0.07 + 0.26);
      });
      return;
    }

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    if (kind === 'pop') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(520, now);
      osc.frequency.exponentialRampToValueAtTime(740, now + 0.06);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
      osc.start(now);
      osc.stop(now + 0.075);
    } else if (kind === 'ok') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(587.33, now);
      osc.frequency.setValueAtTime(880, now + 0.08);
      gain.gain.setValueAtTime(0.11, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
      osc.start(now);
      osc.stop(now + 0.25);
    } else {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(160, now + 0.14);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
      osc.start(now);
      osc.stop(now + 0.16);
    }
  }
}

export const audioService = new AudioService();
