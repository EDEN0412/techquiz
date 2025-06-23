# GitHub Actions Secrets and Variables 設定ガイド

このドキュメントでは、Techquizプロジェクトのデプロイに必要なGitHub ActionsのSecretsとVariablesの設定方法を説明します。

## 設定場所

GitHubリポジトリの **Settings** > **Secrets and variables** > **Actions** から設定します。

## 必要な設定

### Secrets（機密情報）

以下の値を **Secrets** タブから追加してください：

| Secret名 | 説明 | 例 |
|---------|------|-----|
| `AWS_ACCESS_KEY_ID` | AWSアクセスキーID | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWSシークレットアクセスキー | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `DATABASE_URL` | 本番環境のSupabaseデータベース接続URL | `postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres` |
| `DJANGO_SECRET_KEY` | Django本番環境用のシークレットキー | ランダムな50文字以上の文字列 |
| `VITE_API_BASE_URL` | フロントエンドが使用するAPIのベースURL | `https://api.your-domain.com` |
| `VITE_SUPABASE_URL` | SupabaseプロジェクトのURL | `https://[project-ref].supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Supabaseの匿名キー | Supabaseダッシュボードから取得 |
| `SUPABASE_ACCESS_TOKEN` | Supabase CLIアクセストークン | Supabaseダッシュボードから取得 |
| `SUPABASE_PROJECT_ID` | SupabaseプロジェクトID | `[project-ref]` |
| `DEPLOY_HOST` | デプロイ先サーバーのホスト名（オプション） | `your-server.com` |
| `DEPLOY_USER` | デプロイ用のユーザー名（オプション） | `deploy-user` |
| `DEPLOY_KEY` | デプロイ用のSSH秘密鍵（オプション） | SSH秘密鍵の内容 |

### Variables（公開可能な設定値）

以下の値を **Variables** タブから追加してください：

| Variable名 | 説明 | 例 |
|-----------|------|-----|
| `AWS_REGION` | AWSリージョン | `ap-northeast-1` |
| `S3_BUCKET` | フロントエンド用S3バケット名 | `techquiz-frontend-prod` |
| `CLOUDFRONT_DISTRIBUTION_ID` | CloudFrontディストリビューションID | `E1234567890ABC` |
| `PRODUCTION_URL` | 本番環境のフロントエンドURL | `https://www.your-domain.com` |
| `API_BASE_URL` | 本番環境のAPIベースURL | `https://api.your-domain.com` |

## 設定手順

### 1. Secretsの追加

1. リポジトリの **Settings** に移動
2. 左側のメニューから **Secrets and variables** > **Actions** を選択
3. **New repository secret** ボタンをクリック
4. **Name** フィールドにSecret名を入力（例: `AWS_ACCESS_KEY_ID`）
5. **Secret** フィールドに実際の値を入力
6. **Add secret** ボタンをクリック

### 2. Variablesの追加

1. 同じページで **Variables** タブに切り替え
2. **New repository variable** ボタンをクリック
3. **Name** フィールドにVariable名を入力（例: `AWS_REGION`）
4. **Value** フィールドに実際の値を入力
5. **Add variable** ボタンをクリック

## 環境別の設定

production環境とstaging環境で異なる値を使用する場合は、GitHub Environmentsを使用できます：

1. **Settings** > **Environments** から環境を作成
2. 各環境に固有のSecretsとVariablesを設定
3. ワークフローで `environment: production` または `environment: staging` を指定

## セキュリティのベストプラクティス

1. **最小権限の原則**: AWSアクセスキーは必要最小限の権限のみを持つIAMユーザーのものを使用
2. **定期的なローテーション**: シークレットキーは定期的に更新
3. **アクセス制限**: 本番環境へのデプロイは特定のブランチ（main）からのみ許可
4. **監査ログ**: GitHub Actionsのログで誰がいつデプロイしたかを確認可能

## トラブルシューティング

### エラー: `Invalid bucket name ""`

S3_BUCKETがVariablesに設定されていることを確認してください。

### エラー: `ModuleNotFoundError: No module named 'dotenv'`

このエラーは修正済みです。最新のワークフローファイルを使用してください。

### エラー: `no URL specified`

PRODUCTION_URLとAPI_BASE_URLがVariablesに設定されていることを確認してください。

## 参考リンク

- [GitHub Actions のシークレット](https://docs.github.com/ja/actions/security-guides/encrypted-secrets)
- [GitHub Actions の変数](https://docs.github.com/ja/actions/learn-github-actions/variables)
- [環境の使用](https://docs.github.com/ja/actions/deployment/targeting-different-environments/using-environments-for-deployment) 