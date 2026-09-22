CREATE TRIGGER prevent_manual_frequency_tampering
BEFORE UPDATE OF frequency ON combinations
-- Block the update if someone tries to decrease the frequency or keep it the same
WHEN NEW.frequency <= OLD.frequency
BEGIN
    SELECT RAISE(ABORT, 'You can only increase the frequency, not decrease or overwrite it.');
END;