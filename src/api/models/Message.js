import mongoose from 'mongoose';

const messageSchema = new mongoose.Schema({
    thread_id: { type: mongoose.Schema.Types.ObjectId, ref: 'Thread', required: true },
    sender_type: { type: String, enum: ['user', 'system'], required: true },
    content: { type: String, required: true },
    timestamp: { type: Date, default: Date.now },
    relevant_pdf_ids: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Pdf' }]
});

export default mongoose.model('Message', messageSchema);
