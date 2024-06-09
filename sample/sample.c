#include <stddef.h>
#include <stdint.h>

void myprint(const uint8_t *str)
{
	uint8_t *vram;

	vram = (uint8_t *)0xf300;

	while (*str != 0) {
		*vram = *str;
		vram += 2;
		str ++;
	}
}

void main()
{
	myprint("Hello World!");

	while (1) {}
}
