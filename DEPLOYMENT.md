# HyperCast Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites
- GitHub account
- Vercel account (sign up at https://vercel.com)
- Code pushed to GitHub repository

---

## 📱 Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `codekshitij/HyperCast`
   - Click "Import"

3. **Configure Project**
   ```
   Framework Preset: Other
   Root Directory: frontend
   Build Command: (leave empty)
   Output Directory: (leave empty)
   Install Command: (leave empty)
   ```

4. **Environment Variables** (Optional)
   ```
   API_BASE_URL=https://your-api-domain.com
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes for deployment
   - Your site will be live at: `https://hypercast-xxx.vercel.app`

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to project
cd /Users/kshitijmishra/weatherApp

# Deploy
vercel --prod

# Follow the prompts:
# - Set up and deploy: Y
# - Scope: Your account
# - Link to existing project: N
# - Project name: hypercast
# - Directory: ./frontend
# - Override settings: N
```

---

## 🔧 API Configuration

### Update API URL in Frontend

After deploying the API, update the API URL in `frontend/script.js`:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://your-api-domain.com';  // ← Update this
```

Then commit and push:
```bash
git add frontend/script.js
git commit -m "Update API URL for production"
git push origin main
```

Vercel will automatically redeploy!

---

## 🌐 Backend API Deployment Options

### Option 1: Railway (Recommended for Python/ML)

1. **Visit**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select**: `codekshitij/HyperCast`
4. **Root Directory**: `services/api`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   ```
   PYTHON_VERSION=3.13
   PORT=8000
   ```

### Option 2: Render

1. **Visit**: https://render.com
2. **New** → **Web Service**
3. **Connect** GitHub repository
4. **Settings**:
   ```
   Name: hypercast-api
   Environment: Python 3
   Build Command: pip install -r services/api/requirements.txt
   Start Command: cd services/api && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
cd services/api
flyctl launch --name hypercast-api

# Deploy
flyctl deploy
```

### Option 4: Heroku

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create hypercast-api

# Add buildpack
heroku buildpacks:set heroku/python

# Create Procfile
echo "web: cd services/api && uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

---

## 📋 Post-Deployment Checklist

### Frontend (Vercel)
- [ ] Deployed successfully
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled (automatic)
- [ ] PWA working offline
- [ ] Animations loading correctly
- [ ] API URL updated

### Backend API
- [ ] API deployed and accessible
- [ ] Health endpoint responding: `/health`
- [ ] Forecast endpoint working: `/forecast`
- [ ] CORS configured for Vercel domain
- [ ] Model loaded successfully
- [ ] Environment variables set

### DNS & Domain (Optional)
- [ ] Custom domain purchased
- [ ] DNS configured
- [ ] SSL certificate active
- [ ] www redirect setup

---

## 🔐 Security Checklist

- [ ] API keys in environment variables (not code)
- [ ] CORS restricted to your domain
- [ ] HTTPS enforced
- [ ] Service worker secure
- [ ] No sensitive data in frontend

---

## 🎯 Testing Production Deployment

### Test Frontend
```bash
# Visit your Vercel URL
open https://hypercast-xxx.vercel.app

# Check console for errors
# Test search functionality
# Verify API calls
```

### Test API
```bash
# Health check
curl https://your-api-domain.com/health

# Forecast check
curl "https://your-api-domain.com/forecast?lat=33.749&lon=-84.388"
```

---

## 🔄 Continuous Deployment

### Automatic Deployments

Once connected to GitHub:

**Frontend (Vercel)**
- Push to `main` → Auto-deploy frontend
- Pull requests → Preview deployments
- Rollback available from dashboard

**Backend (Railway/Render)**
- Push to `main` → Auto-deploy API
- Environment variables in dashboard
- Logs available for debugging

---

## 📊 Monitoring

### Vercel Analytics
- Enable in Vercel dashboard
- Track page views, performance
- Real user monitoring

### API Monitoring
- Use Railway/Render dashboards
- Set up alerts for downtime
- Monitor response times

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem**: Blank page
```bash
# Check browser console
# Verify API URL is correct
# Check network tab for failed requests
```

**Problem**: API calls failing
```bash
# Verify CORS settings in API
# Check API is deployed and running
# Update API_BASE_URL in script.js
```

**Problem**: PWA not working
```bash
# Clear browser cache
# Re-register service worker
# Check sw.js is accessible
```

### Backend Issues

**Problem**: Model not loading
```bash
# Check model file is deployed
# Verify file paths are correct
# Check logs for errors
```

**Problem**: CORS errors
```bash
# Add Vercel domain to CORS origins in main.py:
allow_origins=["https://your-vercel-app.vercel.app"]
```

**Problem**: Memory issues
```bash
# Increase Railway/Render plan
# Optimize model size
# Use model quantization
```

---

## 🚀 Quick Deploy Commands

### Deploy Frontend to Vercel
```bash
cd /Users/kshitijmishra/weatherApp
vercel --prod
```

### Update After Changes
```bash
# Make changes
git add .
git commit -m "Update message"
git push origin main
# Vercel auto-deploys!
```

---

## 🌟 Custom Domain Setup

### Add Custom Domain to Vercel

1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Domains
4. Add your domain: `hypercast.com`
5. Add DNS records as shown:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

---

## 💰 Cost Estimate

### Free Tier (Hobby)
- **Vercel**: Free (100GB bandwidth/month)
- **Railway**: $5/month credit
- **Render**: Free tier available
- **Total**: $0-5/month

### Production Tier
- **Vercel Pro**: $20/month
- **Railway**: ~$20/month (with usage)
- **Domain**: ~$12/year
- **Total**: ~$40/month

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Frontend loads at Vercel URL
- ✅ Animations and UI work perfectly
- ✅ API calls return predictions
- ✅ PWA installs on mobile
- ✅ Works offline (cached data)
- ✅ Fast load times (<2s)

---

**Need help?** Open an issue on GitHub!

**Project**: https://github.com/codekshitij/HyperCast

