-- PortfolioAI Database Schema
-- Run this script in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- TABLES
-- ========================================

-- Users table (extends Supabase Auth)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_login TIMESTAMPTZ,
  subdomain TEXT UNIQUE, -- e.g., "maya-dev"
  preferences JSONB DEFAULT '{}', -- tone presets, pronouns, model selection
  CONSTRAINT valid_subdomain CHECK (subdomain ~* '^[a-z0-9-]+$')
);

-- Profiles (structured career data)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  email TEXT,
  phone TEXT,
  linkedin_url TEXT,
  work_history JSONB, -- [{title, company, dates, bullets}, ...]
  skills JSONB, -- ["React", "Python", "SQL"]
  education JSONB, -- [{degree, institution, year}, ...]
  projects JSONB, -- [{name, description, technologies, links}, ...]
  contact_info JSONB, -- {github, portfolio, location}
  original_resume_text TEXT, -- raw extracted text
  parsing_confidence FLOAT CHECK (parsing_confidence >= 0 AND parsing_confidence <= 1),
  parsing_method TEXT CHECK (parsing_method IN ('pdf', 'linkedin', 'qa')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_user_profile UNIQUE (user_id)
);

-- Portfolios (generated HTML sites)
CREATE TABLE IF NOT EXISTS portfolios (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  subdomain TEXT UNIQUE NOT NULL, -- maps to users.subdomain
  html_content TEXT NOT NULL,
  css_content TEXT,
  live_url TEXT, -- full URL: https://xxx.supabase.co/storage/v1/object/public/...
  version INT DEFAULT 1, -- track regenerations
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_updated TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_user_portfolio UNIQUE (user_id)
);

-- Résumés (ATS-optimized outputs)
CREATE TABLE IF NOT EXISTS resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  pdf_url TEXT, -- Supabase Storage path
  docx_url TEXT,
  ats_score INT CHECK (ats_score >= 0 AND ats_score <= 100),
  content_text TEXT, -- for optimizer re-analysis
  version INT DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cover Letters
CREATE TABLE IF NOT EXISTS cover_letters (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  job_description_text TEXT NOT NULL,
  generated_letter_text TEXT NOT NULL,
  tone_preset TEXT CHECK (tone_preset IN ('formal', 'friendly', 'technical')),
  user_edits TEXT, -- track edits for fine-tuning dataset
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Job Alerts
CREATE TABLE IF NOT EXISTS job_alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  keywords TEXT[], -- ['junior frontend', 'React', 'remote']
  sources TEXT[], -- ['linkedin', 'wellfound', 'angellist']
  frequency TEXT CHECK (frequency IN ('daily', 'weekly')),
  last_sent TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_user_alert UNIQUE (user_id)
);

-- Mock Interviews
CREATE TABLE IF NOT EXISTS mock_interviews (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_type TEXT, -- 'Frontend', 'Backend', 'Fullstack', 'PM', etc.
  questions JSONB, -- [{type, question, answer, feedback}, ...]
  confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 5),
  transcript_json JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optimizer History (track score improvements)
CREATE TABLE IF NOT EXISTS optimizer_runs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  job_description TEXT NOT NULL,
  resume_version INT,
  score INT CHECK (score >= 0 AND score <= 100),
  missing_keywords TEXT[],
  suggestions JSONB, -- [{section, recommendation}, ...]
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analytics Events (for KPI tracking)
CREATE TABLE IF NOT EXISTS analytics_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  event_type TEXT NOT NULL, -- 'signup', 'portfolio_generated', 'resume_downloaded', etc.
  properties JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ========================================
-- INDEXES
-- ========================================

CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_cover_letters_user_id ON cover_letters(user_id);
CREATE INDEX IF NOT EXISTS idx_job_alerts_user_id ON job_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_mock_interviews_user_id ON mock_interviews(user_id);
CREATE INDEX IF NOT EXISTS idx_optimizer_runs_user_id ON optimizer_runs(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_type_created ON analytics_events(event_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_users_subdomain ON users(subdomain);
CREATE INDEX IF NOT EXISTS idx_portfolios_subdomain ON portfolios(subdomain);

-- ========================================
-- ROW-LEVEL SECURITY (RLS) POLICIES
-- ========================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolios ENABLE ROW LEVEL SECURITY;
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE cover_letters ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE mock_interviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE optimizer_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  USING (auth.uid() = id);

-- Profiles policies
CREATE POLICY "Users can view own profile data"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile data"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile data"
  ON profiles FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile data"
  ON profiles FOR DELETE
  USING (auth.uid() = user_id);

-- Portfolios policies
CREATE POLICY "Users can view own portfolio"
  ON portfolios FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own portfolio"
  ON portfolios FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own portfolio"
  ON portfolios FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own portfolio"
  ON portfolios FOR DELETE
  USING (auth.uid() = user_id);

-- Resumes policies
CREATE POLICY "Users can view own resumes"
  ON resumes FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own resumes"
  ON resumes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own resumes"
  ON resumes FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own resumes"
  ON resumes FOR DELETE
  USING (auth.uid() = user_id);

-- Cover Letters policies
CREATE POLICY "Users can view own cover letters"
  ON cover_letters FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own cover letters"
  ON cover_letters FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own cover letters"
  ON cover_letters FOR DELETE
  USING (auth.uid() = user_id);

-- Job Alerts policies
CREATE POLICY "Users can view own job alerts"
  ON job_alerts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own job alerts"
  ON job_alerts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own job alerts"
  ON job_alerts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own job alerts"
  ON job_alerts FOR DELETE
  USING (auth.uid() = user_id);

-- Mock Interviews policies
CREATE POLICY "Users can view own mock interviews"
  ON mock_interviews FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own mock interviews"
  ON mock_interviews FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Optimizer Runs policies
CREATE POLICY "Users can view own optimizer runs"
  ON optimizer_runs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own optimizer runs"
  ON optimizer_runs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Analytics Events policies (allow inserts for tracking)
CREATE POLICY "Anyone can insert analytics events"
  ON analytics_events FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can view own analytics events"
  ON analytics_events FOR SELECT
  USING (auth.uid() = user_id);

-- ========================================
-- STORAGE BUCKETS
-- ========================================

-- Create storage buckets (run in Supabase Storage UI or via SQL)
-- Note: Bucket creation via SQL is not standard, use Supabase UI:
-- 1. Go to Storage > Create bucket
-- 2. Create 'resumes' bucket (private)
-- 3. Create 'portfolios' bucket (public)

-- Storage policies (add these in Supabase Storage UI > Policies):
-- Bucket: resumes (private)
--   - SELECT: auth.uid() = bucket_id owner
--   - INSERT: auth.uid() = bucket_id owner
--   - DELETE: auth.uid() = bucket_id owner

-- Bucket: portfolios (public)
--   - SELECT: true (public read)
--   - INSERT: auth.uid() = bucket_id owner
--   - UPDATE: auth.uid() = bucket_id owner

-- ========================================
-- FUNCTIONS & TRIGGERS
-- ========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for profiles table
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Function to auto-create user row on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, created_at)
  VALUES (NEW.id, NEW.email, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users (Supabase Auth table)
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_user();

-- ========================================
-- SAMPLE DATA (for testing)
-- ========================================

-- Insert a test user (requires manual auth signup first, then link here)
-- Example:
-- INSERT INTO users (id, email, subdomain)
-- VALUES ('test-uuid-from-auth', 'test@example.com', 'test-user');

-- ========================================
-- ANALYTICS VIEWS (for KPI tracking)
-- ========================================

-- Daily signups
CREATE OR REPLACE VIEW daily_signups AS
SELECT
  DATE(created_at) as signup_date,
  COUNT(*) as signups
FROM users
GROUP BY DATE(created_at)
ORDER BY signup_date DESC;

-- Activation rate (users with portfolio + resume)
CREATE OR REPLACE VIEW activation_rate AS
SELECT
  COUNT(DISTINCT users.id) as total_users,
  COUNT(DISTINCT portfolios.user_id) as users_with_portfolio,
  COUNT(DISTINCT resumes.user_id) as users_with_resume,
  COUNT(DISTINCT CASE WHEN portfolios.id IS NOT NULL AND resumes.id IS NOT NULL THEN users.id END) as activated_users,
  ROUND(
    100.0 * COUNT(DISTINCT CASE WHEN portfolios.id IS NOT NULL AND resumes.id IS NOT NULL THEN users.id END) /
    NULLIF(COUNT(DISTINCT users.id), 0),
    2
  ) as activation_percentage
FROM users
LEFT JOIN portfolios ON users.id = portfolios.user_id
LEFT JOIN resumes ON users.id = resumes.user_id;

-- ========================================
-- GRANT PERMISSIONS
-- ========================================

-- Grant access to authenticated users
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- Grant access to anon (for unauthenticated access - be careful!)
GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT, INSERT ON analytics_events TO anon;

-- ========================================
-- NOTES
-- ========================================

-- 1. After running this script, create Storage buckets manually in Supabase UI:
--    - 'resumes' (private)
--    - 'portfolios' (public)
--
-- 2. Configure storage policies in Supabase UI > Storage > Policies
--
-- 3. Test connection with: SELECT * FROM users;
--
-- 4. For local development, copy .env.example to .env and fill in credentials
