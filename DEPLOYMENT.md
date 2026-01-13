# Vercel Deployment Guide

Complete guide to deploy the Todo application to Vercel.

## Prerequisites

- GitHub account with the repository: https://github.com/Farhat-Naz/phaseII-todo
- Vercel account (sign up at https://vercel.com)
- Neon PostgreSQL database (already configured)

## Step 1: Import Project to Vercel

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository: `Farhat-Naz/phaseII-todo`
4. Select the repository and click "Import"

## Step 2: Configure Project Settings

### Root Directory
- Set "Root Directory" to: `frontend`
- Framework Preset: Next.js (auto-detected)
- Build Command: `npm run build` (default)
- Output Directory: `.next` (default)

## Step 3: Configure Environment Variables

Add these environment variables in Vercel project settings:

### Required Environment Variables:

```bash
# Backend API URL (you'll update this after backend deployment)
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app

# Better Auth Configuration
BETTER_AUTH_SECRET=b105763e0336368cc580d447338bbbc78f38c3faa24451d561398ca0983e9b64
BETTER_AUTH_URL=https://your-vercel-app.vercel.app

# Cookie Configuration
NEXT_PUBLIC_COOKIE_DOMAIN=.vercel.app
NEXT_PUBLIC_SECURE_COOKIES=true
NEXT_PUBLIC_COOKIE_SAMESITE=lax
NEXT_PUBLIC_COOKIE_PATH=/
NEXT_PUBLIC_ACCESS_TOKEN_COOKIE=access_token
NEXT_PUBLIC_REFRESH_TOKEN_COOKIE=refresh_token

# Application Configuration
NEXT_PUBLIC_APP_NAME=TodoApp
NEXT_PUBLIC_APP_URL=https://your-vercel-app.vercel.app
```

### How to Add Environment Variables:

1. In Vercel dashboard, go to your project
2. Click "Settings" → "Environment Variables"
3. Add each variable above:
   - Variable Name: (e.g., `NEXT_PUBLIC_API_URL`)
   - Value: (paste the value)
   - Environment: Select "Production", "Preview", and "Development"
4. Click "Save"

## Step 4: Deploy Backend (Optional - For API)

### Option A: Deploy Backend to Vercel (Serverless)

1. Create a new Vercel project for backend
2. Set "Root Directory" to: `backend`
3. Add environment variables:

```bash
# Database
DATABASE_URL=postgresql+psycopg://neondb_owner:npg_ZAGN4xaUk2mh@ep-red-unit-a13i3o3z-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Application
ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=8000

# JWT Authentication
SECRET_KEY=b105763e0336368cc580d447338bbbc78f38c3faa24451d561398ca0983e9b64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings (update with your Vercel frontend URL)
CORS_ORIGINS=https://your-vercel-app.vercel.app
CORS_ALLOW_CREDENTIALS=True

# Security
CSP_ENABLED=True
HTTPS_REDIRECT=True

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### Option B: Deploy Backend to Railway/Render

If you prefer a traditional server:

1. Go to https://railway.app or https://render.com
2. Create new Python Web Service
3. Connect your GitHub repository
4. Set "Root Directory" to: `backend`
5. Add all environment variables listed above
6. Deploy

## Step 5: Update Frontend Environment Variables

After backend is deployed:

1. Copy your backend URL (e.g., `https://your-backend.vercel.app`)
2. Go to Vercel frontend project → Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` with your backend URL
4. Redeploy frontend (Vercel will auto-redeploy on changes)

## Step 6: Verify Deployment

### Frontend Checks:
1. Visit your Vercel app URL
2. Register a new user
3. Login with credentials
4. Try creating/editing/deleting todos

### Backend Checks:
1. Visit `https://your-backend-url.vercel.app/docs`
2. API documentation should load
3. Test `/api/auth/register` and `/api/auth/login` endpoints

### Database Checks:
1. Login to https://console.neon.tech/
2. Go to your project
3. Check "Tables" tab
4. Verify `user` and `todo` tables have data

## Troubleshooting

### Issue: "API connection failed"
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify backend is deployed and running
- Check CORS settings in backend `.env`

### Issue: "Authentication not working"
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check `SECRET_KEY` in backend environment variables
- Ensure cookies are enabled in browser

### Issue: "Database connection error"
- Verify `DATABASE_URL` is correct
- Check Neon database is active
- Ensure connection pooler is used (pooler endpoint)

### Issue: "Build failed on Vercel"
- Check build logs in Vercel dashboard
- Verify all dependencies are in `package.json`
- Ensure TypeScript types are correct

## Post-Deployment Configuration

### Custom Domain (Optional):
1. Vercel → Project → Settings → Domains
2. Add your custom domain
3. Update environment variables with new domain:
   - `BETTER_AUTH_URL`
   - `NEXT_PUBLIC_APP_URL`
   - Backend `CORS_ORIGINS`

### Enable Analytics:
1. Vercel → Project → Analytics
2. Enable Web Analytics
3. Monitor performance and errors

## Security Checklist

- [ ] All environment variables are set correctly
- [ ] `BETTER_AUTH_SECRET` is secure and unique
- [ ] Database credentials are not exposed in code
- [ ] HTTPS is enabled (`NEXT_PUBLIC_SECURE_COOKIES=true`)
- [ ] CORS is configured correctly (only your frontend domain)
- [ ] Rate limiting is enabled in backend
- [ ] `.env` files are in `.gitignore`

## Quick Deploy Commands

```bash
# Commit and push changes
git add .
git commit -m "Configure Vercel deployment"
git push origin 006-high-priority

# Vercel will auto-deploy on push to connected branch
```

## Manual Deployment (using Vercel CLI)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy frontend
cd frontend
vercel --prod

# Deploy backend (if using Vercel for backend)
cd ../backend
vercel --prod
```

## Support

- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/docs/deployment
- Neon Docs: https://neon.tech/docs

---

**Deployment Status:**
- ✅ GitHub: https://github.com/Farhat-Naz/phaseII-todo
- ⏳ Frontend: Pending Vercel setup
- ⏳ Backend: Pending deployment
- ✅ Database: Neon PostgreSQL configured
