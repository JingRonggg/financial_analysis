# Financial Analysis Server

FastAPI backend server for the financial analysis application.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

### Installing uv

If you don't have uv installed

**With pip:**
```bash
pip install uv
```

## Setup

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Install dependencies:**
   ```bash
   uv sync .
   ```

## Running the Server

### Development Mode
```bash
uv run fastapi dev main.py
```

This will start the server with:
- Hot reload enabled
- Server running on http://127.0.0.1:8000
- Interactive API docs at http://127.0.0.1:8000/docs
- Alternative docs at http://127.0.0.1:8000/redoc

### Production Mode
```bash
fastapi run main.py
```

## API Endpoints

- `GET /health` - Health check endpoint

## Development Commands

### Adding new dependencies
```bash
uv add package-name
```

### Adding development dependencies
```bash
uv add --dev package-name
```

### Running with specific Python version
```bash
uv run --python 3.12 fastapi dev main.py
```

### Updating dependencies
```bash
uv pip install --upgrade -e .
```

## Project Structure

```
server/
├── main.py           # FastAPI application entry point
├── pyproject.toml    # Project configuration and dependencies
├── README.md         # This file
└── .venv/           # Virtual environment (created after setup)
```

## Configuration

The server is configured in `pyproject.toml` with:
- FastAPI with standard extras (includes uvicorn, pydantic, etc.)
- Python 3.12+ requirement

## Troubleshooting

### Virtual Environment Issues
If you encounter issues with the virtual environment:
```bash
# Remove existing venv
rm -rf .venv  # or rmdir /s .venv on Windows

# Recreate venv
uv sync
```

### Port Already in Use
If port 8000 is already in use, specify a different port:
```bash
fastapi dev main.py --port 8001
```
