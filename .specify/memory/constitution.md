<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0 (MINOR)
Date: 2026-01-07

Change Summary:
- Updated Development Tools section (3.3) to replace Poetry/pip with uv package manager
- Added comprehensive uv setup and activation instructions
- No principle changes or removals (MINOR bump justified)

Modified Sections:
- Section 3.3 "Development Tools": Poetry/pip → uv (with setup instructions)

Templates Requiring Updates:
- ✅ plan-template.md: Already generic, no hardcoded package manager references
- ✅ tasks-template.md: Already generic, no hardcoded package manager references
- ✅ spec-template.md: No package manager references found
- ✅ phr-template.prompt.md: No package manager references found
- ✅ No other templates require updates

Follow-up TODOs:
- None - all templates are compatible with uv tooling
-->

# 📜 Agentic Todo Full-Stack Web Application Constitution (Phase II)

---

## 1. Purpose & Vision

The purpose of this project is to build a **modern, secure, multi-user Todo web application** using an **Agentic Development Stack** powered by **Claude Code and Spec-Kit Plus**.

This project must demonstrate:

- 🤖 Agent & Sub-Agent collaboration
-uv package manager
- 📜 Spec-driven development
- ♻️ Reusable intelligence (Agent Skills)
- 🌐 Full-stack architecture
- 🔐 Secure authentication
- 🗣️ Voice commands
- 🌍 Urdu language support
- ☁️ Cloud-native persistence using Neon Database

**No manual coding is allowed.**
All implementation must be produced, reviewed, and refined through Claude Code agents.

---

## 2. Governing Principles

### 2.1 Agentic Development Rule

**All development must strictly follow the Agent-Driven Development workflow:**

1. **User Request** → Analyze requirements
2. **Specification Agent** → Create detailed spec in `specs/<feature>/spec.md`
3. **Planning Agent** → Design architecture in `specs/<feature>/plan.md`
4. **Task Agent** → Break into tasks in `specs/<feature>/tasks.md`
5. **Specialized Agents** → Implement using appropriate sub-agents:
   - Frontend Builder (UI/Voice)
   - Backend API Guardian (Endpoints)
   - Database Architect (Schema)
   - Auth Config Specialist (Authentication)
   - Urdu Translator (Localization)

## 6. Package Management (UV – Mandatory)

### 6.1 UV Package Manager

All Python dependencies **must** be managed using **UV**.

❌ `pip` is not allowed  
❌ `poetry` is not allowed  
✅ `uv` is mandatory

---

### 6.2 Virtual Environment Setup

Create a local virtual environment using UV:   
7. **Verification** → Test and validate implementation
8. **Documentation** → Update PHRs and ADRs as needed

**NO manual coding is permitted.** All code must be generated, reviewed, and refined by Claude Code agents following established skills and patterns.

### 2.2 Skills-First Implementation

**Every agent MUST consult relevant skills before implementing features:**

- **API Skill** (`.claude/skills/api.skill.md`): Request formatting, error handling, JWT attachment
- **Database Skill** (`.claude/skills/database.skill.md`): CRUD, user filtering, pagination
- **Auth Skill** (`.claude/skills/auth.skill.md`): JWT validation, token management
- **Voice Skill** (`.claude/skills/voice.skill.md`): Speech recognition, intent classification
- **UI Skill** (`.claude/skills/ui.skill.md`): Design system, components, accessibility

Skills provide reusable patterns, security best practices, and consistent implementation across the application.

### 2.3 Security-First Architecture

**All security requirements are NON-NEGOTIABLE:**

#### Authentication Flow (MANDATORY)
```
User Login (Next.js)
        ↓
Better Auth issues JWT
        ↓
JWT stored in httpOnly cookie
        ↓
Frontend sends Authorization header
        ↓
FastAPI validates JWT signature
        ↓
User ID extracted from 'sub' claim
        ↓
DB queries filtered by user_id
```

#### Security Rules (CRITICAL)

1. **JWT Validation**: EVERY protected endpoint MUST validate JWT before processing
2. **User Scoping**: ALL database queries MUST filter by authenticated user's ID
3. **No Trust**: NEVER trust `user_id` from request body - ALWAYS extract from validated JWT
4. **Ownership Verification**: UPDATE/DELETE operations MUST verify user owns the resource
5. **Secret Management**: ALL secrets in environment variables, NEVER in code
6. **HTTPS Only**: Production MUST use HTTPS for all authentication requests
7. **Token Expiration**: Access tokens: 30 minutes, Refresh tokens: 7 days

**Violation of security rules results in immediate rejection of implementation.**

### 2.4 Multi-Tenant Data Isolation

**User data isolation is CRITICAL for this multi-user application:**

Every table with user-owned data MUST:
- Have `user_id` foreign key field with index
- Filter ALL queries by `user_id = current_user.id`
- Verify ownership before mutations
- Use proper HTTP status codes (404 for unauthorized access to prevent enumeration)

