import { extractPdfText } from './text.extractor.js';
import { askOpenAI } from './model.js';

const hardcodedPrompt = `Favourite Elephant Name:\n\n`;

export const chatWithPdf = async (pdfPath) => {
  try {
    const extractedText = await extractPdfText(pdfPath);

    const maxLength = 2000;
    const trimmedText = extractedText.length > maxLength
      ? `${extractedText.substring(0, maxLength)}...`
      : extractedText;

    const prompt = `${hardcodedPrompt}${trimmedText}`;

    const aiResponse = await askOpenAI(prompt);
    console.log("OpenAI's Response:", aiResponse);
  } catch (error) {
    console.error("Error:", error);
  }
};
