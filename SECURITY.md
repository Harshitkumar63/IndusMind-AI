# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x.x   | ✅ Actively supported |
| < 1.0   | ❌ No longer supported |

## Reporting a Vulnerability

We take the security of IndusMind AI seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### ⚠️ Please Do NOT

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed
- Exploit the vulnerability beyond what is necessary to demonstrate it

### 📧 How to Report

Please send an email to **[indusmindai@gmail.com](mailto:indusmindai@gmail.com)** with:

1. **Subject**: `[SECURITY] Brief description of the vulnerability`
2. **Description**: A detailed description of the vulnerability
3. **Steps to Reproduce**: Step-by-step instructions to reproduce the issue
4. **Impact**: Your assessment of the potential impact
5. **Suggested Fix**: If you have one (optional)

### ⏱️ Response Timeline

| Action | Timeline |
|--------|----------|
| Acknowledgment | Within 48 hours |
| Initial Assessment | Within 5 business days |
| Fix Development | Within 30 days (critical) |
| Public Disclosure | After fix is released |

### 🔐 Security Best Practices for Deployment

When deploying IndusMind AI in production:

1. **Environment Variables**: Never commit `.env` files. Use the `.env.example` as a template.
2. **Secret Key**: Change the default `SECRET_KEY` to a cryptographically secure random string.
3. **Database Credentials**: Use strong, unique passwords for PostgreSQL, Redis, and Neo4j.
4. **API Keys**: Store OpenAI API keys securely; consider using a secrets manager.
5. **CORS Origins**: Restrict `BACKEND_CORS_ORIGINS` to your specific frontend domain.
6. **HTTPS**: Always use TLS/SSL in production.
7. **Docker Secrets**: Use Docker secrets or environment variable injection for sensitive data.
8. **Network Security**: Ensure database ports (5432, 6379, 7474, 7687) are not exposed publicly.

### 🏗️ Architecture Security

- **Authentication**: JWT-based authentication with configurable expiry
- **RBAC**: Role-based access control (admin, engineer, viewer)
- **Input Validation**: Pydantic v2 for all API request validation
- **SQL Injection**: SQLAlchemy ORM with parameterized queries
- **File Upload**: Type and size validation on all uploads
- **Rate Limiting**: Configurable via middleware (recommended for production)

## Acknowledgments

We are grateful to the security researchers who help keep IndusMind AI and its users safe. Responsible disclosure contributors will be acknowledged in our [CHANGELOG](CHANGELOG.md) (with permission).
