import Thread from '../models/Thread.js';
import User from '../models/Users.js';

export const createThread = async (req, res) => {
    const { user_id, pdf_ids, title } = req.body;

    try {
        const thread = new Thread({
            user_id,
            pdf_ids,
            title
        });
        await thread.save();

        const user = await User.findById(user_id);
        user.threads.push(thread._id);
        await user.save();

        res.status(201).json({ message: 'Thread created', thread });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
