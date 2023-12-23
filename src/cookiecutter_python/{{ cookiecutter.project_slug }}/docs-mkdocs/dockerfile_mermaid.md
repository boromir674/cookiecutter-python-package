## Dockerfile Flow Chart

**Dockerfile: Dockerfile**

```mermaid
graph TB;
  python:3.9.16-slim-bullseye --> builder
  python:3.9.16-slim-bullseye --> install
  builder -. "COPY" .-> install
```
