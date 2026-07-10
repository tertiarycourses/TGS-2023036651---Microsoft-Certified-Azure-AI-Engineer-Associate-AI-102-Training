"""
labs_data.py — the single source of truth for the course content.

Every artifact (the labs/ folder, the Learner Guide DOCX+MD, the Lesson Plan, and the
slide deck) is generated/aligned from the LABS list below, so all five stay identical.

Each lab is a dict:
    num         int        lab number (1..19)
    slug        str        folder name under labs/
    day         int        1 = Docker, 2 = Kubernetes
    topic       str        the concept it teaches
    title       str        human title (used in slides/headings)
    duration    int        minutes (used by the Lesson Plan schedule)
    killercoda  str        KillerCoda scenario URL
    goal        str        one-paragraph goal
    build       str        "What you'll build / do" one-liner
    files       list       file manifest: ("write", relpath, content) or ("copy", src, dst)
    body        list       ordered content blocks shared by lab.md AND the Learner Guide
    test        str        the "Test it" verification

Block helpers build the `body` list; block kinds: h3, p, steps, code, note, table.
"""

# ----------------------------------------------------------------- block helpers
def h3(t):      return ("h3", t)
def p(t):       return ("p", t)
def steps(xs):  return ("steps", list(xs))
def code(t):    return ("code", t.rstrip("\n"))
def note(t):    return ("note", t)
def table(rs):  return ("table", rs)

KC = "https://killercoda.com/tertiary-labs/course/killercoda"

# Canonical TaskBoard source files (reused by several labs). Read once at import.
# Resolve the repo root from $COURSE_REPO or the current working directory, so this
# module works whether it lives at the repo root or inside a skill folder.
import os
def _repo_root():
    cand = os.environ.get("COURSE_REPO") or os.getcwd()
    if os.path.isdir(os.path.join(cand, "labs", "app")):
        return cand
    return os.path.dirname(os.path.abspath(__file__))   # fallback: alongside this file
_APP = os.path.join(_repo_root(), "labs", "app")
def _read(name):
    with open(os.path.join(_APP, name)) as fh:
        return fh.read()

APP_PY        = _read("app.py")
CLI_PY        = _read("cli.py")
INDEX_HTML    = _read("templates/index.html")
REQUIREMENTS  = _read("requirements.txt")

# A trimmed requirements file for the simple single-container labs (no DB driver build).
REQ_WEB = "flask==3.0.3\n"
REQ_WEB_REDIS = "flask==3.0.3\nredis==5.0.8\n"

DOCKERFILE_BASIC = """\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
"""

DOCKERIGNORE = """\
__pycache__/
*.pyc
data/
.git/
.env
*.md
"""

CLI_DOCKERFILE = """\
FROM python:3.11-slim
WORKDIR /app
COPY cli.py .
# ENTRYPOINT fixes the executable; CMD is the default argument (overridable).
ENTRYPOINT ["python", "cli.py"]
CMD ["list"]
"""

LABS = []

# ============================================================================
# DAY 1 — DOCKER
# ============================================================================

LABS.append(dict(
    num=1, slug="lab01-docker-commands", day=1, duration=30,
    topic="Docker commands",
    title="Docker Commands — Run & Manage Containers",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Get comfortable with the core Docker commands by running a real web server "
         "(nginx) and managing its whole lifecycle: start it, list it, read its logs, "
         "run a command inside it, then stop and remove it.",
    build="Run and manage an nginx web server with docker run / ps / logs / exec / stop / rm.",
    files=[],
    body=[
        h3("Part A — Run a web server in the background"),
        p("`nginx` is a real, production web server. Start it detached (`-d`), give it a "
          "name, and publish its port 80 to port 8080 on the host:"),
        code("docker run -d --name web -p 8080:80 nginx:latest\n"
             "docker ps                      # the container is running\n"
             "curl http://localhost:8080     # nginx serves its welcome page"),
        h3("Part B — Inspect a running container"),
        p("Read its logs, then run a command *inside* the container to see its hostname:"),
        code("docker logs web\n"
             "docker exec web cat /etc/hostname\n"
             "docker exec -it web /bin/bash   # open an interactive shell, then 'exit'"),
        h3("Part C — Stop, restart and clean up"),
        code("docker stop web\n"
             "docker ps -a                    # shows stopped containers too\n"
             "docker start web\n"
             "docker rm -f web                # force-remove (stops if running)"),
        note("`docker ps` lists only **running** containers; `docker ps -a` lists **all** "
             "containers including stopped ones."),
    ],
    test="Open http://localhost:8080 and confirm the nginx welcome page loads while the "
         "container is running, and that `docker ps` no longer lists `web` after `docker rm -f web`.",
))

LABS.append(dict(
    num=2, slug="lab02-images-and-inspect", day=1, duration=30,
    topic="Docker commands",
    title="Images & Inspecting Containers — pull, cp, inspect",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Work with images and look inside containers. You will pull images, copy a file "
         "out of a running container with `docker cp`, and inspect container details.",
    build="Pull images, copy a served file out of nginx with docker cp, and inspect a container.",
    files=[],
    body=[
        h3("Part A — Work with images"),
        code("docker pull nginx:latest\n"
             "docker images                  # list local images\n"
             "docker run -d --name web -p 8080:80 nginx:latest"),
        h3("Part B — Copy a file out of the container (docker cp)"),
        p("nginx serves `/usr/share/nginx/html/index.html`. Copy it to the host, edit it, "
          "and copy it back to change the live page — no rebuild needed:"),
        code("docker cp web:/usr/share/nginx/html/index.html ./index.html\n"
             "echo '<h1>Hello from TaskBoard class!</h1>' > index.html\n"
             "docker cp ./index.html web:/usr/share/nginx/html/index.html\n"
             "curl http://localhost:8080     # shows your new page"),
        h3("Part C — Inspect the container"),
        code("docker inspect web | grep -i ipaddress\n"
             "docker stats --no-stream web   # CPU / memory snapshot\n"
             "docker rm -f web"),
        note("`docker cp` copies files between a container and the host in either direction "
             "— handy for grabbing logs or config out of a running container."),
    ],
    test="After copying the edited file back, `curl http://localhost:8080` should show "
         "your custom heading instead of the default nginx page.",
))

