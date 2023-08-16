# SOFA SIMULATOR NOTES

General notes related to setting up and working with the SOFA framework

## Installation

Quick notes: [link](https://github.com/sofa-framework/sofa/releases/tag/v23.06.00)

- Get qt from [here](https://download.qt.io/official_releases/online_installers/)
    Make sure to select qt version 5.13 or above and select
    `Desktop gcc`, `Qt charts`and `Qt WebEngine`.

- Dependencies
```bash
sudo apt install -y build-essential software-properties-common gcc-11       \\
    clang-12 gcc-11 cmake cmake-gui libopengl0 libboost-all-dev libpng-dev  \\
    libjpeg-dev libtiff-dev libglew-dev zlib1g-dev libeigen3-dev
```

- Python, pip, numpy and scipy
- Clone the repo

## Overview

[FULL VIDEO](https://www.youtube.com/watch?v=KHTAgD1oG8Y)

Why the framework
- From inria
- Collaborative framework for physics simulation
- Open source
- Aimed at solving
    - Soft and rigid body dynamics
    - Medical and biology based simulations
    - Robotics and control simulations
    - Heat transfer     (Beta)
    - Fluid Mechanics   (Beta)
- Concepts
    - Flexible
    - Multiple representations and multiple physics engines
    - Modular
    - Interactive
    - Efficient computationally

### Software Architecture

- C++ base
- Open Source (LGPL License)
- Regular releases
- Open to plugins
- Documentation
    - [User docs](http://sofa-framework.org/community/doc)
    - [API docs](http://sofa-framework.org/api)
    - [Github project](github.com/sofa-framework)
- Binary and source compilation available
- Files available
    - C++ core classes
    - Physics models, algorithms, structure
    - Modules are implementations in pre 21.06 release
    - Python integration and plugins available from 21.06 release
    - Examples
    - Plugins
- runSofa is the built in GUI
    - Graph based interface

### Main Principles

- Scene Graph
    - Describes the full simulation as direct acyclic graph
    - Nodes contain components
    - Data can be linked together
    - Described with XML or Python files
    - All simulation data is described in these
- AnimationLoop
    - DOES NOT COMPUTE ANYTHING, ONLY SENDS COMMANDS TO COMPUTE
    - Compulsory
    - Rules for simulation steps
        - Collision
        - Physics
    - Uses simulation graph to order steps in simulation
    - DefaultAL
    - FreeMotionAL
- Mapping
    - Matching mechanism for maintaining coherency in meshes
    - Allows for different collision, physics and visual meshes
    - Separation of meshes allows for speed
    - Allows each model to be a different topology

### Simulation Features

- Topology for discritization in time
    - Points
    - Edges
    - Triangles
    - Quads
    - Tetrahedron
    - Hexadron
- Collision
    - Based on pipleline
        - Broad phase: Quick efficient collision check possibility
        - Narrow phase: Triggered only after broad phase to confirm collisions
        - Response: Reaction of collision
    - $F \propto D$
    - FreeMotionAL alows for Lagrange Multiplier Constraints

- In built plugins
    - Python scripting
    - Images
    - GPU acceleration with CUDA and OpenCL
    - Interactive and haptics plugins to interact with simulation

### Usage tutorial

- Structure of XML scene
    - Root nodes
        - DefaultAL
        - Other subnodes
- MechanicalObjects: is a container of DoF and are added in subnodes
    - x, y, z, w
- Requires solver
    - UniformMass: allows you to add mass to the whole mesh
    - ConstantForceFields: apply constant force field over entire simulation
        - x, y, z, i, j, k
    - EulerImplicitSolver: Integration solver for simple systems
    - CGLinearSolver: Uses congrugate gradient decsent
- Timestep defined by dt parameter
    - Linear solver's timestep is different because it is iterative
- BBox: is the box used for simulation
- MeshGmshLoader: allows loading of the mesh files
- PointSetTopologyContainer acts as container for points in the mesh
    - Needs to be linked to the loader
- Vec3d vs Rigid3d
    - Vec3d: only takes in and calculates position data
    - Rigid3d: takes in and calculates position and orientation data
- TetrahedronFEMForceField
    - elastic constitutive model to define elasticity
    - Considered internal forces
    - Contains description of young's modulus and poisson ratio of the material
- Units
    - Depends on specified units
- OglModel: specifically for visual models
- Mapping between meshes
    - Visual meshes can be fine surface meshes - no tetrahedrons needed
    - IdentityMapping: Use in case of same mesh for physics and visualization
    - BarycentricMapping: Using two deformable matrix
    - RigidMapping: Use when using a rigid body on a deformable matrix
    - RigidRigidMapping: When using two rigid bodies
- Boundary conditions
    - Topology algorithms give you a list of all points
    - Use this to find points/surfaces that are to be fixed
    - FixedConstraint: Takes in point indecies
- Gravity data can be set as a parameter in the root node
    - FEM based model
    - Computes $\int \rho g$
    - x y z
- Extracting triangles from a tetrahedral topology for surface is possible
    - type of mapping funtion
- MeshSpringForceField: Converts model into a spring mass model
- Collision pipleline
    - BruteForceDetection: N2 is used (Broad phase)
    - NewProximityIntersection: requires alarm distance and contact distance
    - CollisionResponse: Stores response forces
    - Balance between collisions and computational speed

#### Other notes:
- [Downloadable materials](http://sofa-framework.org/download-material)
- [Soft robotics tool kit plugin link](https://softroboticstoolkit.com/sofa/plugin)
- [Soft robotics plugin](https://project.inria.fr/softrobot/install-get-started-2/download/)
- [Pneunet gripper example](https://github.com/SofaDefrost/SoftRobots/tree/master/examples/tutorials/PneunetGripper)
- [Soft robotics plugins and simulation tutorials](https://project.inria.fr/softrobot/install-get-started-2/tutorial/)
- Viewer widget shows shortcuts
- Instabilities are caused by numerical settings
    - Time steps small enough?
    - Mesh size small enough?
    - Solvable or converging model?

##### How to make a 3D volumetric mesh

- Make a model, generate a mesh in an STL like format
    - Stanford polygon filetype works best
- Import into Gmsh
- Geometry > Elementary Entities > Add > Volume
    - Click on mesh
    - Select holes if any, press E after selection or if no holes in mesh
- Mesh > 3D
    - This creates the 3D mesh
    -  (Optional) Click Optimize3D
- Check mesh using Tools > Statistics > Mesh
    - It should show >0 values in tetraherons if done right
- Save file as .msh
