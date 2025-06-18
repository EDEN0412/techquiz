-- Add missing fields to difficulty_level table to match Django model
ALTER TABLE quiz_difficultylevel 
ADD COLUMN IF NOT EXISTS slug VARCHAR(50),
ADD COLUMN IF NOT EXISTS level INTEGER,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Create unique constraints
CREATE UNIQUE INDEX IF NOT EXISTS quiz_difficultylevel_slug_unique ON quiz_difficultylevel(slug);
CREATE UNIQUE INDEX IF NOT EXISTS quiz_difficultylevel_level_unique ON quiz_difficultylevel(level);

-- Update existing data with slug and level values
UPDATE quiz_difficultylevel SET 
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
DROP TRIGGER IF EXISTS update_quiz_difficultylevel_updated_at ON quiz_difficultylevel;
CREATE TRIGGER update_quiz_difficultylevel_updated_at
    BEFORE UPDATE ON quiz_difficultylevel
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