```python
# ✅ CORRECT - Always filter by user_id
todos = db.exec(
    select(Todo).where(Todo.user_id == current_user_id)
).all()

# ❌ WRONG - Never query without user filter
todos = db.exec(select(Todo)).all()  # SECURITY VIOLATION
```

### 2.5 Type Safety

**TypeScript and Python type safety is MANDATORY:**

- **Frontend**: TypeScript strict mode, no `any` types
- **Backend**: Python type hints on all functions, Pydantic models for validation
- **API Contracts**: Shared TypeScript/Python types for request/response
- **Database**: SQLModel for type-safe ORM operations

### 2.6 Accessibility (WCAG 2.1 AA)

**All UI components MUST meet accessibility standards:**

- Keyboard navigation for all interactive elements
- ARIA labels for screen readers
- 4.5:1 color contrast ratio for text
- 44x44px minimum touch targets
- Focus indicators on all focusable elements
- Support for `prefers-reduced-motion`
- Semantic HTML (button, nav, main, etc.)

### 2.7 Responsive Design

**Mobile-first, responsive UI is REQUIRED:**

- Design for mobile (320px+) first
- Tablet breakpoints (768px+)
- Desktop breakpoints (1024px+)
- Use Tailwind responsive utilities
- Test on all breakpoints

### 2.8 Documentation

**All significant work MUST be documented:**

- **PHRs** (Prompt History Records): Created after every user interaction in `history/prompts/`
- **ADRs** (Architecture Decision Records): For architecturally significant decisions in `history/adr/`
- **Specs**: Detailed feature specifications in `specs/<feature>/spec.md`
- **Plans**: Architecture and design in `specs/<feature>/plan.md`
- **Tasks**: Actionable task breakdown in `specs/<feature>/tasks.md`

---

## 3. Technology Stack (IMMUTABLE)

### 3.1 Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16+ (App Router) | React framework with SSR/SSG |
| TypeScript | 5+ | Type-safe JavaScript |
| Tailwind CSS | 3.4+ | Utility-first styling |
| Better Auth | Latest | Authentication with JWT |
| Framer Motion | 10+ | Animations and transitions |
| Web Speech API | Native | Voice command input |
| next-themes | Latest | Dark mode support |

### 3.2 Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | Latest | Python async web framework |
| SQLModel | Latest | Type-safe ORM (Pydantic + SQLAlchemy) |
| Neon PostgreSQL | Serverless | Cloud database |
| python-jose | Latest | JWT encoding/decoding |
| Alembic | Latest | Database migrations |
| Uvicorn | Latest | ASGI server |

### 3.3 Development Tools

| Tool | Purpose |
|------|---------|
| Claude Code | AI-powered development |
| Spec-Kit Plus | Spec-driven workflow |
| Git | Version control |
| pnpm | Frontend package manager |
| uv | Backend package manager (Python) |

**uv Setup and Activation:**
- uv is a fast Python package manager and environment manager
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix) or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
- Activate virtual environment: `uv sync` (creates and syncs dependencies from pyproject.toml)
- Run Python scripts: `uv run python main.py` or activate environment first with `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
- Add dependencies: `uv add <package>` (automatically updates pyproject.toml)
- Install dev dependencies: `uv add --dev <package>`

**Technology changes require ADR approval and constitutional amendment.**

---

## 4. API Architecture

### 4.1 REST API Standards

All API endpoints MUST follow these standards:

**Endpoint Structure:**
```
/api/todos              - List all todos for authenticated user
/api/todos/{id}         - Get/Update/Delete specific todo
/api/todos/{id}/complete - Toggle todo completion
/api/auth/login         - User login
/api/auth/register      - User registration
/api/auth/refresh       - Token refresh
/api/auth/me            - Current user info
```

**HTTP Methods:**
- `GET`: Retrieve resources
- `POST`: Create new resources
- `PUT`: Full resource update
- `PATCH`: Partial resource update
- `DELETE`: Remove resources

**Status Codes:**
- `200 OK`: Successful GET/PUT/PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid JWT
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found (or unauthorized access)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

**Response Format:**
```json
{
  "data": {...},           // Success response
  "error": {               // Error response
    "message": "...",
    "code": "...",
    "details": {...}
  }
}
```

### 4.2 Authentication Endpoints

**POST /api/auth/register**
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

Response (201):
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response (200):
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**POST /api/auth/refresh**
```
Authorization: Bearer <access_token>

Response (200):
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**GET /api/auth/me**
```
Authorization: Bearer <access_token>

Response (200):
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-01T00:00:00Z"
}
```

### 4.3 Todo Endpoints

**All todo endpoints require authentication (Authorization: Bearer <token>)**

