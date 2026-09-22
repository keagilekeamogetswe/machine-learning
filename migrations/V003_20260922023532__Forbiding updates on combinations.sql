CREATE TRIGGER prevent_structural_updates
BEFORE UPDATE OF id, combination, size ON combinations
BEGIN
    SELECT RAISE(ABORT, 'Updates are forbidden. You may only insert new combinations.');
END;