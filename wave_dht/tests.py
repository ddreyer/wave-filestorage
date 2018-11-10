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
    
    def test_hierarchicalWriteShare(self):
        key = str(hash(self.client1.ent.hash)) + "/obj1/obj2"
        higher_key = str(hash(self.client1.ent.hash)) + "/obj1/*"
        self.client1.set(higher_key, self.client2.ent.hash, ["write"])
        self.client2.put(key, b"client 2 hello world", self.client1.ent.hash)
        self.assertEqual(self.client2.get(key), b"client 2 hello world")
        self.assertEqual(self.client1.get(key), b"client 2 hello world")

    # def test_revoke(self):

# rv = stub.ListLocations(eapi_pb2.ListLocationsParams())
# print(rv)

# ent3 = agent.CreateEntity(wv.CreateEntityParams())
# agent.PublishEntity(wv.PublishEntityParams(DER=ent3.PublicDER))

# client1.set("obj1", client1)

# client1.test(client2)
# client2.set(client1, "obj1")


# results = dht2.get("obj1", node)


# channel = grpc.insecure_channel("localhost:410")
# agent = wv.WAVEStub(channel)
# att2 = agent.CreateAttestation(wv.CreateAttestationParams(
#     perspective=client1.perspective,
#     subjectHash=client2.ent.hash,
#     publish=True,
#     policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
#         namespace=client1.ent.hash,
#         indirections=5,
#         statements=[
#             wv.RTreePolicyStatement(
#                 # This is a permission set used for special permissions
#                 permissionSet=wv.WaveBuiltinPSET,
#                 # this special permission generates end-to-end decryption keys
#                 permissions=[wv.WaveBuiltinE2EE],
#                 resource="obj1",
#             )]
#     ))))


# ent3perspective = wv.Perspective(
#     entitySecret=wv.EntitySecret(DER=ent3.SecretDER)
# )

# att2 = agent.CreateAttestation(wv.CreateAttestationParams(
#     perspective=perspective,
#     subjectHash=ent3.hash,
#     publish=True,
#     policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
#         namespace=ent.hash,
#         indirections=5,
#         statements=[
#             wv.RTreePolicyStatement(
#                 # This is a permission set used for special permissions
#                 permissionSet=wv.WaveBuiltinPSET,
#                 # this special permission generates end-to-end decryption keys
#                 permissions=[wv.WaveBuiltinE2EE],
#                 resource="objectstore/obj1",
#             )]
#     ))))

# # agent.ResyncPerspectiveGraph(wv.ResyncPerspectiveGraphParams(
# #     perspective=ent2perspective,
# # ))

# resp = agent.DecryptMessage(wv.DecryptMessageParams(
#         perspective= ent2perspective,
#         ciphertext= encrypted.ciphertext,
#         resyncFirst= True))
# if resp.error.code != 0:
#     print ("cannot decrypt", resp.error.message)
#     # return
# print(resp.content)
# resp2 = agent.DecryptMessage(wv.DecryptMessageParams(
#         perspective= ent3perspective,
#         ciphertext= encrypted.ciphertext,
#         resyncFirst= True))
# if resp2.error.code != 0:
#     print ("cannot decrypt", resp.error.message)
#     # return
# print(resp2.content)

# need to understand what is a nameDeclaration
# resp = agent.Revoke(wv.RevokeParams(
#         perspective=perspective,
#         attestationHash=att2.hash,
#         nameDeclarationHash=,
#         revokePerspective=ent3.perspective
# ))
# then break it up into proof + body
# proof, body = decomposeMessage(resp.content)
    
#     # now validate the proof
#     resp = wave.VerifyProof(wv.VerifyProofParams(
#         proofDER=proof,
#         requiredRTreePolicy=wv.RTreePolicy(
#             namespace=homeserver.namespace(),
#             statements=[wv.RTreePolicyStatement(
#                 permissionSet=smarthome_pset,
#                 permissions=["write"],
#                 resource="smarthome/thermostat/report",
#             )]
#         )
#     ))


# att = agent.CreateAttestation(wv.CreateAttestationParams(
#     perspective=perspective,
#     subjectHash=ent2.hash,
#     publish=True,
#     policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
#         namespace=ent.hash,
#         indirections=5,
#         statements=[wv.RTreePolicyStatement(
#             permissionSet=ent.hash,
#             permissions=["foo"],
#             resource="foo/bar",
#         )]
#     ))
# ))


# agent.ResyncPerspectiveGraph(wv.ResyncPerspectiveGraphParams(
#     perspective=ent2perspective,
# ))
# for status in agent.WaitForSyncComplete(wv.SyncParams(perspective=ent2perspective)):
#     print (status)

# proof = agent.BuildRTreeProof(wv.BuildRTreeProofParams(
#     perspective=ent2perspective,
#     namespace=ent.hash,
#     statements=[
#         wv.RTreePolicyStatement(
#             permissionSet=ent.hash,
#             permissions=["foo"],
#             resource="foo/bar",
#         )
#     ]
# ))

# vrfy = agent.VerifyProof(wv.VerifyProofParams(proofDER=proof.proofDER))

if __name__ == '__main__':
    unittest.main()