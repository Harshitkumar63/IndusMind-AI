#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# IndusMind AI — Database Seed Script
# Seeds the database with demo data for development
# ──────────────────────────────────────────────────────────────

set -euo pipefail

echo "🌱 Seeding IndusMind AI database..."

cd backend

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the seed script
python -c "
from app.seed import seed_demo_data
import asyncio

async def main():
    await seed_demo_data()
    print('✅ Demo data seeded successfully!')

asyncio.run(main())
"

echo "Done! Demo data is ready."
