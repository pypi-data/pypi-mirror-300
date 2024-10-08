import contextvars

servers_v = contextvars.ContextVar("server")
rules_v = contextvars.ContextVar("rules")
