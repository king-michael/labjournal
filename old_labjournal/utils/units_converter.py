import numpy as np

__all__=['atom_style',]
##=========================================================================##
## convert atom_style to other atom_style                                  ##
##=========================================================================##
# Michael King
# last mod. 07.02.2017
## ToDo:
# - add metal units

# BEGIN atom_style
class atom_style(object):
  """
Converter for LAMMPS units
use atom_style(x, inp="real", out="SI", unit_type="energy")
x : np.array
inp; real, SI
out : real, SI
unit_type : (e)nergy, (l)ength, (p)ressure, (vol)ume *or use atom_style.help()*
  """
  def __init__(self,x=np.zeros((1)),inp="real", out="SI", unit_type="",debug=False):
    self.x=x                               # values to convert
    
    self.inp_units=inp                    # INPUT  UNITS SI = Kcal/mol vs ps    
    self.out_units=out                    # OUTPUT UNITS SI = KJ/mol vs ps
    self.unit_type=unit_type              # type of UNIT
    
    self.debug=debug                          # debug option
    #===========================================#
    # Dictonary["INP"]["OUT"]=conversion factor #
    #===========================================#
    self.dic_convert={
      "Kcal/mol"  : {"Kcal/mol"   : 1.0                 ,
                     "KJ/mol"     : 4.184               },
      "KJ/mol"    : {"Kcal/mol"   : 1.0/4.184           ,
                     "KJ/mol"     : 1.0                 },
      "A"         : {"A"          : 1.0                 ,
                     "nm"         : 0.1                 },
      "nm"        : {"A"          : 10.0                ,
                     "nm"         : 1.0                 },
      "A^3"       : {"A^3"        : 1.0                 ,
                     "nm^3"       : 0.001               },
      "nm^3"      : {"A^3"        : 1000.0              ,
                     "nm^3"       : 1.0                 },
      "atm"       : {"atm"        : 1.0                 ,
                     "bar"        : 1.01325             ,
                     "Pa"         : 101325.0            ,
                     "torr"       : 760.0               },
      "bar"       : {"atm"        : 0.986923            ,
                     "bar"        : 1.0                 ,
                     "pa"         : 100000              ,
                     "torr"       : 750.062             },
      "Pa"        : {"atm"        : 1.0/101325          ,
                     "bar"        : 0.00001             ,
                     "Pa"         : 1.0                 ,
                     "torr"       : 0.00750062          },
      }
      
    #===========================================#
    # Dictonary["INP"]["OUT"]=conversion factor #
    #===========================================#
    self.dic_unit_types={
      "energy"            : ["Energy", "energy", "e", "E", "pe", "ke", "te"],
      "energy-real"       : ["kcal/mol", "Kcal/mol", "kcal/mole", "Kcal/mol"],
      "energy-SI"         : ["KJ/mol", "kJ/mol", "kj/mol", "KJ/mole", "kJ/mole"],
      "length"            : ["length", "l", "distance", "d", "distance"],
      "length-real"       : ["A", "Angstrom", "Angstroem"],
      "length-SI"         : ["nm"],
      "volume"            : ["Volume", "volume", "V", "vol"],
      "volume-real"       : ["A^3", "A^3", "Angstrom", "Angstroem", "Angstroms"],
      "volume-SI"         : ["nm^3", "nm3"],
      "pressure"          : ["pressure", "Pressure", "p", "press"],
      "pressure-real"     : ["atm", "ATM", "atmospheres", "Atmospheres"],
      "pressure-SI"       : ["Pa", "Pascals"],
      }
      
    
    self.process()                                  # Process input/output options    
    self.out_x=self.convert(self.x,self.inp_units,self.out_units)     # convert    
  #=========================#
  # Process Options
  def process(self):                         #---# Process options
    # process self.x
    if type(self.x) == type(list()): self.x=np.array(self.x)  # convert to numpy array
    # standardized units string
    self.inp_units, self.unit_type=self.unit_type_standardized(self.inp_units,self.unit_type)
    self.out_units, self.unit_type=self.unit_type_standardized(self.out_units,self.unit_type)
    
    self.inp_units, self.unit_type=self.unit_standardized(self.inp_units,self.unit_type)
    self.out_units, self.unit_type=self.unit_standardized(self.out_units,self.unit_type)
  #=========================#
  # standardized units string
  def unit_standardized(self,unit,unit_type):
    if unit == "real":
      if unit_type in self.dic_unit_types["energy"] or unit_type in self.dic_unit_types["energy-real"]:
        unit, unit_type="Kcal/mol" , "energy"
      if unit_type in self.dic_unit_types["length"] or unit_type in self.dic_unit_types["length-real"]:
        unit, unit_type="A", "length"
      if unit_type in self.dic_unit_types["volume"] or unit_type in self.dic_unit_types["volume-real"]:
        unit, unit_type="A^3", "volume"
      if unit_type in self.dic_unit_types["pressure"] or unit_type in self.dic_unit_types["pressure-real"]:
        unit, unit_type="atm", "pressure"
    elif unit == "SI":
      if unit_type in self.dic_unit_types["energy"] or unit_type in self.dic_unit_types["energy-SI"]:
        unit, unit_type="KJ/mol", "energy"
      if unit_type in self.dic_unit_types["length"] or unit_type in self.dic_unit_types["length-SI"]:
        unit, unit_type="nm", "length"
      if unit_type in self.dic_unit_types["volume"] or unit_type in self.dic_unit_types["volume-SI"]:
        unit, unit_type="nm^3", "volume"
      if unit_type in self.dic_unit_types["pressure"] or unit_type in self.dic_unit_types["pressure-SI"]:
        unit, unit_type="bar", "pressure"
    # repot standardized unit
    return unit,unit_type
  
  def unit_type_standardized(self,unit,unit_type): 
    if   unit in self.dic_unit_types["energy-real"]: unit, unit_type="Kcal/mol" , "energy"
    elif unit in self.dic_unit_types["length-real"]: unit, unit_type="A", "length"
    elif unit in self.dic_unit_types["volume-real"]: unit, unit_type="A^3", "volume"
    elif unit in self.dic_unit_types["pressure-real"]: unit, unit_type="atm", "pressure"
    elif unit in self.dic_unit_types["energy-SI"]: unit, unit_type="KJ/mol", "energy"
    elif unit in self.dic_unit_types["length-SI"]: unit, unit_type="nm", "length"
    elif unit in self.dic_unit_types["volume-SI"]: unit, unit_type="nm^3", "volume"
    elif unit in self.dic_unit_types["pressure-SI"]: unit, unit_type="bar", "pressure"
    # repot standardized unit
    if self.debug: print "DEBUG: unit, unit_type:", unit,unit_type
    return unit,unit_type
  #=========================#
  # Convert Units
  def convert(self,x,inp_units, out_units):
    prefactor_energy=self.dic_convert[str(inp_units)][str(out_units)]
    xnew=x*prefactor_energy
    if self.debug: print "DEBUG: Convert: %s * %f -> %s" % (inp_units, prefactor_energy, out_units)
    return xnew
# END atom_style

