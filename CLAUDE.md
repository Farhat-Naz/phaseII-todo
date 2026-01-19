# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

## Project Implementation Details

### Backend Structure (`backend/app/`)

The FastAPI backend follows a modular architecture with clear separation of concerns:

```
backend/app/
├── main.py              # FastAPI application, CORS, middleware
├── models.py            # SQLModel database models (User, Todo)
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Database connection and session management
├── auth.py              # JWT encoding/decoding, password hashing
├── dependencies.py      # FastAPI dependency injection (get_db, get_current_user)
└── routers/
    ├── auth.py          # Authentication endpoints (login, register, me)
    └── todos.py         # Todo CRUD endpoints with user filtering
```

### Frontend Structure (`frontend/`)

The Next.js 16+ frontend uses App Router with internationalization:

```
frontend/
├── app/
│   ├── [locale]/        # i18n routes (en, ur)
│   │   ├── (auth)/      # Route group for auth pages
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── layout.tsx   # Locale-aware layout
│   │   └── page.tsx     # Dashboard (protected)
│   └── layout.tsx       # Root layout
├── components/
│   ├── features/        # Feature-specific components
│   │   ├── auth/        # LoginForm, RegisterForm
│   │   ├── todos/       # TodoForm, TodoItem, TodoList, VoiceInput
│   │   └── shared/      # LanguageSwitcher, LoadingSpinner
│   └── ui/              # Reusable UI components (Button, Card, Input, etc.)
├── hooks/
│   ├── useAuth.ts       # Authentication hook (login, logout, user state)
│   ├── useTodos.ts      # Todo CRUD hook with optimistic updates
│   └── useVoiceCommand.ts # Voice recognition hook
├── lib/
│   ├── api.ts           # API client with JWT token handling
│   └── auth.ts          # Auth utilities (token storage, validation)
├── types/
│   ├── todo.ts          # Todo TypeScript types
│   └── user.ts          # User TypeScript types
└── messages/            # i18n translation files
    ├── en.json          # English translations
    └── ur.json          # Urdu translations
```

### Key Implementation Patterns

#### 1. JWT Extraction (CRITICAL - Never from Request Body)

Backend always extracts user ID from validated JWT token, NEVER from request body:

```python
# ✅ CORRECT - dependencies.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY)
    user_id = payload.get("sub")  # Extract from JWT 'sub' claim
    return user_id

# ✅ CORRECT - routers/todos.py
@router.get("/todos")
def get_todos(current_user_id: str = Depends(get_current_user)):
    todos = db.exec(
        select(Todo).where(Todo.user_id == current_user_id)  # Filter by JWT user
    ).all()

# ❌ WRONG - Never trust user_id from request
@router.post("/todos")
def create_todo(todo: TodoCreate, user_id: str):  # SECURITY VIOLATION
    # user_id from request body can be forged!
```

#### 2. User Filtering (MANDATORY for All Queries)

Every database query MUST filter by authenticated user's ID:

```python
# ✅ CORRECT - All queries filtered
todos = db.exec(
    select(Todo).where(Todo.user_id == current_user_id)
).all()

# ✅ CORRECT - Updates verify ownership
todo = db.exec(
    select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user_id)
).first()
if not todo:
    raise HTTPException(status_code=404)  # Not 403, prevents enumeration

# ❌ WRONG - No user filtering
todos = db.exec(select(Todo)).all()  # SECURITY VIOLATION
```

#### 3. Optimistic UI Updates with Rollback

Frontend updates UI immediately, then syncs with backend:

```typescript
// ✅ CORRECT - useTodos.ts
const toggleTodo = async (id: string) => {
  // 1. Optimistic update (immediate UI feedback)
  setTodos(prev => prev.map(t =>
    t.id === id ? {...t, completed: !t.completed} : t
  ));

  try {
    // 2. Sync with backend
    await api.patch(`/todos/${id}`, { completed: !todo.completed });
  } catch (error) {
    // 3. Rollback on error
    setTodos(prev => prev.map(t =>
      t.id === id ? {...t, completed: !t.completed} : t
    ));
    toast.error("Failed to update todo");
  }
};
```

#### 4. Voice Command Parsing (English + Urdu)

Voice recognition with pattern-based intent classification:

