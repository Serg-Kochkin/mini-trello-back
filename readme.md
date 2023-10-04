# Mini Trello Back

This project is a simplified version of Trello, aimed at visualizing and managing tasks across different columns from backend side.

## Features:

- Create, Update, and Delete Cards.
- Drag and Drop Cards within and between columns.
- Apollo Client and GraphQL backend with DynamoDB.

## Prerequisites:

Ensure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

## Project Structure:

- A Flask application with GraphQL endpoints backed by DynamoDB.

## Getting Started:

### 1. Set up DynamoDB Local:

Follow the official [Amazon DynamoDB documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to get DynamoDB running locally.

### 2. Install dependencies:

**Frontend**:

Clone the repository:

```bash
git clone https://github.com/Serg-Kochkin/mini-trello-front.git
cd mini-trello-front
npm install
```

**Backend**:

```bash
git clone https://github.com/Serg-Kochkin/mini-trello-back.git
cd mini-trello-back
pip install -r requirements.txt
```

### 3. Start the servers:

**Frontend**:

\```bash
cd path/to/frontend
npm start
\```

Your frontend should now be running on http://localhost:5000.

**Backend**:

\```bash
cd path/to/backend
python run.py
\```

Your backend GraphQL server should be running on http://localhost:5000/graphql.

### 4. Interacting with the application:

Navigate to http://localhost:3000 in your browser to interact with the Mini Trello app. You can create, update, and delete cards, as well as drag them between different columns.