LABS.append(dict(
    num=3, slug="lab03-build-image", day=1, duration=45,
    topic="Docker Build / Dockerfile",
    title="Build the TaskBoard Image with a Dockerfile",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Package a real application — the TaskBoard Flask web app — into your own Docker "
         "image using a Dockerfile, then run it as a container. This image is reused by "
         "several later labs.",
    build="Write a Dockerfile for the TaskBoard Flask app, build it, and run the container.",
    files=[
        ("copy", "app.py", "app.py"),
        ("copy", "templates/index.html", "templates/index.html"),
        ("write", "requirements.txt", REQ_WEB),
        ("write", "Dockerfile", DOCKERFILE_BASIC),
    ],
    body=[
        h3("What's in the folder"),
        p("`app.py` (the TaskBoard Flask app), `templates/index.html` (the board UI), "
          "`requirements.txt`, and a `Dockerfile`:"),
        code(DOCKERFILE_BASIC),
        p("Each line is a cached image **layer**. Notice `requirements.txt` is copied and "
          "installed *before* the app code, so editing `app.py` doesn't re-run `pip install`."),
        h3("Build the image"),
        code("docker build -t taskboard:1.0 .\n"
             "docker images | grep taskboard"),
        h3("Run the container"),
        code("docker run -d --name taskboard -p 8080:5000 taskboard:1.0\n"
             "curl http://localhost:8080/health\n"
             "# open http://localhost:8080 and add a few tasks"),
        h3("Watch the build cache"),
        p("Edit `app.py` (e.g. change `APP_TITLE` default) and rebuild — only the layers "
          "from `COPY . .` onward rebuild; the `pip install` layer is reused from cache:"),
        code("docker build -t taskboard:1.0 .\n"
             "docker rm -f taskboard"),
        note("Tag images with a name **and** version (`taskboard:1.0`) so you can roll "
             "forward/back later — exactly what you'll do in the Kubernetes rollout lab."),
    ],
    test="`curl http://localhost:8080/health` returns `{\"status\": \"ok\", ...}` and the "
         "board at http://localhost:8080 lets you add a task that appears in the list.",
))

LABS.append(dict(
    num=4, slug="lab04-dockerfile-best-practices", day=1, duration=30,
    topic="Dockerfile best practices",
    title="Dockerfile Best Practices — .dockerignore & layer caching",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Make the TaskBoard image smaller and faster to build. You'll add a "
         "`.dockerignore`, order instructions for maximum cache reuse, and compare image sizes.",
    build="Add a .dockerignore and cache-friendly layer ordering to slim the TaskBoard build.",
    files=[
        ("copy", "app.py", "app.py"),
        ("copy", "templates/index.html", "templates/index.html"),
        ("write", "requirements.txt", REQ_WEB),
        ("write", "Dockerfile", DOCKERFILE_BASIC),
        ("write", ".dockerignore", DOCKERIGNORE),
    ],
    body=[
        h3("Why .dockerignore"),
        p("`COPY . .` copies everything in the folder into the image — including `.git/`, "
          "caches and local `data/`. A `.dockerignore` keeps them out, shrinking the image "
          "and the build context:"),
        code(DOCKERIGNORE),
        h3("Cache-friendly ordering"),
        p("Dependencies change rarely; source changes often. Copy and install "
          "`requirements.txt` **before** copying the source so the dependency layer is "
          "cached across code edits (this is already done in our Dockerfile):"),
        code("COPY requirements.txt .\n"
             "RUN pip install --no-cache-dir -r requirements.txt\n"
             "COPY . ."),
        h3("Build and compare"),
        code("docker build -t taskboard:slim .\n"
             "docker images taskboard\n"
             "# edit app.py, rebuild, and watch most layers say 'CACHED'\n"
             "docker build -t taskboard:slim ."),
        note("`python:3.11-slim` is already a smaller base than `python:3.11`. For even "
             "smaller images, multi-stage builds copy only the artifacts you need into a "
             "fresh final stage."),
    ],
    test="The second `docker build` completes in seconds with most steps showing `CACHED`, "
         "and `docker images taskboard` shows the image built from the slim base.",
))

LABS.append(dict(
    num=5, slug="lab05-cmd-entrypoint", day=1, duration=40,
    topic="CMD vs ENTRYPOINT",
    title="CMD vs ENTRYPOINT — the taskboard-cli tool",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Understand the difference between CMD and ENTRYPOINT by packaging a real "
         "command-line tool — `taskboard-cli` — that lists and adds tasks. ENTRYPOINT "
         "fixes the program; CMD supplies the default arguments you can override at runtime.",
    build="Package taskboard-cli so ENTRYPOINT is fixed and CMD/args are overridable.",
    files=[
        ("copy", "cli.py", "cli.py"),
        ("write", "Dockerfile", CLI_DOCKERFILE),
    ],
    body=[
        h3("The Dockerfile"),
        code(CLI_DOCKERFILE),
        p("`ENTRYPOINT` is the executable that always runs. `CMD` is the **default "
          "argument** — here `list` — which is replaced by anything you pass on "
          "`docker run`."),
        h3("Build it"),
        code("docker build -t taskboard-cli ."),
        h3("CMD is the default; run args override it"),
        code("docker run --rm taskboard-cli                 # runs the default: list\n"
             "docker run --rm taskboard-cli add \"Buy milk\"   # overrides CMD with: add ...\n"
             "docker run --rm taskboard-cli add \"Ship release\"\n"
             "docker run --rm taskboard-cli list"),
        h3("ENTRYPOINT vs CMD — the contrast"),
        table([
            ["", "CMD only", "ENTRYPOINT + CMD"],
            ["Dockerfile", 'CMD ["python","cli.py","list"]', 'ENTRYPOINT ["python","cli.py"]\nCMD ["list"]'],
            ["`docker run img`", "runs list", "runs list"],
            ["`docker run img add x`", "tries to run `add` as a command (error)", "runs `cli.py add x` ✔"],
        ]),
        note("Use **ENTRYPOINT** when the image *is* a specific tool and arguments vary "
             "(like our CLI). Use **CMD** alone when you want an easily replaceable default "
             "command. Both use the JSON *exec form* `[\"a\",\"b\"]` to avoid an extra shell."),
    ],
    test="`docker run --rm taskboard-cli` prints the task list, and "
         "`docker run --rm taskboard-cli add \"Demo\"` adds a task — the same image, "
         "different CMD arguments.",
))

