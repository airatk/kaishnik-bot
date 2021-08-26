def is_group_chat(peer_id: int) -> bool:
    return peer_id >= 2_000_000_000
