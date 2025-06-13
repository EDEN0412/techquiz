-- Add missing fields to difficulty_level table to match Django model
ALTER TABLE difficulty_level 
ADD COLUMN IF NOT EXISTS slug VARCHAR(50),
ADD COLUMN IF NOT EXISTS level INTEGER,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Create unique constraints
CREATE UNIQUE INDEX IF NOT EXISTS difficulty_level_slug_unique ON difficulty_level(slug);
CREATE UNIQUE INDEX IF NOT EXISTS difficulty_level_level_unique ON difficulty_level(level);

-- Update existing data with slug and level values
UPDATE difficulty_level SET 
    slug = CASE 
        WHEN name = '初級' THEN 'beginner'
        WHEN name = '中級' THEN 'intermediate' 
        WHEN name = '上級' THEN 'advanced'
        ELSE LOWER(REPLACE(name, ' ', '_'))
    END,
    level = CASE
        WHEN name = '初級' THEN 1
        WHEN name = '中級' THEN 2
        WHEN name = '上級' THEN 3
        ELSE id
    END,
    updated_at = created_at
WHERE slug IS NULL OR level IS NULL;

-- Add trigger for updated_at
DROP TRIGGER IF EXISTS update_difficulty_level_updated_at ON difficulty_level;
CREATE TRIGGER update_difficulty_level_updated_at
    BEFORE UPDATE ON difficulty_level
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