LABS.append(dict(
    num=6, slug="lab06-volumes", day=1, duration=40,
    topic="Volumes",
    title="Docker Storage — Named Volumes & Bind Mounts",
    killercoda=f"{KC}/day1-02-docker-storage",
    goal="Make TaskBoard's data survive container removal. You'll persist its tasks.json in "
         "a **named volume**, prove the data outlives the container, then use a **bind "
         "mount** to edit files on the host and see them live in the container.",
    build="Persist TaskBoard tasks in a named volume; live-edit host files via a bind mount.",
    files=[],
    body=[
        h3("The problem: container data is ephemeral"),
        p("By default everything written inside a container lives in its writable layer and "
          "is **lost** when the container is removed. TaskBoard writes its tasks to "
          "`DATA_DIR` — point that at a mounted volume and the data persists."),
        h3("Part A — Named volume (persistent app data)"),
        code("docker volume create taskboard-data\n"
             "docker run -d --name tb -p 8080:5000 \\\n"
             "  -e DATA_DIR=/data -v taskboard-data:/data taskboard:1.0\n"
             "# add a few tasks at http://localhost:8080, then:\n"
             "docker rm -f tb"),
        p("Start a **brand-new** container on the **same volume** — your tasks are still there:"),
        code("docker run -d --name tb2 -p 8080:5000 \\\n"
             "  -e DATA_DIR=/data -v taskboard-data:/data taskboard:1.0\n"
             "curl http://localhost:8080/api/tasks   # the tasks you added are back\n"
             "docker rm -f tb2"),
        h3("Part B — Bind mount (live host files)"),
        p("A bind mount maps a host folder straight into the container. Edit on the host, "
          "see it instantly inside — great for development:"),
        code("mkdir -p data && echo '[]' > data/tasks.json\n"
             "docker run -d --name tb3 -p 8080:5000 \\\n"
             "  -e DATA_DIR=/data -v $(pwd)/data:/data taskboard:1.0\n"
             "# add tasks in the browser, then read them straight off the host:\n"
             "cat data/tasks.json\n"
             "docker rm -f tb3"),
        table([
            ["", "Named volume", "Bind mount"],
            ["Syntax", "-v taskboard-data:/data", "-v $(pwd)/data:/data"],
            ["Managed by", "Docker", "You (host path)"],
            ["Best for", "production data, databases", "local development, live edits"],
        ]),
        note("Named volumes are stored under Docker (`/var/lib/docker/volumes`) and are the "
             "right choice for databases; bind mounts tie you to an exact host path but are "
             "perfect for editing code live."),
    ],
    test="After removing `tb` and starting `tb2` on the same named volume, "
         "`curl http://localhost:8080/api/tasks` returns the tasks you added earlier — they "
         "survived container deletion.",
))

LABS.append(dict(
    num=7, slug="lab07-networking", day=1, duration=45,
    topic="Networking",
    title="Docker Networking — Custom Bridge, DNS & Port Mapping",
    killercoda=f"{KC}/day1-03-docker-networking",
    goal="Connect two containers the way real apps do: TaskBoard reaching a Redis cache by "
         "name over a custom bridge network. You'll see why a custom network (with built-in "
         "DNS) beats the default bridge, then publish the app to the host with port mapping.",
    build="TaskBoard reaches Redis by DNS name on a custom network; publish ports to the host.",
    files=[],
    body=[
        h3("Why a custom network"),
        p("On the **default** bridge, containers can only reach each other by IP address "
          "(which changes on restart). On a **custom** bridge network, Docker provides "
          "automatic DNS, so a container can reach another by its **name** — exactly what a "
          "web app needs to find its database or cache."),
        h3("Part A — Create a network and a Redis cache"),
        code("docker network create tasknet\n"
             "docker run -d --name redis --network tasknet redis:7-alpine"),
        h3("Part B — Run TaskBoard on the same network"),
        p("TaskBoard reads `REDIS_HOST` to find the cache. Set it to the **container name** "
          "`redis` — DNS on `tasknet` resolves it automatically:"),
        code("docker run -d --name tb --network tasknet -p 8080:5000 \\\n"
             "  -e REDIS_HOST=redis taskboard:1.0\n"
             "curl http://localhost:8080      # 'visits' counter increments on each load\n"
             "curl http://localhost:8080"),
        p("Prove the DNS name resolves from inside the app container:"),
        code("docker exec tb getent hosts redis   # resolves to redis's IP on tasknet"),
        h3("Part C — Port mapping (host access)"),
        p("`-p 8080:5000` maps host port 8080 to the container's 5000. Run a second "
          "instance on a different host port — same image, two endpoints:"),
        code("docker run -d --name tb-b --network tasknet -p 8081:5000 \\\n"
             "  -e REDIS_HOST=redis taskboard:1.0\n"
             "curl http://localhost:8081/health\n"
             "docker rm -f tb tb-b redis\n"
             "docker network rm tasknet"),
        note("Because both TaskBoard instances share one Redis on the network, the visit "
             "counter is shared across them — your first taste of stateful, multi-container "
             "apps (which Compose and Kubernetes automate)."),
    ],
    test="Reloading http://localhost:8080 increases the `visits` count (served from Redis), "
         "and `docker exec tb getent hosts redis` resolves the `redis` name to an IP on the "
         "custom network.",
))

