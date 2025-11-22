const express = require("express");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// 🔒 Deep Privacy Middleware
app.use((req, res, next) => {
    // Remove incoming tracking headers
    delete req.headers["cookie"];
    delete req.headers["referer"];
    delete req.headers["authorization"];
    delete req.headers["accept-language"];
    delete req.headers["user-agent"];
    delete req.headers["x-forwarded-for"];
    delete req.headers["x-real-ip"];

    // Replace with a constant anonymous fingerprint
    req.headers["User-Agent"] = "ShadowLens-Proxy/1.0";
    req.headers["Accept-Language"] = "en-US,en";
    req.headers["Connection"] = "close";

    next();
});

// 🕵️ Debug Endpoint — shows sanitized headers for demo
app.get("/debug", (req, res) => {
    res.json({
        message: "Headers after ShadowLens privacy clean-up",
        received_headers: req.headers
    });
});

// ✨ Basic Privacy Proxy Endpoint
app.post("/search", async (req, res) => {
    const { query } = req.body;

    if (!query) {
        return res.status(400).json({ error: "Missing query" });
    }

    const cleanHeaders = {
        "User-Agent": "ShadowLens-Proxy",
        "Accept": "application/json"
    };

    try {
        console.log(`Searching for: ${query}`);
        
        const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
        console.log(`URL: ${url}`);
        
        const response = await fetch(url, { headers: cleanHeaders });
        console.log(`Response status: ${response.status}`);

        if (!response.ok) {
            console.error(`HTTP error: ${response.status} ${response.statusText}`);
            return res.status(500).json({ error: `Search failed: ${response.status}` });
        }

        const data = await response.json();
        console.log(`Data received:`, Object.keys(data));

        // 🧹 Sanitize any HTML returned in text fields
function cleanText(text) {
    if (!text) return "";
    return text
        .replace(/<script[^>]*>([\s\S]*?)<\/script>/gi, "") // remove scripts
        .replace(/on\w+="[^"]*"/gi, "")                    // remove event handlers
        .replace(/on\w+='[^']*'/gi, "")
        .replace(/<iframe[^>]*>[\s\S]*?<\/iframe>/gi, "") // remove iframes
        .replace(/<img[^>]*(pixel|track)[^>]*>/gi, "")    // remove tracking pixels
        .replace(/<[^>]+>/g, "");                         // remove HTML tags
}
        
        res.json({
    results: (data.RelatedTopics || []).slice(0, 10).map(item => ({
        Text: cleanText(item.Text),
        FirstURL: item.FirstURL,
    })),
    abstract: cleanText(data.Abstract),
    query: query
});

    } catch (err) {
        console.error("Full error:", err);
        res.status(500).json({ error: `Proxy failed: ${err.message}` });
    }
});

app.listen(3000, () => {
    console.log("🔐 ShadowLens Privacy Proxy running on http://localhost:3000");
});
