# verify that post_gen_hook knows the docs builder initial docs location
# this will make sure the PostGenProject hook can the necessary file removals
# and replacements for Docs. If Gneration docs features get update, but ie we forget to
# update the post_gen_hook, this test will fail and remind us to update the hook
# Regressoin Test, if you will
def test_post_gen_hook_docs_builder_initial_docs_location():
    # GIVEN a callback to retrieve the 'docs internal config' (dic), as computed by post_gen_hook
    from cookiecutter_python.hooks.post_gen_project import DOCS

    def c1():
        return DOCS

    # GIVEN a callback to compute 'docs internal config', leveraging the runtime
    # installation of our python distro
    from cookiecutter_python.backend.gen_docs_common import get_docs_gen_internal_config

    # GIVEN 'dic' value, from post_gen_hook
    docs_post_gen = c1()
    # GIVEN 'dic' value, as given the cookiecutter_python package/distro
    docs_distro = get_docs_gen_internal_config()

    # WHEN we compare the two 'dic' values
    # THEN they should be equal
    assert docs_post_gen == docs_distro
