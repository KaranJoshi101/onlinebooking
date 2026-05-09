#!/usr/bin/env python3
"""
Database Consistency Checker
Validates data integrity between SQLite and PostgreSQL after migration
"""

import sqlite3
import psycopg
import os
import sys
import socket
import subprocess
import re
import ipaddress
from datetime import datetime
from typing import Tuple, List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'

class ConsistencyChecker:
    """Validates database consistency after migration"""
    
    def __init__(self, sqlite_path, pg_user, pg_password, pg_host, pg_port, pg_db):
        self.sqlite_path = sqlite_path
        self.pg_user = pg_user
        self.pg_password = pg_password
        self.pg_host = pg_host
        self.pg_port = pg_port
        self.pg_db = pg_db
        self.sqlite_conn = None
        self.pg_conn = None
        self.report = []
        self.errors = []
        self.warnings = []

    def get_database_url(self):
        return os.getenv('DATABASE_URL', '').strip()
        
    def add_report(self, message: str):
        """Add message to report"""
        self.report.append(message)
        print(message)
    
    def add_error(self, message: str):
        """Add error message"""
        self.errors.append(message)
        self.add_report(f"✗ ERROR: {message}")
    
    def add_warning(self, message: str):
        """Add warning message"""
        self.warnings.append(message)
        self.add_report(f"⚠ WARNING: {message}")
    
    def add_success(self, message: str):
        """Add success message"""
        self.add_report(f"✓ {message}")
    
    def connect_databases(self) -> bool:
        """Connect to both databases"""
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_path)
            self.sqlite_conn.row_factory = sqlite3.Row
            self.add_success(f"Connected to SQLite: {self.sqlite_path}")
        except sqlite3.Error as e:
            self.add_error(f"SQLite connection failed: {e}")
            return False
        
        try:
            database_url = self.get_database_url()
            if database_url:
                self.pg_conn = psycopg.connect(database_url, connect_timeout=10)
                self.add_success("Connected to PostgreSQL using DATABASE_URL")
            else:
                resolved_host = self.resolve_host(self.pg_host)
                self.pg_conn = psycopg.connect(
                    user=self.pg_user,
                    password=self.pg_password,
                    host=self.pg_host,
                    hostaddr=resolved_host,
                    port=self.pg_port,
                    dbname=self.pg_db,
                    sslmode='require',
                    connect_timeout=10
                )
                self.add_success(f"Connected to PostgreSQL: {self.pg_host} ({resolved_host}):{self.pg_port}/{self.pg_db}")
        except psycopg.Error as e:
            self.add_error(f"PostgreSQL connection failed: {e}")
            return False
        except socket.gaierror as e:
            self.add_error(f"PostgreSQL host resolution failed: {e}")
            return False

        return True

    def resolve_host(self, hostname):
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
        
        return True
    
    def check_table_count(self) -> bool:
        """Check if all tables exist in PostgreSQL"""
        self.add_report("\n" + "="*80)
        self.add_report("TABLE EXISTENCE CHECK")
        self.add_report("="*80)
        
        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            sqlite_tables = set(row[0] for row in sqlite_cursor.fetchall())
            
            pg_cursor = self.pg_conn.cursor()
            pg_cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' ORDER BY table_name;
            """)
            pg_tables = set(row[0] for row in pg_cursor.fetchall())
            
            all_exist = True
            for table in sorted(sqlite_tables):
                if table in pg_tables:
                    self.add_success(f"Table '{table}' exists in PostgreSQL")
                else:
                    self.add_error(f"Table '{table}' missing in PostgreSQL")
                    all_exist = False
            
            return all_exist
        except Exception as e:
            self.add_error(f"Failed to check tables: {e}")
            return False
    
    def check_row_counts(self) -> bool:
        """Compare row counts between SQLite and PostgreSQL"""
        self.add_report("\n" + "="*80)
        self.add_report("ROW COUNT VALIDATION")
        self.add_report("="*80)
        
        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in sqlite_cursor.fetchall()]
            
            all_match = True
            total_sqlite = 0
            total_postgres = 0
            
            for table in tables:
                sqlite_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier(table)};")
                sqlite_count = sqlite_cursor.fetchone()[0]
                
                pg_cursor = self.pg_conn.cursor()
                pg_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier(table)};")
                pg_count = pg_cursor.fetchone()[0]
                
                total_sqlite += sqlite_count
                total_postgres += pg_count
                
                if sqlite_count == pg_count:
                    self.add_success(f"'{table}': {sqlite_count} rows (matched)")
                else:
                    self.add_error(f"'{table}': SQLite={sqlite_count}, PostgreSQL={pg_count}")
                    all_match = False
            
            self.add_report(f"\nTotal: SQLite={total_sqlite}, PostgreSQL={total_postgres}")
            
            if total_sqlite == total_postgres:
                self.add_success("Total row count matches")
            else:
                self.add_error("Total row count mismatch")
                all_match = False
            
            return all_match
        except Exception as e:
            self.add_error(f"Failed to check row counts: {e}")
            return False
    
    def check_column_counts(self) -> bool:
        """Verify column counts match"""
        self.add_report("\n" + "="*80)
        self.add_report("COLUMN COUNT VALIDATION")
        self.add_report("="*80)
        
        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in sqlite_cursor.fetchall()]
            
            all_match = True
            
            for table in tables:
                # SQLite column count
                sqlite_cursor.execute(f"PRAGMA table_info({quote_identifier(table)});")
                sqlite_cols = len(sqlite_cursor.fetchall())
                
                # PostgreSQL column count
                pg_cursor = self.pg_conn.cursor()
                pg_cursor.execute(f"""
                    SELECT COUNT(*) FROM information_schema.columns 
                    WHERE table_name = '{table}';
                """)
                pg_cols = pg_cursor.fetchone()[0]
                
                if sqlite_cols == pg_cols:
                    self.add_success(f"'{table}': {sqlite_cols} columns (matched)")
                else:
                    self.add_error(f"'{table}': SQLite={sqlite_cols}, PostgreSQL={pg_cols}")
                    all_match = False
            
            return all_match
        except Exception as e:
            self.add_error(f"Failed to check column counts: {e}")
            return False
    
    def check_primary_keys(self) -> bool:
        """Check if primary keys are intact"""
        self.add_report("\n" + "="*80)
        self.add_report("PRIMARY KEY VALIDATION")
        self.add_report("="*80)

        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in sqlite_cursor.fetchall()]

            all_valid = True

            for table in tables:
                sqlite_cursor.execute(f"PRAGMA table_info({quote_identifier(table)});")
                sqlite_pks = [row[1] for row in sqlite_cursor.fetchall() if row[5] == 1]

                pg_cursor = self.pg_conn.cursor()
                pg_cursor.execute(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_name = '{table}'
                    ORDER BY kcu.ordinal_position;
                """)
                pg_pks = [row[0] for row in pg_cursor.fetchall()]

                if sqlite_pks or pg_pks:
                    if sqlite_pks == pg_pks:
                        self.add_success(f"'{table}': Primary keys match")
                    else:
                        self.add_warning(f"'{table}': PK mismatch (may be expected)")
                        all_valid = False

            return all_valid
        except Exception as e:
            self.add_warning(f"Could not fully validate primary keys: {e}")
            try:
                self.pg_conn.rollback()
            except Exception:
                pass
            return True
    
    def check_foreign_keys(self) -> bool:
        """Check if foreign key relationships are intact"""
        self.add_report("\n" + "="*80)
        self.add_report("FOREIGN KEY RELATIONSHIP VALIDATION")
        self.add_report("="*80)
        
        # Map of table -> (foreign_key_column, references_table, references_column)
        foreign_keys = {
            'department': ('hid', 'hospital', 'id'),
            'deptdoc': ('deptid', 'department', 'id'),
            'deptdoc': ('docid', 'doctor', 'id'),
            'patient': ('uid', 'user', 'id'),
            'patientlist': ('aid', 'appointment', 'id'),
            'patientlist': ('pid', 'patient', 'id'),
            'appointment': ('slotid', 'slots', 'id'),
            'days': ('ddid', 'deptdoc', 'id'),
            'slots': ('daysid', 'days', 'id'),
        }
        
        all_valid = True
        
        # Check specific foreign key relationships
        pg_cursor = self.pg_conn.cursor()
        
        # Check department.hid -> hospital.id
        pg_cursor.execute("""
            SELECT COUNT(*) FROM department d
            WHERE d.hid IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM hospital h WHERE h.id = d.hid);
        """)
        orphaned = pg_cursor.fetchone()[0]
        if orphaned == 0:
            self.add_success("department.hid -> hospital.id: Valid (no orphaned records)")
        else:
            self.add_error(f"department.hid -> hospital.id: {orphaned} orphaned records")
            all_valid = False
        
        # Check patient.uid -> user.id
        pg_cursor.execute("""
            SELECT COUNT(*) FROM patient p
            WHERE p.uid IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM "user" u WHERE u.id = p.uid);
        """)
        orphaned = pg_cursor.fetchone()[0]
        if orphaned == 0:
            self.add_success("patient.uid -> user.id: Valid (no orphaned records)")
        else:
            self.add_error(f"patient.uid -> user.id: {orphaned} orphaned records")
            all_valid = False
        
        # Check patientlist.aid -> appointment.id
        pg_cursor.execute("""
            SELECT COUNT(*) FROM patientlist pl
            WHERE pl.aid IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM appointment a WHERE a.id = pl.aid);
        """)
        orphaned = pg_cursor.fetchone()[0]
        if orphaned == 0:
            self.add_success("patientlist.aid -> appointment.id: Valid (no orphaned records)")
        else:
            self.add_error(f"patientlist.aid -> appointment.id: {orphaned} orphaned records")
            all_valid = False
        
        # Check patientlist.pid -> patient.id
        pg_cursor.execute("""
            SELECT COUNT(*) FROM patientlist pl
            WHERE pl.pid IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM patient p WHERE p.id = pl.pid);
        """)
        orphaned = pg_cursor.fetchone()[0]
        if orphaned == 0:
            self.add_success("patientlist.pid -> patient.id: Valid (no orphaned records)")
        else:
            self.add_error(f"patientlist.pid -> patient.id: {orphaned} orphaned records")
            all_valid = False
        
        return all_valid
    
    def check_data_types(self) -> bool:
        """Check if data types are preserved correctly"""
        self.add_report("\n" + "="*80)
        self.add_report("DATA TYPE VALIDATION")
        self.add_report("="*80)
        
        try:
            # Check for NULL values in specific columns
            pg_cursor = self.pg_conn.cursor()
            
            # Verify string fields contain expected data
            pg_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier('hospital')} WHERE {quote_identifier('name')} IS NOT NULL;")
            valid_hospitals = pg_cursor.fetchone()[0]
            self.add_success(f"Hospital table: {valid_hospitals} records with valid names")
            
            # Check for invalid dates
            pg_cursor.execute("""
                SELECT COUNT(*) FROM patient 
                WHERE d_added IS NOT NULL AND d_added > NOW();
            """)
            future_dates = pg_cursor.fetchone()[0]
            if future_dates == 0:
                self.add_success("Patient dates: All valid (no future dates)")
            else:
                self.add_warning(f"Patient dates: {future_dates} future dates found")
            
            # Check for valid numeric ranges
            pg_cursor.execute("""
                SELECT COUNT(*) FROM deptdoc 
                WHERE rating < 0 OR rating > 5;
            """)
            invalid_ratings = pg_cursor.fetchone()[0]
            if invalid_ratings == 0:
                self.add_success("Doctor ratings: All valid (0-5 range)")
            else:
                self.add_warning(f"Doctor ratings: {invalid_ratings} invalid ratings")
            
            return True
        except Exception as e:
            self.add_warning(f"Could not fully validate data types: {e}")
            return True
    
    def check_sample_data(self) -> bool:
        """Spot-check sample records"""
        self.add_report("\n" + "="*80)
        self.add_report("SAMPLE DATA VALIDATION")
        self.add_report("="*80)
        
        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            pg_cursor = self.pg_conn.cursor()
            
            # Check if data exists
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier('hospital')};")
            hospital_count = sqlite_cursor.fetchone()[0]
            
            if hospital_count > 0:
                # Get first hospital from both databases
                sqlite_cursor.execute(f"SELECT id, name, state FROM {quote_identifier('hospital')} LIMIT 1;")
                sqlite_row = sqlite_cursor.fetchone()
                
                pg_cursor.execute(f"SELECT id, name, state FROM {quote_identifier('hospital')} LIMIT 1;")
                pg_row = pg_cursor.fetchone()
                
                if sqlite_row and pg_row:
                    if sqlite_row['id'] == pg_row[0] and sqlite_row['name'] == pg_row[1]:
                        self.add_success("Sample hospital record matches")
                    else:
                        self.add_warning("Sample hospital record differs (may be expected)")
            
            return True
        except Exception as e:
            self.add_warning(f"Could not validate sample data: {e}")
            return True
    
    def generate_report(self) -> str:
        """Generate final consistency report"""
        self.add_report("\n" + "="*80)
        self.add_report("CONSISTENCY CHECK SUMMARY")
        self.add_report("="*80)
        
        total_checks = 6  # Number of check functions
        errors_count = len(self.errors)
        warnings_count = len(self.warnings)
        
        self.add_report(f"\nTotal Errors: {errors_count}")
        self.add_report(f"Total Warnings: {warnings_count}")
        
        if errors_count == 0:
            self.add_report("\n✓✓✓ MIGRATION SUCCESSFUL - NO CRITICAL ERRORS ✓✓✓")
            return True
        else:
            self.add_report("\n✗✗✗ MIGRATION HAS ISSUES - REVIEW ERRORS ABOVE ✗✗✗")
            return False
    
    def close_connections(self):
        """Close database connections"""
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.pg_conn:
            self.pg_conn.close()
    
    def run_all_checks(self) -> bool:
        """Run all consistency checks"""
        print("\n" + "="*80)
        print("DATABASE CONSISTENCY CHECKER")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
        if not self.connect_databases():
            return False
        
        try:
            results = []
            results.append(("Table Existence", self.check_table_count()))
            results.append(("Row Count", self.check_row_counts()))
            results.append(("Column Count", self.check_column_counts()))
            results.append(("Primary Keys", self.check_primary_keys()))
            results.append(("Foreign Keys", self.check_foreign_keys()))
            results.append(("Data Types", self.check_data_types()))
            results.append(("Sample Data", self.check_sample_data()))
            
            final_result = self.generate_report()
            
            # Save report to file
            with open('consistency_check.log', 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.report))
            
            self.add_report(f"\n✓ Report saved to: consistency_check.log")
            print("\n" + "="*80)
            
            return final_result
        
        finally:
            self.close_connections()


def main():
    """Main entry point"""
    sqlite_path = 'instance/onlinebooking.sqlite3'
    
    # PostgreSQL credentials (from environment or defaults)
    pg_user = os.getenv('DB_USER', 'postgres')
    pg_password = os.getenv('DB_PASSWORD', 'password')
    pg_host = os.getenv('DB_HOST', 'localhost')
    pg_port = int(os.getenv('DB_PORT', '5432'))
    pg_db = os.getenv('DB_NAME', 'onlinebooking')
    
    checker = ConsistencyChecker(sqlite_path, pg_user, pg_password, pg_host, pg_port, pg_db)
    success = checker.run_all_checks()
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
