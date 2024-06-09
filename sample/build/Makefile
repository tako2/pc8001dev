PROJECT = sample
PROG_ADDR = 8080
DATA_ADDR = c000

TOOLDIR = ../../tools

SDCC = sdcc
CFLAGS = -mz80 -c -I ../
LDFLAGS =  -mz80 --code-loc 0x$(PROG_ADDR) --data-loc 0x$(DATA_ADDR) --no-std-crt0

SRC = $(PROJECT).c
OBJ = mycrt0.rel $(SRC:.c=.rel)
IHX_IMAGE = $(PROJECT).ihx
BIN_IMAGE = $(PROJECT).bin
CMT_IMAGE = $(PROJECT).cmt
WAV_IMAGE = $(PROJECT).wav

all: $(CMT_IMAGE)

mycrt0.rel: ../mycrt0.asm
	sdasz80 -o $@ $<

%.rel: ../%.c
	$(SDCC) $(CFLAGS) $<

$(IHX_IMAGE): $(OBJ)
	$(SDCC) $(LDFLAGS) -o $@ $(OBJ)

$(BIN_IMAGE): $(IHX_IMAGE)
	$(TOOLDIR)/hex2bin $<

$(CMT_IMAGE): $(BIN_IMAGE)
	$(TOOLDIR)/t88tool -M -f $@ $< $(PROG_ADDR)

wav: $(CMT_IMAGE)
	$(TOOLDIR)/cmt2wav.py $< $(WAV_IMAGE)

clean:
	rm -rf $(OBJ) $(IHX_IMAGE) $(BIN_IMAGE) *.lst *.sym *.asm *.lk *.noi *.map *.bin
