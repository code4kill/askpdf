import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    username: { type: String, unique: true, required: true },
    email: { type: String, unique: true, required: true },
    password_hash: { type: String, required: true },
    created_at: { type: Date, default: Date.now },
    last_login: { type: Date, default: Date.now },
    threads: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Thread' }]
});

export default mongoose.model('User', userSchema);
