## Docker Build Process DAG

> Understand how we leverage `Docker` in the build process.

The project features a `Dockerfile`, designed for

- multi-stage builds
- parallel stage building (assuming appropriate build backend)
- size minimization of the produced `Docker` image
- minimization of vulerabilities

## Dockerfile visualized as Directed Acyclic Graph (DAG)

> Understand the execution path of `docker build`, via **DAG visualization**

{% raw %}{% include 'topics/development/dockerfile_mermaid.md' %}{% endraw %}

- `solid boxes` represent distinct docker **stages** and their *aliases*
- `solid arrows` represent **stage dependencies**; `FROM a AS b` type of instructions
- `dotted arrows` represent **stage COPY**: `COPY --from=a /path /path` type of instructions