**GET /api/todos**
```
Query params:
  - page: int (default: 1)
  - page_size: int (default: 20, max: 100)
  - completed: bool (optional filter)

Response (200):
{
  "items": [{...}],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "has_next": true,
  "has_prev": false
}
```

**POST /api/todos**
```json
Request:
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

Response (201):
{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "uuid",
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T00:00:00Z"
}
```

**GET /api/todos/{id}**
```
Response (200):
{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "uuid",
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T00:00:00Z"
}
```

**PUT /api/todos/{id}**
```json
Request:
{
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips",
  "completed": false
}

Response (200): // Same as GET response
```

**PATCH /api/todos/{id}**
```json
Request (partial update):
{
  "completed": true
}

Response (200): // Same as GET response
```

**DELETE /api/todos/{id}**
```
Response (204): // No content
```

---

## 5. Database Schema

### 5.1 User Table
```sql
CREATE TABLE "user" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  hashed_password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON "user"(email);
```

### 5.2 Todo Table
```sql
CREATE TABLE todo (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_todo_user_id ON todo(user_id);
CREATE INDEX idx_todo_completed ON todo(completed);
CREATE INDEX idx_todo_created_at ON todo(created_at DESC);
```

**Schema Rules:**
- UUIDs for primary keys (security + distributed systems)
- Foreign keys with CASCADE delete
- Timestamps on all tables (created_at, updated_at)
- Indexes on user_id, frequently queried fields
- NOT NULL constraints on required fields

---

## 6. Voice Command Support

### 6.1 Supported Commands (English)

| Command | Intent | Example |
|---------|--------|---------|
| "Add todo: [title]" | CREATE_TODO | "Add todo: Buy milk" |
| "Complete todo: [title]" | COMPLETE_TODO | "Complete todo: Buy milk" |
| "Delete todo: [title]" | DELETE_TODO | "Delete todo: Buy milk" |
| "Show all todos" | LIST_TODOS | "Show all todos" |
| "Show completed todos" | FILTER_COMPLETED | "Show completed todos" |
| "Show pending todos" | FILTER_PENDING | "Show pending todos" |
| "Search for [query]" | SEARCH_TODO | "Search for grocery" |

### 6.2 Supported Commands (Urdu)

| Command (Urdu Script) | Command (Roman) | Intent |
|----------------------|-----------------|--------|
| نیا کام: [title] | naya kaam: [title] | CREATE_TODO |
| مکمل کریں: [title] | mukammal karen: [title] | COMPLETE_TODO |
| حذف کریں: [title] | delete karen: [title] | DELETE_TODO |
| سب کام دکھائیں | sab kaam dikhayein | LIST_TODOS |
| مکمل کام دکھائیں | mukammal kaam dikhayein | FILTER_COMPLETED |
| باقی کام دکھائیں | baqi kaam dikhayein | FILTER_PENDING |

**Voice Implementation:**
- Web Speech API with 'ur-PK' language code for Urdu
- Pattern-based intent classification
- Entity extraction for todo titles
- Fallback to manual input if voice fails
- Visual feedback during listening/processing

---

## 7. Code Quality Standards

### 7.1 Frontend Code Quality

**Required:**
- ✅ TypeScript strict mode enabled
- ✅ No `any` types (use `unknown` and type guards)
- ✅ All components have prop types defined
- ✅ Error boundaries for error handling
- ✅ Loading states for async operations
- ✅ Proper use of Server vs Client Components
- ✅ ESLint and Prettier configured

**File Structure:**
```
app/
  ├── (auth)/
  │   ├── login/
  │   └── register/
  ├── (dashboard)/
  │   ├── layout.tsx
  │   └── page.tsx
  ├── api/
  ├── layout.tsx
  └── page.tsx
components/
  ├── ui/         # Reusable UI components
  ├── layouts/    # Layout components
  └── features/   # Feature-specific components
lib/
  ├── api.ts      # API client
  ├── auth.ts     # Auth utilities
  └── utils.ts    # Helper functions
```

### 7.2 Backend Code Quality

**Required:**
- ✅ Type hints on all functions
- ✅ Pydantic models for validation
- ✅ SQLModel for database operations
- ✅ FastAPI dependency injection
- ✅ Proper error handling with HTTPException
- ✅ Logging for debugging
- ✅ Black formatter, isort for imports

**File Structure:**
```
app/
  ├── main.py           # FastAPI app
  ├── models.py         # SQLModel database models
  ├── schemas.py        # Pydantic request/response models
  ├── database.py       # Database connection
  ├── auth.py           # Authentication logic
  ├── dependencies.py   # FastAPI dependencies
  └── routers/
      ├── auth.py       # Auth endpoints
      └── todos.py      # Todo endpoints
```

### 7.3 Testing Standards

**Frontend Testing:**
- Unit tests for utilities and hooks
- Component tests with React Testing Library
- E2E tests for critical flows (login, todo CRUD)

