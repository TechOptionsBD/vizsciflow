#!/bin/bash
echo "source /coge/perl/etc/bashrc && /coge/scripts/synmap/kscalc.pl --config /coge/scripts/synmap/coge.conf --infile $1 --db $2 --blockfile $3"
docker exec cogecont2 bash -c "source /coge/perl/etc/bashrc && /coge/scripts/synmap/kscalc.pl --config /coge/scripts/synmap/coge.conf --infile $1 --db $2 --blockfile $3"