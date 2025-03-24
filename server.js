const express = require("express");
const { exec } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_CMD = process.env.PYTHON_CMD || "python3"; // Use python3 by default

app.get("/fetch-articles", (req, res) => {
    const process = exec(`${PYTHON_CMD} scraper.py`, { timeout: 120000 }, (error, stdout, stderr) => {
        if (error) {
            console.error("Exec Error:", error);
            console.error("Stderr:", stderr);
            return res.status(500).json({ error: "Failed to fetch webpage", details: stderr });
        }
        try {
            const data = JSON.parse(stdout); // Parse Python output
            res.json(data);
        } catch (err) {
            console.error("JSON Parse Error:", err);
            res.status(500).json({ error: "Failed to parse Python response" });
        }
    });

    process.on("error", (err) => console.error("Process error:", err));
});

app.get("/test-python", (req, res) => {
    exec("python3 --version", (error, stdout, stderr) => {
        res.json({ error: error ? error.message : null, stdout, stderr });
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
