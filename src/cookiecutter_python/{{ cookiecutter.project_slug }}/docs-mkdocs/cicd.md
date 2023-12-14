---
tags:
  - CICD
---

## CICD Pipeline, as Github Action Workflow

### Variables to provide for `var` context

Flow Chart, of Jobs Dependencies in the Pipeline.

**config: ./.github/workflows/test.yaml**

{# to be evaluated, post generation, during markdown docs build process #}
{# not during Generation time #}
{% raw %}{% include 'dockerfile_mermaid.md' %}{% endraw %}
