import mongoose from 'mongoose';

const threadSchema = new mongoose.Schema({
    user_id: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    pdf_ids: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Pdf' }],
    title: { type: String, required: true },
    created_at: { type: Date, default: Date.now },
    last_updated: { type: Date, default: Date.now },
    messages: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Message' }]
});

export default mongoose.model('Thread', threadSchema);
