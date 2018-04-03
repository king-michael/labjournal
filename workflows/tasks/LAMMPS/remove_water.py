#!/usr/bin/env python
"""
Task to remove water using LAMMPS rerun

Details:

Author:
    Michael King <michael.king@uni-konstanz.de>
"""

import sys

def _write_lammpsrerun(
        output="input.analysis.remove_water.lammps", # type: str
        inputfile="../production/final_data.${run_no}", # type: str
        sel_water="${OT} ${HT}", # type: str
        path_to_molfile="/home/micha/progs/lib/vmd_1.9.3/plugins/LINUXAMD64/molfile", # type: str
        traj_type_out="dcd", # type: str
        atomstyle="full", # type: str
        units="real", # type: str
        cmap=None,  # type: str | None
        stdout=False # type: bool
        ):
    """function to write LAMMPS rerun file to remove water

    Parameters
    ----------
    output : str, optional
        name of LAMMPS inputfile (default is "input.analysis.remove_water.lammps")
    inputfile : str, optional
        LAMMPS data file for the topology (default is "../production/final_data.${run_no}")
    sel_water : str, optional
        LAMMPS atom types for group water (default is "${OT} ${HT}")
    path_to_molfile : str, optional
        Path to molfile plugin (VMD) (default is "/home/micha/progs/lib/vmd_1.9.3/plugins/LINUXAMD64/molfile")
    traj_type_out : str, optional
        trajectory type for output trajectory (default is "dcd")
    atomstyle : str, optional
        LAMMPS atom_style (default is "full")
    units : str, optional
        LAMMPS units (default is "real")
    cmap : str or None, optional
        Name of the `cmap` file or None (default is None)
    stdout : bool, optional
        Write the output to stdout (default is False)


    Returns
    -------

    Examples
    --------
    >>> _write_lammpsrerun(stdout=True)
    """

    thermo=100 # frequence for the thermodynamic output

    if stdout:
        fp = sys.stdout
    else:
        fp = open(output, 'w')
    # Input sections
    fp.write("variable run_no index 0\n")
    fp.write("variable stride index 1\n")
    # SETTINGS
    fp.write("\natom_style {}\n".format(atomstyle))
    fp.write("units {}\n\n".format(units))
    if cmap is not None:
        # fix cmap init (to store cmap data in it)
        fp.write("fix cmap all cmap {}\n".format(cmap))
        fp.write("fix_modify cmap energy yes\n")
        # read data
        fp.write("read_data %s.${run_no} fix cmap crossterm CMAP nocoeff\n" % inputfile)
    else:
        # read data
        fp.write("read_data %s nocoeff\n" % inputfile)
    # readin force field
    fp.write("\ninclude ${forcefield}\n") # Todo: can we work around this by getting the group via MDAnalysis?

    fp.write("\ngroup water type {}\n".format(sel_water))
    fp.write("group solute subtract all water\n")

    # Deactivate force field
    fp.write("\npair_style zero 5 nocoeff\n")
    fp.write("pair_coeff * *\n")
    fp.write("bond_style zero nocoeff\n")
    fp.write("bond_coeff * *\n")
    fp.write("angle_style none\n")
    fp.write("dihedral_style none\n")
    fp.write("improper_style none\n")
    fp.write("kspace_style none\n")
    if cmap is not None:
        fp.write("unfix cmap") # turn of CMAP

    # write out
    fp.write("\ndump 1 solute %s 1 traj_solute.${run_no}.%s\n" % (traj_type_out,traj_type_out))
    # dump 1 solute xtc 1 traj_solute.${run_no}.xtc
    fp.write("dump_modify 1 unwrap yes\n")
    # Thermo settings to spam the console
    fp.write("\nthermo {}\n".format(thermo))
    fp.write("thermo_style custom step cpu\n")

    # rerun command
    fp.write("\nrerun trajectory.${run_no}.dcd every ${stride} dump x y z wrapped no box yes format molfile dcd %s\n" %
             path_to_molfile)


if __name__ == '__main__':
    _write_lammpsrerun(stdout=True)
