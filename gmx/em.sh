gmx grompp -f $scriptsdir/em.mdp -c GO_ion.gro -p GO_ion_pp.top \
-o ./$rundir/em.tpr -po ./$rundir/em-out -n waterlayer.ndx #-maxwarn 1

cd $rundir ; $gmxrun -v -deffnm em
# echo "potential" | gmx energy -f em.edr -o em-potential.xvg
cp -rf em.gro ../GO2-afterem.gro
cd ..
