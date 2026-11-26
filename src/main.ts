import '@fontsource/baloo-2/vietnamese-500.css';
import '@fontsource/baloo-2/vietnamese-700.css';
import '@fontsource/baloo-2/vietnamese-800.css';
import '@fontsource/baloo-2/latin-500.css';
import '@fontsource/baloo-2/latin-700.css';
import '@fontsource/baloo-2/latin-800.css';
import '@fontsource/noto-sans-sc/chinese-simplified-400.css';
import '@fontsource/noto-sans-sc/chinese-simplified-700.css';

import './styles/tokens.css';
import './styles/base.css';
import { registerPwa } from './services/pwa';
import { startRouter } from './router';

registerPwa();

const app = document.getElementById('app');
if (app) {
  startRouter(app);
}
