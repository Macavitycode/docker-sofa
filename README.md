# Dockerized Sofa Framework for Soft Robotics

A simple repo to setup a constant environment for the Sofa Framework with
plugins for soft robotics simulations setup out of the box.

## Usage

Simple setup:
- Setup Docker on the required system
- Clone this repo
- Run ./build.sh to setup everything to do with the docker images
- Run ./run.sh to run the image built
- Run ./start.sh to login to the image

## Notes

- Read through relevant docs for more info.
- runSofa is located at /home/noroot/SOFA.../bin/runSofa
- Add files simulation files to a dir called code

More helper scripts will be added as needed.

## References
- [Downloadable materials](http://sofa-framework.org/download-material)
- [Soft robotics tool kit plugin link](https://softroboticstoolkit.com/sofa/plugin)
- [Soft robotics plugin](https://project.inria.fr/softrobot/install-get-started-2/download/)
- [Pneunet gripper example](https://github.com/SofaDefrost/SoftRobots/tree/master/examples/tutorials/PneunetGripper)
- [Soft robotics plugins and simulation tutorials](https://project.inria.fr/softrobot/install-get-started-2/tutorial/)
