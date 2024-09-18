# Ask-PDF

Ask-PDF is a Node.js application that extracts text from PDF files and leverages OpenAI's GPT-4 API to summarize or interact with the content. This is useful for gaining quick insights or summaries from large PDF documents.

## Features

- **Extract Text from PDFs**: Extract text content from PDF files using `pdf.js-extract`.
- **Summarize PDF Content**: Interact with OpenAI GPT-4 to summarize or get key points from the extracted text.
- **Rate Limiting Handling**: Automatically retries API requests when rate limits are hit.
- **Customizable API Integration**: You can modify the prompt and extend the interaction logic with the OpenAI API.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Node.js v14+** installed.
- **OpenAI API Key**: You need to have an OpenAI API key to use GPT-4.

## Installation

Follow these steps to get the project up and running:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kaushal726/ask-pdf.git
   cd ask-pdf
   ```

2. **Install the dependencies:**

   Run the following command to install the required packages:

   ```bash
   npm install
   ```

3. **Set up environment variables:**

   Create a `.env` file in the root of your project and add your OpenAI API key:

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Usage

1. Place your PDF file in the root directory or specify its path in the code.
2. Run the following command to start the application:

   ```bash
   bash start.sh
   ```

3. The program will extract text from the PDF file and send it to OpenAI for summarization or interaction. The response will be printed in the console.

### Example

```bash
bash start.sh
```

Output:

```
OpenAI's Response: The key points of the document are...
```

## Important Notes

- **API Rate Limiting**: The app automatically retries if the OpenAI API rate limit is exceeded. Adjust the retry logic if needed.
- **Large PDFs**: If you're working with large PDFs, consider trimming or splitting the content to avoid exceeding OpenAI's token limits.
- **Customizing Prompts**: You can modify the prompt in `pdfToAi.js` to change the interaction with GPT-4.

## Contributing

Contributions are welcome! If you would like to make changes or improvements, feel free to fork the repository and create a pull request.
