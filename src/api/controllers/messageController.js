import Message from '../models/Message.js';
import Thread from '../models/Thread.js';

export const addMessage = async (req, res) => {
    const { thread_id } = req.params;
    const { sender_type, content, relevant_pdf_ids } = req.body;

    try {
        const message = new Message({
            thread_id,
            sender_type,
            content,
            relevant_pdf_ids
        });
        await message.save();

        const thread = await Thread.findById(thread_id);
        thread.messages.push(message._id);
        thread.last_updated = new Date();
        await thread.save();

        res.status(201).json({ message: 'Message added', message });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
