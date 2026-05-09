#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script
Safely migrates data from SQLite to PostgreSQL with comprehensive error handling and validation
"""

import sqlite3
import psycopg
import os
import sys
import socket
import subprocess
import re
import ipaddress
from datetime import datetime, date, time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'

class MigrationLogger:
    """Logs migration progress and errors"""
    def __init__(self, log_file='migration.log'):
        self.log_file = log_file
        self.start_time = datetime.now()
        self.errors = []
        self.warnings = []
        
    def log(self, message, level='INFO'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] [{level}] {message}"
        print(log_msg)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def error(self, message):
        self.log(message, 'ERROR')
        self.errors.append(message)
    
    def warning(self, message):
        self.log(message, 'WARNING')
        self.warnings.append(message)
    
    def summary(self):
        duration = datetime.now() - self.start_time
        summary_msg = f"""
{'='*80}
MIGRATION SUMMARY
{'='*80}
Duration: {duration}
Total Errors: {len(self.errors)}
Total Warnings: {len(self.warnings)}
{'='*80}
"""
        self.log(summary_msg, 'INFO')
        if self.errors:
            self.log("ERRORS:", 'ERROR')
            for error in self.errors:
                self.log(f"  - {error}", 'ERROR')
        if self.warnings:
            self.log("WARNINGS:", 'WARNING')
            for warning in self.warnings:
                self.log(f"  - {warning}", 'WARNING')


class SQLiteToPostgreMigrator:
    """Main migration engine"""
    
    def __init__(self, sqlite_path, pg_user, pg_password, pg_host, pg_port, pg_db, logger):
        self.sqlite_path = sqlite_path
        self.pg_user = pg_user
        self.pg_password = pg_password
        self.pg_host = pg_host
        self.pg_port = pg_port
        self.pg_db = pg_db
        self.logger = logger
        self.sqlite_conn = None
        self.pg_conn = None
        self.migration_stats = {}

    def get_database_url(self):
        return os.getenv('DATABASE_URL', '').strip()
        
    def connect_sqlite(self):
        """Connect to SQLite database"""
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_path)
            self.sqlite_conn.row_factory = sqlite3.Row
            self.logger.log(f"Connected to SQLite database: {self.sqlite_path}")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to SQLite: {e}")
            return False
    
    def connect_postgres(self):
        """Connect to PostgreSQL database"""
        try:
            database_url = self.get_database_url()
            if database_url:
                self.pg_conn = psycopg.connect(database_url, connect_timeout=10)
                self.logger.log("Connected to PostgreSQL using DATABASE_URL")
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
                self.logger.log(f"Connected to PostgreSQL: {self.pg_host} ({resolved_host}):{self.pg_port}/{self.pg_db}")
            return True
        except psycopg.Error as e:
            self.logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
        except socket.gaierror as e:
            self.logger.error(f"Failed to resolve PostgreSQL host: {e}")
            return False

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
    
    def get_sqlite_tables(self):
        """Get all table names from SQLite"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            self.logger.log(f"Found {len(tables)} tables in SQLite: {tables}")
            return tables
        except sqlite3.Error as e:
            self.logger.error(f"Failed to get table list: {e}")
            return []
    
    def get_table_schema(self, table_name):
        """Get column information for a table"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute(f"PRAGMA table_info({quote_identifier(table_name)});")
            columns = cursor.fetchall()
            return columns
        except sqlite3.Error as e:
            self.logger.error(f"Failed to get schema for {table_name}: {e}")
            return []
    
    def convert_sqlite_type_to_postgres(self, sqlite_type):
        """Convert SQLite data types to PostgreSQL equivalents"""
        sqlite_type_upper = sqlite_type.upper()
        
        if 'INT' in sqlite_type_upper:
            return 'INTEGER'
        elif 'CHAR' in sqlite_type_upper or 'TEXT' in sqlite_type_upper:
            return 'TEXT'
        elif 'FLOAT' in sqlite_type_upper or 'REAL' in sqlite_type_upper:
            return 'NUMERIC'
        elif 'BOOL' in sqlite_type_upper:
            return 'BOOLEAN'
        elif 'DATE' in sqlite_type_upper:
            return 'DATE'
        elif 'TIME' in sqlite_type_upper:
            return 'TIME'
        else:
            return 'TEXT'
    
    def create_tables_in_postgres(self):
        """Create all tables in PostgreSQL based on SQLite schema"""
        try:
            cursor = self.pg_conn.cursor()
            tables = self.get_sqlite_tables()
            
            for table in tables:
                schema = self.get_table_schema(table)
                if not schema:
                    continue
                
                # Build CREATE TABLE statement
                create_sql = f"CREATE TABLE IF NOT EXISTS {quote_identifier(table)} (\n"
                columns = []
                
                for col in schema:
                    col_name = col[1]
                    col_type = self.convert_sqlite_type_to_postgres(col[2])
                    col_notnull = "NOT NULL" if col[3] else ""
                    col_pk = "PRIMARY KEY" if col[5] else ""
                    
                    col_def = f"  {quote_identifier(col_name)} {col_type}"
                    if col_pk:
                        col_def += f" {col_pk}"
                    if col_notnull:
                        col_def += f" {col_notnull}"
                    
                    columns.append(col_def)
                
                create_sql += ",\n".join(columns)
                create_sql += "\n);"
                
                cursor.execute(create_sql)
                self.logger.log(f"Created table: {table}")
            
            self.pg_conn.commit()
            self.logger.log("All tables created successfully in PostgreSQL")
            return True
        except psycopg.Error as e:
            self.logger.error(f"Failed to create tables in PostgreSQL: {e}")
            self.pg_conn.rollback()
            return False
    
    def migrate_table_data(self, table_name):
        """Migrate data from SQLite table to PostgreSQL"""
        try:
            # Get data from SQLite
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute(f"SELECT * FROM {quote_identifier(table_name)};")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                self.logger.log(f"No data to migrate for table: {table_name}")
                self.migration_stats[table_name] = 0
                return True
            
            # Get column names
            schema = self.get_table_schema(table_name)
            column_names = [col[1] for col in schema]
            column_types = {col[1]: col[2].upper() for col in schema}
            
            # Prepare INSERT statement
            placeholders = ', '.join(['%s'] * len(column_names))
            insert_sql = f"INSERT INTO {quote_identifier(table_name)} ({', '.join(quote_identifier(column) for column in column_names)}) VALUES ({placeholders});"
            
            # Convert data types if needed
            converted_rows = []
            for row in rows:
                converted_row = []
                for i, value in enumerate(row):
                    column_name = column_names[i]
                    column_type = column_types.get(column_name, '')

                    # Handle NULL values
                    if value is None:
                        converted_row.append(None)
                    elif 'BOOL' in column_type:
                        if isinstance(value, str):
                            converted_row.append(value.lower() in ('1', 'true', 't', 'yes', 'y'))
                        else:
                            converted_row.append(bool(value))
                    else:
                        converted_row.append(value)
                converted_rows.append(tuple(converted_row))
            
            # Insert data into PostgreSQL
            pg_cursor = self.pg_conn.cursor()
            pg_cursor.executemany(insert_sql, converted_rows)
            self.pg_conn.commit()
            
            row_count = len(converted_rows)
            self.migration_stats[table_name] = row_count
            self.logger.log(f"Migrated {row_count} rows to {table_name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to migrate data for {table_name}: {e}")
            self.pg_conn.rollback()
            return False
    
    def migrate_all_data(self):
        """Migrate all data from SQLite to PostgreSQL"""
        tables = self.get_sqlite_tables()
        
        self.logger.log(f"Starting migration of {len(tables)} tables...")

        self.reset_postgres_tables(tables)
        
        for table in tables:
            self.logger.log(f"Migrating table: {table}")
            self.migrate_table_data(table)
        
        self.logger.log("Data migration completed")
        return True

    def reset_postgres_tables(self, tables):
        """Remove existing PostgreSQL rows before reloading data."""
        try:
            cursor = self.pg_conn.cursor()
            quoted_tables = ', '.join(quote_identifier(table) for table in tables)
            cursor.execute(f"TRUNCATE TABLE {quoted_tables} RESTART IDENTITY CASCADE;")
            self.pg_conn.commit()
            self.logger.log("Reset PostgreSQL tables before migration")
        except Exception as e:
            self.logger.error(f"Failed to reset PostgreSQL tables: {e}")
            self.pg_conn.rollback()
            raise
    
    def validate_migration(self):
        """Validate that migration was successful"""
        self.logger.log("Starting migration validation...")
        
        try:
            sqlite_cursor = self.sqlite_conn.cursor()
            pg_cursor = self.pg_conn.cursor()
            
            all_valid = True
            tables = self.get_sqlite_tables()
            
            for table in tables:
                # Get row counts
                sqlite_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier(table)};")
                sqlite_count = sqlite_cursor.fetchone()[0]
                
                pg_cursor.execute(f"SELECT COUNT(*) FROM {quote_identifier(table)};")
                pg_count = pg_cursor.fetchone()[0]
                
                if sqlite_count == pg_count:
                    self.logger.log(f"✓ {table}: {sqlite_count} rows match")
                else:
                    self.logger.warning(f"✗ {table}: SQLite={sqlite_count}, PostgreSQL={pg_count}")
                    all_valid = False
            
            if all_valid:
                self.logger.log("✓ ALL VALIDATIONS PASSED")
            else:
                self.logger.warning("✗ SOME VALIDATIONS FAILED - Review differences above")
            
            return all_valid
        
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
    
    def close_connections(self):
        """Close database connections"""
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.pg_conn:
            self.pg_conn.close()
        self.logger.log("Database connections closed")
    
    def migrate(self):
        """Execute full migration process"""
        # Connect to databases
        if not self.connect_sqlite():
            return False
        
        if not self.connect_postgres():
            return False
        
        # Create tables in PostgreSQL
        if not self.create_tables_in_postgres():
            return False
        
        # Migrate data
        if not self.migrate_all_data():
            return False
        
        # Validate migration
        is_valid = self.validate_migration()
        
        # Close connections
        self.close_connections()
        
        return is_valid


def setup_postgres_database(pg_user, pg_password, pg_host, pg_port, pg_db, logger):
    """Create PostgreSQL database if it doesn't exist"""
    try:
        database_url = os.getenv('DATABASE_URL', '').strip()
        if database_url:
            conn = psycopg.connect(database_url, connect_timeout=10)
            conn.autocommit = True
            cursor = conn.cursor()
            logger.log("PostgreSQL database ready using DATABASE_URL")
            cursor.close()
            conn.close()
            return True

        resolved_host = None
        try:
            resolved_host = socket.gethostbyname(pg_host)
        except socket.gaierror:
            result = subprocess.run(['nslookup', pg_host], capture_output=True, text=True, check=False)
            matches = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', result.stdout)
            if matches:
                resolved_host = matches[-1]
            else:
                raise
        # Connect to default postgres database
        conn = psycopg.connect(
            user=pg_user,
            password=pg_password,
            host=pg_host,
            hostaddr=resolved_host,
            port=pg_port,
            dbname='postgres',
            sslmode='require',
            connect_timeout=10
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # For Supabase, database 'postgres' already exists, so we just use it
        logger.log(f"PostgreSQL database ready: {pg_db} ({resolved_host})")
        
        cursor.close()
        conn.close()
        return True
    
    except psycopg.Error as e:
        logger.error(f"Failed to setup PostgreSQL database: {e}")
        return False
    except socket.gaierror as e:
        logger.error(f"Failed to resolve PostgreSQL host: {e}")
        return False


def main():
    """Main entry point"""
    print("="*80)
    print("SQLite to PostgreSQL Migration Tool")
    print("="*80)
    
    # Configure logging
    logger = MigrationLogger('migration.log')
    
    # SQLite path
    sqlite_path = 'instance/onlinebooking.sqlite3'
    if not Path(sqlite_path).exists():
        logger.error(f"SQLite database not found at {sqlite_path}")
        return False
    
    # PostgreSQL credentials (from environment or defaults)
    pg_user = os.getenv('DB_USER', 'postgres')
    pg_password = os.getenv('DB_PASSWORD', 'password')
    pg_host = os.getenv('DB_HOST', 'localhost')
    pg_port = int(os.getenv('DB_PORT', '5432'))
    pg_db = os.getenv('DB_NAME', 'onlinebooking')
    
    logger.log(f"PostgreSQL Connection: {pg_user}@{pg_host}:{pg_port}/{pg_db}")
    
    # Setup PostgreSQL database
    if not setup_postgres_database(pg_user, pg_password, pg_host, pg_port, pg_db, logger):
        logger.error("Failed to setup PostgreSQL database")
        logger.summary()
        return False
    
    # Create migrator and run migration
    migrator = SQLiteToPostgreMigrator(
        sqlite_path, pg_user, pg_password, pg_host, pg_port, pg_db, logger
    )
    
    success = migrator.migrate()
    
    # Print summary
    logger.summary()
    
    if success:
        print("\n✓ Migration completed successfully!")
        print(f"✓ Check 'migration.log' for detailed information")
        return True
    else:
        print("\n✗ Migration failed or validation did not pass")
        print(f"✗ Check 'migration.log' for error details")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
