#!/bin/sh
# takes three arguments:
# 1: file containing names of locus with column order number,
#    ignoring one initial label column
#    1 D6S1260
#    2 D6S2238
#    3 D6S1281                                      
#
# 2: data file with a first line of labelling info
#    and a first column of labels
#
# 3: name of locus
#

if [ ! $# -eq 3 ]
then
	echo "Usage: 1loc_freq listfile datafile locus"
	exit 1
fi

loc_name=$3

loc_pos=$(grep $loc_name $1 |awk '{print $1}')


awk -v lp=$loc_pos -v ln=$loc_name '
BEGIN{
	counted = 0
	col_a = 2 * lp
	col_b = col_a + 1
}

NR > 1{
	if($col_a ~ "[.X]")
	{
		reject_tot++
		next
	}

	allele[$col_a]++
	counted++
	allele[$col_b]++
	counted++
}

END{
	printf("%s\n", ln)
	printf("Observations used: %d\nRejected         : %d\n", counted, reject_tot)
	printf("%10s%10s%10s\n", "Allele", "Observed", "Frequency")
	close (stdout)
	for(elem in allele)
	{
		printf("%10s%10d%10f\n", elem, allele[elem], allele[elem] / counted) |"sort"
	}
	close("sort")
	printf("%-10s%10d%10f\n", "Total:", counted, counted / counted)
}' $2
