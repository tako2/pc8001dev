	.module	mycrt0
	.globl	_main

	.area	_CODE
	.area	_GSINIT
	.area	_GSFINAL
	.area	_DATA
	.area	_DATAFINAL

	.area	_CODE

_crt0:
	ld	sp, #0
	ld	hl, #_datastart
	ld	bc, #_dataend

_clear_loop:
	ld	a, h
	sub	b
	jr	nz, _clear_next
	ld	a, l
	sub	c
	jr	z, _clear_exit
_clear_next:
	ld	(hl), #0
	inc	hl
	jr	_clear_loop
_clear_exit:
	call	gsinit
	jp	_main
	nop
	nop
	nop
	nop
	
	.area	_GSINIT
gsinit::

	.area	_GSFINAL
	ret

	.area	_DATA
_datastart::

	.area	_DATAFINAL
_dataend::
