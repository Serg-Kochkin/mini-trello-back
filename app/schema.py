import graphene
from graphene import ObjectType, String, Int, Field, List, Mutation
from app.database import trello, create_card, update_card_content, delete_card, update_multiple_card_orders
import uuid


class Board(ObjectType):
    """Description of the Board object in the GraphQL schema."""
    board_id = String()
    board_name = String()


class Column(ObjectType):
    """Description of the column object (Column) in the GraphQL schema."""
    column_id = String()
    column_name = String()
    order = Int()


class Card(ObjectType):
    """Description of the Card object in the GraphQL schema."""
    card_id = String()
    column_id = String()
    card_content = String()
    order = Int()


class Trello(ObjectType):
    """Description of the Trello object that aggregates boards, columns and cards."""
    boards = List(Board)
    columns = List(Column)
    cards = List(Card)


class Query(ObjectType):
    trello = Field(Trello)

    def resolve_trello(self, info):
        boards, columns, cards = trello()
        return Trello(boards=boards, columns=columns, cards=cards)


class CreateCard(Mutation):
    """Mutation to create a new card."""
    class Arguments:
        columnId = String(required=True)
        content = String(required=True)
        order = Int(required=True)

    success = graphene.Boolean()
    card = Field(Card)

    def mutate(self, info, content, columnId, order):
        card_id = str(uuid.uuid4())
        card = {
            'card_id': card_id,
            'column_id': columnId,
            'card_content': content,
            'order': order
        }
        success = create_card(card)

        if success:
            return CreateCard(success=True, card=Card(**card))
        else:
            raise Exception("Failed to create the card")


class DeleteCard(Mutation):
    """Mutation to delete a card."""
    class Arguments:
        card_id = graphene.ID(required=True)

    success = graphene.Boolean()
    card_id = graphene.ID()

    def mutate(self, info, card_id):
        success = delete_card(card_id)
        if success:
            return DeleteCard(success=True, card_id=card_id)
        else:
            raise Exception("Failed to delete the card")


class UpdateCardContent(graphene.Mutation):
    """Mutation to update the contents of the card."""
    class Arguments:
        card_id = graphene.ID(required=True)
        card_content = graphene.String(required=True)

    success = graphene.Boolean()
    card_id = graphene.String()
    card_content = graphene.String()

    def mutate(self, info, card_id, card_content):
        updated = update_card_content(card_id, card_content)
        return UpdateCardContent(success=updated, card_id=card_id, card_content=card_content)


class UpdateMultipleCardOrderInput(graphene.InputObjectType):
    card_id = graphene.ID(required=True)
    column_id = graphene.ID(required=True)
    card_content = graphene.String(required=True)
    order = graphene.Int(required=True)


class UpdateMultipleCardOrder(graphene.Mutation):
    """Mutation for mass update of card order."""
    class Arguments:
        cardsInput = graphene.List(
            UpdateMultipleCardOrderInput, required=True)

    success = graphene.Boolean()
    cards = graphene.List(Card)

    def mutate(self, info, cardsInput):
        cards_to_update = [
            {
                'card_id': card_data.card_id,
                'column_id': card_data.column_id,
                'card_content': card_data.card_content,
                'order': card_data.order
            }
            for card_data in cardsInput
        ]

        # Assuming a function in database.py that updates the cards and returns the updated cards list
        updated_cards, success = update_multiple_card_orders(cards_to_update)

        if not success:
            raise Exception("Failed to update the cards order")

        return UpdateMultipleCardOrder(success=True, cards=updated_cards)


class Mutation(graphene.ObjectType):
    """Combining all mutations into one object."""
    create_card = CreateCard.Field()
    delete_card = DeleteCard.Field()
    update_card_content = UpdateCardContent.Field()
    update_multiple_card_order = UpdateMultipleCardOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
