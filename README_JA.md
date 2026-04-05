<div align="center">

<h1 style="font-size: 3em; font-weight: bold; margin-bottom: 10px;">
  Vibeski
</h1>

<p style="font-size: 1.2em; color: #666; margin-bottom: 20px;">
  <strong>フルスタック AI Agent ベースアプリケーションフレームワーク</strong>
</p>

<p>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python">
  </a>
  <a href="pyproject.toml">
    <img src="https://img.shields.io/badge/version-1.0.0-brightgreen.svg" alt="Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  </a>
  <a href="https://github.com/crabin/VIBESKI/releases">
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  </a>
</p>

<p>
  <a href="https://github.com/langchain-ai/langchain">
    <img src="https://img.shields.io/badge/LangChain-0.1%2B-blueviolet.svg" alt="LangChain">
  </a>
  <a href="https://github.com/langchain-ai/langgraph">
    <img src="https://img.shields.io/badge/LangGraph-0.2%2B-00BFFF.svg" alt="LangGraph">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg" alt="FastAPI">
  </a>
  <a href="https://www.sqlite.org/">
    <img src="https://img.shields.io/badge/SQLite-3.x-003B57.svg" alt="SQLite">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/badge/uv-latest-2E86C1.svg" alt="uv">
  </a>
  <a href="https://github.com/vadimdemedes/ink">
    <img src="https://img.shields.io/badge/Ink-4.4%2B-FF69B4.svg" alt="Ink">
  </a>
</p>

<p>
  <a href="README.md">中文</a> | <a href="README_EN.md">English</a> | 日本語
</p>

</div>

---

# Vibeski

新しいアプリケーションを素早く「バイブコーディング」するための再利用可能なフルスタック AI Agent ベースアプリケーションフレームワーク。

## 特徴

- **統一バックエンド**: FastAPI による REST + SSE インターフェース、CLI/TUI、モバイル、デスクトップクライアントで共有
- **マルチLLM対応**: Ollama、DeepSeek、OpenAI、Anthropic、Google などに標準対応
- **セッション管理**: SQLite ストレージによる永続的な会話
- **イベント駆動アーキテクチャ**: EventBus と SSE によるリアルタイムストリーミング
- **拡張可能なツールシステム**: Python entry_points 経由でカスタムツールを登録
- **複数フロントエンド対応**:
  - ターミナル TUI (TypeScript/Ink)
  - モバイルアプリ (React Native/Expo)
  - デスクトップアプリ (Tauri + Vite)
- **設定の永続化**: SQLite ベースのユーザー設定、3 段階優先順位 (DB > .env > デフォルト)

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontends                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │ Terminal │ │  Mobile   │ │ Desktop  │                    │
│  │  (Ink)   │ │  (Expo)   │ │ (Tauri)  │                    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘                    │
│           │              │              │                     │
│           └──────────────┴─────────────────────────────────┘
│                          │                                │
│                          ▼                                │
│               ┌────────────────────────────┐                │
│               │      FastAPI Backend       │                │
│               │  ┌──────────────────────┐ │                │
│               │  │  Session Manager     │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Event Bus           │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Tool Registry      │ │                │
│               │  └──────────────────────┘ │                │
│               └────────────────────────────┘                │
│                          │                                │
│                          ▼                                │
│               ┌────────────────────────────┐                │
│               │       SQLite Storage       │                │
│               │  ┌──────────────────────┐ │                │
│               │  │  Conversations       │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  User Configs        │ │                │
│               │  ├──────────────────────┤ │                │
│               │  │  Prompt Chains       │ │                │
│               │  └──────────────────────┘ │                │
│               └────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## クイックスタート

### 1. クローンと設定

```bash
git clone https://github.com/crabin/VIBESKI.git
cd vibeski
cp .env.example .env
# .env を編集: LLM_PROVIDER を設定し、API キーを追加
```

### 2. 依存関係のインストール

```bash
# Python 依存関係
uv sync

# ターミナル UI 依存関係
cd terminal-ui && npm install && cd ..
```

### 3. 実行

```bash
python main.py            # バックエンド (ポート 8000) + Ink TUI
```

または個別に実行:

```bash
python main.py --backend  # バックエンドのみ
python main.py --tui      # TUI のみ (バックエンドが実行中である必要があります)
```

API ドキュメント: http://localhost:8000/docs

### 4. モバイル (Expo)

```bash
cd app && npm install && npx expo start
```

### 5. デスクトップ (Tauri - Rust が必要)

```bash
# Rust のインストール: https://rustup.rs
cd desktop && npm install && npm run tauri dev
```

## カスタムツールの追加

1. `tools.base.BaseTool` を継承したクラスを作成
2. `pyproject.toml` に登録:
   ```toml
   [project.entry-points."vibeski.tools.basic"]
   my_tools = "mypackage.tools:MY_TOOLS"
   ```
3. `uv sync` を実行 — ツールは次回起動時に自動検出されます

## 環境変数

| 変数 | 説明 | デフォルト |
|------|-------------|--------|
| `LLM_PROVIDER` | LLM プロバイダー: ollama/deepseek/openai/anthropic/google/... | `ollama` |
| `DATABASE_URL` | SQLite データベースパス | `sqlite:///./data/vibeski.db` |
| `LOG_LEVEL` | ログレベル | `INFO` |
| `VIBESKI_SERVER_HOST` | バックエンドホスト | `0.0.0.0` |
| `VIBESKI_SERVER_PORT` | バックエンドポート | `8000` |
| `OLLAMA_BASE_URL` | Ollama サービス URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | デフォルト Ollama モデル | `gemma3:1b` |

## プロジェクト構成

```
vibeski/
├── main.py                 # エントリーポイント
├── vibeski_config/         # 設定 (pydantic-settings + SQLite)
├── router/                 # FastAPI ルート (chat, sessions, tools, system)
├── core/                  # セッションマネージャー、エグゼキューター、モデル
├── database/              # SQLite モデルとマネージャー
├── tools/                 # ツールレジストリとサンプルツール
├── prompts/               # プロンプトテンプレート
├── skills/                # スキルローダーとインジェクター
├── utils/                 # 共有ユーティリティ (logger, event_bus, model_selector)
├── vibeski_cli/            # CLI コマンドと TUI ランチャー
├── terminal-ui/           # TypeScript/Ink ターミナル UI
├── app/                   # React Native/Expo モバイルアプリ
├── desktop/              # Tauri デスクトップアプリ
└── docs/                  # ドキュメント
```

## CLI コマンド

```bash
vibeski              # バックエンド + TUI (フルスタック)
vibeski --backend    # バックエンドのみ (ポート 8000, API は http://localhost:8000/docs)
vibeski --tui        # TUI のみ (バックエンドが実行中である必要があります)
vibeski-server       # uvicorn を直接実行 (本番環境 / Docker 用)
```

## ドキュメント

| ドキュメント | 説明 |
|----------|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | クイックスタートガイド |
| [docs/API.md](docs/API.md) | API ドキュメント |
| [docs/LLM_PROVIDERS.md](docs/LLM_PROVIDERS.md) | LLM プロバイダー設定 |
| [docs/OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md) | ローカル Ollama 設定 |
| [docs/TOOL_EXTENSION.md](docs/TOOL_EXTENSION.md) | ツール拡張ガイド |

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照してください。

## 作者

**crabin**

- GitHub: [@crabin](https://github.com/crabin)
- Email: [cralpbin@gmail.com](mailto:cralpbin@gmail.com)
