==================
Developer's Corner
==================

Here we present the **Software Architecture** and offer **Guides** on how to
leverage the **CI/CD** to do various Development Operations, in a **GitOps** way.

CI/CD Pipeline
==============

.. toctree::
   :maxdepth: 1

   ci_cd_pipeline

Architecture
============

.. toctree::
   :maxdepth: 1

   architecture

GitOps Guides
=============

*How to* use our ``System`` for **Automated Git Ops.**

.. raw:: html
   <!-- current style forces each box to be below each other, on alabaster theme. on rtd theme it is ok -->
   <!-- OLD -->

   <!-- TODO: style such as that at least 2 blocks can be allowed next to each other, when (responsive) space allows -->
   <!-- NEW -->
      <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-around;">
         <div style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 300px; padding: 20px; margin: 10px;">
               <h3 style="color: #0056b3;"><a style="color: #0056b3;" href="gitops-v2.html">Publish my Branch</a></h3>
               <p>Build, Stress Test, and Release in 4 Steps. <a style="color: #0056b3;" href="gitops-v2-cheatsheet.html">Cheat Sheet</a></p>
         </div>
    </div>


.. Auto Publish
.. ------------
.. .. include:: gitops-v2.md
..    :parser: myst_parser.docutils_

.. toctree::
   :maxdepth: 1

   guide_quick_docs_release
   release_candidate
   


Docker Build
============

.. toctree::
   :maxdepth: 1

   docker_build
