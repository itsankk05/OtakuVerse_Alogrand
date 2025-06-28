from pyteal import *

def marketplace_logic():
    price = Int(1000000)  # 1 ALGO

    return And(
        Txn.type_enum() == TxnType.Payment,
        Txn.amount() >= price,
        Txn.receiver() == Global.current_application_address()
    )
