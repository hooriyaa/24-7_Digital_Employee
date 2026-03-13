-- ===========================================
-- PostgreSQL Initialization Script
-- ===========================================
-- This script runs automatically when the PostgreSQL container
-- is first initialized. It enables the pgvector extension
-- for vector similarity search.
-- ===========================================

-- Enable pgvector extension for vector embeddings
-- Required for RAG (Retrieval-Augmented Generation) memory
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extension is installed
\dx

-- Create schema for application tables
CREATE SCHEMA IF NOT EXISTS app;

-- Grant permissions
GRANT ALL ON SCHEMA app TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA app TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA app TO postgres;

-- Log success
DO $$
BEGIN
    RAISE NOTICE 'pgvector extension enabled successfully!';
    RAISE NOTICE 'Application schema created!';
END $$;
