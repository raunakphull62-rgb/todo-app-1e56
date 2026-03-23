# Setup Instructions for Todo App

## Introduction

This is a REST API for managing todo items, built using FastAPI and Supabase. This guide will walk you through the steps to set up and run the application.

## Prerequisites

* Python 3.9 or higher
* pip 22.0 or higher
* A Supabase instance (sign up for a free account on [Supabase](https://supabase.io/))
* A code editor or IDE of your choice

## Step 1: Clone the Repository

 Clone the repository using the following command:
```bash
git clone https://github.com/your-username/todo-app.git
```
 Replace `your-username` with your actual GitHub username.

## Step 2: Create a .env File

Create a new file named `.env` in the root directory of the project. Add the following environment variables:
```makefile
SUPABASE_URL="https://your-supabase-instance.supabase.io"
SUPABASE_KEY="your-supabase-key"
SUPABASE_SECRET="your-supabase-secret"
JWT_SECRET="your-jwt-secret"
```
 Replace the placeholders with your actual Supabase instance URL, key, and secret, as well as a secret key for JWT authentication.

## Step 3: Install Dependencies

 Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
## Step 4: Run the Application

 Run the application using the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
This will start the development server, and you can access the API at `http://localhost:8000`.

## Step 5: Test the API

Use a tool like `curl` or a REST client (e.g., Postman) to test the API endpoints. You can find the API documentation at `http://localhost:8000/docs`.

## Deployment

To deploy the application to a production environment, you can use a platform like Railway. Create a new Railway project and follow the instructions to deploy the application.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.