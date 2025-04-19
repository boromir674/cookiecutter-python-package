## Docker Build Process DAG

`docker build`  possible execution paths.

Flow Chart, of how exection navigates docker stages (see --target of docker build).

If you run `docker build .` the `target` used by default is the `default_with_demo` Stage in the Graph.

**Dockerfile: ./Dockerfile**

{# we have include 'dockerfile_mermaid.md' statment below #}
{# intention is to leverage markdown imports, on docs build time #}
{# it should not affect dynamically the Generator behaviour #}

{# so we must enusre that jinja does, treats below as literal, and not try to interpret #}

{% raw %}{% include 'dockerfile_mermaid.md' %}{% endraw %}
