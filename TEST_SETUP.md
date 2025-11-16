# Test Setup Guide

This guide helps you create GitHub Issues and Pull Requests that your AI agents can work with.

## 🎯 Repository Purpose

This repository (`KaggleAgentTestRepo`) contains **intentionally vulnerable code** that serves as a test target for the AI agents in [KaggleAIAgents_2025](https://github.com/RamaswamyGCP/KaggleAIAgents_2025).

## 🐛 Vulnerabilities Included

The code contains **8 major security issues** that your PR Review Agent should detect:

1. **SQL Injection** (Critical)
   - File: `database.py`
   - Lines: `get_user_by_username()`, `delete_user()`
   - Impact: Database compromise

2. **Hardcoded Secrets** (Critical)
   - File: `app.py` (line 12: SECRET_KEY)
   - File: `config.py` (lines 11-16: API_KEYS)
   - Impact: Credential exposure

3. **Plain Text Passwords** (High)
   - File: `database.py`
   - Lines: `create_user()`, `authenticate_user()`
   - Impact: Password compromise

4. **Missing Authentication** (Critical)
   - File: `app.py`
   - Function: `delete_user()` (admin endpoint)
   - Impact: Unauthorized access

5. **Information Disclosure** (Medium)
   - File: `app.py`
   - Line: 32 (traceback exposure)
   - Impact: Internal structure exposed

6. **Weak Token Expiration** (Medium)
   - File: `auth.py`
   - Line: 15 (365 days expiration)
   - Impact: Long-lived tokens

7. **Debug Mode Enabled** (High)
   - File: `app.py`
   - Line: 110 (debug=True)
   - Impact: Information leak in production

8. **CORS Misconfiguration** (Medium)
   - File: `config.py`
   - Line: 24 (CORS_ORIGINS = "*")
   - Impact: Cross-origin attacks

## 📝 Creating Test Issues

Create these issues manually on GitHub to test your Issue Triage Agent:

### Issue #1: Critical Bug
```
Title: App crashes on user login with invalid credentials
Labels: (none - let agent add them)

Description:
When attempting to login with incorrect username/password, the application 
crashes instead of returning a proper error message. This is impacting user 
experience and needs immediate attention.

Steps to reproduce:
1. POST to /api/login with wrong credentials
2. Server returns 500 error with full traceback

Expected: 401 Unauthorized with user-friendly message
Actual: 500 Internal Server Error with stack trace
```

### Issue #2: Feature Request
```
Title: Implement password hashing for user security
Labels: (none - let agent add them)

Description:
Currently, passwords are stored in plain text in the database. This is a 
major security concern. We should implement proper password hashing using 
bcrypt or similar.

Note: I see there are hash_password and verify_password functions in auth.py 
but they're not being used anywhere!
```

### Issue #3: Security Vulnerability
```
Title: SQL Injection vulnerability in user lookup endpoint
Labels: security (pre-labeled)

Description:
The get_user_by_username function in database.py uses string concatenation 
to build SQL queries, making it vulnerable to SQL injection attacks.

File: database.py
Line: ~45
Function: get_user_by_username()

Attack example:
GET /api/user/admin' OR '1'='1

This could allow attackers to dump the entire user database.
```

### Issue #4: Documentation
```
Title: API documentation is incomplete
Labels: documentation (pre-labeled)

Description:
The README.md lacks proper API documentation. We need:
- Request/response examples for each endpoint
- Authentication requirements
- Error codes and meanings
- Rate limiting information (if applicable)

This will help developers integrate with our API more easily.
```

### Issue #5: Enhancement
```
Title: Add rate limiting to prevent API abuse
Labels: (none - let agent add them)

Description:
The API currently has no rate limiting, as seen in config.py where 
RATE_LIMIT_ENABLED = False. This makes us vulnerable to:
- Brute force attacks on login endpoint
- API abuse and DoS
- Excessive resource consumption

Suggest: Implement Flask-Limiter with reasonable limits per endpoint
```

## 🔀 Creating Test Pull Requests

### Option 1: Manual PR Creation

1. **Create a branch with a "fix":**
   ```bash
   cd KaggleAgentTestRepo
   git checkout -b fix/add-input-validation
   ```

2. **Make a change** (that still has issues):
   ```python
   # In app.py, add basic validation (but miss the SQL injection):
   @app.route('/api/register', methods=['POST'])
   def register():
       data = request.get_json()
       username = data.get('username')
       
       # NEW: Add length check
       if len(username) > 50:
           return jsonify({'error': 'Username too long'}), 400
       # ... rest of code
   ```

3. **Commit and push:**
   ```bash
   git add app.py
   git commit -m "Add input validation for username length"
   git push origin fix/add-input-validation
   ```

4. **Create PR on GitHub** with description:
   ```
   Title: Add input validation to registration endpoint
   
   Description:
   This PR adds basic input validation to prevent excessively long usernames.
   
   Changes:
   - Added username length check (max 50 characters)
   - Returns 400 error for invalid input
   
   Testing:
   - Tested with usernames of various lengths
   - Verified error response format
   ```

### Option 2: Create PR with Vulnerabilities

Create a PR that **introduces new vulnerabilities** for your agent to catch:

```bash
git checkout -b feature/export-users
# Add this to app.py:

@app.route('/api/export/users', methods=['GET'])
def export_users():
    """Export all users to CSV"""
    # VULNERABILITY: No authentication!
    # VULNERABILITY: Exports sensitive data including passwords!
    users = database.get_all_users()
    # ... export logic
```

## 🤖 Testing Your Agents

### Test PR Review Agent
```bash
# From your KaggleAIAgents_2025 repo
cd ../github_enterprise_agents
python main.py review-pr RamaswamyGCP KaggleAgentTestRepo 1
```

Expected behavior:
- Agent analyzes code changes
- Identifies security vulnerabilities
- Provides actionable feedback
- Comments on specific lines

### Test Issue Triage Agent
```bash
python main.py triage-issue RamaswamyGCP KaggleAgentTestRepo 1 2 3 4 5
```

Expected behavior:
- Agent classifies each issue (bug/feature/security/documentation)
- Assigns priority (low/medium/high/critical)
- Updates labels automatically
- Processes multiple issues in parallel

### Test Documentation Agent
```bash
python main.py update-docs RamaswamyGCP KaggleAgentTestRepo README.md
```

Expected behavior:
- Agent analyzes current documentation
- Suggests improvements
- Iterates based on critique
- Submits improvement PR

## 📊 Success Criteria

Your agents should be able to:

✅ **PR Review Agent:**
- Detect all 8 vulnerability types
- Flag hardcoded secrets
- Identify SQL injection
- Suggest specific fixes

✅ **Issue Triage Agent:**
- Correctly classify issue types
- Assign appropriate priorities
- Add relevant labels
- Process multiple issues simultaneously

✅ **Documentation Agent:**
- Identify documentation gaps
- Generate clear improvements
- Iterate based on feedback
- Maintain consistent style

## 🎯 Demo Workflow

For your capstone presentation:

1. **Show the vulnerable code** in KaggleAgentTestRepo
2. **Create/show issues** that need triaging
3. **Run agents** and demonstrate their capabilities
4. **Show results**: 
   - PR comments from review
   - Updated issue labels
   - Improved documentation

## 🔒 Important Notes

⚠️ **This repository is for educational purposes only!**
- Do NOT use this code in production
- Do NOT deploy this API anywhere public
- The vulnerabilities are intentional for learning

📝 **For Capstone:**
- This demonstrates real-world security analysis
- Shows practical application of AI agents
- Highlights the value of automated code review

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices/)

---

**Ready to test your agents! 🚀**