**Backend Testing:**
- Unit tests for business logic
- Integration tests for endpoints
- Database tests with test fixtures
- Authentication tests

**Test Coverage:**
- Minimum 80% code coverage
- All critical paths tested
- Edge cases covered

---

## 8. Development Workflow

### 8.1 Feature Development Flow

1. **User Request** → Clarify requirements
2. **Create Spec** → `/sp.specify` command → `specs/<feature>/spec.md`
3. **Create Plan** → `/sp.plan` command → `specs/<feature>/plan.md`
4. **Create Tasks** → `/sp.tasks` command → `specs/<feature>/tasks.md`
5. **Implement** → `/sp.implement` command → Execute tasks with specialized agents
6. **Verify** → Test implementation against acceptance criteria
7. **Document** → Create PHR, update ADRs if needed
8. **Commit** → `/sp.git.commit_pr` command → Create commit and PR

### 8.2 Agent Selection Guidelines

**Use the correct agent for each task:**

| Task Type | Agent |
|-----------|-------|
| UI components, layouts, styling | Frontend Builder |
| API endpoints, business logic | Backend API Guardian |
| Database schema, migrations | Database Architect |
| Authentication setup, JWT config | Auth Config Specialist |
| Urdu translation, voice commands | Urdu Translator |
| Feature orchestration | Spec Orchestrator |

### 8.3 Git Commit Standards

**Commit Message Format:**
```
<type>: <description>

<body>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

---

## 9. Environment Variables

### 9.1 Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

### 9.2 Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Environment Rules:**
- ✅ All secrets in environment variables
- ✅ Different secrets for dev/prod
- ✅ `.env.example` files with placeholders
- ✅ Never commit actual `.env` files
- ✅ Minimum 32 characters for secrets

---

## 10. Deployment

### 10.1 Frontend Deployment (Vercel)

**Requirements:**
- Node.js 18+
- Environment variables configured
- Build command: `pnpm build`
- Output directory: `.next`

### 10.2 Backend Deployment (Render/Railway)

**Requirements:**
- Python 3.11+
- PostgreSQL connection string
- Environment variables configured
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 10.3 Database (Neon)

**Configuration:**
- Connection pooling enabled
- SSL required
- Backup schedule: Daily
- Branching for staging/preview

---

## 11. Governance

### 11.1 Constitution Authority

This constitution is the **highest authority** for the Agentic Todo project. All development decisions, code implementations, and architectural choices MUST comply with this document.

**Precedence:**
1. Constitution (this document)
2. ADRs (Architecture Decision Records)
3. Feature Specs
4. Agent Skills
5. Code Comments

### 11.2 Amendment Process

Constitutional changes require:
1. **Proposal**: Document proposed change with rationale
2. **ADR Creation**: Create ADR explaining decision
3. **Review**: Review by project stakeholders
4. **Approval**: Explicit approval required
5. **Migration Plan**: Plan for updating existing code
6. **Update**: Modify constitution with version bump

### 11.3 Compliance Verification

**Every PR/commit must verify:**
- ✅ Follows agentic development workflow
- ✅ Agents consulted relevant skills
- ✅ Security rules followed (JWT, user scoping)
- ✅ Type safety maintained
- ✅ Accessibility standards met
- ✅ Documentation updated (PHRs, ADRs)
- ✅ Tests passing

**Violations result in PR rejection.**

### 11.4 Skills as Living Documents

Skills (`.claude/skills/*.skill.md`) are **living documents** that evolve with the project:

- Skills can be updated based on learnings
- New patterns can be added to skills
- Security improvements must update skills
- Skills changes require PHR documentation
- Agents must be notified of skill updates

---

## 12. Success Metrics

### 12.1 Technical Metrics

- ✅ 100% agent-driven code generation
- ✅ Zero manual code commits
- ✅ 80%+ test coverage
- ✅ WCAG 2.1 AA compliance
- ✅ Sub-second API response times (p95)
- ✅ Zero security vulnerabilities
- ✅ Mobile-responsive UI

### 12.2 Process Metrics

- ✅ PHR created for every user interaction
- ✅ ADR created for significant decisions
- ✅ All features have spec → plan → tasks
- ✅ Skills referenced before implementation
- ✅ Git commits follow standards

### 12.3 User Experience Metrics

- ✅ Voice commands working in English + Urdu
- ✅ Dark mode support
- ✅ RTL support for Urdu
- ✅ Offline-capable (PWA)
- ✅ Fast page loads (< 2s)

---

**Version**: 1.1.0
**Ratified**: 2026-01-06
**Last Amended**: 2026-01-07
**Next Review**: 2026-02-06

---

**This constitution governs all development on the Agentic Todo Full-Stack Web Application (Phase II). All agents, developers, and contributors must comply with these principles and standards.**
