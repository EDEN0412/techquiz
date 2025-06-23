import { defineConfig, devices } from '@playwright/test';

/**
 * Playwrightの設定ファイル
 * ユーザーフロー検証テスト（E2Eテスト）用の設定
 */

// 動的ポート検出のための関数
const getDevServerPort = () => {
  // 環境変数からポート取得を試行
  const envPort = process.env.VITE_PORT || process.env.PORT;
  if (envPort) return parseInt(envPort);
  
  // デフォルトポートとフォールバック
  const defaultPorts = [5173, 5174, 5175, 3000];
  return defaultPorts[0]; // 最初のポートをデフォルトとして使用
};

const DEV_SERVER_PORT = getDevServerPort();
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || `http://localhost:${DEV_SERVER_PORT}`;

// CI環境の検出
const isCI = !!process.env.CI;

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
  reporter: isCI 
    ? [
        ['github-actions'],
        ['html', { open: 'never' }],
        ['junit', { outputFile: 'test-results/junit-results.xml' }]
      ]
    : [
        ['list'],
        ['html', { open: 'on-failure' }]
      ],
  
  // 全テスト共通の設定
  use: {
    // ベースURL
    baseURL: BASE_URL,
    
    // テスト実行時にブラウザのトレースを取得
    trace: 'on-first-retry',
    
    // スクリーンショット撮影タイミング
    screenshot: 'only-on-failure',
    
    // 動画録画設定
    video: isCI ? 'retain-on-failure' : 'off',
    
    // ビューポートサイズ（モバイル対応確認）
    viewport: { width: 1280, height: 720 },
    
    // タイムアウト設定
    actionTimeout: 30000,
    navigationTimeout: 60000,
  },

  // ブラウザ別のプロジェクト設定
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // CI環境ではヘッドレスモードで実行
        headless: isCI ? true : false
      },
    },
    
    // CI環境以外では複数ブラウザでテスト
    ...(!isCI ? [
      {
        name: 'firefox',
        use: { ...devices['Desktop Firefox'] },
      },
      {
        name: 'webkit',
        use: { ...devices['Desktop Safari'] },
      },
      
      // Mobile Chrome
      {
        name: 'Mobile Chrome',
        use: { ...devices['Pixel 5'] },
      },
      
      // Mobile Safari
      {
        name: 'Mobile Safari',
        use: { ...devices['iPhone 12'] },
      },
    ] : []),
  ],

  // 開発サーバーの自動起動設定（CI環境以外）
  webServer: !isCI ? {
    command: `npm run preview -- --port ${DEV_SERVER_PORT}`,
    port: DEV_SERVER_PORT,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  } : undefined,

  // 出力ディレクトリ
  outputDir: 'test-results/',
  
  // タイムアウト設定の詳細
  timeout: 60 * 1000, // 各テストのタイムアウト：60秒
  expect: {
    timeout: 10 * 1000, // expectアサーションのタイムアウト：10秒
  },
}); 