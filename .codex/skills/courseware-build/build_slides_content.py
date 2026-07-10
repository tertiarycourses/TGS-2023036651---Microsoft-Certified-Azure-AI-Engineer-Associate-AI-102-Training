"""Concept slides + slide sequence for the Docker & Kubernetes deck.
build(g) receives build_slides.py's globals (helpers + colours + labs_data as L)."""

def build(g):
    cover=g["cover"]; section=g["section"]; content=g["content"]; two_col=g["two_col"]
    cards3=g["cards3"]; big=g["big_statement"]; brk=g["brk"]
    about=g["about_trainer"]; digital_attendance=g["digital_attendance"]
    icon_cards=g["icon_cards"]; grid_cards=g["grid_cards"]; lesson_plan_cards=g["lesson_plan_cards"]
    learning_outcomes=g["learning_outcomes"]; assessment_twocard=g["assessment_twocard"]
    assessment_flow=g["assessment_flow"]; cert_traqom=g["cert_traqom"]
    lab_deck=g["lab_deck"]
    BLUE=g["BLUE"]; TEAL=g["TEAL"]; VIOLET=g["VIOLET"]; AMBER=g["AMBER"]

    # ===================================================== COVER + ADMIN
    cover()
    section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
    digital_attendance()
    about(name="Mohan Pothula", role="Enterprise DevOps & Cloud Trainer", rows=[
        ("ic_grad","Role","Principal DevOps & Cloud trainer at Tertiary Infotech Academy."),
        ("ic_laptop","Qualifications","Certified Kubernetes Administrator (CKA) · Docker Certified Associate (DCA) · AWS Solutions Architect."),
        ("ic_person","Expertise","Docker · Kubernetes · CI/CD · Cloud (AWS) · platform engineering."),
        ("ic_brief","Experience","20+ years across DBS Bank, SingTel, Mediacorp and SPH Media.")])
    about(blank=True, rows=[("ic_laptop","Qualifications:",""),("ic_person","Expertise:",""),
        ("ic_brief","Experience:",""),("ic_link","Contact / Profile:","")])
    icon_cards("Let's Know Each Other","ICE-BREAKER",[
        ("ic_person2","Your role","Your name and organisation / role."),
        ("ic_code","Your experience","Any experience with Docker, servers or the cloud."),
        ("ic_target","Your goal","What you want to containerise or deploy after this course.")],
        sub="Take a minute to introduce yourself to the class:")
    grid_cards("Ground Rules","HOUSE RULES",[
        ("ic_gr1","Phones on silent","Set your phone to silent mode."),
        ("ic_gr2","Participate actively","No question is too small — ask freely."),
        ("ic_gr3","Mutual respect","One conversation at a time."),
        ("ic_gr4","Be punctual","Return from breaks on time."),
        ("ic_gr6","Step out quietly","For calls or short breaks."),
        ("ic_gr5","75% attendance","Required for funding eligibility.")])
    lesson_plan_cards([
        ("1",[("Docker",True),("· Fundamentals & commands (Labs 1–2)",False),
              ("· Dockerfile, build & CMD/ENTRYPOINT (Labs 3–5)",False),
              ("· Storage, networking, config (Labs 6–8)",False),
              ("· Docker Hub & Compose (Labs 9–12)",False)]),
        ("2",[("Kubernetes",True),("· Pods & Namespaces (Labs 13–14)",False),
              ("· Deployments & Rollouts (Labs 15–16)",False),
              ("· Services (Lab 17)",False),
              ("· Storage, Jobs & CronJobs (Labs 18–19)",False),
              ("· Final assessment from 4:00 PM",False)])],
        "9:00am – 6:00pm   ·   1-hour lunch   ·   short tea breaks within each day")
    learning_outcomes([
        "Explain containerisation and manage containers with the Docker CLI.",
        "Build images with a Dockerfile and use CMD vs ENTRYPOINT correctly.",
        "Persist data with volumes and connect containers over custom networks.",
        "Run multi-service apps (web + cache + database) with Docker Compose.",
        "Deploy, scale and update applications on Kubernetes.",
        "Expose Services and persist data with PersistentVolumes & Claims."])
    assessment_twocard()
    grid_cards("Briefing for Assessment","ASSESSMENT RULES",[
        ("ic_br1","Clear your space","Keep only approved materials on the table."),
        ("ic_br2","No recording","No photos of the assessment."),
        ("ic_br3","Work individually","No discussion during the assessment."),
        ("ic_br4","Use the LMS","The assessment is delivered online."),
        ("ic_br5","Open book","Slides & Learner Guide are allowed."),
        ("ic_br6","Time's up","Submit when time is up.")])

    # ===================================================== DAY 1 — DOCKER
    section("DAY 1","Docker","01","Containers · Images · Storage · Networking · Compose")

    # -- Topic 1: Fundamentals
    section("TOPIC 1","Docker Fundamentals","","Containers, the Docker engine & core commands")
    content("The Problem: 'It Works on My Machine'",[
        "Apps break when the environment differs — OS, language version, missing dependencies or config.",
        "Docker packages the app AND its environment into one portable image that runs identically everywhere.",
        "An image is a read-only blueprint; a container is a running instance of it.",
        "Containers are lightweight — they share the host kernel and start in milliseconds."],kicker="OVERVIEW")
    two_col("Virtual Machines vs Containers",
        [("Full guest OS per VM",0),("Boot time: seconds–minutes",0),("Size: gigabytes",0),
         ("Hypervisor overhead",0),("Examples: VMware, VirtualBox, EC2",0)],
        [("Share the host OS kernel",0),("Start time: milliseconds",0),("Size: megabytes",0),
         ("Minimal overhead",0),("Examples: Docker, containerd",0)],
        kicker="WHY CONTAINERS",lhead="Virtual Machines",rhead="Containers")
    cards3("Docker Architecture",[
        (BLUE,"Docker Client",["The CLI you type","docker run / build / ps","Talks to the daemon"]),
        (TEAL,"Docker Daemon",["Runs on the host","Manages images & containers","Networks & volumes"]),
        (VIOLET,"Registry",["Stores & shares images","Docker Hub = default","pull / push images"])],kicker="HOW IT WORKS")
    content("Core Docker Commands",[
        "docker run — create and start a container from an image.",
        "docker ps / ps -a — list running / all containers.",
        "docker logs / exec — read logs / run a command inside a container.",
        "docker stop / rm — stop / delete a container; docker images — list images."],kicker="THE CLI")
    lab_deck(1,"DAY 1 · DOCKER FUNDAMENTALS")
    lab_deck(2,"DAY 1 · DOCKER FUNDAMENTALS")
    brk("Tea Break","15 minutes",TEAL)

    # -- Topic 2: Dockerfile & Build
    section("TOPIC 2","Dockerfile & Build","","Build your own images — layers, cache, CMD vs ENTRYPOINT")
    content("What is a Dockerfile?",[
        "A text recipe of instructions Docker runs to build an image automatically.",
        "FROM (base image) · WORKDIR · COPY · RUN · EXPOSE · ENV · CMD / ENTRYPOINT.",
        "Each instruction creates a cached layer — unchanged layers are reused.",
        "Order matters: put rarely-changing steps (dependencies) before source code."],kicker="BUILDING IMAGES")
    content("Image Layers & Build Cache",[
        "An image is a stack of layers; each instruction adds one.",
        "If a layer is unchanged, Docker reuses it from cache — fast rebuilds.",
        "COPY requirements.txt + RUN pip install BEFORE COPY . . keeps deps cached.",
        "A .dockerignore keeps junk (.git, caches) out of the build context."],kicker="LAYERS & CACHE")
    two_col("CMD vs ENTRYPOINT",
        [("Default command — overridable",0),('CMD ["python","app.py"]',0),
         ("Override: docker run img bash",0),("Use for a replaceable default",0)],
        [("Fixed executable — args appended",0),('ENTRYPOINT ["python","cli.py"]',0),
         ('CMD ["list"]  → default arg',0),("Use when the image IS a tool",0)],
        kicker="INSTRUCTIONS",lhead="CMD",rhead="ENTRYPOINT")
    lab_deck(3,"DAY 1 · DOCKERFILE & BUILD")
    lab_deck(4,"DAY 1 · DOCKERFILE & BUILD")
    lab_deck(5,"DAY 1 · CMD vs ENTRYPOINT")
    brk("Lunch Break","1 hour",BLUE)

    # -- Topic 3: Storage
    section("TOPIC 3","Docker Storage","","Persist data with volumes & bind mounts")
    content("Why Volumes?",[
        "Data written inside a container is lost when the container is removed.",
        "Named volumes — Docker-managed persistent storage; best for databases & app data.",
        "Bind mounts — map an exact host folder in; best for live code editing in dev.",
        "Mount with -v name:/path (volume) or -v $(pwd)/dir:/path (bind mount)."],kicker="PERSISTENCE")
    lab_deck(6,"DAY 1 · DOCKER STORAGE")

    # -- Topic 4: Networking
    section("TOPIC 4","Docker Networking","","Custom bridge networks, DNS & port mapping")
    content("Networking Concepts",[
        "Default bridge: containers reach each other only by IP (which changes).",
        "Custom bridge: built-in DNS — containers reach each other by name.",
        "That's how a web app finds its database/cache: by container/service name.",
        "Port mapping (-p host:container) exposes a container to the host."],kicker="CONNECTING CONTAINERS")
    lab_deck(7,"DAY 1 · DOCKER NETWORKING")

    # -- Topic 5: Configuration & Docker Hub
    section("TOPIC 5","Configuration & Docker Hub","","Runtime config & sharing images")
    content("Environment Variables & Registries",[
        "Configure the same image per environment with ENV, -e and --env-file — no rebuild.",
        "Never bake secrets into an image; pass them at runtime.",
        "Docker Hub is the default public registry: docker tag → push → pull.",
        "Kubernetes pulls your image from a registry by name:tag (Day 2)."],kicker="CONFIG & REGISTRY")
    lab_deck(8,"DAY 1 · CONFIGURATION")
    brk("Tea Break","15 minutes",TEAL)
    lab_deck(9,"DAY 1 · DOCKER HUB")

    # -- Topic 6: Compose
    section("TOPIC 6","Docker Compose","","Define multi-service apps in one YAML file")
    content("What is Docker Compose?",[
        "Define all your services, networks and volumes in one docker-compose.yml.",
        "Compose creates a shared network; services reach each other by service name.",
        "Lifecycle: docker compose pull → up -d → ps / logs → down (and down -v).",
        "healthcheck + depends_on: condition lets the app wait for the database."],kicker="MULTI-SERVICE")
    cards3("The TaskBoard Stack",[
        (BLUE,"web",["TaskBoard Flask app","Built from the Dockerfile","Port 8080 → 5000"]),
        (VIOLET,"db (Postgres)",["Stores the tasks","Health-checked","pgdata volume"]),
        (TEAL,"redis",["Visit counter / cache","redis:7-alpine","Reached by name"])],kicker="WEB + DB + CACHE")
    lab_deck(10,"DAY 1 · DOCKER COMPOSE")
    lab_deck(11,"DAY 1 · DOCKER COMPOSE")
    lab_deck(12,"DAY 1 · DOCKER COMPOSE")
    big("Day 1 done — you containerised a full app.","Tomorrow: deploy TaskBoard to Kubernetes and scale it.","WRAP-UP",color=BLUE)

    # ===================================================== DAY 2 — KUBERNETES
    section("DAY 2","Kubernetes","02","Pods · Deployments · Services · Storage")
    section("TOPIC 7","Kubernetes Fundamentals","","Architecture, the control plane & kubectl")
    content("Why Kubernetes?",[
        "Docker runs containers on one host; Kubernetes orchestrates them across a cluster.",
        "It self-heals (restarts failed Pods), scales, and rolls out updates with no downtime.",
        "Declarative: you describe desired state in YAML; Kubernetes makes it true.",
        "kubectl is the CLI: get / describe / apply / delete / scale / rollout."],kicker="ORCHESTRATION")
    cards3("Cluster Architecture",[
        (BLUE,"Control Plane",["API Server","etcd (state store)","Scheduler","Controller Manager"]),
        (TEAL,"Worker Nodes",["kubelet (node agent)","kube-proxy (networking)","Run your Pods"]),
        (VIOLET,"Core Objects",["Pod · Deployment","Service · Namespace","PV / PVC · Job"])],kicker="HOW IT WORKS")

    section("TOPIC 8","Pods & Namespaces","","The smallest unit & environment isolation")
    content("Pods & Namespaces",[
        "A Pod is the smallest unit — one or more containers sharing network & storage.",
        "Pods are ephemeral; you normally run them via a Deployment (self-healing).",
        "Create Pods imperatively (kubectl run) or declaratively (kubectl apply -f).",
        "Namespaces isolate environments (dev / staging / prod) on one cluster."],kicker="FOUNDATIONS")
    lab_deck(13,"DAY 2 · PODS")
    lab_deck(14,"DAY 2 · NAMESPACES")
    brk("Tea Break","15 minutes",TEAL)

    section("TOPIC 9","Deployments & Rollouts","","Scaling, self-healing & zero-downtime updates")
    content("Deployments, ReplicaSets & Rollouts",[
        "A Deployment manages a ReplicaSet that keeps N identical Pods running.",
        "Self-healing: delete a Pod and the ReplicaSet recreates it automatically.",
        "Scale with kubectl scale; update the image with kubectl set image.",
        "Rolling updates keep old + new Pods running; rollback = kubectl rollout undo."],kicker="RUN AT SCALE")
    lab_deck(15,"DAY 2 · DEPLOYMENTS")
    lab_deck(16,"DAY 2 · ROLLOUTS & ROLLBACKS")
    brk("Lunch Break","1 hour",BLUE)

    section("TOPIC 10","Services","","Stable endpoints & load balancing")
    content("Why Services?",[
        "Pod IPs change on every restart, scale or update — you can't rely on them.",
        "A Service gives a stable address and load-balances across matching Pods.",
        "ClusterIP — internal only (service-to-service).",
        "NodePort — opens a port on every node for external access (30000–32767)."],kicker="NETWORKING")
    lab_deck(17,"DAY 2 · SERVICES")

    section("TOPIC 11","Storage, Jobs & CronJobs","","Persist data & run batch work")
    content("Storage & Batch Workloads",[
        "emptyDir — scratch storage shared by containers in a Pod (lost with the Pod).",
        "PersistentVolume (PV) + PersistentVolumeClaim (PVC) — durable storage that outlives Pods.",
        "A Job runs Pods to completion (e.g. a report); it doesn't restart on success.",
        "A CronJob runs Jobs on a schedule (standard cron syntax)."],kicker="PERSIST & SCHEDULE")
    lab_deck(18,"DAY 2 · STORAGE")
    lab_deck(19,"DAY 2 · JOBS & CRONJOBS")

    # ===================================================== ASSESSMENT & CLOSING (admin back matter)
    section("COURSE CLOSING","Assessment & Wrap-up","")
    assessment_twocard()
    assessment_flow()
    cert_traqom()
    big("Congratulations!","You took one app from a single container to a scaled Kubernetes deployment.","THANK YOU",color=TEAL)
