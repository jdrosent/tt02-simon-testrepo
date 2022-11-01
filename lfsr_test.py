import itertools

def update(state):
	return [
		state[1],
		state[2],
		state[3] ^ state[0],
		state[4],
		state[4] ^ state[0]
	]

seq = ""

state = [0,0,0,0,1]
for x in range(31*5):
	seq += str(state[4])
	state = update(state)

	if x > 0 and x % 31 == 0:
		print(seq)
		print(state)
		seq = ""
