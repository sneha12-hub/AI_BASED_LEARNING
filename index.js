// app.js
const express = require('express');
const { GeminiAPI } = require('gemini-api'); // Assuming you have a Gemini API library
const { LangChain } = require('langchain'); // And LangChain
const { LangGraph } = require('langgraph'); // And LangGraph

const YOUR_GEMINI_API_KEY = 'AIzaSyAwQ8kR0K4tHxAqfiPyP-NpkvZCHZCGBRs';
const app = express();
app.use(express.json()); // To parse JSON request bodies

// Initialize Gemini API client (replace with your actual API key)
const gemini = new GeminiAPI({ apiKey: YOUR_GEMINI_API_KEY });

// Initialize LangChain
const langchain = new LangChain();

// Initialize LangGraph
const langGraph = new LangGraph();

// Example LangChain prompt template (customize as needed)
const promptTemplate = `
You are a helpful assistant.  Answer the following question: {question}
`;

// Example LangGraph node (you'll likely have many of these)
const questionNode = langGraph.createNode('question', async (input) => {
    return input.question; // Just returns the question for now
});

const geminiNode = langGraph.createNode('gemini', async (input) => {
    const prompt = promptTemplate.replace('{question}', input.question);
    const response = await gemini.generateText({
        model: 'gemini-pro', // Or whichever model you're using
        prompt: prompt,
        temperature: 0.7, // Adjust as needed
        max_output_tokens: 200, // Adjust as needed
    });
    return response.candidates[0].output; // Extract the generated text
});

const answerNode = langGraph.createNode('answer', async (input) => {
    return input.geminiResponse; // Just returns the Gemini response
});



// Connect the LangGraph nodes (define the flow)
langGraph.connect(questionNode, geminiNode, { question: 'question' });
langGraph.connect(geminiNode, answerNode, { geminiResponse: 'gemini' });


// API endpoint to process user questions
app.post('/ask', async (req, res) => {
    const { question } = req.body;

    try {
        // Execute the LangGraph
        const result = await langGraph.execute({ question: question });

        // Extract the final answer from the result
        const answer = result.answer; 

        res.json({ answer: answer });
    } catch (error) {
        console.error("Error processing request:", error);
        res.status(500).json({ error: 'An error occurred.' });
    }
});


// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});


// Example usage (you'd send a POST request to /ask):
/*
{
  "question": "What is the capital of France?"
}
*/