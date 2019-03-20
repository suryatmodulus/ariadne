from typing import Optional

from graphql.type import GraphQLUnionType, GraphQLSchema

from .types import Resolver, SchemaBindable


class UnionType(SchemaBindable):
    _resolve_type: Optional[Resolver]

    def __init__(self, name: str, type_resolver: Optional[Resolver] = None) -> None:
        self.name = name
        self._resolve_type = type_resolver

    def set_type_resolver(self, type_resolver: Resolver) -> Resolver:
        self._resolve_type = type_resolver
        return type_resolver

    type_resolver = (
        set_type_resolver
    )  # Alias type resolver for consistent decorator name

    def bind_to_schema(self, schema: GraphQLSchema) -> None:
        graphql_type = schema.type_map.get(self.name)
        self.validate_graphql_type(graphql_type)
        graphql_type.resolve_type = self._resolve_type

    def validate_graphql_type(self, graphql_type: str) -> None:
        if not graphql_type:
            raise ValueError("Type %s is not defined in the schema" % self.name)
        if not isinstance(graphql_type, GraphQLUnionType):
            raise ValueError(
                "%s is defined in the schema, but it is instance of %s (expected %s)"
                % (self.name, type(graphql_type).__name__, GraphQLUnionType.__name__)
            )
