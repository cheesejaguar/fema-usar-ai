# FEMA USAR AI Assistant

This tool is a private AI assistant for FEMA Urban Search & Rescue teams. It's designed to answer questions about your own documents, like training manuals or standard operating procedures.

Think of it like a private ChatGPT that only uses the information you give it. This keeps your information secure and provides answers based on your team's specific knowledge.

## How to Get Started

To use this tool, you'll need to have [Docker](https://www.docker.com/products/docker-desktop/) installed on your computer. Docker is a program that makes it easy to run applications in a self-contained environment, so you don't have to worry about complicated setup.

Once you have Docker installed, follow these steps:

### Step 1: Download the Files

First, you need to get the files for the AI assistant onto your computer. You can do this by cloning the repository.

```bash
git clone https://github.com/cheesejaguar/fema-usar-ai.git
cd fema-usar-ai
```

### Step 2: Set Up Your Configuration

The AI assistant needs a few secret keys to work, like the key for the AI model. These are stored in a file called `.env`.

1.  **Create the `.env` file:**
    ```bash
    cp .env.example .env
    ```
2.  **Edit the `.env` file:**
    Open the `.env` file in a text editor and fill in the required values. You'll need to get an `OPENAI_API_KEY` from [OpenAI](https://platform.openai.com/account/api-keys).

### Step 3: Add Your Documents

Place the documents you want the AI to learn from (like PDFs, Word documents, or text files) into the `uploads` folder.

### Step 4: Start the Server

Now you're ready to start the AI assistant. Run the following command in your terminal:

```bash
docker-compose up --build
```

This will start the server. The first time you run this, it might take a few minutes to download and set everything up.

### Step 5: Talk to Your AI Assistant

Once the server is running, you can start talking to your AI assistant! You can use a tool like [Postman](https://www.postman.com/) or `curl` to send requests to the server.

For example, to ask a question, you can send a request to `http://localhost:5000/api/chat`.

## For Developers

For more technical information, like details about the API, the project's architecture, and how to contribute, please see the [`DEVELOPER.md`](DEVELOPER.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
