NAME   = hwe
NAME2 = gthwe

CC      = gcc 

# add this to "CFLAGS" if XML mode is desired: -DXML_OUTPUT=1
# add this to "CFLAGS" if you don't want the allele frequency table
#   printed out: -DSUPPRESS_ALLELE_TABLE=1
CFLAGS = -O2 -funroll-loops -Wall $(CFLAGSEXTRA)

SRC = $(NAME).c cal_const.c cal_n.c cal_prob.c\
	check_file.c do_switch.c guo_rand.c\
	new_rand.c\
	ln_p_value.c to_calculate_log.c print_data.c\
	random_choose.c  read_data.c select_index.c\
	stamp_time.c test_switch.c statistics.c

LIB = -lm -lgsl -lgslcblas

OBJS = $(NAME).o cal_const.o cal_n.o cal_prob.o\
	check_file.o do_switch.o\
	new_rand.o\
	ln_p_value.o to_calculate_log.o print_data.o\
	random_choose.o  read_data.o select_index.o\
	stamp_time.o test_switch.o statistics.o

REMOVABLE = $(NAME).o cal_const.o cal_n.o cal_prob.o\
	check_file.o do_switch.o\
	new_rand.o\
	ln_p_value.o to_calculate_log.o print_data.o\
	random_choose.o  read_data.o select_index.o\
	stamp_time.o test_switch.o statistics.o

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) -o $(NAME2) $(OBJS) $(LIB)

$(OBJS): hwe.h func.h

clean:
	rm  $(REMOVABLE)


