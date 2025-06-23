import { defineConfig, devices } from '@playwright/test';

/**
 * Playwrightの設定ファイル
 * ユーザーフロー検証テスト（E2Eテスト）用の設定
 */
export default defineConfig({
  // テストファイルの場所を指定
  testDir: './e2e',
  
  // テストの並列実行を無効化（データベースの競合を避けるため）
  fullyParallel: false,
  
  // CI環境では失敗時にリトライしない
  forbidOnly: !!process.env.CI,
  
  // 失敗時のリトライ回数
  retries: process.env.CI ? 2 : 0,
  
  // 並列実行するワーカー数
  workers: process.env.CI ? 1 : undefined,
  
  // レポート形式（HTMLレポートとJUnitレポートを生成）
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],
  
  // 全テストで共通の設定
  use: {
    // ベースURL（ローカル開発サーバー）
    baseURL: 'http://localhost:5173',
    
    // 失敗時にスクリーンショットを撮影
    screenshot: 'only-on-failure',
    
    // 失敗時にビデオを録画
    video: 'retain-on-failure',
    
    // ブラウザのトレースを記録（デバッグ用）
    trace: 'on-first-retry',
  },

  // 異なるブラウザでのテスト設定
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    
    // 必要に応じて他のブラウザも追加可能
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  // テスト実行前にローカルサーバーを起動
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000, // 2分でタイムアウト
  },
}); 