import express from 'express';
import { createThread } from '../controllers/threadController.js';

const router = express.Router();

router.post('/create', createThread);

export default router;
