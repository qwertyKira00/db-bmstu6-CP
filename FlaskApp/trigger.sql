CREATE OR REPLACE FUNCTION change_infected() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.health_status = 1 THEN
            UPDATE server_data.address
            SET infected = infected + 1
            WHERE id = NEW.id_address;
            RETURN NEW;
        END IF;
        RETURN NEW;
    ELSEIF TG_OP = 'UPDATE' THEN
        IF NEW.health_status = 0 THEN
            UPDATE server_data.address
            SET infected = infected - 1
            WHERE id = NEW.id_address;
            RETURN NEW;
        ELSEIF NEW.health_status = 1 THEN
            UPDATE server_data.address
            SET infected = infected + 1
            WHERE id = NEW.id_address;
            RETURN NEW;
        END IF;
    ELSIF TG_OP = 'DELETE' THEN
        IF OLD.health_status = 1 THEN
            UPDATE server_data.address
            SET infected = infected - 1
            WHERE id = OLD.id_address;
            RETURN OLD;
        END IF;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_percentage
AFTER INSERT OR UPDATE OR DELETE ON server_data.private_office
FOR EACH ROW
EXECUTE PROCEDURE change_infected();
