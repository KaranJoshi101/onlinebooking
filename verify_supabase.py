#!/usr/bin/env python3
"""
Verify Supabase PostgreSQL connection and database setup
Run this from your local machine to test Supabase connectivity
"""

import os
import sys
import socket
import subprocess
import re
import ipaddress

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Supabase credentials (loaded from .env when available)
SUPABASE_CREDS = {
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'postgres')
}

def test_supabase_connection():
    """Test connection to Supabase PostgreSQL"""
    try:
        import psycopg

        def resolve_host(hostname: str) -> str:
            def valid_ip(candidate: str) -> bool:
                ip = ipaddress.ip_address(candidate)
                return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast)

            def parse_answer_address(output: str):
                capture = False
                for line in output.splitlines():
                    stripped = line.strip()
                    if stripped.lower().startswith('name:'):
                        capture = True
                        continue
                    if capture and stripped.lower().startswith('address:'):
                        match = re.search(r'(?:\d{1,3}\.){3}\d{1,3}', stripped)
                        if match:
                            candidate = match.group(0)
                            if valid_ip(candidate):
                                return candidate
                return None

            try:
                candidate = socket.gethostbyname(hostname)
                if valid_ip(candidate):
                    return candidate
            except socket.gaierror:
                pass

            for dns_server in ('1.1.1.1', '8.8.8.8'):
                result = subprocess.run(['nslookup', hostname, dns_server], capture_output=True, text=True, check=False)
                candidate = parse_answer_address(result.stdout)
                if candidate:
                    return candidate

            result = subprocess.run(['nslookup', hostname], capture_output=True, text=True, check=False)
            candidate = parse_answer_address(result.stdout)
            if candidate:
                return candidate

            raise socket.gaierror(f'No public IP found for {hostname}')
        
        print("=" * 80)
        print("Supabase PostgreSQL Connection Test")
        print("=" * 80)
        print()
        
        # Display connection info
        print("Connection Details:")
        database_url = os.getenv('DATABASE_URL', '').strip()
        if database_url:
            print("  Using DATABASE_URL from .env")
        else:
            print(f"  Host: {SUPABASE_CREDS['host']}")
            print(f"  Port: {SUPABASE_CREDS['port']}")
            print(f"  User: {SUPABASE_CREDS['user']}")
            print(f"  Database: {SUPABASE_CREDS['database']}")
        print()
        
        # Connect
        print("Connecting to Supabase...")
        if database_url:
            conn = psycopg.connect(database_url, connect_timeout=10)
        else:
            resolved_host = resolve_host(SUPABASE_CREDS['host'])
            print(f"  Resolved IP: {resolved_host}")
            conn = psycopg.connect(
                user=SUPABASE_CREDS['user'],
                password=SUPABASE_CREDS['password'],
                host=SUPABASE_CREDS['host'],
                hostaddr=resolved_host,
                port=SUPABASE_CREDS['port'],
                dbname=SUPABASE_CREDS['database'],
                sslmode='require',
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
        print("✗ psycopg not installed")
        print("Install it with: pip install 'psycopg[binary]'")
        return False

    except socket.gaierror as e:
        print("✗ Host resolution failed before connection")
        print(f"Error: {e}")
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
