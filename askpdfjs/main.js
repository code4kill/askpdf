import { chatWithRelevantText } from './model.js';

const pdfPath = './data/sample.pdf';
const prompt = 'Elephant Name';

chatWithRelevantText(pdfPath, prompt);
