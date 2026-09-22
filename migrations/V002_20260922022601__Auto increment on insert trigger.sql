CREATE TRIGGER auto_increment_frequency
BEFORE INSERT ON combinations
FOR EACH ROW
-- Only run this trigger if the combination already exists
WHEN EXISTS (SELECT 1 FROM combinations WHERE combination = NEW.combination)
BEGIN
    -- Update the existing row by adding the new frequency (or 1 if none was provided)
    UPDATE combinations 
    SET frequency = frequency + COALESCE(NEW.frequency, 1)
    WHERE combination = NEW.combination;
    
    -- Silently cancel the original INSERT statement so it doesn't throw a UNIQUE error
    SELECT RAISE(IGNORE);
END;