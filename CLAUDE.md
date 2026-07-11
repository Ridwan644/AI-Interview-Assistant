# CLAUDE.md

Context for AI assistants working on this project. Read this first.

## What This Project Is

An AI-powered mock interview platform. Users practice mock interviews with an AI
that acts like a real interviewer, then receive detailed, category-scored feedback
on how to improve. The problem it solves: people grind LeetCode and system design
but freeze in real interviews because they lack actual interview *experience* -
articulating thoughts, communicating a process out loud, handling follow-ups.

Target users: students and early-career engineers preparing for SWE, data, and
AI/ML interviews.

## Scope

**V1 (target: end of July) - text-based**
- Account creation + login (Clerk)
- First-login onboarding (name, major, target companies, target role)
- Two paths: Practice (mock interview) and Learn (study concepts)
- Mock interview in two types: Behavioral and Technical
- AI conducts a turn-by-turn interview, asks follow-ups, pushes back on weak answers
- Structured, category-scored feedback at the end
- Dashboard of strengths / weaknesses / areas to improve
- History of past interviews and feedback

**Learn section (V1):** readable lessons only. Topics: SQL, Git/GitHub, Linux.
User picks a topic, reads lessons about what it is and key concepts.

**V2 (target: end of August) - voice**
- Speak to the AI and hear it respond (Whisper STT, ElevenLabs TTS)
- Likely WebSockets / WebRTC for real-time feel
- S3 for audio file storage (V2 only - text V1 has no files)

**Future / backlog (NOT scheduled - do not let these block V1/V2)**
- NORTH-STAR FEATURE: AI-observed LeetCode sandbox - a live code editor where the
  student solves a problem while the AI watches their thinking/code in real time
  and interacts like a real interviewer. This is the "better than HackerRank"
  differentiator. Very complex (browser code editor, safe sandboxed code
  execution, real-time AI observation, streaming infra). V3+. Let it inform
  architecture; do NOT build it in V1/V2.
- Interactive GeeksforGeeks-style Learn exercises (Git/bash/SQL hands-on)
- Marketplace: engineers/tutors get paid to run mock interviews
- News feed: latest interview intel from tech companies

Protect scope. Capture exciting ideas in backlog; do not build them early.

## Scoring Model

Four categories, each 1-10, plus overall score, summary, areas to improve.
- Behavioral: Articulation, Answer Quality
- Technical: Correctness, Thought Process Clarity
Only the two relevant categories are used per interview; the other two columns
stay empty (accepted V1 tradeoff - one feedback row holds all four).

## Tech Stack

- Frontend: Next.js (React), runs on Node.js. GOAL: intentional, non-templated
  design (not "vibe-coded"). Revisit design direction when building frontend.
- Backend: FastAPI (Python)
- Database: PostgreSQL
- ORM: SQLAlchemy (+ psycopg2 driver)
- Config: pydantic-settings (reads .env)
- AI: Anthropic Claude API
- Auth: Clerk
- Containerization: Docker + Docker Compose
- Package manager: uv (not pip/venv directly)
- Version control: Git + GitHub

## Repository Layout

```
AI-Interview-Assistant/
|-- docker-compose.yml        # Postgres service (committed)
|-- .env                      # root secrets for Compose (GITIGNORED)
|-- backend/
|   |-- .env                  # backend app secrets (GITIGNORED)
|   |-- create_tables.py      # imports app.models, then Base.metadata.create_all
|   |-- seed_data.py          # seeds sample learn topics (Git, SQL, Linux)
|   |-- pyproject.toml
|   |-- uv.lock
|   |-- Dockerfile
|   |-- app/
|       |-- main.py           # FastAPI entry point; includes routers
|       |-- config.py         # pydantic-settings loads .env
|       |-- db/
|       |   |-- __init__.py   # EMPTY (model import here caused a circular import - keep empty)
|       |   |-- database.py   # engine, SessionLocal, Base, get_db()
|       |-- models/
|       |   |-- __init__.py   # imports ALL models (Learn, User) so Base registers them
|       |   |-- learn.py      # Learn model (DONE)
|       |   |-- user.py       # User model (DONE)
|       |-- routers/
|       |   |-- learn.py      # GET /learn (DONE)
|       |-- schemas/
|       |   |-- learn.py      # LearnListItem, LearnDetail (DONE)
|       |-- services/         # ai_service.py, feedback_service.py (not started)
|-- frontend/                 # Next.js (not started)
```

## Database Schema (V1)

- **users** - id, clerk_user_id (UNIQUE - real identifier), name, major,
  target_role, target_company, created_at   [TABLE CREATED]
- **learn** - id, title, topic, content, created_at   [TABLE CREATED + SEEDED]
- **mock_interviews** - id, user_id (FK -> users), interview_type, status,
  started_at, ended_at   [NOT BUILT YET]
- **messages** - id, interview_id (FK), role (ai/user), content, created_at   [NOT BUILT]
- **feedback** - id, interview_id (FK), articulation_score, answer_quality_score,
  correctness_score, thought_process_score, overall_score, summary,
  areas_to_improve, created_at   [NOT BUILT]

Design note: only genuine unique IDENTIFIERS get unique=True (e.g. clerk_user_id).
Shared attributes (name, major, topic, target_company) do NOT.

## API Contract (V1)

```
PATCH  /users/me                     # save onboarding info (identity from auth token)
POST   /interviews                   # start a new interview          <- PHASE 4 (building)
POST   /interviews/{id}/messages     # send a message during an interview
PATCH  /interviews/{id}              # end an interview (status -> completed)
GET    /interviews                   # list the user's past interviews
GET    /interviews/{id}/feedback     # get feedback for an interview
GET    /learn                        # list learn topics              <- DONE
GET    /learn/{id}                   # get one topic's full content
```

