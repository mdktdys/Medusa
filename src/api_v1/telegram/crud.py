from src.parser.methods import sup


async def subscribe_zamena_notifications(
    chat_id: str, target_type: int, target_id: int
):
    result = (
        sup.client.table("Subscribers")
        .insert(
            {"chat_id": chat_id, "target_type": target_type, "target_id": target_id}
        )
        .execute()
    )
    print(result)
    print(result.dict)


async def unsubscribe_zamena_notifications(
    chat_id: str, target_type: int, target_id: int
):
    result = (
        sup.client.table("Subscribers")
        .delete()
        .eq("chat_id", chat_id)
        .eq("chat_id", chat_id)
        .eq("target_type", target_type)
        .eq("target_id", target_id)
        .execute()
    )
    print(result)
    print(result.dict)
