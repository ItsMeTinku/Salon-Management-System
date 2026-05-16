-- ==========================================
-- SUPABASE POSTGRESQL SETUP SCRIPT  v2
-- ==========================================
-- Run this entire script in Supabase → SQL Editor → New Query.
--
-- WHY THE ORIGINAL SCRIPT CAUSED 42501 ERRORS
-- ─────────────────────────────────────────────
-- The original script enabled RLS on all tables but only created
-- DENY policies for the anon role and ALLOW policies for the
-- service_role.  If your secrets.toml contained the ANON key
-- (not the service_role key), every INSERT and SELECT was blocked
-- by RLS, producing error code 42501.
--
-- RECOMMENDED FIX (choose ONE approach):
--
--   APPROACH A — Use service_role key (recommended for internal ERPs)
--   ─────────────────────────────────────────────────────────────────
--   In .streamlit/secrets.toml set:
--       SUPABASE_SERVICE_ROLE_KEY = "eyJ..."   ← from Supabase → Settings → API
--       SUPABASE_URL              = "https://xxxx.supabase.co"
--
--   The service_role key bypasses RLS entirely on the server side.
--   No policy changes required.  Never expose this key in the browser.
--
--   APPROACH B — Keep anon key, add permissive policies
--   ─────────────────────────────────────────────────────────────────
--   Run the ALLOW ANON policies section below.
--   This is less secure but acceptable for a LAN-only salon system.
-- ==========================================


-- ──────────────────────────────────────────
-- 1. CREATE TABLES
-- ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS admin (
    username   TEXT PRIMARY KEY,
    password   TEXT NOT NULL,
    role       TEXT DEFAULT 'Staff'
);

CREATE TABLE IF NOT EXISTS employees (
    id         TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    profession TEXT,
    salary     TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emp_id     TEXT REFERENCES employees(id) ON DELETE CASCADE,
    emp_name   TEXT NOT NULL,
    status     TEXT NOT NULL,
    date       DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- Prevent duplicate entries for the same employee on the same day
    UNIQUE (emp_id, date)
);

CREATE TABLE IF NOT EXISTS customers (
    phone      TEXT PRIMARY KEY,
    cust_name  TEXT NOT NULL,
    service    TEXT,
    visit_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    -- id MUST be UUID so the Update tab can match a unique row.
    -- If this column is missing you get "Could not identify appointment ID".
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cust_name  TEXT NOT NULL,
    service    TEXT,
    emp_id     TEXT REFERENCES employees(id) ON DELETE SET NULL,
    date       DATE NOT NULL,
    status     TEXT DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS billing (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cust_name  TEXT NOT NULL,
    service    TEXT,
    amount     NUMERIC NOT NULL,
    date       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- ──────────────────────────────────────────
-- 2. SEED DEFAULT ADMIN
-- ──────────────────────────────────────────

INSERT INTO admin (username, password, role)
VALUES ('admin', 'admin123', 'Admin')
ON CONFLICT (username) DO NOTHING;


-- ──────────────────────────────────────────
-- 3. ENABLE RLS
-- ──────────────────────────────────────────

ALTER TABLE admin        ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees    ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance   ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers    ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing      ENABLE ROW LEVEL SECURITY;


-- ──────────────────────────────────────────
-- 4a. APPROACH A — service_role policies
--     (service_role bypasses RLS anyway, but
--      explicit policies make intent clear)
-- ──────────────────────────────────────────

-- Drop any conflicting old policies before recreating
DO $$ BEGIN
  DROP POLICY IF EXISTS "Enable all for service_role" ON admin;
  DROP POLICY IF EXISTS "Enable all for service_role" ON employees;
  DROP POLICY IF EXISTS "Enable all for service_role" ON attendance;
  DROP POLICY IF EXISTS "Enable all for service_role" ON customers;
  DROP POLICY IF EXISTS "Enable all for service_role" ON appointments;
  DROP POLICY IF EXISTS "Enable all for service_role" ON billing;
EXCEPTION WHEN OTHERS THEN NULL;
END $$;

CREATE POLICY "service_role_all_admin"        ON admin        FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_employees"    ON employees    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_attendance"   ON attendance   FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_customers"    ON customers    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_appointments" ON appointments FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_billing"      ON billing      FOR ALL TO service_role USING (true) WITH CHECK (true);


-- ──────────────────────────────────────────
-- 4b. APPROACH B — anon key policies
--     Uncomment this block if you cannot
--     switch to the service_role key.
--     This grants full access to the anon role,
--     which is acceptable only for a private
--     internal application not exposed to the internet.
-- ──────────────────────────────────────────

/*
-- Remove the old DENY policies for anon first
DROP POLICY IF EXISTS "Deny anonymous select" ON admin;
DROP POLICY IF EXISTS "Deny anonymous insert" ON admin;
DROP POLICY IF EXISTS "Deny anonymous update" ON admin;
DROP POLICY IF EXISTS "Deny anonymous delete" ON admin;

-- employees
CREATE POLICY "anon_select_employees"    ON employees    FOR SELECT TO anon USING (true);
CREATE POLICY "anon_insert_employees"    ON employees    FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "anon_update_employees"    ON employees    FOR UPDATE TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_delete_employees"    ON employees    FOR DELETE TO anon USING (true);

-- attendance
CREATE POLICY "anon_select_attendance"   ON attendance   FOR SELECT TO anon USING (true);
CREATE POLICY "anon_insert_attendance"   ON attendance   FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "anon_update_attendance"   ON attendance   FOR UPDATE TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_delete_attendance"   ON attendance   FOR DELETE TO anon USING (true);

-- customers
CREATE POLICY "anon_select_customers"    ON customers    FOR SELECT TO anon USING (true);
CREATE POLICY "anon_insert_customers"    ON customers    FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "anon_update_customers"    ON customers    FOR UPDATE TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_delete_customers"    ON customers    FOR DELETE TO anon USING (true);

-- appointments
CREATE POLICY "anon_select_appointments" ON appointments FOR SELECT TO anon USING (true);
CREATE POLICY "anon_insert_appointments" ON appointments FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "anon_update_appointments" ON appointments FOR UPDATE TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_delete_appointments" ON appointments FOR DELETE TO anon USING (true);

-- billing
CREATE POLICY "anon_select_billing"      ON billing      FOR SELECT TO anon USING (true);
CREATE POLICY "anon_insert_billing"      ON billing      FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "anon_update_billing"      ON billing      FOR UPDATE TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_delete_billing"      ON billing      FOR DELETE TO anon USING (true);

-- admin: keep blocked for anon (login credentials must stay protected)
CREATE POLICY "anon_deny_admin"          ON admin        FOR ALL  TO anon USING (false);
*/


-- ──────────────────────────────────────────
-- 5. INDEXES FOR COMMON QUERIES
-- ──────────────────────────────────────────

-- Appointment lookups by customer name are frequent
CREATE INDEX IF NOT EXISTS idx_appointments_cust_name ON appointments (cust_name);
CREATE INDEX IF NOT EXISTS idx_appointments_status     ON appointments (status);

-- Attendance lookups by date and emp_id
CREATE INDEX IF NOT EXISTS idx_attendance_date   ON attendance (date);
CREATE INDEX IF NOT EXISTS idx_attendance_emp_id ON attendance (emp_id);

-- Billing lookups by customer name
CREATE INDEX IF NOT EXISTS idx_billing_cust_name ON billing (cust_name);
