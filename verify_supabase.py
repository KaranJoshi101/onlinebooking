#!/usr/bin/env python3
"""
Verify Supabase PostgreSQL connection and database setup
Run this from your local machine to test Supabase connectivity
"""

import os
import sys

# Supabase credentials
SUPABASE_CREDS = {
    'user': 'postgres',
    'password': 'a-g4SGTknzENbpu',
    'host': 'db.stpowaxbrnwtwjmzpvim.supabase.co',
    'port': '5432',
    'database': 'postgres'
}

def test_supabase_connection():
    """Test connection to Supabase PostgreSQL"""
    try:
        import psycopg2
        
        print("=" * 80)
        print("Supabase PostgreSQL Connection Test")
        print("=" * 80)
        print()
        
        # Display connection info
        print("Connection Details:")
        print(f"  Host: {SUPABASE_CREDS['host']}")
        print(f"  Port: {SUPABASE_CREDS['port']}")
        print(f"  User: {SUPABASE_CREDS['user']}")
        print(f"  Database: {SUPABASE_CREDS['database']}")
        print()
        
        # Connect
        print("Connecting to Supabase...")
        conn = psycopg2.connect(
            user=SUPABASE_CREDS['user'],
            password=SUPABASE_CREDS['password'],
            host=SUPABASE_CREDS['host'],
            port=SUPABASE_CREDS['port'],
            database=SUPABASE_CREDS['database'],
            connect_timeout=10
        )
        
        print("✓ Connection successful!\n")
        
        # Get version
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        print(f"✓ PostgreSQL Version:\n  {version}\n")
        
        # List tables
        cur.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            ORDER BY tablename
        """)
        tables = cur.fetchall()
        print(f"✓ Tables in database ({len(tables)}):")
        for (table,) in tables:
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  - {table}: {count} rows")
        
        print()
        
        # Get database size
        cur.execute("SELECT pg_size_pretty(pg_database_size('postgres'))")
        size = cur.fetchone()[0]
        print(f"✓ Database Size: {size}\n")
        
        # Get connection count
        cur.execute("""
            SELECT count(*) FROM pg_stat_activity 
            WHERE datname = 'postgres'
        """)
        connections = cur.fetchone()[0]
        print(f"✓ Active Connections: {connections}\n")
        
        cur.close()
        conn.close()
        
        print("=" * 80)
        print("✓✓✓ SUPABASE CONNECTION TEST SUCCESSFUL ✓✓✓")
        print("=" * 80)
        print()
        print("Ready for migration! Run:")
        print("  python migrate_sqlite_to_postgres.py")
        print()
        
        return True
        
    except ImportError:
        print("✗ psycopg2 not installed")
        print("Install it with: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print("=" * 80)
        print("✗ Connection Test Failed")
        print("=" * 80)
        print(f"\nError: {e}\n")
        print("Troubleshooting:")
        print("1. Check internet connection")
        print("2. Verify Supabase project is active")
        print("3. Disable VPN/firewall temporarily")
        print("4. Check credentials in .env file")
        print("5. Verify hostname is correct")
        print()
        return False


if __name__ == '__main__':
    # Set environment variables from dict
    for key, value in SUPABASE_CREDS.items():
        os.environ[f'DB_{key.upper()}'] = value
    
    success = test_supabase_connection()
    sys.exit(0 if success else 1)
