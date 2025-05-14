# Software Architecture

[//]: # (this is a comment)
[//]: # (Description of what is this Page)

Here you can find the software architecture of the project.

## Module Dependencies

[//]: # (Description of what is this Section)

Here you can find the dependencies between the modules of the project.

The dependencies are Visualized as a Graph, where Nodes are the modules and the Edges are python ``import`` statements.

The dependencies are visualized, after running the following command:

```sh
tox -e pydeps
```

!!! Tip

    Right-click and open image in new Tab for better inspection

### First-party Dependencies

[//]: # (Inner Python Imports SVG Graph)

![First-party Dependencies](../assets/deps_inner.svg)


### First and Third party Dependencies

[//]: # (First-Party with 3rd-party having all incoming edges to our individual Modules)

![All Dependencies - C](../assets/deps_all.svg)


### 1st+3rd party Deps - 1st as Cluster

[//]: # ("Boxed" First-Party with 3rd-party having all incoming edges to our Box)

![All Dependencies - B](../assets/deps_ktc.svg)


### 1st+3rd party Deps - 1st+3rd as Cluster

[//]: # ("Boxed" First-Party with 3rd-party having 1 incoming edge to our Box)

![All Dependencies - A](../assets/deps_ktc-mcs_2.svg)
