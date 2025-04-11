const express = require('express');
const router = express.Router();
const { analyzeJD } = require('../services/analyzeJD');

router.post('/analyze-jd', async (req, res) => {
  const { title, description } = req.body;
  try {
    const result = await analyzeJD(title, description);
    res.json(result);
  } catch (err) {
    console.error("JD Analysis Failed:", err);
    res.status(500).json({ error: 'JD analysis failed' });
  }
});

module.exports = router;