LABS.append(dict(
    num=8, slug="lab08-env-vars", day=1, duration=30,
    topic="Environment variables",
    title="Configuration with Environment Variables",
    killercoda=f"{KC}/day1-04-docker-config",
    goal="Configure the SAME TaskBoard image for different environments without rebuilding. "
         "You'll set defaults with ENV in the Dockerfile, override per-container with `-e`, "
         "and load many values at once from an `--env-file`.",
    build="Configure TaskBoard (APP_ENV, APP_TITLE) via ENV, -e and --env-file — no rebuild.",
    files=[
        ("write", ".env", "APP_ENV=production\nAPP_TITLE=TaskBoard (Prod)\n"),
    ],
    body=[
        h3("Three ways to pass configuration"),
        p("TaskBoard reads `APP_ENV` and `APP_TITLE` at runtime. The image already ships "
          "sensible defaults; you override them per environment."),
        h3("1. Defaults baked into the image (ENV)"),
        code("docker run -d --name tb -p 8080:5000 taskboard:1.0\n"
             "curl http://localhost:8080/health   # \"env\": \"development\"\n"
             "docker rm -f tb"),
        h3("2. Override per container with -e"),
        code("docker run -d --name tb -p 8080:5000 \\\n"
             "  -e APP_ENV=staging -e 'APP_TITLE=TaskBoard (Staging)' taskboard:1.0\n"
             "curl http://localhost:8080/health   # \"env\": \"staging\"\n"
             "docker rm -f tb"),
        h3("3. Load many values from an --env-file"),
        p("Keep environment config in a file (`.env`) and load it all at once:"),
        code("cat .env\n"
             "docker run -d --name tb -p 8080:5000 --env-file .env taskboard:1.0\n"
             "curl http://localhost:8080/health   # \"env\": \"production\"\n"
             "docker rm -f tb"),
        note("Never bake secrets into an image. Pass them at runtime with `-e` / "
             "`--env-file` (and in Kubernetes, with ConfigMaps and Secrets — Day 2)."),
    ],
    test="The `/health` endpoint reports `development`, then `staging`, then `production` "
         "as you change only the environment variables — the image is never rebuilt.",
))

LABS.append(dict(
    num=9, slug="lab09-docker-hub", day=1, duration=30,
    topic="Docker Hub",
    title="Sharing Images — Push to Docker Hub",
    killercoda=f"{KC}/day1-01-docker-fundamentals",
    goal="Publish your TaskBoard image to Docker Hub so anyone (and any Kubernetes cluster) "
         "can pull and run it. You'll log in, tag the image under your account, push it, "
         "then pull and run it as if you were a new user.",
    build="Tag, push and pull the TaskBoard image via Docker Hub.",
    files=[],
    body=[
        h3("Registry vs repository"),
        p("A **registry** (Docker Hub) hosts **repositories**; each repository holds the "
          "tagged versions of one image. Public images like `nginx` and `redis` live there too."),
        h3("Log in and tag"),
        p("Replace `<user>` with your Docker Hub username:"),
        code("docker login\n"
             "docker tag taskboard:1.0 <user>/taskboard:1.0"),
        h3("Push"),
        code("docker push <user>/taskboard:1.0\n"
             "# browse to https://hub.docker.com/r/<user>/taskboard to see it"),
        h3("Pull & run as a new user"),
        code("docker rmi <user>/taskboard:1.0          # remove the local copy\n"
             "docker run -d --name tb -p 8080:5000 <user>/taskboard:1.0\n"
             "curl http://localhost:8080/health\n"
             "docker rm -f tb\n"
             "docker logout"),
        note("This is exactly how Kubernetes gets your app on Day 2: the cluster pulls your "
             "image from a registry by `name:tag`. Always push a versioned tag, not just "
             "`latest`."),
    ],
    test="Your image appears at hub.docker.com under `<user>/taskboard`, and after removing "
         "the local image you can `docker run` it straight from the registry.",
))

LABS.append(dict(
    num=10, slug="lab10-compose-single", day=1, duration=30,
    topic="Docker Compose",
    title="Docker Compose — Single Service",
    killercoda=f"{KC}/day1-05-docker-compose",
    goal="Replace long `docker run` commands with a single declarative file. You'll define "
         "TaskBoard in a docker-compose.yml and manage it with the compose lifecycle: "
         "pull, up, ps, logs, down.",
    build="Define TaskBoard in docker-compose.yml; manage it with pull / up / ps / logs / down.",
    files=[
        ("copy", "app.py", "app.py"),
        ("copy", "templates/index.html", "templates/index.html"),
        ("write", "requirements.txt", REQ_WEB),
        ("write", "Dockerfile", DOCKERFILE_BASIC),
        ("write", "docker-compose.yml",
         "services:\n"
         "  web:\n"
         "    build: .\n"
         "    ports:\n"
         "      - \"8080:5000\"\n"
         "    environment:\n"
         "      - APP_ENV=development\n"
         "      - APP_TITLE=TaskBoard (Compose)\n"),
    ],
    body=[
        h3("The compose file"),
        code("services:\n"
             "  web:\n"
             "    build: .            # build from the Dockerfile in this folder\n"
             "    ports:\n"
             "      - \"8080:5000\"     # host:container\n"
             "    environment:\n"
             "      - APP_ENV=development\n"
             "      - APP_TITLE=TaskBoard (Compose)"),
        h3("The Compose lifecycle"),
        code("docker compose pull        # pull any pre-built images (none to build here)\n"
             "docker compose up -d       # build if needed and start in the background\n"
             "docker compose ps          # service status\n"
             "docker compose logs web    # logs for the web service\n"
             "curl http://localhost:8080/health"),
        h3("Tear down"),
        code("docker compose down        # stop and remove containers + network\n"
             "docker compose down -v     # also remove named volumes (full reset)"),
        note("`docker compose up -d` is idempotent — re-run it after editing the file and "
             "Compose only changes what's needed. One file replaces a page of `docker run` flags."),
    ],
    test="`docker compose up -d` starts the service and http://localhost:8080 serves "
         "TaskBoard titled 'TaskBoard (Compose)'; `docker compose down` removes it cleanly.",
))

