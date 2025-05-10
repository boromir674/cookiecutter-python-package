## Docker Build Process DAG

`docker build`  possible execution paths.

Flow Chart, of how exection navigates docker stages (see --target of docker build).

If you run `docker build .` the `target` used by default is the `default_with_demo` Stage in the Graph.

**Dockerfile: ./Dockerfile**

- `Nodes` represent docker **stages**
- `Continuous arrows/edges` represent `FROM A AS B` docker statements
- `Dotted arrows/edges` represent `COPY --from=A /path/to/file /local/path` statements


{% include 'dockerfile_mermaid.md' %}

With this **multi-stage** Dockerfile design, stages can be **built in parallel** (assuming appropiate build backend)!
