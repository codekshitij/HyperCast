# Vercel Deployment - Quick Reference

## 🚀 One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/codekshitij/HyperCast)

---

## ⚡ Manual Deploy Steps

### 1. Visit Vercel
```
https://vercel.com/new
```

### 2. Import Settings
```
Repository: codekshitij/HyperCast
Root Directory: frontend
Framework: Other
Build Command: (empty)
Output Directory: (empty)
```

### 3. Deploy!
Click "Deploy" button - Done in 90 seconds!

---

## 🔧 Configuration

### Vercel Settings (Already Configured)
- ✅ `vercel.json` - Routing and headers
- ✅ `.vercelignore` - Exclude backend
- ✅ Security headers - XSS, CSP
- ✅ PWA support - Service worker

### Environment Variables (Optional)
```
Name: API_BASE_URL
Value: https://your-api-domain.com
```

---

## 📱 What Gets Deployed

```
frontend/
├── index.html              → Main page
├── script.js               → App logic (with API auto-detect)
├── styles-enhanced.css     → Premium UI
├── sw.js                   → Service worker
├── manifest.json           → PWA config
└── vercel.json            → Deployment config
```

---

## 🌐 After Deployment

### Your Live URL
```
https://hypercast-xxx.vercel.app
```

### Test Checklist
- [ ] Page loads
- [ ] Animations work
- [ ] UI looks correct
- [ ] PWA installable
- [ ] Mobile responsive
- [ ] No console errors (except API)

---

## 🔄 Auto-Deploy

Every push to GitHub main branch:
```bash
git push origin main
# ↓ Triggers automatic Vercel deployment
# ↓ Live in ~60 seconds
# ✅ Done!
```

---

## 🐛 Common Issues

### Issue: 404 Not Found
**Fix**: Set root directory to `frontend`

### Issue: API Calls Failing
**Fix**: Normal! Deploy backend separately or run locally

### Issue: Blank Page
**Fix**: Check browser console for errors

---

## 📊 Vercel Dashboard

Access your deployment:
```
https://vercel.com/dashboard
```

Features:
- Real-time logs
- Analytics
- Custom domains
- Environment variables
- Preview deployments

---

## 💰 Cost

**Free Tier** (Hobby):
- 100GB bandwidth/month
- Unlimited projects
- HTTPS included
- Perfect for this project!

---

## 🎯 Next Steps

1. ✅ Deploy frontend to Vercel
2. ⏳ Deploy API to Railway/Render
3. 🔗 Update API URL in script.js
4. 🌟 Add custom domain (optional)

---

**Need Help?** See full guide: `VERCEL_DEPLOY.md`

