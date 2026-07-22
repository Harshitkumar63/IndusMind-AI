# Backend Tests

This directory contains the pytest test suite for the IndusMind AI backend.

## Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_health.py       # Health check smoke tests
├── test_documents.py    # Document API tests (future)
├── test_chat.py         # Chat/RAG API tests (future)
├── test_knowledge.py    # Knowledge graph tests (future)
└── test_pipeline.py     # AI pipeline tests (future)
```

## Running Tests

```bash
cd backend

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run a specific test file
python -m pytest tests/test_health.py -v
```

## Writing Tests

- Use `pytest-asyncio` for async tests
- Use fixtures from `conftest.py` for test client and database
- Follow the Arrange-Act-Assert pattern
- Test both success and error cases
