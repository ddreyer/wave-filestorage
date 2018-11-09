import wave_dht as wdht
import grpc
import base64
import wave3 as wv

class Client:
    def __init__(self):
        channel = grpc.insecure_channel("localhost:410")
        self.agent = wv.WAVEStub(channel)
        self.ent = self.agent.CreateEntity(wv.CreateEntityParams())
        self.pub_hash = str(base64.b64encode(self.ent.hash), "utf8").replace("=", "")
        self.agent.PublishEntity(wv.PublishEntityParams(DER=self.ent.PublicDER))
        self.perspective = wv.Perspective(
            entitySecret=wv.EntitySecret(DER=self.ent.SecretDER)
        )
        self.wdht_handle = wdht.WaveDht()


    def put(self, key, value):
        encrypted = self.agent.EncryptMessage(
            wv.EncryptMessageParams(
                namespace=self.ent.hash,
                resource=str(key),
                content=value))

        if encrypted.error.code != 0:
            raise Exception(encrypted.error.message)

        print("in client put")
        print("/".join(key.split("/")[:-1]), self.pub_hash)
        # print(key.split("/")[0])
        # print(self.pub_hash)
        # print(key.split("/")[0] == self.pub_hash)
        # print(str(key))

        # if we are trying to put on a resource in our namespace, sign
        # key contains modified entity hash of namespace that the object is under
        if "/".join(key.split("/")[:-1]) == self.pub_hash:
            print("client is signing")
            sig = self.agent.Sign(wv.SignParams(
                perspective=self.perspective,
                content=encrypted.ciphertext
            ))
            if sig.error.code != 0:
                raise Exception(sig.error.message)
            self.wdht_handle.put(key, encrypted.ciphertext, sig.signature, False)
        else:
            print("client is building proof")
            print("/".join(key.split("/")[:-1]) + "==")
            print(self.pub_hash)
            decode = base64.b64decode("/".join(key.split("/")[:-1]) + "==")
            proof = self.agent.BuildRTreeProof(wv.BuildRTreeProofParams(
                perspective=self.perspective,
                namespace=base64.b64decode("/".join(key.split("/")[:-1]) + "=="),
                resyncFirst=True,
                statements=[
                    wv.RTreePolicyStatement(
                        permissionSet=base64.b64decode("/".join(key.split("/")[:-1]) + "=="),
                        permissions=["write"],
                        resource=key,
                    )
                ]
            ))
            if proof.error.code != 0:
                raise Exception(proof.error.message)

            self.wdht_handle.put(key, encrypted.ciphertext, proof.proofDER, True)



    # for now, just fetch the data that is protected with E2EE
    def get(self, key):
        # proof = self.agent.BuildRTreeProof(wv.BuildRTreeProofParams(
        #     perspective=self.perspective,
        #     namespace=namespace.ent.hash,
        #     statements=[
        #         wv.RTreePolicyStatement(
        #             permissionSet=wv.WaveBuiltinPSET,
        #             permissions=[wv.WaveBuiltinE2EE],
        #             resource=key,
        #         )
        #     ]
        # ))
        results = self.wdht_handle.get(key)
        # self.agent.ResyncPerspectiveGraph(wv.ResyncPerspectiveGraphParams(
        #     perspective=self.perspective,
        # ))
        for r in results:
            resp = self.agent.DecryptMessage(wv.DecryptMessageParams(
                perspective= self.perspective,
                ciphertext= r.data,
                resyncFirst=True))
            if resp.error.code == 0:
                return resp.content
        return None
    
    def set(self, key, subj, perms=None):
        print("in set")
        att = self.agent.CreateAttestation(wv.CreateAttestationParams(
            perspective=self.perspective,
            subjectHash=subj,
            publish=True,
            policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
                namespace=self.ent.hash,
                indirections=5,
                statements=[
                    wv.RTreePolicyStatement(
                        # This is a permission set used for special permissions
                        permissionSet=wv.WaveBuiltinPSET if not perms else self.ent.hash,
                        # this special permission generates end-to-end decryption keys
                        permissions=[wv.WaveBuiltinE2EE] if not perms else perms,
                        resource=key,
                    )]
            ))))
        if att.error.code != 0:
            raise Exception(att.error.message)
