# Techquiz: DBマイグレーション管理手順書

## 1. 概要

本プロジェクトでは、**Djangoモデル定義を正として**、その定義に基づいてSupabase（PostgreSQL）のテーブル構造を自動的に同期する方式を採用しています。この手順書では、モデル変更時のマイグレーション手順、注意点、トラブルシューティング方法について説明します。

## 2. 基本方針

- **Djangoモデル定義を正とする**: データ構造の変更はDjangoモデルの修正から始める
- **`sync_supabase`コマンド**: モデル変更後は専用コマンドで同期を実行
- **自動同期機能**: Django標準のマイグレーション後に自動で同期する仕組みも実装済み
- **テスト駆動開発**: スキーマ変更前にユニットテストを作成し、変更後も動作を確認する

## 3. 開発フロー

### 3.1 新しいモデル作成時

1. Djangoモデルを作成し、`SupabaseModelMixin`を継承する
   ```python
   from techskillsquiz.supabase_mixins import SupabaseModelMixin
   from django.db import models
   
   class NewModel(SupabaseModelMixin, models.Model):
       name = models.CharField(max_length=100)
       
       # Supabaseテーブル名を指定（オプション、指定しない場合はモデルのdb_tableが使用される）
       supabase_table = 'new_models'
   ```

2. Djangoマイグレーションを作成・適用
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Supabaseとの同期を実行（通常は自動実行されるが、手動で確認したい場合）
   ```bash
   python manage.py sync_supabase --verbose
   ```

### 3.2 既存モデル変更時

1. Djangoモデルを変更（フィールド追加・修正・削除など）

2. Djangoマイグレーションを作成・適用
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. 必要に応じて手動同期を実行（特にデータ移行が必要な場合など）
   ```bash
   python manage.py sync_supabase --verbose
   ```

### 3.3 モデル削除時

1. Djangoモデルを削除するマイグレーションを作成・適用
   ```bash
   python manage.py makemigrations --name remove_obsolete_model
   python manage.py migrate
   ```

2. 手動でSupabaseテーブルを削除（オプション）
   - Supabase管理画面から該当テーブルを削除
   - または、SQL実行機能を使用してDROPコマンドを実行

## 4. 同期コマンド活用方法

`sync_supabase`コマンドには様々なオプションがあります：

### 4.1 基本的な使用方法

```bash
# 全モデルの同期
python manage.py sync_supabase

# 特定アプリのモデルのみ同期
python manage.py sync_supabase --app=users

# 特定モデルのみ同期
python manage.py sync_supabase --model=User

# 確認なしで実行
python manage.py sync_supabase --no-input

# 詳細ログ出力
python manage.py sync_supabase --verbose
```

### 4.2 整合性チェックと修復

```bash
# モデルとテーブルの整合性チェックのみ実行
python manage.py sync_supabase --check

# 不整合を検出して自動修正
python manage.py sync_supabase --check --fix
```

### 4.3 レポート生成

```bash
# 同期結果の詳細レポートを生成
python manage.py sync_supabase --report
```

## 5. 自動同期の仕組み

1. Djangoの`post_migrate`シグナルをフックして自動同期を実行
2. `settings.py`の`SUPABASE_AUTO_SYNC`設定で有効/無効を切り替え可能
   ```python
   # 自動同期を無効化
   SUPABASE_AUTO_SYNC = False
   ```

## 6. SupabaseModelMixinの適用

既存のモデルをSupabaseと同期するには：

1. モデルクラスに`SupabaseModelMixin`を追加
   ```python
   from techskillsquiz.supabase_mixins import SupabaseModelMixin
   
   class ExistingModel(SupabaseModelMixin, models.Model):
       # 既存のフィールド定義...
   ```

2. 必要に応じて`supabase_table`プロパティを設定
   ```python
   class ExistingModel(SupabaseModelMixin, models.Model):
       # 既存のフィールド定義...
       supabase_table = 'custom_table_name'  # 省略可能
   ```

3. 同期コマンドを実行
   ```bash
   python manage.py sync_supabase --model=ExistingModel --verbose
   ```

## 7. 複雑なスキーマ変更のケース

### 7.1 フィールド名変更

Djangoではフィールド名変更は「削除して新規作成」と認識されるため、注意が必要です：

1. 一時的な新フィールドを追加するマイグレーションを作成
2. データ移行ロジックを実装（RunPythonマイグレーション）
3. 古いフィールドを削除するマイグレーションを作成
4. 新フィールドの名前を目的の名前に変更するマイグレーションを作成

### 7.2 データ型変更

互換性のないデータ型変更も同様の手順で実施します。

## 8. 環境別の考慮事項

### 8.1 開発環境

- ローカルSupabaseインスタンスを使用
- `supabase start`コマンドでローカルサーバー起動
- `.env.development`ファイルで接続情報を設定

### 8.2 テスト環境

- テスト用の分離されたSupabaseプロジェクトを使用
- CI/CDパイプラインでテスト前に同期を実行
- `.env.test`ファイルで接続情報を設定

### 8.3 本番環境

- 本番用Supabaseプロジェクトは変更に細心の注意を払う
- バックアップを取ってから同期を実行
- 大規模な変更は計画的に行い、ダウンタイムを最小化