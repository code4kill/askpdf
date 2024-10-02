import multer from 'multer';
import path from 'path';
import Pdf from './models/Pdf'; // Make sure to replace this with the actual path to your PDF model

// Set up file upload with multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, './storage/pdfs'), // Define the destination folder
    filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`) // Filename is timestamp-originalname
});

export const upload = multer({ storage }).single('pdf'); // Expect a single file named 'pdf'

// Route handler to upload PDF
export const uploadPdf = async (req, res) => {
    const { user_id } = req.body; // Extract user ID from the form data
    const { filename, path: filePath } = req.file; // Extract file details

    try {
        // Create a new PDF document with the metadata
        const pdf = new Pdf({
            user_id,
            file_name: filename,
            file_path: filePath,
            file_size: req.file.size, // Size of the uploaded file
            content_hash: 'sha256_hash_placeholder' // Placeholder for now
        });
        await pdf.save(); // Save the PDF metadata in MongoDB

        res.status(201).json({ message: 'PDF uploaded successfully', pdf }); // Return a success response
    } catch (err) {
        res.status(500).json({ error: err.message }); // Handle errors
    }
};
