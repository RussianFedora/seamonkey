#!/bin/sh 
FREEBLDIR=./security/nss/lib/freebl
set -e 

mv ${FREEBLDIR}/ecl/ecl-exp.h ${FREEBLDIR}/save
rm -rf ${FREEBLDIR}/ecl/tests
rm -rf ${FREEBLDIR}/ecl/CVS
for i in ${FREEBLDIR}/ecl/* ; do
echo clobbering $i
 > $i
done
mv ${FREEBLDIR}/save ${FREEBLDIR}/ecl/ecl-exp.h

for j in ${FREEBLDIR}/ec.*; do
        echo unifdef $j
	cat $j | \
	awk    'BEGIN {ech=1; prt=0;} \
		/^#[ \t]*ifdef.*NSS_ENABLE_ECC/ {ech--; next;} \
                /^#[ \t]*if/ {if(ech < 1) ech--;} \
		{if(ech>0) {;print $0};} \
		/^#[ \t]*endif/ {if(ech < 1) ech++;} \
		{if (prt && (ech<=0)) {;print $0}; } \
		{if (ech>0) {prt=0;} } \
                /^#[ \t]*else/ {if (ech == 0) prt=1;}' > $j.hobbled && \
	mv $j.hobbled $j
done
