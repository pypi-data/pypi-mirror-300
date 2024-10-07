"""Internal utility functions."""

import json
from typing import Any

from .schemas import (
    Chunk,
    ChunkMetadata,
    Node,
    Relation,
    SchemaEntity,
    SchemaRelation,
    SchemaTriplePattern,
    Triple,
)


def _create_graph_from_knowledge_table(
    client: Any, file_path: str, workspace_name: str, graph_name: str
) -> str:
    """
    Create a graph from a knowledge table file.

    This internal function handles the process of creating a graph
    from a knowledge table file, including data loading, structuring,
    and uploading to the specified workspace.

    Parameters
    ----------
    client
        The client object used for API interactions.
    file_path : str
        Path to the knowledge table file.
    workspace_name : str
        Name of the workspace to use or create.
    graph_name : str
        Name for the graph to be created.

    Returns
    -------
    str
        The ID of the created graph.
    """
    print(f"Starting graph creation from knowledge table: {file_path}")

    # 1. Import the file
    with open(file_path, "r") as f:
        data = json.load(f)
    print(f"Loaded data from {file_path}")

    # 2. Structure the chunks and triples
    formatted_chunks = [
        Chunk(
            chunk_id=c["chunk_id"],
            content=c["content"],
            metadata=ChunkMetadata(page=int(c["page"])),
        )
        for c in data["chunks"]
    ]
    print(f"Structured {len(formatted_chunks)} chunks")

    formatted_triples = [
        Triple(
            triple_id=t["triple_id"],
            head=Node(label=t["head"]["label"], name=t["head"]["name"]),
            tail=Node(label=t["tail"]["label"], name=t["tail"]["name"]),
            relation=Relation(name=t["relation"]["name"]),
            chunk_ids=t["chunk_ids"],
        )
        for t in data["triples"]
    ]

    print(f"Structured {len(formatted_triples)} triples")

    # 3. Get or create the workspace
    workspaces = list(client.workspaces.get_all(name=workspace_name))
    workspace = next(iter(workspaces), None)
    if not workspace:
        workspace = client.workspaces.create(name=workspace_name)
        print(f"Created new workspace: {workspace_name}")
    else:
        print(f"Using existing workspace: {workspace_name}")

    # 4. Upload the chunks to the workspace
    created_chunks = client.chunks.create(
        workspace_id=workspace.workspace_id, chunks=formatted_chunks
    )
    print(f"Uploaded {len(created_chunks)} chunks to workspace")

    # 5. Make the schema
    generated_relations = {
        triple.relation.name for triple in formatted_triples
    }
    generated_entity_types = {
        triple.head.label for triple in formatted_triples
    } | {triple.tail.label for triple in formatted_triples}

    entities = [
        SchemaEntity(
            name=entity_type, description=f"Description for {entity_type}"
        )
        for entity_type in generated_entity_types
    ]
    relations = [
        SchemaRelation(
            name=relation, description=f"Description for {relation}"
        )
        for relation in generated_relations
    ]
    patterns = []

    for triple in formatted_triples:
        pattern = SchemaTriplePattern(
            head=SchemaEntity(name=triple.head.label),
            relation=SchemaRelation(name=triple.relation.name),
            tail=SchemaEntity(name=triple.tail.label),
            description=f"{triple.head.label} {triple.relation.name} {triple.tail.label}",
        )
        if pattern not in patterns:
            patterns.append(pattern)

    created_schema = client.schemas.create(
        workspace_id=workspace.workspace_id,
        name="Knowledge Table Schema",
        entities=entities,
        relations=relations,
        patterns=patterns,
    )
    print(f"Created schema: {created_schema.schema_id}")

    # # 6. Make the graph
    # graph = client.graphs.create(
    #     name=graph_name,
    #     workspace_id=workspace.workspace_id,
    #     schema_id=created_schema.schema_id,
    #     mode="unstructured",
    # )
    # print(f"Created graph: {graph.graph_id}")

    # # 7. Add the triples to the graph
    # # Temporarily disable the logger
    # logger = logging.getLogger("whyhow.raw.base")
    # original_level = logger.level
    # logger.setLevel(logging.CRITICAL)

    # try:
    #     client.graphs.add_triples(
    #         graph_id=graph.graph_id, triples=formatted_triples
    #     )
    #     print("Added triples to the graph")
    # except ResponseSuccessValidationError:
    #     # Silently continue execution without printing any message
    #     pass
    # finally:
    #     # Restore the original logger level
    #     logger.setLevel(original_level)

    graph = client.graphs.create_graph_from_triples(
        name=graph_name,
        workspace_id=workspace.workspace_id,
        triples=formatted_triples,
    )

    print("Successfully created graph from knowledge table.")
    return graph.graph_id
