import opendht as dht
import wave_dht as wdht
import client

import unittest
import numpy as np
import timeit

# import imp

# dht = imp.load_source('opendht', '/usr/local/lib/python3.6/dist-packages/opendht.cpython-36m-x86_64-linux-gnu.so')

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

def get_key(k, is_wave, namespace=None):
    if is_wave:
        return str(hash(namespace)) + "/%s" % k
    else:
        return str(k)

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
            key = get_key(k, is_wave=IS_WAVE)
            val = np.random.bytes(NUM_BYTES)
            node.put(dht.InfoHash.get(key), dht.Value(val))
        return nodes

    def test_bulk_put(self):
        N = 10
        print("Setting up network...")
        nodes = setup_network(is_wave=IS_WAVE, N=N)
        print("Finished setup...")
        NUM_BYTES = 2**10
        NUM_PUTS = 10
        def f():
            for k in range(NUM_PUTS):
                node = nodes[k % N]

                # blocking call (provide callback arguments to make the call non-blocking)
                key = get_key(k, is_wave=IS_WAVE, namespace=node.ent.hash if IS_WAVE else None)
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
                key = get_key(k, is_wave=IS_WAVE)
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

                key = get_key(k, is_wave=IS_WAVE)
                node.set(key, subject.ent.hash)

        times = timeit.repeat(f, number=1)
        print("[%s]: %d nodes, %d SETS of %d bytes ==> %.4f seconds" % (LABEL, N, NUM_SETS, NUM_BYTES, min(times)))

    def test_long_set_get(self):
        assert(IS_WAVE)
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
    
    def test_bulk_set_put(self):
        assert(IS_WAVE)
        N = 10
        NUM_BYTES = 2**10
        NUM_PUTS = 10

        # nodes = init_bulk_put(N, NUM_BYTES, NUM_PUTS)
        nodes = setup_network(is_wave=IS_WAVE, N=N)
        # key = str(hash(self.client1.ent.hash)) + "/obj1"
    
        for k in range(N - 1):
            node = nodes[k]
            subject = nodes[k + 1]
            key = get_key(k, is_wave=IS_WAVE, namespace=node.ent.hash if IS_WAVE else None)
            node.set(key, subject.ent.hash, node.ent.hash, ["write"])

        def f():
            for k in range(N - 1):
                node = nodes[k]
                subject = nodes[k + 1]

                key = get_key(k, is_wave=IS_WAVE, namespace=node.ent.hash if IS_WAVE else None)
                val = np.random.bytes(NUM_BYTES)
                subject.put(key, val, node.ent.hash)

        times = timeit.repeat(f, number=1)
        print("[%s]: %d nodes, %d PUTS of %d bytes ==> %.4f seconds" % (LABEL, N, NUM_PUTS, NUM_BYTES, min(times)))
        # print(k, min(times))
    # def test_random_bulk_put_get(self):

            
if __name__ == '__main__':
    unittest.main()

