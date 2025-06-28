from pyteal import (
    Approve, 
    App, 
    Bytes, 
    Cond, 
    Int, 
    Mode, 
    Reject, 
    Seq, 
    Txn,
    compileTeal
)

def nft_data_approval():
    creator_key = Bytes("creator")         # Address
    metadata_cid_key = Bytes("metadata")   # IPFS CID
    image_cid_key = Bytes("image")         # First NFT image CID

    on_create = Seq([
        App.globalPut(creator_key, Txn.sender()),
        App.globalPut(metadata_cid_key, Txn.application_args[0]),
        App.globalPut(image_cid_key, Txn.application_args[1]),
        Approve()
    ])

    # No other transactions allowed
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Int(1), Reject()]
    )

    return program

def nft_data_clear():
    return Approve()
