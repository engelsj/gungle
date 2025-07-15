```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env

# Run development server
python -m uvicorn src.gungle.main:app --reload
```

## API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Lint
flake8 src/ tests/

# Run all quality checks
pre-commit run --all-files
```

## Project Structure

```
src/firearm_game/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration
├── api/                 # API routes
├── models/              # Data models
├── services/            # Business logic
└── utils/               # Utilities
```
