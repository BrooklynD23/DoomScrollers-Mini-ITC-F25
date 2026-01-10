#!/usr/bin/env python3
"""
MissaTech Security Monitoring Dashboard
Real-time GUI for tracking breach metrics and KPIs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from PIL import Image, ImageTk

from src.data.database import get_all_incidents
from src.analysis.breach_analysis import (
    generate_executive_summary,
    cost_analysis_by_dimension,
    risk_score_calculation,
    detection_response_analysis
)


class MissaTechDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("MissaTech Security Monitoring Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a202c')

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # Load data
        self.refresh_data()

        # Create main layout
        self.create_layout()

    def configure_styles(self):
        """Configure ttk styles for dark theme."""
        self.style.configure('Dashboard.TFrame', background='#1a202c')
        self.style.configure('Card.TFrame', background='#2d3748')
        self.style.configure('Header.TLabel',
                           background='#1a202c',
                           foreground='#ffffff',
                           font=('Segoe UI', 24, 'bold'))
        self.style.configure('KPI.TLabel',
                           background='#2d3748',
                           foreground='#ffffff',
                           font=('Segoe UI', 28, 'bold'))
        self.style.configure('KPITitle.TLabel',
                           background='#2d3748',
                           foreground='#a0aec0',
                           font=('Segoe UI', 10))
        self.style.configure('Status.TLabel',
                           background='#2d3748',
                           foreground='#68d391',
                           font=('Segoe UI', 9))
        self.style.configure('Alert.TLabel',
                           background='#2d3748',
                           foreground='#fc8181',
                           font=('Segoe UI', 10, 'bold'))
        self.style.configure('Refresh.TButton',
                           font=('Segoe UI', 10))

    def refresh_data(self):
        """Load fresh data from database."""
        try:
            self.df = get_all_incidents()
            self.summary = generate_executive_summary()
            self.system_costs = cost_analysis_by_dimension('system_name')
            self.risk_scores = risk_score_calculation().head(5)
            self.detection_stats = detection_response_analysis()
        except Exception as e:
            messagebox.showerror("Data Error", f"Failed to load data: {str(e)}")

    def create_layout(self):
        """Create the main dashboard layout."""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dashboard.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header_frame = ttk.Frame(main_frame, style='Dashboard.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(header_frame,
                               text="MissaTech Security Dashboard",
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT)

        refresh_btn = ttk.Button(header_frame,
                                text="Refresh Data",
                                command=self.on_refresh,
                                style='Refresh.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=5)

        # KPI Cards Row
        kpi_frame = ttk.Frame(main_frame, style='Dashboard.TFrame')
        kpi_frame.pack(fill=tk.X, pady=(0, 15))

        self.create_kpi_cards(kpi_frame)

        # Charts Row
        charts_frame = ttk.Frame(main_frame, style='Dashboard.TFrame')
        charts_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Charts
        left_frame = ttk.Frame(charts_frame, style='Dashboard.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.create_system_chart(left_frame)
        self.create_detection_chart(left_frame)

        # Right column - Tables and alerts
        right_frame = ttk.Frame(charts_frame, style='Dashboard.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.create_risk_table(right_frame)
        self.create_alerts_panel(right_frame)

    def create_kpi_cards(self, parent):
        """Create KPI metric cards."""
        kpis = [
            ("Total Cost", f"${self.summary['total_cost']/1e6:.1f}M", "#fc8181"),
            ("Avg Detection", f"{self.summary['avg_detection_days']:.1f} days", "#f6ad55"),
            ("Avg Response", f"{self.summary['avg_response_days']:.1f} days", "#68d391"),
            ("Records Exposed", f"{self.summary['total_records_exposed']/1e6:.2f}M", "#63b3ed"),
            ("High Sensitivity", f"{self.summary['highest_sensitivity_incidents']}", "#b794f4"),
        ]

        for i, (title, value, color) in enumerate(kpis):
            card = tk.Frame(parent, bg='#2d3748', relief=tk.FLAT)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

            # Color indicator
            indicator = tk.Frame(card, bg=color, height=4)
            indicator.pack(fill=tk.X)

            # Content
            content = tk.Frame(card, bg='#2d3748')
            content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

            tk.Label(content, text=title, bg='#2d3748', fg='#a0aec0',
                    font=('Segoe UI', 9)).pack(anchor=tk.W)
            tk.Label(content, text=value, bg='#2d3748', fg='#ffffff',
                    font=('Segoe UI', 20, 'bold')).pack(anchor=tk.W)

    def create_system_chart(self, parent):
        """Create system cost chart."""
        card = tk.Frame(parent, bg='#2d3748')
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        tk.Label(card, text="Cost by System", bg='#2d3748', fg='#ffffff',
                font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)

        fig = Figure(figsize=(6, 3), facecolor='#2d3748')
        ax = fig.add_subplot(111)

        systems = self.system_costs['system_name'].tolist()
        costs = (self.system_costs['total_cost'] / 1e6).tolist()
        colors = ['#fc8181', '#f6ad55', '#68d391', '#63b3ed', '#b794f4']

        bars = ax.barh(systems, costs, color=colors)
        ax.set_xlabel('Cost (Millions USD)', color='#a0aec0')
        ax.set_facecolor('#2d3748')
        ax.tick_params(colors='#a0aec0')
        for spine in ax.spines.values():
            spine.set_color('#4a5568')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_detection_chart(self, parent):
        """Create detection/response time chart."""
        card = tk.Frame(parent, bg='#2d3748')
        card.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        tk.Label(card, text="Detection & Response Times", bg='#2d3748', fg='#ffffff',
                font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)

        fig = Figure(figsize=(6, 3), facecolor='#2d3748')
        ax = fig.add_subplot(111)

        systems = self.detection_stats['system_name'].tolist()
        x = range(len(systems))
        width = 0.35

        detection = self.detection_stats['avg_detection'].tolist()
        response = self.detection_stats['avg_response'].tolist()

        ax.bar([i - width/2 for i in x], detection, width, label='Detection', color='#f6ad55')
        ax.bar([i + width/2 for i in x], response, width, label='Response', color='#68d391')

        ax.set_ylabel('Days', color='#a0aec0')
        ax.set_xticks(x)
        ax.set_xticklabels(systems)
        ax.legend(facecolor='#2d3748', edgecolor='#4a5568', labelcolor='#ffffff')
        ax.set_facecolor('#2d3748')
        ax.tick_params(colors='#a0aec0')
        for spine in ax.spines.values():
            spine.set_color('#4a5568')

        # Target line
        ax.axhline(y=3, color='#fc8181', linestyle='--', linewidth=1, label='Target')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_risk_table(self, parent):
        """Create high-risk combinations table."""
        card = tk.Frame(parent, bg='#2d3748')
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        tk.Label(card, text="High-Risk System-Region Combinations",
                bg='#2d3748', fg='#ffffff',
                font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)

        # Create treeview
        columns = ('System', 'Region', 'Risk Score', 'Cost')
        tree = ttk.Treeview(card, columns=columns, show='headings', height=5)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for _, row in self.risk_scores.iterrows():
            tree.insert('', tk.END, values=(
                row['system_name'],
                row['region'],
                f"{row['risk_score']:.1f}/100",
                f"${row['total_cost']/1e6:.2f}M"
            ))

        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_alerts_panel(self, parent):
        """Create alerts and recommendations panel."""
        card = tk.Frame(parent, bg='#2d3748')
        card.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        tk.Label(card, text="Active Alerts & Recommendations",
                bg='#2d3748', fg='#ffffff',
                font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)

        alerts_frame = tk.Frame(card, bg='#2d3748')
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        alerts = [
            ("CRITICAL", "Billing system requires immediate security audit", "#fc8181"),
            ("CRITICAL", "72% of incidents from misconfiguration", "#fc8181"),
            ("HIGH", "Detection time exceeds 3-day target", "#f6ad55"),
            ("HIGH", "HR system has 13+ day avg detection", "#f6ad55"),
            ("MEDIUM", "Regional security not standardized", "#68d391"),
        ]

        for severity, message, color in alerts:
            alert_row = tk.Frame(alerts_frame, bg='#2d3748')
            alert_row.pack(fill=tk.X, pady=2)

            tk.Label(alert_row, text=f"[{severity}]", bg='#2d3748', fg=color,
                    font=('Segoe UI', 9, 'bold'), width=10).pack(side=tk.LEFT)
            tk.Label(alert_row, text=message, bg='#2d3748', fg='#e2e8f0',
                    font=('Segoe UI', 9), wraplength=300).pack(side=tk.LEFT, padx=5)

    def on_refresh(self):
        """Refresh all dashboard data."""
        self.refresh_data()
        # Clear and rebuild
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_layout()
        messagebox.showinfo("Refresh", "Dashboard data refreshed successfully!")


def launch_dashboard():
    """Launch the monitoring dashboard."""
    root = tk.Tk()
    app = MissaTechDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    launch_dashboard()
