import '@testing-library/jest-dom';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// テスト間でReactコンポーネントをクリーンアップ
afterEach(() => {
  cleanup();
}); 