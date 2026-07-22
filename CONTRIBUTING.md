# Contributing to IndusMind AI

First off, thank you for considering contributing to IndusMind AI! 🎉

This document provides guidelines and steps for contributing. Following these guidelines helps communicate that you respect the time of the developers managing and developing this open-source project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [indusmindai@gmail.com](mailto:indusmindai@gmail.com).

---

## How Can I Contribute?

### 🐛 Report Bugs

- Use the [Bug Report](https://github.com/Harshitkumar63/IndusMind-AI/issues/new?template=bug_report.yml) issue template
- Include steps to reproduce, expected vs actual behavior, and screenshots if applicable
- Check existing issues first to avoid duplicates

### 💡 Suggest Features

- Use the [Feature Request](https://github.com/Harshitkumar63/IndusMind-AI/issues/new?template=feature_request.yml) issue template
- Describe the problem you're trying to solve
- Propose your solution and any alternatives you've considered

### 📝 Improve Documentation

- Fix typos, improve explanations, add examples
- Documentation PRs are always welcome and don't require an issue

### 🔧 Submit Code Changes

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes following our coding standards
4. Submit a pull request

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 20+ | Frontend runtime |
| Python | 3.11+ | Backend runtime |
| Docker | Latest | Container orchestration |
| Git | Latest | Version control |

### Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/IndusMind-AI.git
cd IndusMind-AI

# 2. Frontend setup
cd frontend
npm install
npm run dev
# → http://localhost:3000

# 3. Backend setup (in a new terminal)
cd backend
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000

# 4. Full stack (alternative)
cd docker
docker compose up -d
```

---

## Project Structure

```
IndusMind AI/
├── frontend/          # Next.js 15 + TypeScript + Tailwind
├── backend/           # FastAPI + Python 3.11
│   ├── app/
│   │   ├── ai/        # AI Pipeline (OCR, RAG, NER, Embeddings)
│   │   ├── api/       # REST API endpoints
│   │   ├── core/      # Configuration, security, logging
│   │   ├── domain/    # Domain models (SQLAlchemy)
│   │   ├── services/  # Business logic layer
│   │   └── infrastructure/  # External systems (DB, Redis, LLM)
│   └── tests/         # pytest test suite
├── docs/              # Project documentation
├── docker/            # Docker configurations
└── scripts/           # Development scripts
```

---

## Coding Standards

### Python (Backend)

- **Formatter**: [Black](https://black.readthedocs.io/) (line length: 100)
- **Import sorting**: [isort](https://pycqa.github.io/isort/) (Black-compatible profile)
- **Linting**: [Ruff](https://docs.astral.sh/ruff/)
- **Type hints**: Required for all function signatures
- **Docstrings**: Required for all public classes and functions (Google style)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes

```python
# ✅ Good
async def get_document_by_id(document_id: str) -> Document | None:
    """Retrieve a document by its unique identifier."""
    ...

# ❌ Bad
async def getDoc(id):
    ...
```

### TypeScript (Frontend)

- **Formatter**: [Prettier](https://prettier.io/)
- **Linting**: [ESLint](https://eslint.org/) with Next.js config
- **Components**: Functional components with TypeScript interfaces
- **Naming**: `camelCase` for functions/variables, `PascalCase` for components and types
- **Styling**: Tailwind CSS utility classes

```tsx
// ✅ Good
interface DashboardCardProps {
  title: string;
  value: number;
  trend: "up" | "down";
}

function DashboardCard({ title, value, trend }: DashboardCardProps) { ... }

// ❌ Bad
function card(props: any) { ... }
```

### General

- Keep files under 300 lines where possible
- Use meaningful variable and function names
- Add comments for complex logic, not obvious code
- No hardcoded secrets or API keys

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |
| `perf` | Performance improvements |

### Examples

```
feat(chat): add streaming response support
fix(documents): resolve PDF upload timeout on large files
docs(api): add authentication flow documentation
refactor(backend): extract vector search into dedicated service
test(rag): add integration tests for RAG pipeline
```

---

## Pull Request Process

1. **Create an issue first** (for non-trivial changes)
2. **Fork & branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. **Make changes**: Follow coding standards above
4. **Test locally**:
   ```bash
   # Frontend
   cd frontend && npm run build

   # Backend
   cd backend && python -m pytest
   ```
5. **Commit**: Use conventional commit messages
6. **Push & create PR**: Fill out the PR template completely
7. **Review**: Address any feedback from maintainers

### PR Requirements

- [ ] Code follows project coding standards
- [ ] All existing tests pass
- [ ] New features have corresponding tests
- [ ] Documentation is updated if needed
- [ ] PR description clearly explains the change
- [ ] No unrelated changes are included

---

## Issue Guidelines

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check the [documentation](docs/) for answers
3. Try the latest version of the project

### Writing Good Issues

- Use a clear, descriptive title
- Provide as much context as possible
- Include steps to reproduce (for bugs)
- Attach screenshots or logs when applicable
- Tag with appropriate labels

---

## 🙏 Recognition

Contributors are recognized in:
- The [README.md](README.md) contributors section
- The [CHANGELOG.md](CHANGELOG.md) for each release
- GitHub's contributor graph

Thank you for helping make IndusMind AI better! 🚀
