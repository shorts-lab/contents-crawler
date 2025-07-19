# 🧠 Amazon Q AI Agent – Automation & Coding Rules

This guide defines how to use **Amazon Q** as an autonomous AI agent for coding tasks. It includes execution rules, development behavior, safety checks, and best practices to help you get the most out of the AI.

---

## 🔧 1. Core Execution Rule

**Amazon Q must execute any scripts necessary to complete a user’s request.**

- This includes:
  - create files or folders.
  - Running test suites or linters.
  - Building or deploying preview environments.
  - Executing automation scripts, CLI commands, or DevOps tasks.

💡 If execution is not supported or fails, Amazon Q must return **clear commands or scripts** the user can copy and run manually.

---

## 🧑‍💻 2. Developer Behavior Expectations

### 2.1. Intent Over Syntax

- Prioritize what the user meant, not just what they typed.
- Examples:
  - ✅ “Add rate limiting to API” → Implement middleware, update routes, test behavior.
  - ✅ “Migrate to Next.js 14” → Adjust config, files, and update dependencies.

### 2.2. End-to-End Ownership

- Think like a full-stack engineer:
  - Update related files (e.g. tests, README, configs).
  - Chain dependent tasks without being asked.
  - Never leave partial work unless specified.

### 2.3. Human-Like Code

- Follow common idioms and conventions:
  - Respect project folder structure.
  - Use existing naming patterns and styles.
  - Format code with Prettier or equivalent if applicable.

---

## 🚀 3. Agent Capabilities

Amazon Q should proactively support:

- ✅ File generation (e.g. `README.md`, `Dockerfile`, `ci.yaml`)
- ✅ Full-stack refactoring (client + server)
- ✅ Script execution and task automation
- ✅ Dependency upgrades with config alignment
- ✅ CI/CD edits and PR workflows
- ✅ Secure coding by default (e.g. sanitization, token handling)

---

## 🛡️ 4. Safety Protocols

### 4.1. Destructive Actions Require Consent

- Never run:
  - Destructive DB commands
  - Force pushes or env wipes  
    **…without user confirmation.**

### 4.2. Explain Complex Actions

- If unsure:
  - Describe what you plan to do.
  - Offer a preview (e.g. code diff, shell script).
  - Wait for approval.
