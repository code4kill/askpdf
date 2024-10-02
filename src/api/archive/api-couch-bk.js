import express from 'express';
import bodyParser from 'body-parser';
import nano from 'nano';
import { v4 as uuidv4 } from 'uuid';

// Set up CouchDB connection
const couchdbUrl = 'http://localhost:5984';
const nanoInstance = nano(couchdbUrl);
const dbName = 'ask-pdf';

// Initialize the app
const app = express();
const port = 3000;

// Middleware to parse JSON request body
app.use(bodyParser.json());

// Connect to CouchDB database
const db = nanoInstance.db.use(dbName);

// Helper function to create the database if it doesn't exist
async function createDatabase() {
    try {
        await nanoInstance.db.create(dbName);
        console.log(`Database "${dbName}" created successfully.`);
    } catch (err) {
        if (err.statusCode === 412) {
            console.log(`Database "${dbName}" already exists.`);
        } else {
            console.error(`Error creating database: ${err.message}`);
        }
    }
}

// Helper function to check database connection
async function testDbConnection() {
    try {
        const dbList = await nanoInstance.db.list();
        return dbList.includes(dbName);
    } catch (err) {
        throw new Error('Database connection failed.');
    }
}

// Helper function to get the next sequence number for a conversation
async function getNextSequenceNumber(conversationId) {
    const messages = await db.find({
        selector: {
            conversation_id: conversationId,
            type: 'message',
        },
        fields: ['sequence_number'],
        sort: [{ sequence_number: 'desc' }],
        limit: 1,
    });
    return messages.docs.length > 0 ? messages.docs[0].sequence_number + 1 : 1;
}

// API Endpoints

// 1. Test if database connection is successful
app.get('/test-db', async (req, res) => {
    try {
        const connected = await testDbConnection();
        if (connected) {
            res.status(200).json({ message: `Database "${dbName}" is connected.` });
        } else {
            res.status(500).json({ error: `Failed to connect to database "${dbName}".` });
        }
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 2. Create a new user
app.post('/users', async (req, res) => {
    const { username, email, password_hash } = req.body;
    const userDoc = {
        _id: `user:${username}`,
        type: 'user',
        username,
        email,
        password_hash,
        created_at: new Date().toISOString(),
        last_login: new Date().toISOString(),
    };
    try {
        await db.insert(userDoc);
        res.status(201).json({ message: `User "${username}" created.` });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 3. Upload a PDF
app.post('/pdfs', async (req, res) => {
    const { user_id, file_name, file_path, file_size, content_hash } = req.body;
    const pdfDoc = {
        _id: `pdf:${uuidv4()}`,
        type: 'pdf',
        user_id,
        file_name,
        file_path,
        upload_date: new Date().toISOString(),
        file_size,
        content_hash,
        conversation_ids: [],
    };
    try {
        await db.insert(pdfDoc);
        res.status(201).json({ message: `PDF "${file_name}" uploaded.` });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 4. Create a conversation
app.post('/conversations', async (req, res) => {
    const { user_id, pdf_ids, title } = req.body;
    const conversationDoc = {
        _id: `conversation:${uuidv4()}`,
        type: 'conversation',
        user_id,
        pdf_ids,
        start_time: new Date().toISOString(),
        last_updated: new Date().toISOString(),
        title,
        message_count: 0,
    };
    try {
        await db.insert(conversationDoc);
        res.status(201).json({ message: `Conversation "${title}" created.` });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 5. Add a message
app.post('/conversations/:conversationId/messages', async (req, res) => {
    const { conversationId } = req.params;
    const { user_id, content, tokens_used, relevant_chunks } = req.body;
    const sequence_number = await getNextSequenceNumber(conversationId);
    const messageDoc = {
        _id: `msg:${uuidv4()}`,
        type: 'message',
        conversation_id: conversationId,
        sender_type: 'user',
        content,
        timestamp: new Date().toISOString(),
        tokens_used,
        relevant_chunks,
        sequence_number,
    };
    try {
        await db.insert(messageDoc);
        res.status(201).json({ message: 'Message added to conversation.' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 6. Add a bot response
app.post('/conversations/:conversationId/bot-response', async (req, res) => {
    const { conversationId } = req.params;
    const { content, tokens_used } = req.body;
    const sequence_number = await getNextSequenceNumber(conversationId);
    const botResponseDoc = {
        _id: `bot_resp:${uuidv4()}`,
        type: 'bot_response',
        conversation_id: conversationId,
        sender_type: 'bot',
        content,
        timestamp: new Date().toISOString(),
        tokens_used,
        sequence_number,
    };
    try {
        await db.insert(botResponseDoc);
        res.status(201).json({ message: 'Bot response added to conversation.' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Initialize the database and start the server
createDatabase().then(() => {
    app.listen(port, () => {
        console.log(`Server running at http://localhost:${port}`);
    });
});
