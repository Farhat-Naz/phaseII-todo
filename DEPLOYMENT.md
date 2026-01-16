# Deployment Guide

## Application Deployed Successfully!

**Production URL:** https://phase-ii-todo-9c0x9oz87-farhats-projects-27800a4d.vercel.app

## Quick Setup - Add Environment Variables

Go to Vercel Dashboard and add these environment variables:
https://vercel.com/farhats-projects-27800a4d/phase-ii-todo/settings/environment-variables

Required variables:
- DATABASE_URL (your Neon PostgreSQL connection string)
- SECRET_KEY (JWT secret key)
- ALGORITHM = HS256
- ACCESS_TOKEN_EXPIRE_MINUTES = 30
- CORS_ORIGINS (your Vercel app URL)
- ENV = production
- DEBUG = False

After adding variables, redeploy: vercel --prod

## Test Your App

Health Check:
curl https://phase-ii-todo-9c0x9oz87-farhats-projects-27800a4d.vercel.app/health

App URL:
https://phase-ii-todo-9c0x9oz87-farhats-projects-27800a4d.vercel.app
