# Quick Reference - Fixed RAG System

## ✅ Problem SOLVED
**Before:** Dumped entire document chunks  
**After:** Returns 1-4 sentence answers with citations

## Key Changes Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Context Size** | 6000-8000 chars | 1600 chars max |
| **Context Blocks** | 6-12 blocks | 4 blocks max |
| **Max Tokens** | 256-512 | 160 |
| **Temperature** | 0.2 | 0.1 |
| **Sentences** | No limit | 1-4 max |
| **Citations** | Optional | Required on EVERY sentence |
| **Fallback** | 600 chars | 400 chars |
| **Summary Mode** | Special handling | Removed - all same |

## Usage

### Start Server
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### Test in Browser
1. Open `tester.html`
2. Upload a PDF/TXT
3. Ask questions
4. Get SHORT answers (1-4 sentences)

### Example Questions & Expected Answers

**Q: "What is the refund policy?"**  
A: "Refunds are available within 30 days [1]. Original receipt required [2]."

**Q: "What is this document about?"**  
A: "This document outlines company policies for customers [1]."

**Q: "How do I reset my password?"**  
A: "Click 'Forgot Password' and enter your email [1]. You'll receive a reset link within 5 minutes [2]."

## Answer Format
```
[1-4 sentences] + [citations] = Perfect Answer
```

Every sentence MUST have [1], [2], etc.

## What Changed in Code

### `_build_context()`
- Takes `max_blocks=4` and `budget_chars=1600`
- Hard limit: 4 blocks, 1600 chars
- Truncates last block if needed

### `_gemini_answer()`
- Strict prompt: "1-4 sentences, cite everything"
- Generation: 160 tokens max, temp 0.1
- Validation: Checks each sentence for [n]
- Fallback: 400 chars only

### `/ask` endpoint
- `k = min(k, 4)` - max 4 chunks
- `_build_context(hits, max_blocks=4, budget_chars=1600)`
- `strict=True` always

## Environment
```env
GOOGLE_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-flash
```

## Health Check
```bash
curl http://localhost:8000/healthz
# {"ok":true,"message":"healthy"}
```

## Debug Models
```bash
curl http://localhost:8000/debug/models
# Lists available Gemini models
```

## Success Criteria
✅ Answers are 1-4 sentences  
✅ Every sentence has [n] citation  
✅ No content dumps  
✅ Fast responses  
✅ Grounded in document  

## If You See Long Answers
1. Check `GOOGLE_API_KEY` is set correctly
2. Verify `GEMINI_MODEL=gemini-1.5-flash`
3. Check `/debug/models` endpoint
4. Look at server logs for errors

## Files Modified
- `backend/app.py` (3 functions rewritten)

---
**Status: FIXED ✅**  
All queries now return concise, cited answers!
