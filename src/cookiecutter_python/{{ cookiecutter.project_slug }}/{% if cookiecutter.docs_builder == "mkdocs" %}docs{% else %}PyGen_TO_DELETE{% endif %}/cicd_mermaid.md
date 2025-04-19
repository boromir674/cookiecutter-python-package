{% if cookiecutter.cicd == "stable" %}```mermaid
graph LR;
  set_github_outputs --> test_suite
  test_suite --> codecov_coverage_host
  set_github_outputs --> docker_build
  test_suite --> docker_build
  set_github_outputs --> check_which_git_branch_we_are_on
  test_suite --> pypi_publish
  check_which_git_branch_we_are_on --> pypi_publish
  set_github_outputs --> lint
  set_github_outputs --> docs
  set_github_outputs --> code_visualization
```{% elif cookiecutter.cicd == "experimental" %}```mermaid
graph LR;
  test_n_build
  test_n_build --> codecov_coverage_host
  test_n_build --> docker_build
  lint
  docs
  code_visualization
  test_n_build --> signal_deploy
  signal_deploy --> pypi_publish
  signal_deploy --> gh_release
```{% endif %}