Dashboard: NO separate table. It's a VIEW built by querying existing feedback
data. Will need endpoint(s) that aggregate feedback, later.

## Backend Build Roadmap

1.  Prove the skeleton (Hello World)         - DONE
2.  Database connection                      - DONE
3.  Learn Content (GET /learn)               - DONE (first vertical slice + first PR)
4.  Create an Interview (POST /interviews)   - IN PROGRESS
5.  Get Interviews (GET /interviews)
6.  End an Interview (PATCH /interviews/{id})
7.  Save Onboarding (PATCH /users/me)
8.  AI Integration (the interview engine)
9.  Feedback Generation
10. Auth (Clerk integration)
11. Error handling
12. Testing (pytest)
13. Dockerize the backend
(then: frontend, then deployment)

Approach: build one full VERTICAL SLICE at a time (table -> model -> schema ->
router -> endpoint -> working) before moving to the next resource.

## Current Status (as of this session)

**Phase 3 COMPLETE** - GET /learn works end to end. Merged to main via a full
Pull Request (first PR done: branch -> commit -> push -> PR -> review diff ->
merge -> cleanup).

**Phase 4 IN PROGRESS - Create an Interview (POST /interviews).**
New concepts this phase: (1) a POST with a REQUEST BODY (receiving/validating
input, not just sending output), (2) a FOREIGN KEY relationship (interviews
belong to a user).

Auth decision: NOT doing real auth yet (Phase 10). Instead seed a TEST USER, use
its ID during development, and swap in the real authenticated user ID in Phase 10.

Done so far in Phase 4:
- User model built; users table created + verified.
- models/__init__.py imports all models (Learn, User); create_tables.py imports
  app.models so create_all sees everything.

NEXT STEPS in Phase 4 (in order, by dependency):
1. Seed a test user (so interviews have someone to belong to)
2. Build MockInterview model (with user_id ForeignKey -> users) + create table
3. Build interview schemas (a "create" INPUT schema + a response schema)
4. Build POST /interviews router/endpoint (uses request body + test user id)
5. Verify it creates an interview row linked to the test user

## Tooling Plan

- CLAUDE CODE: Ridwan will use Claude Code on this project to speed up REPETITIVE
  phases that repeat an already-learned pattern (e.g. Phases 5/6/7 repeat the
  Phase 3/4 vertical-slice pattern). Rule: do the FIRST instance of any new
  pattern by hand (e.g. Phase 4's FK + POST body is new - do it himself); use
  Claude Code for repeats. ALWAYS read/understand every generated line and review
  it like a PR he owns. Force-multiplier on things he understands, not a
  substitute for understanding.

## Git Workflow

Learned the full PR workflow once (Phase 3). For solo speed now commits directly
to main:
```
git status
git status --short | grep -i env   # secret safety check - ALWAYS
git add .
git commit -m "..."
git push
```
Switch back to branch+PR the moment anyone else joins, or on any real job.

## Conventions & Commands

- Run backend: `cd backend && uv run uvicorn app.main:app --reload`
- Add dependency: `uv add <pkg>` (dev: `uv add --dev <pkg>`)
- Start DB: `docker compose up -d`
- Reset DB (wipes volume, re-inits from .env): `docker compose down -v && docker compose up -d`
- Create tables: `cd backend && uv run python create_tables.py`
- Seed data: `cd backend && uv run python seed_data.py`
- Inspect DB: `docker exec -it ai-interview-assistant-db-1 psql -U ridwan -d interview_db`
  then `\dt` (list tables), `\d <table>` (structure), `\q` (quit)
- Check a port's owner (debugging): `lsof -i :5432`
- Python: snake_case. Keep routers thin; business logic in services.
- Secrets in gitignored .env files, never hardcoded, never committed.
- Imports resolve from where you RUN the command; run backend commands from backend/.
- create_all only builds tables for models that have been IMPORTED. create_tables.py
  must import app.models (which triggers models/__init__.py).

## Concepts Ridwan Has Learned (for calibration)

Docker (images/containers/compose/volumes/ports), ORM vs raw SQL tradeoffs,
SQLAlchemy engine/session/Base, models vs schemas (storage vs API shape),
multiple schemas per model (list vs detail), response_model as output filter,
sessions + get_db (yield/finally), dependency injection (Depends), routers
(APIRouter), querying (db.query().all()), writing data (add/commit), seed scripts
vs manual inserts, imports connect code / database connects separate programs'
data, the full PR workflow, unique-identifier design, API vs endpoint.

Debugging worked through: port collisions (lsof), Postgres volume init, circular
imports (dependency direction), NameError (imports), create_all needing model imports.

## How to Work With the Owner (Ridwan)

Deliberate learning exercise. Goal is building engineering skill (critical
thinking, decision-making, figuring out "what's next" independently), not just a
finished app. Wants to avoid the "guise of competency" from offloading thinking to AI.

- Teach the concept before implementing anything new.
- At transitions, help him reason through what's next via the checklist:
  (1) what did I finish and what does it enable, (2) smallest next step,
  (3) what must be true first (dependencies), (4) how will I know it worked.
- Let him attempt reasoning before giving answers; correct his real attempts.
- He writes his own code for new patterns - guide and review, don't autopilot.
  Claude Code allowed for repetitive/already-learned patterns (he reviews output).
- Don't firehose. One step at a time. He'll say when it's too much.
- Verify, don't assume ("I saw it work," not "it should work").
- Debugging is his to drive - highest-value learning. Give hints, let him diagnose.
- Provide interview-ready explanations when asked (concise, plain language).
