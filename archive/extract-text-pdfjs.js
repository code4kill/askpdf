// import fs from 'fs';
// import { getDocument } from 'pdfjs-dist/build/pdf';

// const pdfPath = './sample.pdf';

// // Read the PDF file as a binary
// const dataBuffer = fs.readFileSync(pdfPath);

// // Load the PDF document
// getDocument({ data: dataBuffer }).promise.then(async function (pdfDocument) {
//     const numPages = pdfDocument.numPages;
//     let extractedText = '';

//     // Loop through each page
//     for (let i = 1; i <= numPages; i++) {
//         const page = await pdfDocument.getPage(i);
//         const content = await page.getTextContent();

//         // Extract the text from the page content
//         const textItems = content.items.map(item => item.str);
//         extractedText += textItems.join(' ') + '\n\n'; // Join text from all items and add a newline
//     }

//     // Log the extracted text
//     console.log(extractedText);
// }).catch(function (err) {
//     console.error('Error: ' + err);
// });


const pdfjsLib = require("pdfjs-dist");

async function GetTextFromPDF(path) {
    let doc = await pdfjsLib.getDocument(path).promise;
    let page1 = await doc.getPage(1);
    let content = await page1.getTextContent();
    let strings = content.items.map(function(item) {
        return item.str;
    });
    return strings;
}


module.exports = { GetTextFromPDF }