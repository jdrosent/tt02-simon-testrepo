import json

# Key & Plaintext
key = 0x1918111009080100
plaintext = 0x65656877

test_data = {
	"key": key,
	"plaintext": plaintext,
	"keys": [],
	"rounds": []
}

# SIMON Cipher Constants
z0 = 0b0110011100001101010010001011111
c = 2**16 - 4

# Bit rotate functions
def left_rotate(x, d):
    return ((x << d) | (x >> (16 - d))) & 0xFFFF

def right_rotate(x, d):
    return ((x >> d) | (x << (16 - d))) & 0xFFFF

# Pretty print key
def print_key(key):
	key = " ".join([f"{x:04x}" for x in key])
	print(f"Key: {key}")

# Generate key expansions
key = [key >> (16*x) & 0xFFFF for x in range(3,-1,-1)]

for i in range(33):
	v = right_rotate(key[0],3) ^ key[2]
	v = right_rotate(v, 1) ^ v ^ key[3]
	v = v ^ c ^ ((z0 >> (i % 31)) & 0x01)

	new_key = [
		v,
		key[0],
		key[1],
		key[2]
	]

	test_data["keys"].append(sum([
		key[x] << (16*(3-x)) for x in range(0,4)
	]))
	print_key(key)
	key = new_key

	i += 1

# Generate feistel network stages
cur_round = [(plaintext >> (16*(1-x))) & 0xFFFF for x in range(2)]

rounds = []
for x in range(33):
	v = left_rotate(cur_round[0], 1) & left_rotate(cur_round[0], 8)
	v = v ^ left_rotate(cur_round[0], 2)
	v = v ^ test_data["keys"][x] & 0xFFFF
	v = v ^ cur_round[1]

	new_round = [
		v,
		cur_round[0]
	]

	print(f"Round: " + " ".join([f"{x:04x}" for x in cur_round]))
	test_data["rounds"].append(sum([
		cur_round[x] << (16*(1-x)) for x in range(2)
	]))
	cur_round = new_round

# Write to file
with open("test_data.json", "w+") as tfile:
	json.dump(test_data, tfile)