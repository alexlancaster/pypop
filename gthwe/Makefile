NAME   = hwe
NAME2 = gthwe

CC      = gcc 

#CFLAGS = -O2 -fno-strength-reduce
CFLAGS = -O2 -funroll-loops -DXML_OUTPUT=1
#CFLAGS = -g -static


SRC = $(NAME).c cal_const.c cal_n.c cal_prob.c\
	check_file.c do_switch.c guo_rand.c\
	new_rand.c\
	ln_p_value.c to_calculate_log.c print_data.c\
	random_choose.c  read_data.c select_index.c\
	stamp_time.c test_switch.c

LIB = -lm

OBJS = $(NAME).o cal_const.o cal_n.o cal_prob.o\
	check_file.o do_switch.o\
	new_rand.o\
	ln_p_value.o to_calculate_log.o print_data.o\
	random_choose.o  read_data.o select_index.o\
	stamp_time.o test_switch.o

REMOVABLE = $(NAME).o cal_const.o cal_n.o cal_prob.o\
	check_file.o do_switch.o\
	new_rand.o\
	ln_p_value.o to_calculate_log.o print_data.o\
	random_choose.o  read_data.o select_index.o\
	stamp_time.o test_switch.o 

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) -o $(NAME2) $(OBJS) $(LIB)

$(OBJS): hwe.h func.h

clean:
	rm  $(REMOVABLE)


