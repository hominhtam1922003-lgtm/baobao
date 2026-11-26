import { defineConfig, type Plugin } from 'vite';
import fs from 'node:fs';
import path from 'node:path';

function copyDirSync(src: string, dest: string) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function contentStaticPlugin(base: string): Plugin {
  const contentRoot = path.resolve(__dirname, 'content');
  const prefix = `${base.replace(/\/$/, '')}/content/`;

  return {
    name: 'baobao-content-static',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const reqPath = (req.url || '').split('?')[0];
        if (!reqPath.startsWith(prefix)) return next();
        const rel = decodeURIComponent(reqPath.slice(prefix.length));
        const resolved = path.resolve(contentRoot, rel);
        if (!resolved.startsWith(contentRoot) || !fs.existsSync(resolved) || fs.statSync(resolved).isDirectory()) {
          res.statusCode = 404;
          res.end('Not found');
          return;
        }
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        fs.createReadStream(resolved).pipe(res);
      });
    },
    writeBundle(options) {
      const outDir = options.dir ? path.resolve(options.dir) : path.resolve(__dirname, 'dist');
      copyDirSync(contentRoot, path.join(outDir, 'content'));
    },
  };
}

export default defineConfig(({ command }) => {
  const base = command === 'build' ? (process.env.VITE_BASE || '/baobao/') : '/';
  return {
    base,
    plugins: [contentStaticPlugin(base)],
    build: {
      outDir: 'dist',
      sourcemap: false,
    },
  };
});
