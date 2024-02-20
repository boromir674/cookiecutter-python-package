.. mermaid::

   graph TB;
     base --> builder
     builder --> prod_builder
     builder --> test_builder
     scratch --> source
     prod_builder -. "requirements.txt" .-> source
     base --> base_env
     base_env --> build_wheels
     source -. "/app" .-> build_wheels
     base_env --> install
     build_wheels -. "${DISTRO_WHEELS}" .-> install
     base --> test_dev
     test_builder -. "requirements-test.txt" .-> test_dev
     install --> test
     test_builder -. "requirements-test.txt" .-> test
     install --> prod
   
