-- カテゴリテーブルの修正と不足カテゴリの追加
-- 重複と不足を解決してダッシュボードと一致させる

BEGIN;

-- 1. 重複したHTML/CSSカテゴリを削除（id=6を削除、id=1を保持）
DELETE FROM category WHERE id = 6 AND name = 'HTML/CSS';

-- 2. 既存カテゴリの名前を統一（HTML/CSS → HTML & CSS）
UPDATE category 
SET name = 'HTML & CSS',
    description = 'Webの基礎とスタイリングを習得',
    updated_at = NOW()
WHERE id = 1;

-- 3. 不足している4つのカテゴリを追加
INSERT INTO category (name, slug, description, icon, display_order, is_active, created_at, updated_at) VALUES
('Ruby', 'ruby', 'オブジェクト指向スクリプト言語の基礎', 'ruby', 2, true, NOW(), NOW()),
('Ruby on Rails', 'ruby-rails', 'Rubyベースの高速Webアプリケーション開発', 'rails', 3, true, NOW(), NOW()),
('Webアプリケーション基礎', 'web-app-basic', 'Webアプリ開発の基礎知識とアーキテクチャ', 'web', 5, true, NOW(), NOW()),
('データベース', 'database', 'SQLとデータベース管理', 'database', 9, true, NOW(), NOW());

-- 4. display_orderを適切に再設定（ダッシュボードのモックデータに合わせる）
UPDATE category SET display_order = 1, updated_at = NOW() WHERE slug = 'html-css';    -- HTML & CSS
UPDATE category SET display_order = 2, updated_at = NOW() WHERE slug = 'ruby';        -- Ruby  
UPDATE category SET display_order = 3, updated_at = NOW() WHERE slug = 'ruby-rails'; -- Ruby on Rails
UPDATE category SET display_order = 4, updated_at = NOW() WHERE slug = 'javascript';  -- JavaScript
UPDATE category SET display_order = 5, updated_at = NOW() WHERE slug = 'web-app-basic'; -- Webアプリケーション基礎
UPDATE category SET display_order = 6, updated_at = NOW() WHERE slug = 'python';      -- Python
UPDATE category SET display_order = 7, updated_at = NOW() WHERE slug = 'git';         -- Git
UPDATE category SET display_order = 8, updated_at = NOW() WHERE slug = 'linux';       -- Linux コマンド
UPDATE category SET display_order = 9, updated_at = NOW() WHERE slug = 'database';    -- データベース

-- 5. Linux カテゴリの名前を統一（Linuxコマンド → Linux コマンド）
UPDATE category 
SET name = 'Linux コマンド',
    description = '基本的なターミナル操作',
    updated_at = NOW()
WHERE slug = 'linux';

COMMIT;

-- 結果を確認するクエリ
SELECT id, name, slug, description, icon, display_order, is_active 
FROM category 
ORDER BY display_order;
