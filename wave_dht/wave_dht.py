import opendht as dht
import grpc
import base64
import wave3 as wv

class WaveDht:
    def __init__(self):
        self.node = dht.DhtRunner()
        self.node.run()
        # Join the network through any running node,
        # here using a known bootstrap node.
        self.node.bootstrap("bootstrap.ring.cx", "4222")

        channel = grpc.insecure_channel("localhost:410")
        self.agent = wv.WAVEStub(channel)

    def put(self, key, ciphertext, proof_or_sig, flag, namespace):
        if flag:
            if (str(hash(namespace)) != key.split("/")[0]):
                raise Exception("invalid namespace put")
            print("dht verifying proof")
            resp = self.agent.VerifyProof(wv.VerifyProofParams(
                proofDER=proof_or_sig,
                requiredRTreePolicy=wv.RTreePolicy(
                    namespace=namespace,
                    statements=[wv.RTreePolicyStatement(
                        permissionSet=namespace,
                        permissions=["write"],
                        resource=key,
                    )]
                )
            ))

            if resp.error.code != 0:
                raise Exception(resp.error.message)
        else:
            print("dht verifying sig")
            if (str(hash(namespace)) != key.split("/")[0]):
                raise Exception("invalid namespace put")
            vsig = self.agent.VerifySignature(wv.VerifySignatureParams(
                signer=namespace,
                signature=proof_or_sig,
                content=ciphertext
            ))
            if vsig.error.code != 0:
                raise Exception(vsig.error.message)

        # blocking call (provide callback arguments to make the call non-blocking)
        self.node.put(dht.InfoHash.get(key), dht.Value(ciphertext))

    def get(self, key):
        return self.node.get(dht.InfoHash.get(key))