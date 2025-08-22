🇬🇧 UK Crime Analysis: From Local Observation to Actionable Insight 🔍
Project Overview
This project demonstrates how a simple, local observation can be scaled into a comprehensive data analysis to uncover broader trends. It began with noticing frequent shoplifting incidents in Oxford and asking a key question: Is this a local problem, or a pattern worth investigating across the UK?.


To answer this, I analysed over 

600,000 crime records from the past two years, covering three major UK police forces: Thames Valley Police (Oxford), Cambridgeshire Constabulary (Cambridge), and the Metropolitan Police Service (London).

The goal was to transform an everyday issue into 

actionable insights that could be valuable for public safety, retail risk, and urban planning.

💡 Key Findings & Insights
The analysis yielded three main insights:

1. The Concern is Real: Crime is Geographically Concentrated 📍
The initial gut feeling about shoplifting in Oxford was validated by the data. The hotspot analysis clearly shows that incidents are not random but are 

highly concentrated in Oxford’s commercial centre. This confirms that high-footfall commercial areas are significant focal points for this type of crime.


2. Prioritisation is Key: Identifying Chronic Issues ⚖️
To help allocate focus and resources, I developed a 

Crime Priority Matrix. This tool plots crime volume against the "unsolved" rate to identify which issues are draining resources the most.


For Oxford, the matrix shows that 

Shoplifting and Bicycle Theft are chronic issues—they occur in high volumes but have low resolution rates.

3. Location Matters: The "Spatial Fingerprint" of Crime 🗺️
A one-size-fits-all strategy for policing doesn't work because different crimes have unique "spatial fingerprints". For example, commercial crimes like 

Shoplifting are clustered in the city centre, while residential crimes like Burglary are concentrated in different zones entirely. This highlights the need for location-specific strategies.

<p float="left">
<img src="https://www.google.com/search?q=https://storage.googleapis.com/static.a-shared-brain.com/images/github-readme/22082025-5.png" width="49%" alt="Burglary Hotspots in Oxford" />
<img src="https://www.google.com/search?q=https://storage.googleapis.com/static.a-shared-brain.com/images/github-readme/22082025-6.png" width="49%" alt="Public order hotspots in Oxford" />
</p>

📊 Comparative Analysis: Oxford 🆚 Cambridge & London
The analysis was expanded to compare crime trends across the three police forces. This provides a broader context for Oxford's local challenges.

Overall Crime Rate: The Metropolitan Police Service has the highest average annual crime rate, followed by Cambridgeshire Constabulary and then Thames Valley Police.

Top Crime Types: While all three forces deal with similar crime types, the scale is vastly different. The Metropolitan Police Service records significantly higher volumes of crimes like "Violence and sexual offences" and "Other theft" compared to the other two forces.

Seasonality of Crime 📅: Certain crimes show distinct seasonal patterns. Shoplifting and Bicycle Theft incidents tend to peak during specific months of the year, with notable variations between the police forces.

🛠️ Tools & Methodology
Tools: Python 🐍, Pandas 🐼, Matplotlib, Seaborn, Folium/GeoPandas.

Analysis Techniques 🧠:

Hotspot Analysis: Kernel Density Estimation (KDE) to identify geographic clusters of crime.

Priority Matrix: A custom 2x2 matrix plotting crime volume against the unsolved rate to categorise issues from "Well-Managed" to "Chronic Problems."

Comparative Analysis: Aggregating and comparing crime statistics across different police force jurisdictions.

📂 Data Source
The analysis is based on over 600,000 crime records from the past 2 years, sourced from official UK police data portals. The data covers the Thames Valley Police, Cambridgeshire Constabulary, and Metropolitan Police Service jurisdictions.
