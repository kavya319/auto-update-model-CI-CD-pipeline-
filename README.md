# 🤖 CI/CD ML Auto-Update Pipeline

An automated machine learning pipeline that monitors incoming user data, automatically retrains models when sufficient data is collected, and deploys improved models through GitHub Actions.

## 🎯 Overview

This project demonstrates a complete CI/CD pipeline for machine learning that:

- ✅ **Monitors Data**: Tracks new user datasets continuously
- 🔄 **Auto-Trains**: Triggers model training when 200+ new datasets arrive
- 📊 **Compares Performance**: Evaluates new models against production versions
- 🚀 **Auto-Deploys**: Creates and merges PRs for improved models
- 🔐 **Fully Automated**: No manual intervention required

## 🏗️ Architecture

```
┌─────────────────┐
│  New User Data  │
│   (CSV Files)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Data Counter   │◄─────┤  Hourly Cron Job │
│  (JSON Track)   │      │  (check-data.yml)│
└────────┬────────┘      └──────────────────┘
         │
         │ Count >= 200?
         ▼
┌─────────────────┐
│  Train New      │
│  Model Version  │
│  (train.py)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Compare with   │
│  Current Model  │
│  (R² Score)     │
└────────┬────────┘
         │
         │ Improved?
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Create PR      │─────►│   Auto-Approve   │
│  (auto-train)   │      │   & Merge        │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  New Model       │
                         │  in Production!  │
                         └──────────────────┘
```

## 📁 Project Structure

```
ci-cd ml project/
├── .github/
│   └── workflows/
│       ├── check-data.yml      # Hourly data monitoring
│       ├── auto-train.yml      # Training & PR creation
│       └── auto-merge.yml      # Auto-approve & merge
├── data/
│   ├── new_data/               # Incoming user datasets (CSV)
│   └── new_data_counter.json   # Tracking counter
├── model/
│   ├── v1.pkl                  # Current production model
│   ├── v2.pkl                  # Next version (after training)
│   └── model_metadata.json     # Version history & metrics
├── src/
│   ├── config.py               # Configuration constants
│   ├── data_manager.py         # Data loading & tracking
│   ├── add_data.py             # Utility to add datasets
│   ├── train.py                # Training & comparison logic
│   └── main.py                 # FastAPI service
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- Git
- GitHub repository
- GitHub Personal Access Token

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd "ci-cd ml project"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure GitHub Secrets

You need to create a GitHub Personal Access Token (PAT) for automated workflows:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Action workflows)
4. Generate and copy the token
5. In your repository: Settings → Secrets and variables → Actions → New repository secret
   - Name: `PAT_TOKEN`
   - Value: [paste your token]

### 4. Enable Auto-Merge in Repository Settings

1. Go to your repository Settings → General
2. Scroll down to "Pull Requests"
3. ✅ Enable "Allow auto-merge"

## 💡 How It Works

### Adding New Data

Simulate adding user data:

```bash
# Add single dataset
cd src
python add_data.py 5  # Adds 5 datasets

# Add many datasets for testing
python add_data.py 220  # Adds 220 datasets
```

Each dataset is saved as a CSV file in `data/new_data/` and increments the counter.

### Automated Workflow

1. **Data Monitoring** (`check-data.yml`)
   - Runs every hour via cron schedule
   - Checks if `data/new_data_counter.json` shows count >= 200
   - If yes, triggers the training workflow

2. **Model Training** (`auto-train.yml`)
   - Loads all new data from `data/new_data/`
   - Trains new model version (e.g., v2)
   - Compares R² score with current model (v1)
   - If improved:
     - Saves new model
     - Creates a branch
     - Commits model files
     - Opens a PR with performance metrics
     - Enables auto-merge
   - If not improved:
     - Discards new model
     - No PR created

3. **Auto-Approval** (`auto-merge.yml`)
   - Automatically approves PRs labeled "model-update"
   - Adds comment with approval details
   - PR merges automatically when checks pass

### Manual Testing

You can manually trigger workflows:

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select a workflow (e.g., "Check New Data and Trigger Training")
4. Click "Run workflow"

## 📊 Monitoring

### Check Data Status

```bash
cd src
python -c "from add_data import check_status; check_status()"
```

### View Model Metadata

```bash
cat model/model_metadata.json
```

This shows all trained model versions with their accuracy scores and timestamps.

## 🧪 Testing Locally

### Test Data Management

```bash
cd src
python data_manager.py
```

### Test Training Pipeline

```bash
# Add test data
python add_data.py 220

# Run training
python train.py
```

### Test FastAPI Service

```bash
uvicorn src.main:app --reload

# In another terminal
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 5}'
```

## 🔧 Configuration

Edit `src/config.py` to change:

- `NEW_DATA_THRESHOLD`: Number of datasets required for training (default: 200)
- `TEST_SIZE`: Train/test split ratio (default: 0.2)
- Directory paths

## 📈 Performance Metrics

Models are compared using:
- **R² Score**: Coefficient of determination (0-1)
- **Accuracy**: R² × 100 for percentage representation
- **MSE**: Mean squared error (lower is better)

A new model is deployed only if its R² score exceeds the current production model.

## 🎬 Complete Demo Workflow

```bash
# 1. Start with clean state
rm -rf data/new_data/*.csv

# 2. Add 220 simulated datasets
cd src
python add_data.py 220

# 3. Check status
python -c "from add_data import check_status; check_status()"

# 4. Manually trigger GitHub Actions workflow
# (Go to GitHub Actions → "Check New Data" → "Run workflow")

# 5. Watch the automation:
#    - Training runs
#    - PR is created
#    - PR is auto-approved
#    - PR is merged
#    - New model is in production!
```

## 🛡️ Security Notes

- **PAT Token**: Keep your Personal Access Token secure. Never commit it to the repository.
- **Auto-Merge**: In production, consider adding required reviewers or status checks before auto-merge.
- **Data Validation**: Add data quality checks before training in production environments.

## 🤝 Contributing

To add features or fix bugs:

1. Create a feature branch
2. Make changes
3. Test locally
4. Submit a PR (manual review required for non-model updates)

## 📝 License

This is a demo project for educational purposes.

## 🙋 Troubleshooting

### Workflow not triggering?

- Check that `PAT_TOKEN` secret is set correctly
- Ensure "Allow auto-merge" is enabled in repository settings
- Verify cron syntax in `check-data.yml`

### PR not auto-merging?

- Ensure branch protection rules allow auto-merge
- Check that all required checks are passing
- Verify the PR has the "model-update" label

### Import errors locally?

- Run from the project root directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Built with ❤️ using GitHub Actions, Python, and scikit-learn**
