import express from 'express';
import mongoose from 'mongoose';
import http from 'http';
import { Server } from 'socket.io';
import userRoutes from './routes/userRoute.js';

import threadRoutes from './routes/threadRoute.js';
import messageRoutes from './routes/messageRoute.js';
import pdfRoutes from './routes/pdfRoute.js';

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/ask-pdf', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

// Routes
app.use('/users', userRoutes);
app.use('/threads', threadRoutes);
app.use('/messages', messageRoutes);
app.use('/pdfs', pdfRoutes);

// Socket.io for real-time message communication
io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('joinThread', (threadId) => {
        socket.join(threadId);
    });

    socket.on('sendMessage', (messageData) => {
        io.to(messageData.threadId).emit('receiveMessage', messageData);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Start the server
const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
