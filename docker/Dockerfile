FROM node:18-alpine

WORKDIR /app

# 依存関係のインストール
COPY package.json package-lock.json ./
RUN npm ci

# アプリケーションファイルのコピー
COPY . .

# ビルド
RUN npm run build

# 本番環境用のポート公開
EXPOSE 3000

# 開発環境用コマンド
CMD ["npm", "run", "dev"] 