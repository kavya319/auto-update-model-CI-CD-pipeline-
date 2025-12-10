# GitHub Setup Guide for CI/CD ML Pipeline

## Quick Setup (5 minutes)

Follow these steps to deploy your automated ML pipeline to GitHub.

## Step 1: Create GitHub Personal Access Token

1. Go to GitHub.com → Click your profile picture → Settings
2. Scroll to bottom → Click "Developer settings"
3. Click "Personal access tokens" → "Tokens (classic)"
4. Click "Generate new token (classic)"
5. Give it a name: `ML Pipeline Auto-Merge`
6. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
7. Click "Generate token" at bottom
8. **COPY THE TOKEN** (you won't see it again!)

## Step 2: Push Code to GitHub

```bash
cd "c:\Users\DELL\OneDrive\Desktop\ci-cd ml project"

# Initialize git (if not already done)
git init
git add .
git commit -m "Add CI/CD ML auto-update pipeline"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 3: Add Secret to GitHub Repository

1. Go to your repository on GitHub.com
2. Click "Settings" tab
3. In left sidebar → "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `PAT_TOKEN`
6. Value: [Paste the token you copied in Step 1]
7. Click "Add secret"

## Step 4: Enable Auto-Merge

1. Still in your repository Settings
2. Scroll down to "Pull Requests" section
3. ✅ Check "Allow auto-merge"
4. Click "Save" (if there's a save button)

## Step 5: Test the Pipeline!

### Option A: Manually Trigger Workflow

1. Go to "Actions" tab in your repository
2. Click "Check New Data and Trigger Training" workflow
3. Click "Run workflow" dropdown → Click green "Run workflow" button
4. Watch it run!

### Option B: Add Data and Wait

```bash
# Add 220 test datasets
python src/add_data.py 220

# The hourly cron job will automatically detect and trigger training
# Or manually trigger from GitHub Actions
```

## Verification Checklist

After setup, verify:

- [ ] Repository has all files pushed
- [ ] `PAT_TOKEN` secret is added
- [ ] Auto-merge is enabled in settings
- [ ] Can see 3 workflows in Actions tab:
  - Check New Data and Trigger Training
  - Auto Train and Create PR
  - Auto-Approve and Merge Model Updates

## Troubleshooting

### "Workflow not found"
- Make sure you pushed the `.github/workflows/` directory
- Check that workflow files are in the correct location

### "Secret PAT_TOKEN not set"
- Go back to Step 3 and add the secret
- Make sure the name is exactly `PAT_TOKEN` (case-sensitive)

### "Auto-merge failed"
- Check that auto-merge is enabled (Step 4)
- Verify your PAT token has `workflow` scope

### "Permission denied"
- Your PAT token might have expired or wrong scopes
- Create a new token with `repo` and `workflow` scopes

## What Happens Next?

Once set up:
1. Every hour, GitHub Actions checks for new data
2. When 200+ datasets exist, training starts automatically
3. If new model is better, a PR is created
4. PR is auto-approved and merged
5. New model goes to production!

## Testing Locally First

Before pushing to GitHub, you can test locally:

```bash
# Test adding data
python src/add_data.py 50

# Check status
python -c "from src.add_data import check_status; check_status()"

# Test training (need 200+ datasets)
python src/add_data.py 200
python src/train.py
```

---

**You're all set! 🚀**

The pipeline is now fully automated. Just commit new data, and the system handles the rest.
