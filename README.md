# 📝 Blog API

This repository contains a **FastAPI** application that provides an API for users to create accounts, log in, and browse
people's blogs. Authenticated users (bloggers) can write, read, update, and delete their own blogs, while admins have
the privilege to delete any blog.

## 🌟 Features

- **Public endpoints** to view blogs created by others.
- **User registration** to create a new account.
- **Login functionality** to authenticate users and provide them with JWT tokens.
- **Authenticated user endpoints** that allow bloggers to:
    - Create a new blog post.
    - Read their own blog posts or all public blogs.
    - Update their own blog posts.
    - Delete their own blog posts.
- **Admin functionality** to delete any blog post.
- **JWT Authentication** to ensure secure access to the API.
- **WebSocket** notifications for real-time updates, such as notifications for new blog posts.
- **SQLite** database to persist user and blog data.

## ⚙️ Configuration

The application uses an SQLite database, and no additional configuration is required for the database. The database file
will be created automatically when the app starts.

## 🚀 Usage

### 🐍 Running the FastAPI Application

To run the application locally, follow these steps:

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Start the FastAPI application**:
    ```bash
    uvicorn src.main:app --reload
    ```

3. **Access the API**:
   The application will be running at `http://localhost:8000`. You can also access the Swagger UI documentation at
   `http://localhost:8000/docs` for easy interaction with the API.

## 📦 Deploy on AWS Lambda

To deploy the Blog API on **AWS Lambda**, you can package your application with its dependencies into a `.zip` file and upload it as a Lambda function artifact.

Follow these steps:

1. **Install the dependencies into a `dependencies/` folder for the AWS Lambda-compatible platform**:
   ```bash
   pip3 install -r requirements.txt \
     --platform manylinux2014_x86_64 \
     --target=dependencies \
     --implementation cp \
     --python-version 3.12 \
     --only-binary=:all: \
     --upgrade openai

2. **Create a .zip archive containing the dependencies**:: `(cd dependencies; zip ../aws_lambda_artifact.zip -r .)`

3. **Add the `src/` folder to the archive**: `zip aws_lambda_artifact.zip -u -r src`

4. **Upload `aws_lambda_artifact.zip` to AWS Lambda using the AWS Console, AWS CLI, or an infrastructure-as-code tool like Terraform or AWS SAM**.
