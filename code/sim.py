"""
Simple pneunet model for the sofa framework

Copyright © 2023 macavitycode <macavitycode@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import Sofa
import Sofa.Core
import Sofa.constants.Key as Key


def createScene(rootNode):
    rootNode.addObject("VisualStyle", displayFlags="showForceFields showBehaviorModels")
    rootNode.addObject("RequiredPlugin", pluginName="SoftRobots SofaPython3")
    rootNode.gravity.value = [-9810, 0, 0]
    rootNode.addObject("AttachBodyButtonSetting", stiffness=10)
    rootNode.addObject("FreeMotionAnimationLoop")
    rootNode.addObject("GenericConstraintSolver", tolerance=1e-12, maxIterations=10000)

    finger = rootNode.addChild("finger")
    finger.addObject(
        "EulerImplicitSolver", name="odesolver", rayleighStiffness=0.1, rayleighMass=0.1
    )
    finger.addObject("SparseLDLSolver", name="directSolver")
    finger.addObject(
        "MeshVTKLoader", name="loader", filename="meshes/pneunetCutCoarse.vtk"
    )
    finger.addObject("MeshTopology", src="@loader", name="container")
    finger.addObject(
        "MechanicalObject",
        name="tetras",
        template="Vec3",
        showObject=True,
        showObjectScale=1,
    )
    finger.addObject(
        "TetrahedronFEMForceField",
        template="Vec3",
        name="FEM",
        method="large",
        poissonRatio=0.3,
        youngModulus=500,
    )
    finger.addObject("UniformMass", totalMass=0.0008)
    finger.addObject(
        "BoxROI", name="boxROISubTopo", box=[-100, 22.5, -8, -19, 28, 8], strict=False
    )
    finger.addObject(
        "BoxROI", name="boxROI", box=[-10, 0, -20, 0, 30, 20], drawBoxes=True
    )
    finger.addObject(
        "RestShapeSpringsForceField",
        points="@boxROI.indices",
        stiffness=1e12,
        angularStiffness=1e12,
    )
    finger.addObject("LinearSolverConstraintCorrection")

    modelSubTopo = finger.addChild("modelSubTopo")
    modelSubTopo.addObject(
        "MeshTopology",
        position="@loader.position",
        tetrahedra="@boxROISubTopo.tetrahedraInROI",
        name="container",
    )
    modelSubTopo.addObject(
        "TetrahedronFEMForceField",
        template="Vec3",
        name="FEM",
        method="large",
        poissonRatio=0.3,
        youngModulus=1500,
    )

    cavity = finger.addChild("cavity")
    cavity.addObject(
        "MeshSTLLoader", name="cavityLoader", filename="meshes/pneunetCavityCut.stl"
    )
    cavity.addObject("MeshTopology", src="@cavityLoader", name="cavityMesh")
    cavity.addObject("MechanicalObject", name="cavity")
    cavity.addObject(
        "SurfacePressureConstraint",
        name="SurfacePressureConstraint",
        template="Vec3",
        value=1,
        triangles="@cavityMesh.triangles",
        valueType="pressure",
    )
    cavity.addObject(
        "BarycentricMapping", name="mapping", mapForces=False, mapMasses=False
    )

    rootNode.addObject(FingerController(rootNode))


class FingerController(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        # print("DEBUG: initialized controller")
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.node = args[0]
        self.fingerNode = self.node.getChild("finger")
        self.pressureConstraint = self.fingerNode.cavity.getObject(
            "SurfacePressureConstraint"
        )

    def onKeypressedEvent(self, e):
        pressureValue = self.pressureConstraint.value.value[0]

        print("DEBUG: current pressure: ", pressureValue)
        print("DEBUG: key pressed: ", e["key"])

        if e["key"] == Key.plus:
            pressureValue += 0.01
            if pressureValue > 1.5:
                pressureValue = 1.5

        if e["key"] == Key.minus:
            pressureValue -= 0.01
            if pressureValue < -1.5:
                pressureValue = -1.5

        self.pressureConstraint.value = [pressureValue]
