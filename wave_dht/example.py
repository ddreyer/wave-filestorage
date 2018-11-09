import grpc
import wave3 as wv

channel = grpc.insecure_channel("localhost:410")
agent = wv.WAVEStub(channel)
ent = agent.CreateEntity(wv.CreateEntityParams())
ent2 = agent.CreateEntity(wv.CreateEntityParams())
agent.PublishEntity(wv.PublishEntityParams(DER=ent.PublicDER))
agent.PublishEntity(wv.PublishEntityParams(DER=ent2.PublicDER))
perspective = wv.Perspective(
            entitySecret=wv.EntitySecret(DER=ent.SecretDER)
)

att = agent.CreateAttestation(wv.CreateAttestationParams(
        perspective=perspective,
        subjectHash=ent2.hash,
        publish=True,
        policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
            namespace=ent.hash,
            indirections=5,
            statements=[
                wv.RTreePolicyStatement(
                    # This is a permission set used for special permissions
                    permissionSet=wv.WaveBuiltinPSET,
                    # this special permission generates end-to-end decryption keys
                    permissions=wv.WaveBuiltinE2EE,
                    resource="temp",
                )]
        ))))
if att.error.code != 0:
    raise Exception(att.error.message)

# proof = agent.BuildRTreeProof(wv.BuildRTreeProofParams(
#             perspective=perspective,
#             namespace=ent.hash,
#             resyncFirst=True,
#             statements=[
#                 wv.RTreePolicyStatement(
#                     permissionSet=ent.hash,
#                     permissions=["write"],
#                     resource="temp",
#                 )
#             ]
#         ))
# if proof.error.code != 0:
#     raise Exception(proof.error.message)