```typescript
// ✅ CORRECT - useVoiceCommand.ts
const parseVoiceCommand = (transcript: string, locale: string) => {
  const lower = transcript.toLowerCase().trim();

  // English patterns
  if (locale === 'en') {
    if (lower.startsWith('add todo:') || lower.startsWith('create todo:')) {
      return { intent: 'CREATE_TODO', title: lower.split(':')[1].trim() };
    }
    if (lower.startsWith('complete todo:')) {
      return { intent: 'COMPLETE_TODO', title: lower.split(':')[1].trim() };
    }
  }

  // Urdu patterns
  if (locale === 'ur') {
    if (lower.includes('نیا کام') || lower.includes('naya kaam')) {
      return { intent: 'CREATE_TODO', title: extractAfterColon(lower) };
    }
    if (lower.includes('مکمل کریں') || lower.includes('mukammal karen')) {
      return { intent: 'COMPLETE_TODO', title: extractAfterColon(lower) };
    }
  }

  return { intent: 'UNKNOWN', error: 'Command not recognized' };
};
```

#### 5. RTL Layout for Urdu

Dynamic text direction based on locale:

```tsx
// ✅ CORRECT - app/[locale]/layout.tsx
export default function LocaleLayout({ children, params }: Props) {
  const locale = params.locale;
  const direction = locale === 'ur' ? 'rtl' : 'ltr';

  return (
    <html lang={locale} dir={direction}>
      <body className={cn(
        locale === 'ur' && 'font-urdu',  // Noto Nastaliq Urdu font
        'antialiased'
      )}>
        {children}
      </body>
    </html>
  );
}
```

### Agent Skills Applied

All implementation follows established patterns from skills:

- **API Skill** (`.claude/skills/api.skill.md`):
  - JWT token attached to all protected requests
  - Consistent error handling with toast notifications
  - Request/response type safety with TypeScript
  - Proper HTTP status codes (200, 201, 400, 401, 404)

- **Database Skill** (`.claude/skills/database.skill.md`):
  - User filtering on ALL queries (`WHERE user_id = ...`)
  - SQLModel for type-safe ORM operations
  - Proper indexes on `user_id`, `completed`, `created_at`
  - Foreign key CASCADE delete (user deletion removes todos)

- **Auth Skill** (`.claude/skills/auth.skill.md`):
  - JWT extraction from `Authorization: Bearer <token>`
  - User ID from JWT `sub` claim (never request body)
  - Password hashing with bcrypt before storage
  - Token expiration (30 min access, 7 day refresh)

- **Voice Skill** (`.claude/skills/voice.skill.md`):
  - Web Speech API with language detection (`en-US`, `ur-PK`)
  - Pattern-based intent classification
  - Entity extraction (todo titles from commands)
  - Graceful fallback to manual input on errors

- **UI Skill** (`.claude/skills/ui.skill.md`):
  - Accessible components (ARIA labels, keyboard nav)
  - Responsive design (mobile-first, 320px+)
  - Loading states for async operations
  - Error boundaries for error handling
  - Dark mode support with Tailwind

### Completed User Stories

All 7 user stories from spec.md implemented:

- **US1**: User Registration and Authentication - ✅ COMPLETE
  - JWT-based auth with Better Auth
  - Secure password hashing
  - Token storage in httpOnly cookies

- **US2**: Create and View Personal Todos - ✅ COMPLETE
  - Todo CRUD operations
  - User-scoped queries
  - Optimistic UI updates

- **US3**: Mark Todos as Complete/Incomplete - ✅ COMPLETE
  - Toggle completion status
  - Visual indicators (strikethrough, checkmark)
  - Persistent state

- **US4**: Update and Delete Todos - ✅ COMPLETE
  - Edit title and description
  - Delete with confirmation
  - Ownership verification

- **US5**: Voice Command Task Creation - ✅ COMPLETE
  - English voice input ("Add todo: Buy milk")
  - Urdu voice input ("نیا کام: دودھ خریدیں")
  - Visual feedback during listening

- **US6**: Voice Command Task Completion - ✅ COMPLETE
  - Complete/delete via voice
  - Filter todos by status ("Show completed")
  - Multi-language support

- **US7**: Multilingual UI (Urdu Support) - ✅ COMPLETE
  - Full Urdu UI translation
  - RTL text rendering
  - Language switcher component
  - Urdu font (Noto Nastaliq Urdu)

### Implementation Metrics

- **Total Tasks**: 80/80 (100% complete)
- **Files Created**: ~100+ (backend + frontend)
- **User Stories**: 7/7 implemented
- **Functional Requirements**: 28/28 satisfied (FR-001 to FR-028)
- **Success Criteria**: 12/12 met (SC-001 to SC-012)
- **Agent-Driven**: 100% (zero manual coding)

### Next Steps

For new features:
1. Run `/sp.specify` to create specification
2. Run `/sp.plan` for architecture design
3. Run `/sp.tasks` to break down implementation
4. Run `/sp.implement` to execute tasks with agents
5. Run `/sp.git.commit_pr` to commit and create PR

All work follows the constitution and leverages established skills.
