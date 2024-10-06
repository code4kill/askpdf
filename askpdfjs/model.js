import dotenv from 'dotenv';
import { OpenAI } from 'openai';
// import appConfig from './data/config.json';
import { extractPdfText, chunkText } from './text.extractor.js';
import { getEmbedding, processAndEmbedChunks } from './embedding.js';
import { findRelevantChunks } from './similarity.js';

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const askOpenAI = async (prompt) => {
  const appConfig = await import('./data/config.json', { assert: { type: 'json' } });
  try {
    const { MAX_TOKEN, MODEL, TEMPERATURE } = appConfig;
    const response = await openai.chat.completions.create({
      model: MODEL,
      messages: [{ role: "user", content: prompt }],
      max_tokens: MAX_TOKEN,
      temperature: TEMPERATURE,
    });

    return response.choices[0].message.content.trim();
  } catch (error) {
    if (error.response && error.response.status === 429) {
      console.warn("Rate limit exceeded. Retrying...");
      await new Promise((resolve) => setTimeout(resolve, 60000));
      return askOpenAI(prompt);
    } else {
      console.error("Error interacting with OpenAI API: ", error);
      throw error;
    }
  }
};

export const chatWithRelevantText = async (pdfPath, prompt) => {
  try {
    const extractedText = await extractPdfText(pdfPath);
    const chunks = chunkText(extractedText);
    const chunkEmbeddings = await processAndEmbedChunks(chunks);
    const queryEmbedding = await getEmbedding(prompt);
    const relevantChunks = await findRelevantChunks(queryEmbedding, chunkEmbeddings);
    const combinedText = relevantChunks.join(' ');
    const finalPrompt = `${prompt}\n\n${combinedText}`;
    const response = await askOpenAI(finalPrompt);
    console.log("ChatGPT Response:", response);
  } catch (error) {
    console.error("Error:", error);
  }
};
