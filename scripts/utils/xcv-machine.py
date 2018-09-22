# This implements a simple scripting system for locking-unlocking transection
# This implementation uses python list as a script object

class OpCode:
	
	def __init__(self, code):
		self.code = code

	def __eq__(self, value):
		return self.code == value.code

	def __int__(self):
		return self.code

# A few common instructions
NOP 	= OpCode(0)
PUSH 	= OpCode(1)
POP 	= OpCode(2)
DUP		= OpCode(3)
HASH 	= OpCode(4)
VERIFY 	= OpCode(5)
RET 	= OpCode(6)
ADD		= OpCode(7)

def VerifySignature(pubKey, sig):
	pass

class Engine:

	def __init__(self):
		self.stack = []
	
	def Exec(self, code):
		self.stack.clear()
		top = None
		for instr in code:
			if type(instr) != OpCode:
				top = instr # Data value
			elif instr == NOP:
				continue
			elif instr == PUSH:
				self.stack.append(top)
			elif instr == POP:
				top = self.stack.pop()
			elif instr == DUP:
				self.stack.append(self.stack[-1])
			elif instr == HASH:
				top = hash(top)
			elif instr == VERIFY:
				top = VerifySignature(top, self.stack.pop())
			elif instr == RET:
				break
			elif instr == ADD:
				top += self.stack.pop()
			else:
				raise Exception("Invalid Instruction")
		return top


if __name__ == '__main__':
	code = ['hello', 		# Load 'hello' on top
			PUSH, 			# Push top in stack
			' ', 			# Load ' ' on top
			PUSH, 			# Push top in stack
			'world', 		# Load 'world' on top
			ADD, 			# Add top with stack's top and store on top
			ADD]			# ..
	result = Engine().Exec(code)
	print(result)


	