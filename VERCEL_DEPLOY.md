# 🚀 Deploy HyperCast to Vercel - Quick Guide

## ⚡ Quick Deploy (5 minutes)

### Step 1: Go to Vercel
Visit: **https://vercel.com/new**

### Step 2: Import from GitHub
1. Click **"Import Project"**
2. Select **"Import Git Repository"**
3. Choose: `codekshitij/HyperCast`
4. Click **"Import"**

### Step 3: Configure Build Settings
```
Framework Preset: Other
Root Directory: frontend
Build Command: (leave empty)
Output Directory: (leave empty)
Install Command: (leave empty)
```

### Step 4: Deploy!
- Click **"Deploy"**
- Wait 1-2 minutes ⏱️
- Your site is live! 🎉

---

## 🌐 Your Live URL

After deployment, you'll get a URL like:
```
https://hypercast-xxx.vercel.app
```

---

## 🔧 After Deployment

### 1. Test Your Site
Visit your Vercel URL and check:
- ✅ UI loads correctly
- ✅ Animations work
- ✅ Search bar functional
- ✅ PWA installable

### 2. Note About API
Currently, the API calls will fail because the backend isn't deployed yet. The frontend will show an error when trying to fetch weather data.

**Two options:**

**Option A: Use Local API (Development)**
```javascript
// In script.js, it auto-detects:
// localhost → http://localhost:8000
// production → https://your-api-url.com
```

**Option B: Deploy Backend API**
Follow [DEPLOYMENT.md](DEPLOYMENT.md) to deploy the API to Railway/Render.

---

## 🎨 What's Deployed

Your Vercel deployment includes:
- ✨ Premium UI with glassmorphism
- 🌈 Animated background with particles
- 📱 Progressive Web App (PWA)
- 🎯 Responsive design
- ⚡ Fast loading
- 💫 Smooth animations

---

## 🔄 Auto-Deployment

Every time you push to GitHub:
- Changes are automatically deployed
- No manual action needed
- Vercel rebuilds in ~1 minute

```bash
# Make changes
git add .
git commit -m "Update UI"
git push origin main
# Vercel auto-deploys! 🚀
```

---

## 🌟 Custom Domain (Optional)

### Add Your Domain

1. **Vercel Dashboard** → Your Project
2. **Settings** → **Domains**
3. **Add Domain**: `yourdomain.com`
4. **Follow DNS instructions**

Example:
```
hypercast.com → Your site
www.hypercast.com → Redirects to main
```

---

## 📊 Preview Deployments

Create a pull request on GitHub:
- Vercel creates a preview URL
- Test changes before merging
- Share with team for review

---

## 🐛 Troubleshooting

### Problem: Blank Page
**Solution**: Check browser console for errors

### Problem: 404 Not Found
**Solution**: Verify `frontend/` directory structure

### Problem: API Calls Failing
**Solution**: Normal! Deploy backend API separately

### Problem: PWA Not Installing
**Solution**: Clear cache and reload

---

## 💡 Pro Tips

1. **Enable Analytics**
   - Vercel Dashboard → Analytics
   - Track visitors and performance

2. **Preview Deployments**
   - Every PR gets its own URL
   - Perfect for testing

3. **Environment Variables**
   - Add in Vercel Dashboard
   - Settings → Environment Variables

4. **Custom 404 Page**
   - Create `frontend/404.html`
   - Auto-served on 404 errors

---

## 🎯 Success Checklist

After deployment, verify:
- [ ] Site loads at Vercel URL
- [ ] UI looks correct
- [ ] Animations working
- [ ] Mobile responsive
- [ ] PWA badge shows (install prompt)
- [ ] No console errors (except API calls)

---

## 📱 Share Your Deployment

Share your live site:
```
🌦️ Check out HyperCast!
https://hypercast-xxx.vercel.app

Built with LSTM AI + NOAA Data
```

---

## 🚀 Next Steps

1. ✅ Frontend deployed on Vercel
2. ⏳ Deploy API backend (Railway/Render)
3. 🔗 Update API URL in `script.js`
4. 🌟 Add custom domain (optional)
5. 📊 Enable analytics (optional)

---

**That's it! Your weather app is live! 🎉**

Visit: **https://vercel.com/dashboard** to manage your deployment

