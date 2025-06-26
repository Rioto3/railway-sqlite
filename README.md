# Railway SQLite Server

SQLiteデータベースをRailway上でホストするためのFastAPIサーバー。永続ボリュームによりデータが保持されます。

## 特徴

- **永続データストレージ**: Railwayの永続ボリューム使用
- **REST API**: SQLクエリをHTTP経由で実行
- **健全性チェック**: `/health`エンドポイント
- **自動初期化**: 初回起動時にサンプルデータ作成

## API エンドポイント

### 基本情報
- `GET /` - サーバー情報
- `GET /health` - 健全性チェック

### データベース操作
- `POST /query` - SQLクエリ実行
- `GET /tables` - テーブル一覧
- `GET /tables/{table_name}/schema` - テーブルスキーマ
- `GET /database/schema` - データベース全体スキーマ

## デプロイ手順

### 1. GitHubリポジトリ作成
```bash
git clone https://github.com/Rioto3/railway-sqlite.git
cd railway-sqlite
```

### 2. Railwayデプロイ
1. [Railway](https://railway.app) にログイン
2. "Deploy from GitHub repo" を選択
3. このリポジトリを選択
4. 自動的にデプロイされます

### 3. 永続ボリューム設定
Railwayダッシュボードで：
1. Variables タブ
2. "Add Variable" 
3. `RAILWAY_VOLUME_MOUNT_PATH` = `/data`

## ローカル開発

```bash
# 依存関係インストール
pip install -r requirements.txt

# データベース初期化
python init_db.py

# サーバー起動
python app.py
```

## 使用例

### SQLクエリ実行
```bash
curl -X POST "https://your-app.railway.app/query" \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM users"}'
```

### テーブル一覧
```bash
curl "https://your-app.railway.app/tables"
```

## MCP連携

このサーバーはClaudeのMCP（Model Context Protocol）と連携可能です：

```json
{
  "mcpServers": {
    "railway-sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "https://your-app.railway.app"]
    }
  }
}
```

## ファイル構成

```
railway-sqlite/
├── Dockerfile              # コンテナ設定
├── railway.toml            # Railway設定
├── requirements.txt        # Python依存関係
├── app.py                 # FastAPIメインアプリ
├── init_db.py            # DB初期化スクリプト
└── README.md             # このファイル
```

## 注意事項

- SQLiteは単一ライター制限があります
- 大量の同時接続には適しません
- 本格的な本番環境にはPostgreSQLを推奨
