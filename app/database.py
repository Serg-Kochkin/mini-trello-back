import boto3
import uuid

# Connecting to DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://dynamodb-local:8000',
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy',
    verify=False
)


def table_exists(table_name):
    """Checks whether the specified table exists."""
    try:
        dynamodb.Table(table_name).load()
        return True
    except:
        return False


def initialize_tables():
    """Initializes all necessary tables in the database."""
    # Creating a table Boards, if its not created.
    if not table_exists('Boards'):
        boards_table = dynamodb.create_table(
            TableName='Boards',
            KeySchema=[
                {
                    'AttributeName': 'board_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'board_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 12,
                'WriteCapacityUnits': 123
            }
        )
        # Wait for the table to be created
        # columns_table.wait_until_exists()
        boards_table.meta.client.get_waiter(
            'table_exists').wait(TableName='Boards')

        # Adding default board
        boards_table = dynamodb.Table('Boards')
        boards = ['Test Board']
        for board_name in boards:
            boards_table.put_item(
                Item={
                    'board_id': str(uuid.uuid4()),
                    'board_name': str(board_name)
                }
            )
        print("Boards table has been initialized.")

    # Creating a table Columns, if its not created.
    if not table_exists('Columns'):
        columns_table = dynamodb.create_table(
            TableName='Columns',
            KeySchema=[
                {
                    'AttributeName': 'column_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'column_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 123,
                'WriteCapacityUnits': 123
            }
        )
        # Wait for the table to be created
        columns_table.meta.client.get_waiter(
            'table_exists').wait(TableName='Columns')

        # Adding default columns
        columns = ['To Do', 'In Progress', 'Done']
        for index, column_name in enumerate(columns):
            columns_table.put_item(
                Item={
                    # 'column_id': str(uuid.uuid4()),
                    'column_id': str(uuid.uuid4()),
                    'column_name': column_name,
                    'order': index
                }
            )
        print("Columns and Cards table has been initialized.")

    # Creating a table Cards, if its not created.
    if not table_exists('Cards'):
        cards_table = dynamodb.create_table(
            TableName='Cards',
            KeySchema=[
                {
                    'AttributeName': 'card_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'card_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 123,
                'WriteCapacityUnits': 123
            }
        )
        # Wait for the table to be created
        cards_table.meta.client.get_waiter(
            'table_exists').wait(TableName='Cards')
        print("Cards table has been initialized.")


def trello():
    """Receives all information on boards, columns and cards."""
    # Defining tables
    boards_table = dynamodb.Table('Boards')
    columns_table = dynamodb.Table('Columns')
    cards_table = dynamodb.Table('Cards')

    # Extracting all boards
    boards_response = boards_table.scan()
    boards = boards_response['Items']

    # Extracting all columns
    columns_response = columns_table.scan()
    columns = columns_response['Items']

    # Extracting all cards
    cards_response = cards_table.scan()
    cards = cards_response['Items']

    return boards, columns, cards


def update_card_content(card_id, new_content):
    """Updates the contents of the specified card."""
    cards_table = dynamodb.Table('Cards')
    response = cards_table.update_item(
        Key={
            'card_id': card_id
        },
        UpdateExpression="set card_content = :c",
        ExpressionAttributeValues={
            ':c': new_content
        },
        ReturnValues="UPDATED_NEW"
    )
    return response['ResponseMetadata']['HTTPStatusCode'] == 200


def create_card(card):
    """Create a new card."""
    cards_table = dynamodb.Table('Cards')
    try:
        response = cards_table.put_item(Item=card)
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except:
        return False


def delete_card(card_id):
    """Delete a card by card_id."""
    cards_table = dynamodb.Table('Cards')
    try:
        response = cards_table.delete_item(
            Key={
                'card_id': card_id
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except:
        return False


def update_multiple_card_orders(cards):
    """Updates cards in the column."""
    cards_table = dynamodb.Table('Cards')
    updated_cards = []
    success = True

    for card in cards:
        try:
            response = cards_table.update_item(
                Key={'card_id': card['card_id']},
                UpdateExpression="set column_id = :columnVal, #order_attr = :orderVal",
                ExpressionAttributeNames={'#order_attr': 'order'},
                ExpressionAttributeValues={
                    ':columnVal': card['column_id'],
                    ':orderVal': card['order']
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                success = False
            else:
                updated_cards.append(card)
        except:
            success = False

    return updated_cards, success
