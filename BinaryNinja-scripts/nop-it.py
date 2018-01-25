# NOPs reapeted occurances of MOV al, const.
# Alternative to IDA Pro script showed in https://www.youtube.com/watch?v=HfSQlC76_s4&feature=youtu.be
# Binaryninja does not support collapsing parts of the code which is why we NOP and then look at the code in
# IL view which optimizes the NOPs away.

from binaryninja import *
from collections import deque

def go(bv,function):
	latestInstr = deque([])

	for block in function.low_level_il:
		for il in block:

			if il.operation == enums.LowLevelILOperation.LLIL_SET_REG and \
				il.prefix_operands[1].name == "al" and \
				il.prefix_operands[2].operation  == enums.LowLevelILOperation.LLIL_CONST:
				latestInstr.append(il)
				continue

			elif len(latestInstr)>=4 and \
				 (il.operation != enums.LowLevelILOperation.LLIL_SET_REG or \
				 il.prefix_operands[1].name != "al" or \
				 il.prefix_operands[2].operation  != enums.LowLevelILOperation.LLIL_CONST):
				
				for instr in latestInstr:
					bv.convert_to_nop(instr.address)

			latestInstr = deque([])

	bv.update_analysis()

PluginCommand.register_for_function("NOP uninteresting instructions", "NOP uninteresting instructions", go)

