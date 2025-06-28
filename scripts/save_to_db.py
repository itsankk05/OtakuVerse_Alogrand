from utils.db_utils import get_connection


def save_to_db(tx_id, wallet):
    # Save wallet + app_id into DB
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Wait for confirmation
        from algosdk.v2client import algod
        from utils.algod_client import get_algod_client

        algod_client = get_algod_client()

        def wait_for_confirmation(client, txid):
            last_round = client.status().get("last-round")
            while True:
                pending = client.pending_transaction_info(txid)
                if pending.get("confirmed-round", 0) > 0:
                    return pending
                last_round += 1
                client.status_after_block(last_round)

        confirmed_txn = wait_for_confirmation(algod_client, tx_id)
        app_id = confirmed_txn.get("application-index")

        if app_id:
            cursor.execute(
                "INSERT INTO user_contracts (wallet, app_id) VALUES (?, ?)",
                (wallet, app_id),
            )
            conn.commit()
            print(f"✅ Stored user contract: {wallet} → App ID {app_id}")
        return app_id

    except Exception as db_err:
        print(f"⚠️ Failed to store App ID in DB: {db_err}")

    finally:
        conn.close()
