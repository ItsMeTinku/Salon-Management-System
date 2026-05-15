-- ==========================================
-- SUPABASE POSTGRESQL SETUP SCRIPT
-- ==========================================
-- Please run this script in your Supabase SQL Editor to create the necessary tables and secure them.

-- 1. Create Tables
CREATE TABLE IF NOT EXISTS admin (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'Staff'
);

CREATE TABLE IF NOT EXISTS employees (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    profession TEXT,
    salary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emp_id TEXT REFERENCES employees(id) ON DELETE CASCADE,
    emp_name TEXT NOT NULL,
    status TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    phone TEXT PRIMARY KEY,
    cust_name TEXT NOT NULL,
    service TEXT,
    visit_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cust_name TEXT NOT NULL,
    service TEXT,
    emp_id TEXT REFERENCES employees(id) ON DELETE SET NULL,
    date DATE NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS billing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cust_name TEXT NOT NULL,
    service TEXT,
    amount NUMERIC NOT NULL,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Default Admin
INSERT INTO admin (username, password, role) 
VALUES ('admin', 'admin123', 'Admin') 
ON CONFLICT (username) DO NOTHING;

-- 2. Enable Row Level Security (RLS)
ALTER TABLE admin ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing ENABLE ROW LEVEL SECURITY;

-- 3. Create RLS Policies
-- NOTE: If you are using the 'service_role' key in Streamlit secrets, RLS is automatically bypassed.
-- If you use the 'anon' key, you will need policies to allow access. Since this is an internal ERP, 
-- we restrict access to authenticated requests or define custom access if using the anon key. 
-- For strict security with service_role backend, we can block anon access completely.

-- Restrict all public anonymous access
CREATE POLICY "Deny anonymous select" ON admin FOR SELECT TO anon USING (false);
CREATE POLICY "Deny anonymous insert" ON admin FOR INSERT TO anon WITH CHECK (false);
CREATE POLICY "Deny anonymous update" ON admin FOR UPDATE TO anon USING (false);
CREATE POLICY "Deny anonymous delete" ON admin FOR DELETE TO anon USING (false);

-- Enable service role access (bypasses RLS anyway, but good for explicit tracking)
CREATE POLICY "Enable all for service_role" ON admin FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for service_role" ON employees FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for service_role" ON attendance FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for service_role" ON customers FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for service_role" ON appointments FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for service_role" ON billing FOR ALL TO service_role USING (true) WITH CHECK (true);
