## Docker Build Process DAG

`docker build`  possible execution paths.

Flow Chart, of how exection navigates docker stages (see --target of docker build).

If you run `docker build .` the `target` used by default is the `default_with_demo` Stage in the Graph.

**Dockerfile: ./Dockerfile**







{% include 'dockerfile_mermaid.md' %}
