from pyteal import *
from mint_nft import approval_program, clear_state_program
from nft_data_contract import nft_data_approval, nft_data_clear

def compile_to_teal():
    # 🟣 Compile Mint NFT contract
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=6)
    with open("build/mint_nft_approval.teal", "w") as f:
        f.write(approval_teal)

    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
    with open("build/mint_nft_clear.teal", "w") as f:
        f.write(clear_teal)

    # 🟢 Compile NFT Data Collection contract
    nft_data_approval_teal = compileTeal(nft_data_approval(), mode=Mode.Application, version=6)
    with open("build/nft_data_approval.teal", "w") as f:
        f.write(nft_data_approval_teal)

    nft_data_clear_teal = compileTeal(nft_data_clear(), mode=Mode.Application, version=6)
    with open("build/nft_data_clear.teal", "w") as f:
        f.write(nft_data_clear_teal)

if __name__ == "__main__":
    compile_to_teal()
