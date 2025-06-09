const express = require('express');
const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode');

const app = express();
const port = 3001;

let qrImage = null;
let isAuthenticated = false;

const client = new Client({
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
        ]
    },
    authStrategy: null // Forces new login every time
});

// Handle QR Code event
client.on('qr', async (qr) => {
    console.log('QR received');
    qrImage = await qrcode.toDataURL(qr);
    isAuthenticated = false;
});

// Handle successful authentication
client.on('authenticated', () => {
    console.log('Authenticated successfully');
    qrImage = null; // Clear the QR image after login
    isAuthenticated = true;
});

// Ready to send/receive messages
client.on('ready', () => {
    console.log('Client is ready!');
});

client.initialize();

// Serve QR code
app.get('/qr', (req, res) => {
    if (isAuthenticated) {
        return res.send(`
            <html>
                <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#e6ffe6;">
                    <div style="text-align:center;">
                        <h2>✅ Already Authenticated</h2>
                        <p>You can now use WhatsApp automation.</p>
                    </div>
                </body>
            </html>
        `);
    }

    if (!qrImage) {
        return res.send(`
            <html>
                <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#fffbe6;">
                    <div style="text-align:center;">
                        <h2>⏳ QR Not Ready</h2>
                        <p>Waiting for WhatsApp to generate a QR code. Try again shortly.</p>
                    </div>
                </body>
            </html>
        `);
    }

    res.send(`
        <html>
            <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#f9f9f9;">
                <div style="text-align:center;">
                    <h2>📱 Scan this QR Code with WhatsApp</h2>
                    <img src="${qrImage}" alt="QR Code" style="border:1px solid #ccc; padding:10px; background:white;" />
                    <p style="margin-top:10px;">Keep your phone connected to the internet.</p>
                </div>
            </body>
        </html>
    `);
});

// Optional status route for debugging
app.get('/status', (req, res) => {
    if (isAuthenticated) return res.send('Authenticated ✅');
    if (qrImage) return res.send('QR Ready 📷');
    return res.send('Waiting for QR ⏳');
});

app.listen(port, () => {
    console.log(`🚀 QR server running on http://localhost:${port}`);
});


app.get('/qr-json', (req, res) => {
    try {
        if (isAuthenticated) {
            return res.json({ status: 'authenticated' });
        }
        if (!qrImage) {
            return res.json({ status: 'pending' });
        }
        res.json({ status: 'qr', image: qrImage });
    } catch (e) {
        res.status(500).json({ status: 'error', message: e.toString() });
    }
});