LABS.append(dict(
    num=11, slug="lab11-compose-redis", day=1, duration=35,
    topic="Docker Compose",
    title="Docker Compose — Multi-Service (Web + Redis)",
    killercoda=f"{KC}/day1-05-docker-compose",
    goal="Add a second service. Compose puts both containers on one network and gives each "
         "a DNS name equal to its service name, so TaskBoard reaches Redis at host `redis` "
         "with zero manual networking. The visit counter is now shared and survives restarts.",
    build="Run TaskBoard + Redis with Compose; services find each other by name automatically.",
    files=[
        ("copy", "app.py", "app.py"),
        ("copy", "templates/index.html", "templates/index.html"),
        ("write", "requirements.txt", REQ_WEB_REDIS),
        ("write", "Dockerfile", DOCKERFILE_BASIC),
        ("write", "docker-compose.yml",
         "services:\n"
         "  web:\n"
         "    build: .\n"
         "    ports:\n"
         "      - \"8080:5000\"\n"
         "    environment:\n"
         "      - REDIS_HOST=redis        # the service name below\n"
         "    depends_on:\n"
         "      - redis\n"
         "  redis:\n"
         "    image: redis:7-alpine\n"
         "    volumes:\n"
         "      - redis-data:/data\n"
         "volumes:\n"
         "  redis-data:\n"),
    ],
    body=[
        h3("Two services, one file"),
        code("services:\n"
             "  web:\n"
             "    build: .\n"
             "    ports: [\"8080:5000\"]\n"
             "    environment:\n"
             "      - REDIS_HOST=redis     # <-- the other service's name\n"
             "    depends_on: [redis]\n"
             "  redis:\n"
             "    image: redis:7-alpine\n"
             "    volumes: [redis-data:/data]\n"
             "volumes:\n"
             "  redis-data:"),
        p("Compose creates a network automatically and registers each service under its "
          "name, so `REDIS_HOST=redis` just works — no IPs, no `docker network create`."),
        h3("Run the full lifecycle"),
        code("docker compose pull        # pulls redis:7-alpine\n"
             "docker compose up -d\n"
             "docker compose ps\n"
             "curl http://localhost:8080 && curl http://localhost:8080  # visits go up"),
        h3("Prove persistence, then tear down"),
        code("docker compose restart web\n"
             "curl http://localhost:8080   # counter kept (it lives in redis-data)\n"
             "docker compose down          # keep the volume\n"
             "docker compose down -v       # remove the redis-data volume too"),
        note("`depends_on` controls **start order**, not readiness — the next lab adds a "
             "**health check** so the web service waits until the database is truly ready."),
    ],
    test="Reloading http://localhost:8080 increments the visit counter, and the count "
         "survives `docker compose restart web` because it is stored in the `redis-data` volume.",
))

LABS.append(dict(
    num=12, slug="lab12-compose-fullstack", day=1, duration=40,
    topic="Docker Compose",
    title="Docker Compose — Full-Stack (Web + PostgreSQL + Redis)",
    killercoda=f"{KC}/day1-05-docker-compose",
    goal="Build the complete TaskBoard stack: the web app backed by PostgreSQL for tasks "
         "and Redis for the visit counter, with a health check so the app starts only once "
         "the database is ready. This is the architecture you'll deploy to Kubernetes on Day 2.",
    build="Run TaskBoard + Postgres + Redis with healthchecks and condition-based depends_on.",
    files=[
        ("copy", "app.py", "app.py"),
        ("copy", "templates/index.html", "templates/index.html"),
        ("write", "requirements.txt", REQUIREMENTS),
        ("write", "Dockerfile", DOCKERFILE_BASIC),
        ("write", "docker-compose.yml",
         "services:\n"
         "  web:\n"
         "    build: .\n"
         "    ports:\n"
         "      - \"8080:5000\"\n"
         "    environment:\n"
         "      - APP_ENV=production\n"
         "      - DATABASE_URL=postgresql://taskboard:secret@db:5432/taskboard\n"
         "      - REDIS_HOST=redis\n"
         "    depends_on:\n"
         "      db:\n"
         "        condition: service_healthy\n"
         "      redis:\n"
         "        condition: service_started\n"
         "  db:\n"
         "    image: postgres:16-alpine\n"
         "    environment:\n"
         "      - POSTGRES_USER=taskboard\n"
         "      - POSTGRES_PASSWORD=secret\n"
         "      - POSTGRES_DB=taskboard\n"
         "    volumes:\n"
         "      - pgdata:/var/lib/postgresql/data\n"
         "    healthcheck:\n"
         "      test: [\"CMD-SHELL\", \"pg_isready -U taskboard\"]\n"
         "      interval: 5s\n"
         "      timeout: 3s\n"
         "      retries: 5\n"
         "  redis:\n"
         "    image: redis:7-alpine\n"
         "volumes:\n"
         "  pgdata:\n"),
    ],
    body=[
        h3("The full stack"),
        p("Three services: `web` (TaskBoard), `db` (PostgreSQL, storing tasks), and `redis` "
          "(visit counter). The web service waits for the database's **health check** to "
          "pass before it starts, so it never crashes on a not-yet-ready database."),
        code("services:\n"
             "  web:\n"
             "    build: .\n"
             "    ports: [\"8080:5000\"]\n"
             "    environment:\n"
             "      - DATABASE_URL=postgresql://taskboard:secret@db:5432/taskboard\n"
             "      - REDIS_HOST=redis\n"
             "    depends_on:\n"
             "      db: { condition: service_healthy }\n"
             "      redis: { condition: service_started }\n"
             "  db:\n"
             "    image: postgres:16-alpine\n"
             "    healthcheck:\n"
             "      test: [\"CMD-SHELL\", \"pg_isready -U taskboard\"]\n"
             "      interval: 5s\n"
             "      retries: 5\n"
             "  redis: { image: redis:7-alpine }"),
        h3("Run the lifecycle"),
        code("docker compose pull        # pulls postgres + redis\n"
             "docker compose up -d        # builds web, waits for db health, then starts web\n"
             "docker compose ps           # db shows (healthy)\n"
             "docker compose logs web"),
        h3("Verify tasks persist in Postgres"),
        code("# add tasks at http://localhost:8080, then prove they're in the DB:\n"
             "docker compose exec db psql -U taskboard -c 'SELECT id, text, done FROM tasks;'\n"
             "docker compose restart web\n"
             "curl http://localhost:8080/api/tasks   # tasks still there (in Postgres)"),
        h3("Tear down"),
        code("docker compose down         # stop & remove containers + network\n"
             "docker compose down -v      # also drop the pgdata volume"),
        note("This web + database + cache shape is the canonical cloud app. On Day 2 you'll "
             "deploy this very app to Kubernetes — as Pods, a Deployment, a Service, and "
             "persistent storage."),
    ],
    test="`docker compose ps` shows `db` as `(healthy)`, tasks added in the browser appear "
         "in `SELECT * FROM tasks`, and they survive `docker compose restart web`.",
))

