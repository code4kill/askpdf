import User from '../models/Users.js';
import bcrypt from 'bcryptjs';
import { v4 as uuidv4 } from 'uuid';
import jwt from 'jsonwebtoken';


const JWT_SECRET = process.env.JWT_SECRET || 'your_jwt_secret';
// Register a new user
export const registerUser = async (req, res) => {
    const { username, email, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);

    try {
        const user = new User({
            username,
            email,
            password_hash: hashedPassword
        });
        await user.save();
        res.status(201).json({ message: 'User registered successfully', user });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Login user
// export const loginUser = async (req, res) => {
//     const { email, password } = req.body;

//     try {
//         const user = await User.findOne({ email });
//         if (!user || !(await bcrypt.compare(password, user.password_hash))) {
//             return res.status(400).json({ error: 'Invalid credentials' });
//         }
//         user.last_login = new Date();
//         await user.save();
//         res.status(200).json({ message: 'Login successful', user });
//     } catch (err) {
//         res.status(500).json({ error: err.message });
//     }
// };

export const loginUser = async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user || !(await bcrypt.compare(password, user.password_hash))) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }

        // Update last login time
        user.last_login = new Date();
        await user.save();

        // Create JWT token
        const token = jwt.sign(
            { id: user._id, username: user.username, email: user.email }, // Payload
            JWT_SECRET, // Secret key
            { expiresIn: '1h' } // Token expiration time
        );

        res.status(200).json({ message: 'Login successful', token });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
