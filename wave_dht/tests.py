import wave_dht as wdht
import client
# import wave3 as wv
# import grpc

import unittest

class TestWaveDht(unittest.TestCase):
    def setUp(self):
        self.client1 = client.Client()
        self.client2 = client.Client()

    # def test_invalidGet(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.assertRaises(Exception, self.client2.get, key)
    
    # def test_simpleShare(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client1.set(key, self.client2.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"hello world")
    #     self.assertEqual(self.client1.get(key), b"hello world")

    # def test_simpleTransShare(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     client3 = client.Client()
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client1.set(key, self.client2.ent.hash, self.client1.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"hello world")
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client2.set(key, client3.ent.hash, self.client1.ent.hash)
    #     self.assertEqual(client3.get(key), b"hello world")
    #     self.assertEqual(self.client2.get(key), b"hello world")
    #     self.assertEqual(self.client1.get(key), b"hello world")
    
    def test_simpleBadTransShare(self):
        key = str(hash(self.client1.ent.hash)) + "/obj1"
        client3 = client.Client()
        self.client1.put(key, b"hello world", self.client1.ent.hash)
        self.assertEqual(self.client1.get(key), b"hello world")
        self.client2.set(key, client3.ent.hash, self.client1.ent.hash)
        self.assertRaises(Exception, client3.get, key)
        self.assertEqual(self.client1.get(key), b"hello world")
    
    # def test_badPut(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.assertRaises(Exception, self.client2.put, key, b"bad")
    #     self.assertEqual(self.client1.get(key), b"hello world")
    
    # def test_simpleWriteShare(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1"
    #     self.client1.set(key, self.client2.ent.hash, ["write"])
    #     self.client2.put(key, b"client 2 hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"client 2 hello world")
    #     self.assertEqual(self.client1.get(key), b"client 2 hello world")

    # def test_hierarchichalShare(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1/obj2"
    #     higher_key = str(hash(self.client1.ent.hash)) + "/obj1/*"
    #     self.client1.put(key, b"hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client1.get(key), b"hello world")
    #     self.client1.set(higher_key, self.client2.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"hello world")
    #     self.assertEqual(self.client1.get(key), b"hello world")
    
    # def test_hierarchicalWriteShare(self):
    #     key = str(hash(self.client1.ent.hash)) + "/obj1/obj2"
    #     higher_key = str(hash(self.client1.ent.hash)) + "/obj1/*"
    #     self.client1.set(higher_key, self.client2.ent.hash, ["write"])
    #     self.client2.put(key, b"client 2 hello world", self.client1.ent.hash)
    #     self.assertEqual(self.client2.get(key), b"client 2 hello world")
    #     self.assertEqual(self.client1.get(key), b"client 2 hello world")
    

    # def test_revoke(self):

if __name__ == '__main__':
    unittest.main()