/***************************************************************************

  program name: cal_prob.c

  function to calculate 

  status: modified from g-t program

  date: 12/99

***************************************************************************/

#include "hwe.h"

double cal_prob(a, index, ln_p_old, actual_switch)

		 int *a;
		 Index index;
		 double ln_p_old;
		 int *actual_switch;

{

	double p1_ratio, p2_ratio;
	register double ln_p_new;
	double rand_num;
	int switch_ind, type;
	double new_rand();
	void test_switch(), do_switch();

	*actual_switch = 0;

/* determine the switchability and direction of switch for given face */

	test_switch(a, index, &switch_ind, &type, &p1_ratio, &p2_ratio);

	switch (switch_ind)
	{
	case 0:											/* non-switchable */

		ln_p_new = ln_p_old;				/* retain the pattern, probability unchanged */
		break;

	case 1:											/* partially-switchable */

		if (type == 1)
			p1_ratio = p2_ratio;
		rand_num = new_rand();

		if (rand_num < TRANS(p1_ratio))
		{														/* switch w/ transition P TRANS */
			do_switch(a, index, type);
			ln_p_new = ln_p_old + log(p1_ratio);	/* ln P_after-switch */
			*actual_switch = 1;
		}
		else												/* remain the same w/ P = 1 - TRANS */
			ln_p_new = ln_p_old;			/* probability unchanged */
		break;

	default:											/* fully switchable */
		rand_num = new_rand();

		if (rand_num <= TRANS(p1_ratio))
		{
			do_switch(a, index, 0);		/* D-switch */
			ln_p_new = ln_p_old + log(p1_ratio);	/* ln P_after-switch */
			*actual_switch = 2;
		}
		else if (rand_num <= TRANS(p1_ratio) + TRANS(p2_ratio))
		{
			do_switch(a, index, 1);		/* R-switch */
			ln_p_new = ln_p_old + log(p2_ratio);
			*actual_switch = 2;
		}
		else
			ln_p_new = ln_p_old;
		break;
	}

	return (ln_p_new);
}

