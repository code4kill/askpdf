import dotenv from 'dotenv';
import  OpenAI  from 'openai';

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const getEmbedding = async (text) => {
  const response = await openai.embeddings.create({
    model: "text-embedding-ada-002",
    input: text,
  });
  return response.data[0].embedding;
};

export const processAndEmbedChunks = async (chunks) => {
  const chunkEmbeddings = [];

  for (const chunk of chunks) {
    const embedding = await getEmbedding(chunk);
    chunkEmbeddings.push({ chunk, embedding });
  }

  return chunkEmbeddings;
};
