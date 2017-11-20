


set fname at_calcite_6x6x2_graf_1961

topo readlammpsdata tmp.data


source /home/micha/scripts/tcl/tcl_procs_assign_standart.tcl

set sel_CO [atomselect top "type 2"] ; lsort -unique [$sel_CO get mass]
set sel_CA [atomselect top "type 1"] ; lsort -unique [$sel_CA get mass]
set sel_OC [atomselect top "type 3"] ; lsort -unique [$sel_OC get mass]
set sel_CO3 [atomselect top "index [$sel_CO list] [$sel_OC list]"]

micha::assign $sel_CA CAL at
micha::assign $sel_CO CO at
micha::assign $sel_OC OC at

topo retypebonds
topo retypeangles
topo retypedihedrals
topo retypeimpropers

#----------------------------#
#      change resid          #
#----------------------------#
# Every residue has a own resid (starting from 1 not from 0 !)
# foreach ID [[atomselect top all] list] {
#  set seltmp [atomselect top "index $ID"]
#  $seltmp set resid [expr [$seltmp get residue] + 1]
#  $seltmp delete
# }

mol reanalyze top
#===============================================#
#                      Info                     #
#===============================================#
vmdcon -info "
# Structure:
# Num Ca: [$sel_CA num]
# Num CO: [$sel_CO num]
# Num OC: [$sel_OC num]
# 
# Bonds Total: [topo bondtypenames]
# Bonds CO3: [topo bondtypenames -sel $sel_CO3]
#        should: [$sel_OC num] have: [topo numbonds -sel $sel_CO3]
# 
# Angles Total: [topo angletypenames]
#          Num: [topo numangles]
# Angles CO3: [topo angletypenames -sel $sel_CO3]
#        should: [$sel_OC num] have: [topo numangles -sel $sel_CO3]
# 
# Dihedrals Total: [topo dihedraltypenames]
#             Num: [topo numdihedrals]
# 
# Impropers Total: [topo impropertypenames]
#             Num: [topo numimpropers]
# Impropers CO3: [topo impropertypenames -sel $sel_CO3]
#        should: [$sel_CO num] have: [topo numimpropers -sel $sel_CO3]
" 
 

topo writelammpsdata ${fname}.data
animate write psf    ${fname}.psf
animate write pdb    ${fname}.pdb
animate write hoomd  ${fname}.xml

#exit
