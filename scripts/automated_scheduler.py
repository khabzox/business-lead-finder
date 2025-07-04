#!/usr/bin/env python3
"""
Automated Scheduler for Massive Marrakesh Business Search
This script runs automated weekly/monthly searches and manages massive datasets.

Features:
- Automated weekly searches (every Monday)
- Automated monthly mega searches 
- Results archival and management
- Email notifications (optional)
- Data cleanup and optimization
"""

import os
import sys
import time
import schedule
import asyncio
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import json
import zipfile

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.massive_marrakesh_search import MassiveMarrakeshSearch, run_massive_search
from rich.console import Console

console = Console()

class AutomatedSearchScheduler:
    """Manages automated searches and data archival for massive datasets."""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.archive_dir = Path("archive")
        self.results_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for automated searches."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "automated_scheduler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def run_weekly_search(self):
        """Run automated weekly search with medium dataset."""
        self.logger.info("🔄 Starting automated weekly search...")
        console.print("[blue]🔄 Running scheduled weekly Marrakesh search...[/blue]")
        
        try:
            # Weekly search: 50 results per query = ~50,000+ businesses
            total = await run_massive_search(max_per_query=50)
            
            self.logger.info(f"✅ Weekly search completed: {total:,} businesses found")
            console.print(f"[green]✅ Weekly search completed: {total:,} businesses![/green]")
            
            # Archive older weekly results
            await self.archive_old_results("weekly")
            
        except Exception as e:
            self.logger.error(f"❌ Weekly search failed: {e}")
            console.print(f"[red]❌ Weekly search failed: {e}[/red]")
    
    async def run_monthly_mega_search(self):
        """Run automated monthly mega search with massive dataset."""
        self.logger.info("🚀 Starting automated monthly MEGA search...")
        console.print("[blue]🚀 Running scheduled monthly MEGA Marrakesh search...[/blue]")
        
        try:
            # Monthly search: 200 results per query = ~200,000+ businesses
            total = await run_massive_search(max_per_query=200)
            
            self.logger.info(f"✅ Monthly MEGA search completed: {total:,} businesses found")
            console.print(f"[green]✅ Monthly MEGA search completed: {total:,} businesses![/green]")
            
            # Archive older monthly results
            await self.archive_old_results("monthly")
            
            # Generate monthly analytics report
            await self.generate_monthly_analytics()
            
        except Exception as e:
            self.logger.error(f"❌ Monthly MEGA search failed: {e}")
            console.print(f"[red]❌ Monthly MEGA search failed: {e}[/red]")
    
    async def archive_old_results(self, search_type: str):
        """Archive old search results to save space."""
        cutoff_days = 7 if search_type == "weekly" else 30
        cutoff_date = datetime.now() - timedelta(days=cutoff_days)
        
        archived_count = 0
        
        for file_path in self.results_dir.glob("*.json"):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                # Create archive folder for this date
                archive_folder = self.archive_dir / search_type / file_path.stem[:8]  # YYYYMMDD
                archive_folder.mkdir(parents=True, exist_ok=True)
                
                # Move file to archive
                shutil.move(str(file_path), str(archive_folder / file_path.name))
                archived_count += 1
        
        if archived_count > 0:
            self.logger.info(f"📁 Archived {archived_count} old {search_type} result files")
            console.print(f"[yellow]📁 Archived {archived_count} old {search_type} files[/yellow]")
    
    async def generate_monthly_analytics(self):
        """Generate monthly analytics from all search results."""
        console.print("[blue]📊 Generating monthly analytics...[/blue]")
        
        try:
            analytics = {
                'month': datetime.now().strftime("%Y-%m"),
                'generated_date': datetime.now().isoformat(),
                'total_businesses': 0,
                'excellent_leads': 0,
                'high_leads': 0,
                'medium_leads': 0,
                'low_leads': 0,
                'categories': {},
                'areas': {},
                'no_website_businesses': 0,
                'top_opportunities': []
            }
            
            # Process all recent result files
            for file_path in self.results_dir.glob("*marrakesh_massive_search*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                businesses = data.get('businesses', [])
                analytics['total_businesses'] += len(businesses)
                
                for business in businesses:
                    # Count by opportunity level
                    level = business.get('opportunity_level', 'LOW')
                    if level == 'EXCELLENT':
                        analytics['excellent_leads'] += 1
                    elif level == 'HIGH':
                        analytics['high_leads'] += 1
                    elif level == 'MEDIUM':
                        analytics['medium_leads'] += 1
                    else:
                        analytics['low_leads'] += 1
                    
                    # Count by category
                    category = business.get('search_category', 'unknown')
                    analytics['categories'][category] = analytics['categories'].get(category, 0) + 1
                    
                    # Count by area
                    area = business.get('search_area', 'unknown')
                    analytics['areas'][area] = analytics['areas'].get(area, 0) + 1
                    
                    # Count businesses without websites
                    if not business.get('website'):
                        analytics['no_website_businesses'] += 1
                    
                    # Collect top opportunities
                    if business.get('lead_score', 0) >= 85:
                        analytics['top_opportunities'].append({
                            'name': business.get('name', ''),
                            'category': business.get('category', ''),
                            'area': business.get('search_area', ''),
                            'score': business.get('lead_score', 0),
                            'phone': business.get('phone', ''),
                            'rating': business.get('rating', 0)
                        })
            
            # Sort top opportunities by score
            analytics['top_opportunities'].sort(key=lambda x: x['score'], reverse=True)
            analytics['top_opportunities'] = analytics['top_opportunities'][:100]  # Top 100
            
            # Sort categories and areas by count
            analytics['categories'] = dict(sorted(analytics['categories'].items(), key=lambda x: x[1], reverse=True))
            analytics['areas'] = dict(sorted(analytics['areas'].items(), key=lambda x: x[1], reverse=True))
            
            # Save analytics
            analytics_path = self.results_dir / f"monthly_analytics_{datetime.now().strftime('%Y%m')}.json"
            with open(analytics_path, 'w', encoding='utf-8') as f:
                json.dump(analytics, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]📊 Monthly analytics saved: {analytics['total_businesses']:,} businesses analyzed[/green]")
            self.logger.info(f"📊 Monthly analytics generated: {analytics['total_businesses']:,} businesses")
            
        except Exception as e:
            self.logger.error(f"❌ Analytics generation failed: {e}")
            console.print(f"[red]❌ Analytics generation failed: {e}[/red]")
    
    def compress_results(self):
        """Compress old result files to save disk space."""
        console.print("[blue]🗜️ Compressing old result files...[/blue]")
        
        compressed_count = 0
        cutoff_date = datetime.now() - timedelta(days=3)
        
        for file_path in self.results_dir.glob("*.json"):
            if (file_path.stat().st_mtime < cutoff_date.timestamp() and 
                not file_path.name.endswith("_SUMMARY.json") and
                not file_path.name.startswith("monthly_analytics")):
                
                # Create compressed version
                zip_path = file_path.with_suffix('.json.zip')
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(file_path, file_path.name)
                
                # Remove original file
                file_path.unlink()
                compressed_count += 1
        
        if compressed_count > 0:
            console.print(f"[green]🗜️ Compressed {compressed_count} result files[/green]")
            self.logger.info(f"🗜️ Compressed {compressed_count} old result files")
    
    def get_results_summary(self) -> Dict:
        """Get summary of all results in the system."""
        summary = {
            'total_files': 0,
            'total_businesses': 0,
            'total_size_mb': 0,
            'excellent_leads': 0,
            'recent_searches': []
        }
        
        for file_path in self.results_dir.glob("*.json"):
            if file_path.name.endswith("_SUMMARY.json"):
                continue
                
            summary['total_files'] += 1
            summary['total_size_mb'] += file_path.stat().st_size / (1024 * 1024)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    businesses = data.get('businesses', [])
                    summary['total_businesses'] += len(businesses)
                    
                    for business in businesses:
                        if business.get('opportunity_level') == 'EXCELLENT':
                            summary['excellent_leads'] += 1
                    
                    # Track recent searches
                    if len(summary['recent_searches']) < 10:
                        metadata = data.get('metadata', {})
                        summary['recent_searches'].append({
                            'date': metadata.get('search_date', ''),
                            'batch_size': metadata.get('batch_size', 0),
                            'file': file_path.name
                        })
                        
            except Exception as e:
                self.logger.warning(f"Error reading {file_path}: {e}")
        
        return summary
    
    def display_system_status(self):
        """Display current system status and statistics."""
        summary = self.get_results_summary()
        
        from rich.table import Table
        table = Table(title="🚀 Massive Marrakesh Search System Status")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta", justify="right")
        table.add_column("Details", style="green")
        
        table.add_row("Total Result Files", f"{summary['total_files']:,}", "JSON batch files")
        table.add_row("Total Businesses", f"{summary['total_businesses']:,}", "All discovered businesses")
        table.add_row("Excellent Leads", f"{summary['excellent_leads']:,}", "Score 80+ (ready for outreach)")
        table.add_row("Data Size", f"{summary['total_size_mb']:.1f} MB", "Storage used")
        table.add_row("Recent Searches", f"{len(summary['recent_searches'])}", "Last 10 search operations")
        
        console.print(table)
        
        from rich.panel import Panel
        panel = Panel(
            f"System running with {summary['total_businesses']:,} businesses discovered!\n"
            f"🎯 {summary['excellent_leads']:,} excellent leads ready for outreach\n"
            f"📁 Data stored in {summary['total_files']:,} JSON files\n"
            f"💾 Using {summary['total_size_mb']:.1f} MB storage",
            title="System Status",
            border_style="green"
        )
        console.print(panel)

def setup_scheduled_searches():
    """Setup and run the automated search scheduler."""
    scheduler = AutomatedSearchScheduler()
    
    console.print("[blue]🔄 Setting up automated Marrakesh business searches...[/blue]")
    
    # Define scheduled functions
    def weekly_search_job():
        asyncio.run(scheduler.run_weekly_search())
    
    def monthly_search_job():
        asyncio.run(scheduler.run_monthly_mega_search())
    
    def compression_job():
        scheduler.compress_results()
    
    # Schedule jobs
    schedule.every().monday.at("09:00").do(weekly_search_job)
    schedule.every().first.day.at("06:00").do(monthly_search_job)  # First day of month
    schedule.every().day.at("02:00").do(compression_job)  # Daily compression at 2 AM
    
    console.print("[green]✅ Automated searches configured:[/green]")
    console.print("   📅 Weekly Search: Every Monday at 9:00 AM (~50,000+ businesses)")
    console.print("   📅 Monthly MEGA: First day of month at 6:00 AM (~200,000+ businesses)")
    console.print("   📅 Compression: Daily at 2:00 AM (saves disk space)")
    
    scheduler.display_system_status()
    
    console.print("\n[yellow]Scheduler is now running. Press Ctrl+C to stop.[/yellow]")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        console.print("\n[yellow]Scheduler stopped.[/yellow]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Marrakesh Business Search Scheduler")
    parser.add_argument("--start", action="store_true", help="Start the automated scheduler")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--test-weekly", action="store_true", help="Run test weekly search")
    parser.add_argument("--test-monthly", action="store_true", help="Run test monthly search")
    
    args = parser.parse_args()
    
    scheduler = AutomatedSearchScheduler()
    
    if args.status:
        scheduler.display_system_status()
    elif args.test_weekly:
        console.print("[blue]🧪 Running test weekly search...[/blue]")
        asyncio.run(scheduler.run_weekly_search())
    elif args.test_monthly:
        console.print("[blue]🧪 Running test monthly search...[/blue]")
        asyncio.run(scheduler.run_monthly_mega_search())
    elif args.start:
        setup_scheduled_searches()
    else:
        console.print("[yellow]Use --start to begin automated searches, --status to see current data[/yellow]")
        parser.print_help()
