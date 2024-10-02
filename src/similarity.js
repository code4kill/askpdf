// import appConfig from './data/config.json' assert { type: 'json' };

export function cosineSimilarity(vecA, vecB) {
  const dotProduct = vecA.reduce((acc, val, i) => acc + val * vecB[i], 0);
  const magnitudeA = Math.sqrt(vecA.reduce((acc, val) => acc + val * val, 0));
  const magnitudeB = Math.sqrt(vecB.reduce((acc, val) => acc + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

export const findRelevantChunks = async (queryEmbedding, chunkEmbeddings) => {
  const appConfig = await import('./data/config.json', { assert: { type: 'json' } });
  const relevantChunks = [];

  for (const { chunk, embedding } of chunkEmbeddings) {
    const similarity = cosineSimilarity(queryEmbedding, embedding);

    if (similarity > appConfig.THRESHOLD) {
      relevantChunks.push(chunk);
    }
  }

  return relevantChunks;
};
