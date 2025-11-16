# User Management API - Test Project

A simple Flask-based user management API for testing AI agent capabilities.

⚠️ **WARNING**: This repository contains intentional security vulnerabilities for educational and testing purposes. DO NOT use this code in production!

## Purpose

This repository serves as a test target for the [KaggleAIAgents_2025](https://github.com/RamaswamyGCP/KaggleAIAgents_2025) project, which demonstrates AI agents that can:
- Review pull requests for security issues
- Triage GitHub issues
- Improve documentation
- Detect code quality problems

## Features

- User registration and login
- JWT-based authentication
- SQLite database
- REST API endpoints

## Intentional Vulnerabilities

This project contains several intentional security issues that AI agents should detect:

1. **SQL Injection** - Unsafe database queries
2. **Hardcoded Secrets** - API keys in code
3. **Weak Authentication** - Poor password handling
4. **Information Disclosure** - Verbose error messages
5. **Missing Input Validation** - Unvalidated user input

## Setup

```bash
pip install flask pyjwt sqlite3
python app.py
```

## API Endpoints

- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `GET /api/user/<username>` - Get user details
- `GET /api/users` - List all users (requires auth)

## Testing

This project is designed to be analyzed by AI agents. Do not deploy to production!

## License

MIT License - For educational purposes only

