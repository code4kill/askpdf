import mongoose from 'mongoose';

const pdfSchema = new mongoose.Schema({
    user_id: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    file_name: { type: String, required: true },
    file_path: { type: String, required: true },
    upload_date: { type: Date, default: Date.now },
    file_size: { type: Number, required: true },
    content_hash: { type: String, required: true }
});

export default mongoose.model('Pdf', pdfSchema);
