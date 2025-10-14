# Testing Guide for Summary Question Improvements

## Quick Start

1. **Start the server** (if not already running):
   ```powershell
   uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the web interface**:
   - Open `tester.html` in your browser
   - URL: `file:///d:/RAG/tester.html`

## Test Scenarios

### Scenario 1: Document Overview Questions ✅

Upload a PDF or TXT file, then try these questions:

1. **"What is this document about?"**
   - Expected: Comprehensive overview of document content
   - Should include: Main topics, purpose, key sections
   - Citations: Optional (natural summary)

2. **"What does this document contain?"**
   - Expected: Detailed list of what's in the document
   - Should cover: All major sections and topics
   - Citations: Optional

3. **"Give me a summary"**
   - Expected: Well-structured summary with bullet points or sections
   - Length: Longer response (up to 1024 tokens)
   - Citations: Optional

4. **"What are the main topics?"**
   - Expected: List of main topics/themes
   - Should be: Organized and comprehensive
   - Citations: Optional

5. **"Tell me about this"**
   - Expected: Natural overview of the document
   - Should feel: Conversational and informative
   - Citations: Optional

### Scenario 2: Specific Questions (Should Still Work) ✅

1. **"What is the refund policy?"**
   - Expected: Specific answer about refunds
   - Must include: Citations like [1], [2]
   - Length: Concise (1-4 sentences)

2. **"How do I reset my password?"**
   - Expected: Specific instructions
   - Must include: Citations
   - Length: Concise

3. **"What are the business hours?"**
   - Expected: Specific hours
   - Must include: Citations
   - Length: Concise

### Scenario 3: Edge Cases ✅

1. **Very short query: "about"**
   - Should be detected as summary question
   - Should expand with synonyms

2. **Typo in summary: "sumary of document"**
   - Should still be detected and corrected

3. **Mixed query: "What is this about and what's the refund policy?"**
   - Should handle as summary question
   - Should cover both aspects

## What to Look For

### ✅ Good Summary Response:
- Comprehensive coverage of document
- Well-organized (sections, bullet points, or logical flow)
- 200-1000 tokens long
- Natural language (doesn't force citations)
- Covers main purpose, topics, and key points
- Based ONLY on document content

### ✅ Good Specific Response:
- Direct answer to the question
- 1-4 sentences typically
- Contains citations: [1], [2], etc.
- Grounded in document
- Concise and to-the-point

### ❌ Bad Response:
- "I don't know based on the provided document" (when answer should be available)
- Made-up information not in the document
- Too short for summary questions
- Missing citations for specific questions

## Behind the Scenes

### For Summary Questions:
- **Chunks Retrieved**: 12 (instead of 6)
- **Context Budget**: 8000 characters (instead of 6000)
- **Max Tokens**: 1024 (instead of 256)
- **Temperature**: 0.2 (slightly creative)
- **Citation Requirement**: Optional
- **Overlap Threshold**: 30% (lenient)

### For Specific Questions:
- **Chunks Retrieved**: 6 (default)
- **Context Budget**: 6000 characters
- **Max Tokens**: 256 (concise)
- **Temperature**: 0.2
- **Citation Requirement**: Required
- **Overlap Threshold**: 30% (strict)

## Sample Test Documents

### Good Test Documents:
- Company policy documents (HR, refunds, support)
- Product manuals
- Research papers
- Terms of service
- FAQs

### Test Questions by Document Type:

**HR Policy Document:**
- Summary: "What does this HR policy cover?"
- Specific: "How many vacation days do employees get?"

**Product Manual:**
- Summary: "What is this product and what can it do?"
- Specific: "How do I clean the device?"

**Research Paper:**
- Summary: "What is this research about?"
- Specific: "What methodology was used?"

## Troubleshooting

### Issue: Summary too short
- Check: Is question detected as summary? (Look at server logs)
- Fix: Use more explicit keywords like "summary", "overview", "about"

### Issue: "I don't know" for valid question
- Check: Is document properly uploaded and chunked?
- Check: Content overlap (may need to adjust threshold)
- Try: Rephrasing the question

### Issue: Made-up information
- This should NOT happen - strict grounding is enforced
- If it does: Report as bug

## Success Criteria

✅ All summary questions return comprehensive answers  
✅ All specific questions return concise, cited answers  
✅ No hallucination (all answers from document)  
✅ Natural language in summaries  
✅ Proper structure and organization  
✅ Fast response time (< 5 seconds)  

## Next Steps After Testing

1. Collect feedback on answer quality
2. Adjust thresholds if needed (in `backend/app.py`)
3. Add more synonym expansions if certain queries fail
4. Consider adding document type detection for specialized prompts
