from supabase import create_client
import os

# Option 1 (recommended): environment variables
SUPABASE_URL = os.getenv("https://jchbgnaptdqmwtbepilc.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_axdEu7H3zZQ9g37zM0IDwA_PECmbpm5")

# Option 2 (fallback - only for local dev)
if not SUPABASE_URL:
    SUPABASE_URL = "https://jchbgnaptdqmwtbepilc.supabase.co"

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjaGJnbmFwdGRxbXd0YmVwaWxjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTM5MDQ4MiwiZXhwIjoyMDg2OTY2NDgyfQ.PxabJcJ26ni2Kif7th22G2D-DtMSFtsRDVSNiKme6FI"

# Create reusable client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)