# ============================================================================
# DAY 2 — KUBERNETES (deploy the TaskBoard app)
# ============================================================================

POD_YAML = """\
apiVersion: v1
kind: Pod
metadata:
  name: taskboard
  labels:
    app: taskboard
spec:
  containers:
    - name: web
      image: nginx          # swap for <user>/taskboard:1.0 to run your own image
      ports:
        - containerPort: 80
"""

DEPLOY_YAML = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: taskboard
  template:
    metadata:
      labels:
        app: taskboard
    spec:
      containers:
        - name: web
          image: nginx
          ports:
            - containerPort: 80
"""

SERVICE_YAML = """\
apiVersion: v1
kind: Service
metadata:
  name: taskboard-svc
spec:
  type: NodePort
  selector:
    app: taskboard
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080
"""

EMPTYDIR_YAML = """\
apiVersion: v1
kind: Pod
metadata:
  name: shared-pod
spec:
  containers:
    - name: writer
      image: busybox
      command: ["sh", "-c", "echo 'hello from writer' > /data/message.txt && sleep 3600"]
      volumeMounts:
        - name: shared-data
          mountPath: /data
    - name: reader
      image: busybox
      command: ["sh", "-c", "sleep 5 && cat /data/message.txt && sleep 3600"]
      volumeMounts:
        - name: shared-data
          mountPath: /data
  volumes:
    - name: shared-data
      emptyDir: {}
"""

PV_YAML = """\
apiVersion: v1
kind: PersistentVolume
metadata:
  name: taskboard-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/taskboard-data
"""

PVC_YAML = """\
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: taskboard-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
"""

POD_PVC_YAML = """\
apiVersion: v1
kind: Pod
metadata:
  name: pvc-pod
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "echo 'persistent data' > /data/file.txt && sleep 3600"]
      volumeMounts:
        - name: store
          mountPath: /data
  volumes:
    - name: store
      persistentVolumeClaim:
        claimName: taskboard-pvc
"""

JOB_YAML = """\
apiVersion: batch/v1
kind: Job
metadata:
  name: taskboard-report
spec:
  completions: 3
  parallelism: 2
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: report
          image: busybox
          command: ["sh", "-c", "echo 'Generating TaskBoard report...'; sleep 5; echo done"]
"""

CRONJOB_YAML = """\
apiVersion: batch/v1
kind: CronJob
metadata:
  name: taskboard-cleanup
spec:
  schedule: "*/1 * * * *"     # every minute (demo); real cleanup might be nightly
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: cleanup
              image: busybox
              command: ["sh", "-c", "echo 'Cleaning up old TaskBoard sessions...'; date"]
