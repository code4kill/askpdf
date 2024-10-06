import express from 'express';
import { addMessage } from '../controllers/messageController.js';

const router = express.Router();

router.post('/:thread_id/add', addMessage);

export default router;
