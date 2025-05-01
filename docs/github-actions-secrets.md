# GitHub Actionsシークレットの設定方法

Supabaseマイグレーションワークフローを使用するには、以下のシークレット（機密情報）をGitHubリポジトリに設定する必要があります。

## 必要なシークレット

### 本番環境（mainブランチ）
1. `SUPABASE_ACCESS_TOKEN` - Supabase CLIアクセストークン
2. `SUPABASE_PROJECT_ID` - 本番環境のSupabaseプロジェクトID
3. `SUPABASE_DB_PASSWORD` - 本番環境のSupabaseデータベースパスワード

### ステージング環境（developブランチ）
1. `SUPABASE_ACCESS_TOKEN` - Supabase CLIアクセストークン（本番環境と共通で使用可能）
2. `SUPABASE_STAGING_PROJECT_ID` - ステージング環境のSupabaseプロジェクトID
3. `SUPABASE_STAGING_DB_PASSWORD` - ステージング環境のSupabaseデータベースパスワード

## シークレットの設定方法

### リポジトリ全体で共有するシークレット

1. GitHubリポジトリのページで「Settings」タブをクリックします。
2. 左側のメニューから「Secrets and variables」→「Actions」を選択します。
3. 「New repository secret」ボタンをクリックします。
4. シークレットの名前と値を入力して保存します。

### 環境ごとのシークレット（本番/ステージング）

1. GitHubリポジトリのページで「Settings」タブをクリックします。
2. 左側のメニューから「Environments」を選択します。
3. 「New environment」ボタンをクリックし、`production`と`staging`の2つの環境を作成します。
4. 各環境をクリックし、「Environment secrets」セクションで「Add secret」ボタンを使用して環境固有のシークレットを追加します。

## シークレットの取得方法

### SUPABASE_ACCESS_TOKEN

1. [Supabaseダッシュボード](https://app.supabase.io/)にログインします。
2. 右上のユーザーアイコンをクリックし、「Access Tokens」を選択します。
3. 「Generate New Token」をクリックして新しいトークンを作成します。
4. 作成したトークンをコピーします（一度しか表示されないので注意）。

### プロジェクトID（SUPABASE_PROJECT_ID, SUPABASE_STAGING_PROJECT_ID）

1. [Supabaseダッシュボード](https://app.supabase.io/)で対象の環境のプロジェクトを選択します。
2. 「Project Settings」→「General」を選択します。
3. 「Project ID」の値をコピーします。

### データベースパスワード（SUPABASE_DB_PASSWORD, SUPABASE_STAGING_DB_PASSWORD）

1. [Supabaseダッシュボード](https://app.supabase.io/)で対象の環境のプロジェクトを選択します。
2. 「Project Settings」→「Database」を選択します。
3. 「Database Password」セクションで「View」または「Reset」でパスワードを確認します。

## 注意事項

- これらのシークレットは機密情報です。公開リポジトリではGitHub Secretsを使って保護し、コード内に直接記述しないでください。
- シークレットを変更した場合は、関連するワークフローを再実行する必要があります。
- 環境変数の名前はワークフローファイル内の参照名と完全に一致する必要があります。
- ワークフローファイルで`environment: production`や`environment: staging`を指定すると、その環境に設定されたシークレットのみが利用可能になります。 