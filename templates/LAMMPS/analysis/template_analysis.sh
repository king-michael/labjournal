#!/usr/bin/env bash

# Creates and goes into analysis folder
[[ ! -d analysis ]] && mkdir -p analysis
pushd analysis

# Link EM_and_Equilibration
for i in trajectory.0.dcd log.0.lammps; do
    [[ ! -f $i ]] && ln -sf ../EM_and_Equilibration/$i
done

# Link production folder
for f in $(ls ../production/*); do
  echo $f | egrep -q "trajectory.[[:digit:]]{1,}.dcd"
  [ $? -eq 0 ] && ([[ ! -f $(basename $f) ]] && ln -sf $f)
  echo $f | egrep -q "log.[[:digit:]]{1,}.lammps"
  [ $? -eq 0 ] && ([[ ! -f $(basename $f) ]] && ln -sf $f)
done

# Link Start structures
STRUCTURE_PSF=$(cd ..; ls *.psf)
FNAME=${STRUCTURE_PSF%.psf}
for i in data pdb psf; do
  ln -sf ../${FNAME}.$i
done

# GET RUN_FROM RUN_TO
TMP=$(cd ../production; ls trajectory.*.dcd -v | head -1)
TMP=${TMP%.dcd}
RUN_FROM=${TMP#trajectory.}

TMP=$(cd ../production; ls trajectory.*.dcd -v | tail -1)
TMP=${TMP%.dcd}
RUN_TO=${TMP#trajectory.}

#@ begin analysis


#@ end analysis
popd # analysis
