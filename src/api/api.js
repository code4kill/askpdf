const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const { body, validationResult } = require("express-validator");
// const { chatWithRelevantText } = require("./chatWithGPT");

const app = express();
const uploadFolder = "data/";
const maxSize = 10 * 1024 * 1024;

// Multer configuration: Limit file size and restrict file type
const upload = multer({
  dest: uploadFolder,
  limits: { fileSize: maxSize },
  fileFilter: (req, file, cb) => {
    if (file.mimetype !== "application/pdf") {
      return cb(new Error("Only PDF files are allowed!"), false);
    }
    cb(null, true);
  },
});

// Delete all files in the upload folder except the new one
function clearUploadFolder() {
  fs.readdir(uploadFolder, (err, files) => {
    if (err) throw err;

    for (const file of files) {
      fs.unlink(path.join(uploadFolder, file), (err) => {
        if (err) throw err;
      });
    }
  });
}

// Route to upload and process PDF
app.post(
  "/upload",
  upload.single("pdf"),
  [
    // Custom validation to check file size and name
    (req, res, next) => {
      // Check if file exists
      if (!req.file) {
        return res
          .status(400)
          .json({ errors: [{ msg: "PDF file is required" }] });
      }

      // Validate file size (handled by multer already)
      if (req.file.size > maxSize) {
        return res
          .status(400)
          .json({ errors: [{ msg: `PDF size should not exceed 10MB` }] });
      }

      // Validate the file name
      if (req.file.originalname !== "sample.pdf") {
        return res
          .status(400)
          .json({ errors: [{ msg: "File name must be sample.pdf" }] });
      }

      // Proceed to the next middleware
      next();
    },
  ],
  async (req, res) => {
    // Delete existing files in the folder
    clearUploadFolder();

    // Move uploaded file to the target destination
    const pdfPath = path.join(uploadFolder, "sample.pdf");
    fs.rename(req.file.path, pdfPath, async (err) => {
      if (err) {
        return res.status(500).json({ errors: [{ msg: "Error saving file" }] });
      }

      try {
        // Run core functionality (e.g., chunking, embedding)
        const prompt = req.body.prompt || "Default prompt";
        // const result = await chatWithRelevantText(pdfPath, prompt);
        res.json({ success: true });
      } catch (error) {
        res.status(500).json({ success: false, error: error.message });
      }
    });
  }
);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
