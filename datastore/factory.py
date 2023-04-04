from datastore.datastore import DataStore
import os


def get_namespace_name(account_id: int, agentbot_id: int) -> str:
    """
    Returns the namespace name for a given account and agentbot.

    Args:
        account_id: The account id.
        agentbot_id: The agentbot id.

    Returns:
        The namespace name.
    """
    return f"{account_id}_{agentbot_id}"


def get_datastore() -> DataStore:
    """
    Returns the datastore instance.

    Returns:
        The datastore instance.
    """

    datastore = os.environ.get("DATASTORE")
    assert datastore is not None

    match datastore:
        case "pinecone":
            from datastore.providers.pinecone_datastore import PineconeDataStore

            return PineconeDataStore()
        case "weaviate":
            from datastore.providers.weaviate_datastore import WeaviateDataStore

            return WeaviateDataStore()
        case "milvus":
            from datastore.providers.milvus_datastore import MilvusDataStore

            return MilvusDataStore()
        case "zilliz":
            from datastore.providers.zilliz_datastore import ZillizDataStore

            return ZillizDataStore()
        case "redis":
            from datastore.providers.redis_datastore import RedisDataStore

            return RedisDataStore.init()
        case "qdrant":
            from datastore.providers.qdrant_datastore import QdrantDataStore

            return QdrantDataStore()
        case _:
            raise ValueError(f"Unsupported vector database: {datastore}")


datastore = get_datastore()
