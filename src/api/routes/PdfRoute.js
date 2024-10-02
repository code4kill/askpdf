import express from 'express';
import { upload, uploadPdf } from '../controllers/pdfController.js';

const router = express.Router();

router.post('/upload', upload.single('pdf'), uploadPdf);

export default router;
