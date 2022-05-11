
Ready to enjoy some of your newly generated Python Package Project **features** available out-of-the-box!?

For instance:

1. Leverage the supplied `tox environments` to automate various **Testing** and **DevOps** related activities.

   Assuming you have `tox` installed (example installation command: `python3 -m pip install --user tox`)
   and you have done a `cd` into the newly generated Project directory, you can do for example:

   a. Run the **Test Suite** against different combinations of `Python versions` (ie 3.7, 3.8) and different ways of installing (ie 'dev', 'sdist', 'wheel') the `<my_great_python_package>` package:

      .. code-block:: sh

         tox -e "py{3.7, 3.8}-{dev, sdist, wheel}"

   b. Check the code for **compliance** with **best practises** of the `Python packaging ecosystem` (ie PyPI, pip),
      build `sdist` and `wheel` distributions and store them in the `dist` directory:

      .. code-block:: sh

           tox -e check && tox -e build

   c. **Deploy** the package's distributions in a `pypi` (index) server:

      1. Deploy to **staging**, using the `test` pypi (index) server at `test.pypi.org`_:

         .. code-block:: sh

             TWINE_USERNAME=username TWINE_PASSWORD=password PACKAGE_DIST_VERSION=1.0.0 tox -e deploy

      2. Deploy to **production**, using the `production` pypi (index) server at `pypi.org`_:

         .. code-block:: sh

             TWINE_USERNAME=username TWINE_PASSWORD=password PACKAGE_DIST_VERSION=1.0.0 PYPI_SERVER=pypi tox -e deploy

         .. note::
            Setting PYPI_SERVER=pypi indicates to deploy to `pypi.org` (instead of `test.pypi.org`).

      .. note::
         Please modify the TWINE_USERNAME, TWINE_PASSWORD and PACKAGE_DIST_VERSION environment variables, accordingly.

         TWINE_USERNAME & TWINE_PASSWORD are used to authenticate (user credentials) with the targeted pypi server.

         PACKAGE_DIST_VERSION is used to avoid accidentally uploading distributions of different versions than intended.


2. Leverage the **CI Pipeline** and its **build matrix** to run the **Test Suite** against a combination of
   different Platforms, different Python interpreter versions and different ways of installing the subject Python Package:

    `Trigger` the **Test Workflow** on the **CI server**, by `pushing` a git commit to a remote branch (ie `master` on github).

    `Navigate` to the `CI Pipeline web interface` (hosted on `Github Actions`) and inspect the **build** results!


   .. note::
      You might have already `pushed`, in case you answered `yes`, in the `initialize_git_repo` prompt, while generating the Python Package,
      and in that case, the **Test Workflow** should have already started running!

      Out-of-the-box, `triggering` the **Test Workflow** happens only when pushing to the `master` or `dev` branch.


.. LINK DEFINITIONS

.. _pypi.org: https://pypi.org/

.. _test.pypi.org: https://test.pypi.org/
