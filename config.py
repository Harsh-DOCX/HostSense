DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"

MAX_TOKENS = 300
REQUEST_TIMEOUT_SECONDS = 45
USER_DATA_FILE = "data/user_sessions.json"

LIFE_LIMIT = 3
RECOVERY_REQUIRED = 4

ALLOWED_TOPICS = [
    # Core infra
    "server", "servers", "hosting", "host", "vps", "cloud",
    "infrastructure", "instance", "vm", "virtual machine", "node",
    # OS / web servers
    "linux", "nginx", "apache", "webserver",
    # Networking
    "dns", "ip", "http", "https", "tcp", "udp",
    "port", "socket", "bandwidth", "ping",
    # Security
    "ssl", "tls", "firewall", "ssh", "encryption",
    "certificate", "permissions",
    # Containers / orchestration
    "docker", "container", "image",
    "kubernetes", "pod", "cluster",
    # Performance / issues
    "uptime", "latency", "slow", "lag", "down",
    "crash", "timeout", "not loading", "overload",
    # Deployment / DevOps
    "deployment", "deploy", "pipeline", "ci", "cd",
    "build", "release", "rollback",
    # Database
    "database", "db", "sql", "nosql",
    "query", "backup", "restore",
    # Web / hosting context
    "website", "site", "domain", "subdomain", "url",
    # Cloud providers
    "aws", "gcp", "azure", "digitalocean",
    # Backend / API
    "api", "backend", "auth", "jwt",
    # Data / AI
    "data", "model", "models", "ai", "ml", "llm",
    # Intent words
    "error", "issue", "problem", "fix",
    "setup", "install", "configure", "why", "how",
    # hosters
    "giganodes", "gbnodes","shockbyte","bisecthosting","apexhosting",
    "sparkedhost","pebblehost","revivenode","hosthavoc","nodecraft",
    #error
    "404", "500", "502", "503",
    "bad gateway", "gateway timeout",
    "internal server error",
    #hosting and deploying
    "hosting panel", "control panel", "cpanel", "pterodactyl",
    "ftp", "sftp", "file manager",
    "deploy failed", "build failed", "logs", "error log",
    #backend
    "nodejs", "express", "fastapi", "flask", "django",
    "spring", "php", "laravel",
    "rest", "graphql", "endpoint", "request", "response",
    "middleware", "cors"
]

INTENT_WORDS = [
    "error", "issue", "problem", "fix",
    "setup", "install", "configure", "why", "how"
]

NEUTRAL_MESSAGES = [
    "hi", "hello", "hey", "yo", "sup",
    "good morning", "good afternoon", "good evening",
    "thanks", "thank you", "thx", "ok", "okay",
    "cool", "nice", "great", "bye", "good night","thank you",
    "wassup", "gg", "ohoi", "okhii", "okii"
]
