import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/tests/setup.ts'],
    // Vitestのテスト対象をsrcディレクトリ配下に限定
    // これによりe2eディレクトリのPlaywrightテストファイルが読み込まれるのを防ぐ
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    // 念のため、e2eディレクトリを明示的に除外
    exclude: ['node_modules', 'dist', 'e2e'],
    coverage: {
      reporter: ['text', 'json', 'html'],
    },
  },
}); 