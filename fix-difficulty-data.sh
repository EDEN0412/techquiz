#!/bin/bash

# Supabase難易度データ修正スクリプト
echo "🔧 Supabaseの難易度テーブルを修正中..."

# Supabaseローカル環境が起動していることを確認
if ! supabase status | grep -q "API URL"; then
    echo "❌ Supabaseローカル環境が起動していません"
    echo "まず 'supabase start' を実行してください"
    exit 1
fi

# マイグレーションの実行
echo "📊 データベーススキーマを更新中..."
supabase db push

# 更新されたマイグレーションの適用
echo "🔄 難易度テーブルのスキーマを修正中..."
supabase db reset --linked=false

echo "✅ データベースの修正が完了しました！"
echo ""
echo "次の手順："
echo "1. Django開発サーバーを起動: python backend/manage.py runserver"
echo "2. フロントエンド開発サーバーを起動: npm run dev"
echo "3. ブラウザで難易度選択画面をテスト"
