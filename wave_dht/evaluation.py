import opendht as dht
import wave_dht as wdht
import client

import unittest
import numpy as np
import timeit

IS_WAVE = False
LABEL = "WAVE" if IS_WAVE else "DHT"

def make_node(is_wave_client=False, ip="bootstrap.ring.cx", port="4222"):
	node = None

	if is_wave_client:
		node = client.Client()
	else:
		node = dht.DhtRunner()
		node.run()

		# Join the network through any running node,
		# here using a known bootstrap node.
		node.bootstrap(ip, port)

	return node

def setup_network(is_wave=False, N=100):
	# Make N nodes / wave clients
	nodes = []
	for i in range(N):
		node = make_node(is_wave)
		nodes.append(node)

	return nodes

class TestWaveDht(unittest.TestCase):
    def setUp(self):
    	pass
        # self.client1 = client.Client()
        # self.client2 = client.Client()

    # def test_invalidGet(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.assertRaises(Exception, self.client2.get, key)

    def init_bulk_put(N, NUM_BYTES, NUM_PUTS):
		nodes = setup_network(is_wave=IS_WAVE, N=N)
		for k in range(NUM_PUTS):
			node = nodes[k % N]

			# blocking call (provide callback arguments to make the call non-blocking)
			key = str(k)
			val = np.random.bytes(NUM_BYTES)
			node.put(dht.InfoHash.get(key), dht.Value(val))
		return nodes

    def test_bulk_put(self):
    	N = 100
    	nodes = setup_network(is_wave=IS_WAVE, N=N)
    	NUM_BYTES = 2**10
		NUM_PUTS = 1000
    	def f():
			for k in range(NUM_PUTS):
				node = nodes[k % N]

				# blocking call (provide callback arguments to make the call non-blocking)
				key = str(k)
				val = np.random.bytes(NUM_BYTES)

				if IS_WAVE:
					node.put(key, val, node.ent.hash)
				else:
					node.put(dht.InfoHash.get(key), dht.Value(val))

		times = timeit.repeat(f, number=1)
		print("[%s]: %d nodes, %d PUTS of %d bytes ==> %.4f seconds" % (LABEL, N, NUM_PUTS, NUM_BYTES, min(times)))

	def test_bulk_get(self):
		N = 100
    	NUM_BYTES = 2**10
		NUM_PUTS = 1000

		nodes = init_bulk_put(N, NUM_BYTES, NUM_PUTS)
		NUM_GETS = NUM_PUTS

    	def f():
			for k in range(NUM_GETS):
				node = nodes[k % N]

				# blocking call (provide callback arguments to make the call non-blocking)
				key = str(k)
				results = node.get(dht.InfoHash.get(key))

		times = timeit.repeat(f, number=1)
		print("[%s]: %d nodes, %d GETS of %d bytes ==> %.4f seconds" % (LABEL, N, NUM_GETS, NUM_BYTES, min(times)))

	def test_bulk_set(self):
		N = 100
    	NUM_BYTES = 2**10
		NUM_PUTS = 1000

		nodes = init_bulk_put(N, NUM_BYTES, NUM_PUTS)
		NUM_SETS = NUM_PUTS

    	def f():
			for k in range(NUM_SETS):
				node = nodes[k % N]
				subject = nodes[(k + 1) % N]

				key = str(k)
				self.client1.set(key, subject.ent.hash)

		times = timeit.repeat(f, number=1)
		print("[%s]: %d nodes, %d SETS of %d bytes ==> %.4f seconds" % (LABEL, N, NUM_SETS, NUM_BYTES, min(times)))

	def test_long_set(self):
		    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client1.set(key, self.client2.ent.hash, self.client1.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"hello world")
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client2.set(key, client3.ent.hash, self.client1.ent.hash)
    #     self.assertEqual(client3.get(key), b"hello world")
    	N = 100
    	NUM_BYTES = 2**10
		NUM_PUTS = 1000

		nodes = init_bulk_put(N, NUM_BYTES, NUM_PUTS)

		# key = str(hash(self.client1.ent.hash)) + "/obj1"
		key = str(0)
		for k in range(N - 1):
			node = nodes[k]
			subject = nodes[k + 1]
			node.set(key, subject.ent.hash, node.ent.hash)

		for k in range(N):
			node = nodes[k]
			times = timeit.repeat(node.get(key), number=1)
			print(k, min(times))

	# def test_random_bulkd
			
if __name__ == '__main__':
    unittest.main()

