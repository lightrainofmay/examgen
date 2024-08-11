# Automated Question and Essay Generation Tool

This tool is designed to automatically generate educational materials such as multiple-choice questions, fill-in-the-blank questions, essay questions, and sample essays. It leverages the power of OpenAI's GPT-3.5 to create high-quality content based on user-provided text and topics.

## Features
- Generate multiple-choice questions, fill-in-the-blank questions, and essay questions from PDF or TXT files.
- Create custom sample essays based on user-inputted topics.
- Easy file upload and content extraction.
- Test the connection to the OpenAI API.
- Configurable via environment variables.

## Requirements
- Python 3.7 or higher
- OpenAI API Key
- Internet connection

## Installation, Usage, Contributing, and License

   ```bash
   # 1. Clone the Repository
   git clone https://github.com/your-username/repo-name.git
   cd repo-name

   # 2. Create and Activate a Virtual Environment
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`

   # 3. Install the Required Packages
   pip install -r requirements.txt

   # 4. Set Up Environment Variables
   # Create a `.env` file in the root of your project and add the following:
   echo "OPENAI_API_KEY=your-openai-api-key" >> .env
   echo "BASE_URL=https://api.openai.com/v1" >> .env

   # 5. Run the Application
   streamlit run app.py

   # 6. Upload a File
   # - Upload a PDF or TXT file to generate questions.
   # - View the extracted content from the file.

   # 7. Generate Questions
   # - Click the buttons to generate multiple-choice, fill-in-the-blank, or essay questions.
   # - Alternatively, use the "Generate All Questions" button to create all types at once.

   # 8. Generate a Sample Essay
   # - Enter an essay topic in the provided text box.
   # - Click "Generate Sample Essay" to create a well-crafted essay based on your topic.

   # 9. Test API Connection
   # - Click "Test API Connection" to ensure the application can communicate with the OpenAI API.

   # 10. Contributing
   # Contributions are welcome! Please fork this repository and submit a pull request for any changes.

   # 11. License
   # This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Now, the entire setup, usage instructions, contribution guidelines, and license information are all included in one code block for easy reference and execution.
