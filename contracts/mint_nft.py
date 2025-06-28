from pyteal import *


def approval_program():
    handle_creation = Seq([App.globalPut(Bytes("Creator"), Txn.sender()), Approve()])
    return Cond([Txn.application_id() == Int(0), handle_creation])


def clear_state_program():
    return Approve()


# {
#     "userWallet": "TAWEKOHN2WH3UXRQGM3ZCOXH2CIXYXB6DEQK2YWJH4GGSNT7SVA7OSCV2A",
#     "animeId": "5",
#     "episodeId": "5_episode_1",
#     "watchTime": 9,
#     "nftMetadata": {
#         "id": 5,
#         "name": "jlkljklj",
#         "description": "Exclusive NFT from fdfsdf",
#         "image": "https://ipfs.io/ipfs/QmZbkMRLZaYmzqVR5iizcU8jsoffeaWVWAx8grp1g9nMgZ",
#         "anime": "fdfsdf",
#         "animeId": "5",
#         "episode": 1,
#         "watchTime": 15,
#         "rarity": "Common",
#         "isListed": False,
#         "attributes": [
#             {"trait_type": "Series", "value": "fdfsdf"},
#             {"trait_type": "Episode", "value": 1},
#             {"trait_type": "Rarity", "value": "Common"},
#             {"trait_type": "Actual Watch Time", "value": "0 Minutes"},
#             {"trait_type": "Video Progress", "value": "91%"},
#             {"trait_type": "Mint Trigger", "value": "watch_completion"},
#             {"trait_type": "Episode Number", "value": 1},
#             {"trait_type": "Series Title", "value": "fdfsdf"},
#             {"trait_type": "Total Episodes"},
#             {"trait_type": "Collection Type", "value": "Watch-to-Earn"},
#             {"trait_type": "Platform", "value": "OtakuVerse"},
#             {"trait_type": "Creator", "value": "Unknown Creator"},
#             {"trait_type": "Creator ID", "value": "unknown"},
#             {"trait_type": "Genre", "value": "Action"},
#             {"trait_type": "Mint Date", "value": "2025-06-28"},
#         ],
#         "ipfs_metadata": {
#             "cid": "QmRj2WryQAiNKEhsjP8tUqfBC4KhEJhrtKezKGcYm4J9uK",
#             "gateway_url": "https://ipfs.io/ipfs/QmZbkMRLZaYmzqVR5iizcU8jsoffeaWVWAx8grp1g9nMgZ",
#             "pinned": True,
#         },
#         "creator": {"id": "unknown", "username": "Unknown Creator"},
#         "mintedAt": "2025-06-28T12:12:19.796Z",
#         "mintedBy": "TAWEKOHN2WH3UXRQGM3ZCOXH2CIXYXB6DEQK2YWJH4GGSNT7SVA7OSCV2A",
#         "sourceAnimeData": {
#             "title": "fdfsdf",
#             "description": "dsfsdfs",
#             "genres": ["Action", "Adventure"],
#             "views": 0,
#             "likes": 0,
#         },
#     },
#     "platform": "OtakuVerse",
#     "version": "2.0",
#     "timestamp": "2025-06-28T12:12:19.796Z",
#     "mintingContext": {
#         "triggerType": "watch_completion",
#         "actualWatchTime": 9,
#         "videoProgress": 91.44700283303958,
#         "sessionId": "session_1751112739795",
#     },
# }
