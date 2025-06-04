# NHS Performance Dashboard

An interactive dashboard for visualizing NHS performance metrics across England.  
The project combines datasets such as referral-to-treatment waiting times, A&E admissions, avoidable mortality, and population deprivation levels to support data-driven insights.

The dashboard is currently in development. Initial stages involve dataset review, cleaning, and setting up the application structure.

## Project Structure

```
NHS-Performance-Dashboard/
├── src/             # Python scripts (data loading, cleaning, visualization functions, Dash app files)
├── notebooks/       # Jupyter notebooks for exploration, prototyping, and testing
├── data/            # Final cleaned datasets that will be used for the dashboard
├── final_outputs/   # Images, plots, exports, or dashboard screenshots for report/presentation
├── docs/            # Project documentation (notes, diagrams, references, methodology)
├── README.md        # Overview of the project
└── .gitignore       # Tells Git which files/folders to ignore (e.g., raw data or temporary files)
```
## Current Prototype

This dashboard was built using [Panel](https://panel.holoviz.org/) It visualises NHS England's performance data, focusing on referral-to-treatment (RTT) wait times and healthcare access disparities providing a regional performance comparison and service breakdown.

📄 [View the notebook](notebooks/nhs_dashboard_panel.ipynb)  
🌐 [View the exported HTML](final_outputs/nhs_dashboard_panel.html)

*Note: The final thesis version will be rebuilt using Dash for better performance and scalability.*
