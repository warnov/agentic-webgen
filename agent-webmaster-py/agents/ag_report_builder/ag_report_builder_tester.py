# File: ag_report_builder_tester.py
import os
import sys
import json
import time
import webbrowser
import tempfile
import uuid
from datetime import datetime

# Ensure current directory is on Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from ag_report_builder import AgentModule

class ReportTester:
    def __init__(self):
        """Initialize the report tester with agent module."""
        self.agent_module = AgentModule()
        self.client = self.agent_module.client
        self.agent = self.agent_module.instance
        self.generated_reports = []  # Track generated reports for easy access
        
    def get_sample_datasets(self):
        """Return a dictionary of sample datasets for different report types."""
        return {
            "1": {
                "name": "📊 Sales Performance Dashboard",
                "description": "Monthly sales data with revenue and units sold",
                "data": {
                    "sales_data": [
                        {"month": "January", "revenue": 85000, "units_sold": 340, "region": "North"},
                        {"month": "February", "revenue": 92000, "units_sold": 380, "region": "North"},
                        {"month": "March", "revenue": 78000, "units_sold": 295, "region": "North"},
                        {"month": "January", "revenue": 65000, "units_sold": 250, "region": "South"},
                        {"month": "February", "revenue": 71000, "units_sold": 275, "region": "South"},
                        {"month": "March", "revenue": 89000, "units_sold": 350, "region": "South"}
                    ],
                    "metadata": {
                        "report_period": "Q1 2025",
                        "currency": "USD",
                        "generated_at": datetime.now().isoformat()
                    }
                },
                "prompt": "Create a comprehensive sales performance dashboard showing monthly trends, regional comparison, and key metrics. Include charts for revenue trends and units sold by region."
            },
            "2": {
                "name": "👥 Employee Analytics Report",
                "description": "Employee demographics and performance metrics",
                "data": {
                    "employees": [
                        {"id": 1, "name": "Alice Johnson", "department": "Engineering", "salary": 95000, "performance_rating": 4.8, "years_experience": 5},
                        {"id": 2, "name": "Bob Smith", "department": "Marketing", "salary": 72000, "performance_rating": 4.2, "years_experience": 3},
                        {"id": 3, "name": "Carol Davis", "department": "Engineering", "salary": 110000, "performance_rating": 4.9, "years_experience": 8},
                        {"id": 4, "name": "David Wilson", "department": "Sales", "salary": 68000, "performance_rating": 4.1, "years_experience": 2},
                        {"id": 5, "name": "Emma Brown", "department": "HR", "salary": 75000, "performance_rating": 4.6, "years_experience": 4},
                        {"id": 6, "name": "Frank Miller", "department": "Engineering", "salary": 88000, "performance_rating": 4.3, "years_experience": 4}
                    ],
                    "department_summary": {
                        "Engineering": {"count": 3, "avg_salary": 97667, "avg_rating": 4.67},
                        "Marketing": {"count": 1, "avg_salary": 72000, "avg_rating": 4.2},
                        "Sales": {"count": 1, "avg_salary": 68000, "avg_rating": 4.1},
                        "HR": {"count": 1, "avg_salary": 75000, "avg_rating": 4.6}
                    }
                },
                "prompt": "Generate an employee analytics report with department breakdowns, salary distributions, performance ratings, and experience levels. Include both detailed tables and visual charts."
            },
            "3": {
                "name": "💰 Financial Summary Report",
                "description": "Quarterly financial data with expenses and profit margins",
                "data": {
                    "quarterly_financials": [
                        {"quarter": "Q1 2024", "revenue": 2500000, "expenses": 1800000, "profit": 700000, "profit_margin": 28.0},
                        {"quarter": "Q2 2024", "revenue": 2800000, "expenses": 1950000, "profit": 850000, "profit_margin": 30.4},
                        {"quarter": "Q3 2024", "revenue": 3200000, "expenses": 2100000, "profit": 1100000, "profit_margin": 34.4},
                        {"quarter": "Q4 2024", "revenue": 3500000, "expenses": 2300000, "profit": 1200000, "profit_margin": 34.3}
                    ],
                    "expense_breakdown": {
                        "Q4 2024": {
                            "personnel": 1200000,
                            "marketing": 400000,
                            "operations": 500000,
                            "technology": 200000
                        }
                    },
                    "kpis": {
                        "annual_growth": 40.0,
                        "avg_profit_margin": 31.8,
                        "total_annual_revenue": 12000000
                    }
                },
                "prompt": "Create a comprehensive financial summary report showing quarterly performance trends, expense breakdowns, profit margins, and key financial indicators."
            },
            "4": {
                "name": "📈 Customer Analytics Dashboard",
                "description": "Customer behavior and satisfaction metrics",
                "data": {
                    "customer_metrics": [
                        {"month": "January", "new_customers": 245, "churn_rate": 3.2, "satisfaction_score": 4.3, "avg_order_value": 157},
                        {"month": "February", "new_customers": 298, "churn_rate": 2.8, "satisfaction_score": 4.4, "avg_order_value": 162},
                        {"month": "March", "new_customers": 312, "churn_rate": 2.5, "satisfaction_score": 4.6, "avg_order_value": 171},
                        {"month": "April", "new_customers": 278, "churn_rate": 2.9, "satisfaction_score": 4.5, "avg_order_value": 165}
                    ],
                    "customer_segments": {
                        "Premium": {"count": 450, "avg_ltv": 2800, "satisfaction": 4.7},
                        "Standard": {"count": 1200, "avg_ltv": 1200, "satisfaction": 4.3},
                        "Basic": {"count": 800, "avg_ltv": 600, "satisfaction": 4.1}
                    },
                    "feedback_summary": {
                        "total_reviews": 1247,
                        "avg_rating": 4.4,
                        "response_rate": 23.5
                    }
                },
                "prompt": "Build a customer analytics dashboard showing acquisition trends, churn analysis, satisfaction metrics, and customer segmentation insights."
            },
            "5": {
                "name": "🏭 Operations Performance Report",
                "description": "Manufacturing and operational efficiency metrics",
                "data": {
                    "production_data": [
                        {"facility": "Plant A", "month": "March", "units_produced": 15400, "efficiency": 92.3, "downtime_hours": 48, "quality_score": 96.8},
                        {"facility": "Plant B", "month": "March", "units_produced": 12800, "efficiency": 89.1, "downtime_hours": 72, "quality_score": 94.2},
                        {"facility": "Plant C", "month": "March", "units_produced": 18200, "efficiency": 94.7, "downtime_hours": 36, "quality_score": 97.5}
                    ],
                    "supply_chain": {
                        "supplier_performance": {
                            "on_time_delivery": 94.2,
                            "quality_rating": 96.1,
                            "cost_variance": -2.3
                        },
                        "inventory_levels": {
                            "raw_materials": 85.4,
                            "work_in_progress": 23.7,
                            "finished_goods": 67.2
                        }
                    },
                    "safety_metrics": {
                        "incidents": 2,
                        "days_without_incident": 45,
                        "safety_training_completion": 98.5
                    }
                },
                "prompt": "Generate an operations performance report covering production efficiency, quality metrics, supply chain performance, and safety indicators."
            }
        }
    
    def display_header(self):
        """Display the application header with branding."""
        print("╔" + "═" * 60 + "╗")
        print("║" + " " * 60 + "║")
        print("║" + " 🚀 AGENTIC REPORT BUILDER - TEST SUITE 🚀 ".center(60) + "║")
        print("║" + " " * 60 + "║")
        print("║" + " Generate Beautiful Reports from Sample Datasets ".center(60) + "║")
        print("║" + " 🌐 Reports auto-open in your default browser! ".center(60) + "║")
        print("║" + " " * 60 + "║")
        print("╚" + "═" * 60 + "╝")
        print()
        
    def display_menu(self, datasets):
        """Display the interactive menu with available datasets."""
        print("┌" + "─" * 58 + "┐")
        print("│" + " 📋 AVAILABLE DATASET TEMPLATES ".center(58) + "│")
        print("├" + "─" * 58 + "┤")
        
        for key, dataset in datasets.items():
            print(f"│ {key}. {dataset['name']:<48} │")
            print(f"│    {dataset['description']:<51} │")
            print("├" + "─" * 58 + "┤")
            
        print("│ 6. 🔄 Generate Custom Report (Enter your own data)     │")
        if self.generated_reports:
            print("│ 7. 📂 View Previously Generated Reports                │")
        print("│ 0. 🚪 Exit                                            │")
        print("└" + "─" * 58 + "┘")
        print()
        
    def get_custom_data(self):
        """Allow user to input custom JSON data."""
        print("📝 Enter your custom JSON data (press Enter twice to finish):")
        print("Example: {\"users\": [{\"name\": \"John\", \"age\": 30}]}")
        print()
        
        lines = []
        while True:
            try:
                line = input()
                if line == "" and lines:
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Custom data input cancelled.")
                return None
                
        if not lines:
            print("❌ No data provided.")
            return None
            
        try:
            data_str = "\n".join(lines)
            data = json.loads(data_str)
            
            print("\n📊 Enter a description for your report:")
            description = input("Prompt: ").strip()
            
            if not description:
                description = "Create a comprehensive report from the provided dataset."
                
            return {"data": data, "prompt": description}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON format: {e}")
            return None
    
    def generate_report(self, dataset_info):
        """Generate a report using the selected dataset."""
        print(f"\n🎯 Selected: {dataset_info['name']}")
        print(f"📝 Description: {dataset_info['description']}")
        print("─" * 60)
        
        # Prepare the prompt with data
        full_prompt = f"{dataset_info['prompt']}\n\nDataset:\n{json.dumps(dataset_info['data'], indent=2)}"
        
        try:
            # Create thread and send message
            thread = self.client.threads.create()
            self.client.messages.create(
                thread_id=thread.id, 
                role="user", 
                content=full_prompt
            )
            
            print("⏳ Generating report... This may take a moment.")
            print("🔄 The agent is analyzing data and creating visualizations...")
            
            # Start the run
            start_time = time.time()
            run = self.client.runs.create_and_process(
                thread_id=thread.id, 
                agent_id=self.agent.id
            )
            
            generation_time = time.time() - start_time
            
            if run.status == "completed":
                print(f"✅ Report generated successfully in {generation_time:.1f} seconds!")
                print("─" * 60)
                
                # Get the assistant's response
                for msg in reversed(list(self.client.messages.list(thread_id=thread.id))):
                    if msg.role == "assistant":
                        html_content = msg.content[0].text.value if hasattr(msg.content[0], "text") else str(msg.content)
                        
                        # Generate a unique filename with timestamp and random ID
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        random_id = str(uuid.uuid4())[:8]  # First 8 characters of UUID
                        filename = f"report_{timestamp}_{random_id}.html"
                        
                        try:
                            # Save to file
                            file_path = os.path.abspath(filename)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            
                            # Track the generated report
                            report_info = {
                                "filename": filename,
                                "path": file_path,
                                "timestamp": datetime.now(),
                                "dataset_name": dataset_info['name']
                            }
                            self.generated_reports.append(report_info)
                            
                            print(f"💾 Report saved as: {filename}")
                            print(f"📁 Full path: {file_path}")
                            
                            # Open in default browser
                            try:
                                print("🌐 Opening report in your default browser...")
                                webbrowser.open(f'file://{file_path}')
                                print("✨ Report opened successfully!")
                            except Exception as browser_error:
                                print(f"⚠️  Could not open browser automatically: {browser_error}")
                                print(f"🌐 Please manually open: {file_path}")
                                
                        except Exception as e:
                            # Fallback: Save to temp directory and try to open
                            print(f"⚠️  Could not save to current directory: {e}")
                            try:
                                # Create temp file
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
                                    temp_file.write(html_content)
                                    temp_path = temp_file.name
                                
                                print(f"💾 Report saved to temporary location: {temp_path}")
                                
                                # Try to open temp file
                                try:
                                    print("🌐 Opening report in your default browser...")
                                    webbrowser.open(f'file://{temp_path}')
                                    print("✨ Report opened successfully!")
                                except Exception as browser_error:
                                    print(f"⚠️  Could not open browser: {browser_error}")
                                    print("📄 HTML Content (first 500 chars):")
                                    print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
                                    
                            except Exception as temp_error:
                                print(f"❌ Could not create temp file: {temp_error}")
                                print("📄 HTML Content (first 500 chars):")
                                print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
                        break
            else:
                print(f"❌ Report generation failed with status: {run.status}")
                if getattr(run, "last_error", None):
                    print(f"🔍 Error details: {run.last_error}")
                    
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        print("\n" + "=" * 60)
        input("Press Enter to continue...")
    
    def view_previous_reports(self):
        """Display and allow user to re-open previously generated reports."""
        if not self.generated_reports:
            print("\n📭 No reports have been generated yet.")
            print("🚀 Generate some reports first!")
            input("Press Enter to continue...")
            return
            
        print("\n" + "─" * 60)
        print("📂 PREVIOUSLY GENERATED REPORTS")
        print("─" * 60)
        
        for i, report in enumerate(self.generated_reports, 1):
            time_str = report['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {report['dataset_name']}")
            print(f"   📅 Generated: {time_str}")
            print(f"   📁 File: {report['filename']}")
            print(f"   📍 Path: {report['path']}")
            
            # Check if file still exists
            if os.path.exists(report['path']):
                print("   ✅ Status: File exists")
            else:
                print("   ❌ Status: File not found")
            print()
        
        print("Options:")
        print("• Enter a number (1-{}) to re-open a report".format(len(self.generated_reports)))
        print("• Press Enter to return to main menu")
        
        try:
            choice = input("\n🎯 Select option: ").strip()
            
            if choice == "":
                return
                
            choice_num = int(choice)
            if 1 <= choice_num <= len(self.generated_reports):
                report = self.generated_reports[choice_num - 1]
                
                if os.path.exists(report['path']):
                    try:
                        print(f"🌐 Opening {report['filename']} in your browser...")
                        webbrowser.open(f'file://{report["path"]}')
                        print("✨ Report opened successfully!")
                    except Exception as e:
                        print(f"❌ Could not open browser: {e}")
                        print(f"🔗 Manual path: {report['path']}")
                else:
                    print(f"❌ File no longer exists: {report['path']}")
            else:
                print("❌ Invalid selection.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            
        input("\nPress Enter to continue...")
        
    def run_interactive_menu(self):
        """Run the main interactive menu loop."""
        datasets = self.get_sample_datasets()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
            self.display_header()
            self.display_menu(datasets)
            
            try:
                max_option = "7" if self.generated_reports else "6"
                choice = input(f"🎯 Select an option (0-{max_option}): ").strip()
                
                if choice == "0":
                    print("\n👋 Thank you for using Agentic Report Builder!")
                    print("🚀 Happy reporting!")
                    break
                elif choice in datasets:
                    self.generate_report(datasets[choice])
                elif choice == "6":
                    print("\n" + "─" * 60)
                    custom_data = self.get_custom_data()
                    if custom_data:
                        custom_dataset = {
                            "name": "🔧 Custom Dataset Report",
                            "description": "User-provided custom data",
                            "data": custom_data["data"],
                            "prompt": custom_data["prompt"]
                        }
                        self.generate_report(custom_dataset)
                elif choice == "7" and self.generated_reports:
                    self.view_previous_reports()
                else:
                    print(f"\n❌ Invalid option: '{choice}'. Please select 0-{max_option}.")
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point for the report tester."""
    try:
        tester = ReportTester()
        tester.run_interactive_menu()
    except Exception as e:
        print(f"❌ Failed to initialize report tester: {e}")
        print("🔍 Make sure your Azure AI credentials are properly configured.")

if __name__ == "__main__":
    main()