"""

LABS.append(dict(
    num=13, slug="lab13-pods", day=2, duration=35,
    topic="Pods",
    title="Kubernetes Pods — Imperative & Declarative",
    killercoda=f"{KC}/day2-01-k8s-pods-namespaces",
    goal="Meet the smallest deployable unit in Kubernetes — the Pod. You'll create one "
         "imperatively with a single command, inspect it, then create one declaratively "
         "from a YAML file (the approach you'll use for everything afterwards).",
    build="Create, inspect and delete a Pod both imperatively and from a pod.yaml manifest.",
    files=[("write", "pod.yaml", POD_YAML)],
    body=[
        h3("Part A — Imperative (one command)"),
        code("kubectl run web --image=nginx\n"
             "kubectl get pods\n"
             "kubectl get pods -o wide          # node + Pod IP\n"
             "kubectl describe pod web          # events, container, volumes"),
        p("Look inside the Pod, then remove it:"),
        code("kubectl logs web\n"
             "kubectl exec web -- cat /etc/hostname\n"
             "kubectl exec -it web -- /bin/sh   # interactive shell, then 'exit'\n"
             "kubectl delete pod web"),
        h3("Part B — Declarative (pod.yaml)"),
        p("Real work is declarative: you describe the desired state in YAML and apply it."),
        code(POD_YAML),
        code("kubectl apply -f pod.yaml\n"
             "kubectl get pods\n"
             "kubectl describe pod taskboard\n"
             "kubectl delete -f pod.yaml"),
        note("Pods are **ephemeral** — if a Pod dies it is not recreated. That's why you "
             "almost always run Pods through a **Deployment** (Lab 15), not on their own."),
    ],
    test="`kubectl get pods` shows the `taskboard` Pod as `Running` after `kubectl apply`, "
         "and it disappears after `kubectl delete -f pod.yaml`.",
))

LABS.append(dict(
    num=14, slug="lab14-namespaces", day=2, duration=25,
    topic="Namespaces",
    title="Kubernetes Namespaces — Environment Isolation",
    killercoda=f"{KC}/day2-01-k8s-pods-namespaces",
    goal="Use namespaces to keep environments apart inside one cluster. You'll create a "
         "`dev` namespace, run a Pod in it, and see how resources are isolated by namespace.",
    build="Create a dev namespace, run a Pod inside it, and list resources per namespace.",
    files=[],
    body=[
        h3("List and create namespaces"),
        code("kubectl get namespaces\n"
             "kubectl create namespace dev"),
        h3("Run a Pod inside a namespace"),
        code("kubectl run web --image=nginx -n dev\n"
             "kubectl get pods -n dev\n"
             "kubectl get pods                  # default ns: not shown here\n"
             "kubectl get pods --all-namespaces"),
        h3("Clean up the whole namespace"),
        p("Deleting a namespace removes **everything** inside it — a fast way to tear down "
          "an environment:"),
        code("kubectl delete namespace dev"),
        note("Namespaces are perfect for separating `dev` / `staging` / `prod` (or per-team "
             "quotas) on a single shared cluster."),
    ],
    test="`kubectl get pods -n dev` lists the Pod while it exists, and "
         "`kubectl delete namespace dev` removes the namespace and its Pod together.",
))

LABS.append(dict(
    num=15, slug="lab15-deployments", day=2, duration=40,
    topic="Deployments",
    title="Deployments — Scaling & Self-Healing",
    killercoda=f"{KC}/day2-02-k8s-deployments",
    goal="Run TaskBoard the production way — as a Deployment that keeps a desired number of "
         "replicas alive. You'll scale it, watch it self-heal when a Pod is deleted, and "
         "manage it both imperatively and from YAML.",
    build="Create a Deployment, scale it, and watch Kubernetes self-heal a deleted Pod.",
    files=[("write", "deployment.yaml", DEPLOY_YAML)],
    body=[
        h3("Part A — Create and scale (imperative)"),
        code("kubectl create deployment taskboard --image=nginx\n"
             "kubectl get deployments\n"
             "kubectl get pods\n"
             "kubectl scale deployment taskboard --replicas=3\n"
             "kubectl get pods               # now 3 Pods"),
        h3("Part B — Watch it self-heal"),
        p("Delete one Pod and watch the Deployment's ReplicaSet immediately create a "
          "replacement to restore the desired count:"),
        code("kubectl get pods\n"
             "kubectl delete pod <one-pod-name>\n"
             "kubectl get pods               # a new Pod is already being created"),
        h3("Part C — Declarative (deployment.yaml)"),
        code(DEPLOY_YAML),
        code("kubectl delete deployment taskboard\n"
             "kubectl apply -f deployment.yaml\n"
             "kubectl get pods\n"
             "kubectl delete -f deployment.yaml"),
        note("A Deployment manages a **ReplicaSet**, which guarantees the desired Pod count "
             "is always running — this is the self-healing that naked Pods (Lab 13) lack."),
    ],
    test="After `kubectl delete pod <name>`, `kubectl get pods` still shows 3 Pods because "
         "the Deployment recreated the missing one automatically.",
))

LABS.append(dict(
    num=16, slug="lab16-rollouts", day=2, duration=35,
    topic="Rolling updates & rollbacks",
    title="Rolling Updates & Rollbacks",
    killercoda=f"{KC}/day2-03-k8s-rollouts",
    goal="Ship a new version of TaskBoard with zero downtime, then instantly roll back when "
         "something's wrong. You'll update the container image, track the rollout, and "
         "revert to a previous revision.",
    build="Roll a Deployment forward to a new image with no downtime, then roll it back.",
    files=[],
    body=[
        h3("Part A — Deploy v1, then update the image"),
        code("kubectl create deployment taskboard --image=nginx:1.24 --replicas=3\n"
             "kubectl rollout status deployment taskboard\n"
             "kubectl describe deployment taskboard | grep Image"),
        p("Update the image — Kubernetes shifts Pods gradually from the old to the new "
          "ReplicaSet (rolling update, the default strategy):"),
        code("kubectl set image deployment/taskboard nginx=nginx:1.25\n"
             "kubectl rollout status deployment taskboard\n"
             "kubectl describe deployment taskboard | grep Image   # now 1.25"),
        h3("Part B — Roll back"),
        code("kubectl rollout history deployment taskboard\n"
             "kubectl rollout undo deployment taskboard            # back to 1.24\n"
             "kubectl describe deployment taskboard | grep Image\n"
             "kubectl rollout undo deployment taskboard --to-revision=2   # forward to 1.25 again\n"
             "kubectl delete deployment taskboard"),
        note("Rolling updates keep old and new Pods running simultaneously so users never "
             "see downtime; a rollback is just a rollout to a previous revision."),
    ],
    test="`kubectl describe deployment taskboard | grep Image` shows `nginx:1.25` after the "
         "update and `nginx:1.24` after `kubectl rollout undo`.",
))

LABS.append(dict(
    num=17, slug="lab17-services", day=2, duration=40,
    topic="Services",
    title="Services — ClusterIP & NodePort",
    killercoda=f"{KC}/day2-04-k8s-services",
    goal="Give your Pods a stable address. Pod IPs change constantly; a Service provides one "
         "durable endpoint with built-in load balancing. You'll expose TaskBoard internally "
         "with ClusterIP and externally with NodePort, both imperatively and from YAML.",
    build="Expose a Deployment with ClusterIP (internal) and NodePort (external) Services.",
    files=[("write", "deployment.yaml", DEPLOY_YAML), ("write", "service.yaml", SERVICE_YAML)],
    body=[
        h3("Part A — ClusterIP (internal)"),
        code("kubectl create deployment taskboard --image=nginx --replicas=2\n"
             "kubectl expose deployment taskboard --port=80 --target-port=80\n"
             "kubectl get service taskboard\n"
             "kubectl get endpoints taskboard      # the Pod IPs behind the Service"),
        h3("Part B — NodePort (external)"),
        code("kubectl delete service taskboard\n"
             "kubectl expose deployment taskboard \\\n"
             "  --type=NodePort --port=80 --target-port=80\n"
             "kubectl get service taskboard         # note the 3xxxx port"),
        h3("Part C — Declarative (Service + Deployment YAML)"),
        code(SERVICE_YAML),
        code("kubectl delete deployment taskboard service taskboard\n"
             "kubectl apply -f deployment.yaml\n"
             "kubectl apply -f service.yaml\n"
             "kubectl get svc taskboard-svc          # NodePort 30080\n"
             "kubectl delete -f service.yaml -f deployment.yaml"),
        note("ClusterIP is internal-only (service-to-service). NodePort opens a port on every "
             "node for outside access. In the cloud, LoadBalancer fronts NodePort with a real "
             "external IP."),
    ],
    test="`kubectl get endpoints taskboard` lists 2 Pod IPs behind the Service, and the "
         "NodePort Service shows a port in the 30000–32767 range.",
))

LABS.append(dict(
    num=18, slug="lab18-storage", day=2, duration=40,
    topic="Storage",
    title="Kubernetes Storage — emptyDir, PV & PVC",
    killercoda=f"{KC}/day2-05-k8s-storage-jobs",
    goal="Persist data in Kubernetes. You'll share a scratch directory between two "
         "containers with `emptyDir`, then provision durable storage with a PersistentVolume "
         "and claim it with a PersistentVolumeClaim so data survives Pod deletion.",
    build="Share data with emptyDir; provision durable storage with a PV + PVC.",
    files=[
        ("write", "emptydir-pod.yaml", EMPTYDIR_YAML),
        ("write", "pv.yaml", PV_YAML),
        ("write", "pvc.yaml", PVC_YAML),
        ("write", "pod-with-pvc.yaml", POD_PVC_YAML),
    ],
    body=[
        h3("Part A — emptyDir (shared, temporary)"),
        p("`emptyDir` is a scratch volume shared by all containers in a Pod and deleted with "
          "the Pod. Here a `writer` container writes a file a `reader` container reads:"),
        code(EMPTYDIR_YAML),
        code("kubectl apply -f emptydir-pod.yaml\n"
             "kubectl exec shared-pod -c reader -- cat /data/message.txt\n"
             "kubectl delete pod shared-pod      # emptyDir data is gone"),
        h3("Part B — PersistentVolume & Claim (durable)"),
        p("A PV is cluster storage; a PVC requests a slice of it. Bind them, then mount the "
          "claim in a Pod:"),
        code("kubectl apply -f pv.yaml\n"
             "kubectl apply -f pvc.yaml\n"
             "kubectl get pv,pvc                 # both should show Bound"),
        code("kubectl apply -f pod-with-pvc.yaml\n"
             "kubectl exec pvc-pod -- cat /data/file.txt\n"
             "kubectl delete pod pvc-pod\n"
             "kubectl apply -f pod-with-pvc.yaml # recreate...\n"
             "kubectl exec pvc-pod -- cat /data/file.txt   # ...data is still there\n"
             "kubectl delete pod pvc-pod\n"
             "kubectl delete -f pvc.yaml -f pv.yaml"),
        note("This PV/PVC pattern is how a real TaskBoard Postgres database keeps its data in "
             "Kubernetes — storage outlives any individual Pod."),
    ],
    test="After deleting and recreating `pvc-pod`, `kubectl exec pvc-pod -- cat /data/file.txt` "
         "still prints `persistent data` — the PVC kept it across Pod deletion.",
))

LABS.append(dict(
    num=19, slug="lab19-jobs-cronjobs", day=2, duration=35,
    topic="Jobs & CronJobs",
    title="Jobs & CronJobs — Batch and Scheduled Tasks",
    killercoda=f"{KC}/day2-05-k8s-storage-jobs",
    goal="Run work that finishes (unlike a web server that runs forever). A Job runs Pods to "
         "completion — perfect for a TaskBoard report — and a CronJob runs Jobs on a "
         "schedule, perfect for a nightly cleanup.",
    build="Run a batch Job (report) to completion and a scheduled CronJob (cleanup).",
    files=[("write", "job.yaml", JOB_YAML), ("write", "cronjob.yaml", CRONJOB_YAML)],
    body=[
        h3("Part A — Job (run to completion)"),
        code("kubectl create job hello --image=busybox -- echo 'Hello from a Job!'\n"
             "kubectl get jobs\n"
             "kubectl logs job/hello\n"
             "kubectl delete job hello"),
        p("Declarative — 3 completions, 2 running in parallel:"),
        code(JOB_YAML),
        code("kubectl apply -f job.yaml\n"
             "kubectl get pods                 # up to 2 running at once\n"
             "kubectl get job taskboard-report # COMPLETIONS climbs to 3/3\n"
             "kubectl delete -f job.yaml"),
        h3("Part B — CronJob (scheduled)"),
        code(CRONJOB_YAML),
        code("kubectl apply -f cronjob.yaml\n"
             "kubectl get cronjob taskboard-cleanup\n"
             "# wait ~1 minute for the first Job to be created:\n"
             "kubectl get jobs\n"
             "kubectl logs job/<created-job-name>\n"
             "kubectl delete -f cronjob.yaml"),
        note("Jobs use `restartPolicy: Never` and do **not** restart after success — unlike a "
             "Deployment, which keeps Pods running forever. CronJobs use standard cron syntax."),
    ],
    test="`kubectl get job taskboard-report` reaches `3/3` completions, and after ~1 minute "
         "the CronJob has spawned at least one Job visible in `kubectl get jobs`.",
))

# ----------------------------------------------------------------- helpers for generators
DAY1 = [l for l in LABS if l["day"] == 1]
DAY2 = [l for l in LABS if l["day"] == 2]

def lab_by_num(n):
    return next(l for l in LABS if l["num"] == n)

