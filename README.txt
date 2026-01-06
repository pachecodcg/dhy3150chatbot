# DHYG 3150 Course Chatbot - Complete Package

## 📁 Folder Structure

```
chatbot-complete/
├── backend/                          # Backend API (Flask + Claude)
│   ├── app.py                       # Smart backend with selective chapter loading
│   ├── requirements.txt             # Python dependencies
│   ├── instructions.txt             # Chatbot behavior and pedagogy
│   └── knowledge_base/              # Course materials folder
│       └── README-DELETE-ME.txt     # Placeholder (replace with your files)
│
├── docs/                            # Frontend website (HTML + JS)
│   └── index.html                   # Beautiful AU-designed interface
│
└── README.txt                       # This file
```

---

## 🚀 UPLOAD TO GITHUB - STEP BY STEP

### Step 1: Create Fresh Repository (Or Use Existing)

**Option A: Start Fresh**
1. Go to github.com
2. Click "New repository"
3. Name: `dhy3150chatbot`
4. Public or Private (your choice)
5. Don't initialize with anything
6. Click "Create repository"

**Option B: Use Your Existing Repository**
1. Go to: github.com/pachecodcg/dhy3150chatbot
2. Delete all current files (you're starting fresh)

---

### Step 2: Upload Backend Files

**Upload these files to the `backend/` folder:**

1. Go to your repository
2. Click "Add file" → "Create new file"
3. In the filename box, type: `backend/app.py`
4. Copy the entire contents of `backend/app.py` from this package
5. Paste it
6. Scroll down, click "Commit new file"

**Repeat for:**
- `backend/requirements.txt`
- `backend/instructions.txt`

---

### Step 3: Upload Your Course Materials

1. In your repo, navigate to create: `backend/knowledge_base/`
2. Delete the `README-DELETE-ME.txt` placeholder
3. Upload YOUR files:
   - ✅ Your actual course syllabus (.txt file)
   - ✅ Your lecture notes (.txt or .md files)
   - ✅ Phillips textbook chapters (if you have them split into 20 files)

**Important:** Keep these files small!
- Syllabus: Under 50 KB is best
- Each lecture: Under 100 KB
- Phillips chapters: Already split properly (50-175 KB each)

---

### Step 4: Upload Frontend File

1. In your repo, click "Add file" → "Create new file"
2. In the filename box, type: `docs/index.html`
3. Copy the entire contents of `docs/index.html` from this package
4. Paste it
5. **IMPORTANT:** The file already has the correct API URL (`https://dhy3150chatbot.vercel.app`)
6. If your Vercel URL is different, change line ~390:
   ```javascript
   const API_URL = 'https://YOUR-PROJECT.vercel.app';
   ```
7. Commit the file

---

## ⚙️ DEPLOY TO VERCEL

### Step 1: Sign Up / Login to Vercel

1. Go to: vercel.com
2. Sign up with your GitHub account (or login)

### Step 2: Import Project

1. Click "Add New..." → "Project"
2. Import your `dhy3150chatbot` repository
3. **CRITICAL SETTING:**
   - Root Directory: `backend`
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

### Step 3: Add Environment Variable

1. Before deploying, click "Environment Variables"
2. Add variable:
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your Claude API key (starts with `sk-ant-api03-...`)
   - Environment: All (Production, Preview, Development)
3. Click "Add"

### Step 4: Deploy

1. Click "Deploy"
2. Wait 2-3 minutes
3. You'll get a URL like: `https://dhy3150chatbot.vercel.app`
4. **Save this URL!**

---

## 🌐 SETUP GITHUB PAGES

### Step 1: Enable GitHub Pages

1. In your repo, go to Settings
2. Scroll to "Pages" in left sidebar
3. Under "Source":
   - Branch: `main`
   - Folder: `/docs`
4. Click "Save"
5. Wait 2-3 minutes

### Step 2: Get Your URL

Your chatbot will be live at:
```
https://yourusername.github.io/dhy3150chatbot/
```

---

## ✅ VERIFICATION CHECKLIST

After uploading everything:

**GitHub Structure:**
```
your-repo/
├── backend/
│   ├── app.py ✅
│   ├── requirements.txt ✅
│   ├── instructions.txt ✅
│   └── knowledge_base/
│       ├── your-syllabus.txt ✅
│       ├── lecture-notes.txt ✅
│       └── Phillips_Ch##_*.txt ✅ (if using textbook)
└── docs/
    └── index.html ✅
```

**Vercel:**
- ✅ Project deployed
- ✅ Environment variable `ANTHROPIC_API_KEY` set
- ✅ Root directory set to `backend`
- ✅ Backend URL working

**GitHub Pages:**
- ✅ Enabled on `/docs` folder
- ✅ Website accessible

---

## 🧪 TESTING

### Test 1: Backend Health Check

Visit: `https://your-project.vercel.app/health`

Should see: `{"status":"ok"}`

### Test 2: Frontend Connection

1. Visit your GitHub Pages URL
2. Should see the chatbot interface
3. Status should say "Connected" (not "Offline")

### Test 3: Ask a Question

Try: "When is the first lecture?"

Should get a response from your syllabus!

### Test 4: Phillips Textbook (If Uploaded)

Try: "Explain composite polymerization"

Should get detailed response citing Phillips Chapter 5!

---

## 🔧 TROUBLESHOOTING

### Issue: "Offline" Status

**Fix:** Check that `API_URL` in `docs/index.html` matches your Vercel URL

### Issue: Rate Limit Error 429

**Fix:** 
- Your files are too large
- Remove Phillips chapters temporarily
- Test with just syllabus
- Verify backend is the SMART version (should have `get_relevant_chapters` function)

### Issue: "API key not configured"

**Fix:**
- Add `ANTHROPIC_API_KEY` in Vercel environment variables
- Redeploy the project

### Issue: No Response

**Fix:**
- Check Vercel deployment logs
- Verify `backend/knowledge_base/` has your files
- Make sure API key is valid

---

## 📚 ADDING PHILLIPS TEXTBOOK CHAPTERS

If you want to add the Phillips textbook:

1. You should have 20 files named:
   - `Phillips_Ch01_Overview_Dental_Materials.txt`
   - `Phillips_Ch02_Structure_Matter.txt`
   - ... (through Ch20)

2. Upload ALL 20 files to: `backend/knowledge_base/`

3. The smart backend will automatically:
   - Only load relevant chapters per question
   - Keep requests under rate limits
   - Cite specific chapters in responses

---

## 💰 COST

- GitHub: FREE
- GitHub Pages: FREE
- Vercel: FREE tier (sufficient for this)
- Claude API: ~$10-30 per semester (depending on usage)

---

## 🎯 KEY FEATURES

✅ **Smart Backend**
- Loads only relevant Phillips chapters
- Avoids rate limits
- Fast responses

✅ **Beautiful Interface**
- Augusta University colors
- Clean, professional design
- Mobile responsive

✅ **Pedagogical Approach**
- Teaches concepts, doesn't just answer
- Encourages critical thinking
- Cites sources properly

✅ **Academic Integrity**
- Helps students understand
- Doesn't complete assignments
- Guides learning process

---

## 📞 SUPPORT

If students have issues:
1. Check if they're on the correct URL
2. Verify backend is deployed
3. Check Vercel logs for errors
4. Ensure API key has credits

---

## 🎉 YOU'RE DONE!

Once everything is uploaded:
1. Share the GitHub Pages URL with students
2. Monitor usage in Claude console
3. Add more lecture content as semester progresses

**Your chatbot is live and ready to help students learn!**
