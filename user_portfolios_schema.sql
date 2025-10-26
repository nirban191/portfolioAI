-- Create user_portfolios table for saving portfolios
CREATE TABLE IF NOT EXISTS user_portfolios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  profile_data JSONB NOT NULL,
  portfolio_html TEXT,
  subdomain TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add index for faster queries by user_id
CREATE INDEX IF NOT EXISTS idx_user_portfolios_user_id ON user_portfolios(user_id);

-- Add index for created_at for sorting
CREATE INDEX IF NOT EXISTS idx_user_portfolios_created_at ON user_portfolios(created_at DESC);

-- Enable Row Level Security
ALTER TABLE user_portfolios ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see their own portfolios
CREATE POLICY "Users can view their own portfolios"
  ON user_portfolios
  FOR SELECT
  USING (auth.uid() = user_id);

-- RLS Policy: Users can insert their own portfolios
CREATE POLICY "Users can create their own portfolios"
  ON user_portfolios
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can update their own portfolios
CREATE POLICY "Users can update their own portfolios"
  ON user_portfolios
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can delete their own portfolios
CREATE POLICY "Users can delete their own portfolios"
  ON user_portfolios
  FOR DELETE
  USING (auth.uid() = user_id);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function on update
CREATE TRIGGER update_user_portfolios_updated_at
  BEFORE UPDATE ON user_portfolios
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
