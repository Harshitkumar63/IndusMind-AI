-- IndusMind AI — Initial Database Schema
-- This script creates the database and enables extensions.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE indusmind_db TO indusmind;
