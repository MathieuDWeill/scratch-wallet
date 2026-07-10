from engine.chain_anchor import rpc_status, load_anchor_config

if __name__ == "__main__":
    cfg = load_anchor_config()
    print(rpc_status(cfg))
