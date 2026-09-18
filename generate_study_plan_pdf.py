"""
InsightOS - 10-Day Master Study Plan PDF Generator
Generates a comprehensive, beautifully styled PDF guide for interview preparation.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically add 'Page X of Y' footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "InsightOS — 10-Day Master Learning & Interview Preparation Blueprint")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "InsightOS • Python • Pandas • Scikit-Learn • PostgreSQL • GenAI/RAG")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def create_study_plan_pdf(output_filename="InsightOS_10_Day_Master_Study_Plan.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    C_PRIMARY = colors.HexColor("#0F172A")    # Deep Slate / Navy
    C_ACCENT = colors.HexColor("#2563EB")     # Royal Blue
    C_TEXT = colors.HexColor("#1E293B")       # Body Text
    C_MUTED = colors.HexColor("#475569")      # Subtitle / Muted
    C_BORDER = colors.HexColor("#E2E8F0")     # Light Gray Border
    C_LIGHT_BG = colors.HexColor("#F8FAFC")   # Card Background
    C_GREEN = colors.HexColor("#059669")      # Success / Callout

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_PRIMARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_ACCENT,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=C_PRIMARY,
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_ACCENT,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=4
    )

    q_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#B45309"),
        spaceBefore=4,
        spaceAfter=2
    )

    ans_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=C_TEXT,
        leftIndent=10,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # COVER / HEADER SECTION
    # =========================================================================
    story.append(Paragraph("InsightOS — 10-Day Master Study Plan", title_style))
    story.append(Paragraph("Comprehensive Interview Preparation Blueprint (From Zero to Job-Ready)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceAfter=14))

    intro_text = (
        "<b>Namaste & Welcome!</b> Yeh document specially aapke liye banaya gaya hai taaki aap <b>InsightOS</b> ke har single "
        "component ko basic se lekar advanced level tak asani se samajh sakein. Agar aapko data analysis, SQL ya Machine Learning ka "
        "koi purana background nahi hai, toh bhi yeh plan aapko <b>10 din mein interview-ready</b> bana dega.<br/><br/>"
        "<b>Aapka Daily Target (60 Minutes Total):</b><br/>"
        "• <b>20 Mins</b>: Hamari batayi hui exact short targeted video dekhein.<br/>"
        "• <b>20 Mins</b>: InsightOS ke project code mein dekhein ki yeh feature kahan aur kaise likha gaya hai.<br/>"
        "• <b>20 Mins</b>: Interview Questions & Answers ko bol kar practice karein."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 10-DAY SUMMARY TABLE
    # =========================================================================
    table_data = [
        ["Day", "Core Domain", "Topic & Real-World Concept", "Target File", "Video Time"],
        ["Day 1", "Python & Pandas", "DataFrames, Series & Vectorized Math", "data/generator.py", "15 Mins"],
        ["Day 2", "Data Cleaning & EDA", "Missing Values, IQR Outliers & Correlation", "ingestion/eda_engine.py", "10 Mins"],
        ["Day 3", "Database & SQL", "PostgreSQL Schema, Primary/Foreign Keys, Joins", "database/schema.sql", "12 Mins"],
        ["Day 4", "Advanced SQL", "Window Functions (LAG, DENSE_RANK) & CTEs", "database/analytics_queries.py", "18 Mins"],
        ["Day 5", "Machine Learning", "Customer Churn Prediction (Random Forest & Recall)", "ml/churn_predictor.py", "15 Mins"],
        ["Day 6", "Machine Learning", "Customer Personas (RFM & K-Means Clustering)", "ml/customer_segmentation.py", "12 Mins"],
        ["Day 7", "Machine Learning", "Sales Forecasting (Lags & 90% Confidence Bands)", "ml/sales_forecaster.py", "15 Mins"],
        ["Day 8", "Machine Learning", "Transaction Anomaly Detection (Isolation Forest)", "ml/anomaly_detector.py", "12 Mins"],
        ["Day 9", "GenAI & RAG", "Retrieval-Augmented Generation & Executive Briefs", "ai_analyst/rag_engine.py", "14 Mins"],
        ["Day 10", "Full-Stack & Prep", "Streamlit Architecture, Resume Pitch & Mock Q&A", "app.py, ui/styles.py", "15 Mins"],
    ]

    t = Table(table_data, colWidths=[42, 90, 182, 120, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), C_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # =========================================================================
    # DETAILED DAY BY DAY BREAKDOWN
    # =========================================================================
    days_content = [
        {
            "day": "Day 1: Python for Data Analysis & Pandas Essentials",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Pandas ko Excel ka supercharged digital version samjhiye. Excel mein 10 lakh rows "
                "aate hi computer hang ho jata hai, lekin Pandas billions of rows ko memory mein seconds ke andar filter, group aur "
                "calculate kar deta hai.<br/>"
                "• <b>Series:</b> Excel ka ek single column.<br/>"
                "• <b>DataFrame:</b> Poora Excel sheet/table (Rows aur Columns).<br/>"
                "• <b>Vectorized Math:</b> Bina for-loop lagaye poore column ke numbers ko ek sath multiply ya add karna."
            ),
            "video_title": "Pandas in 15 Minutes by Alex The Analyst",
            "video_search": "Search YouTube: 'Alex The Analyst Pandas in 15 minutes'",
            "video_time": "Exact Duration: 0:00 to 15:30 (Watch full 15 minutes)",
            "code_file": "data/generator.py (Lines 35–110)",
            "code_explanation": (
                "Humne 1,200 customer accounts aur 12,000 transaction receipts create karne ke liye <code>pd.DataFrame()</code> use kiya. "
                "Line 95 dekhiye: <code>txns_df['net_profit'] = txns_df['total_amount'] - (txns_df['cost_price'] * txns_df['quantity'])</code>. "
                "Yeh bina kisi loop ke sabhi 12,000 orders ka profit ek microsecond mein calculate kar deta hai!"
            ),
            "qa": [
                ("Q: What is a DataFrame and why is it faster than Python lists?",
                 "A: A DataFrame is a 2D labeled data structure built in C on top of NumPy arrays. It utilizes vectorized operations in contiguous memory, avoiding Python's slow iterative loop overhead and achieving 50x-100x faster processing."),
                ("Q: How does Pandas handle grouping data?",
                 "A: Using .groupby(), which implements the Split-Apply-Combine pattern: splitting data into groups based on keys, applying aggregate functions (like sum, mean), and combining the results into a summary DataFrame.")
            ]
        },
        {
            "day": "Day 2: Data Cleaning, Outlier Detection & Automated EDA",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Real-world data hamesha ganda hota hai. Kahin email missing hoti hai, kahin date aage-piche "
                "hoti hai, ya kisi ne galti se $10 ka product $1,000,000 mein bech diya (jisko <b>Outlier</b> bolte hain).<br/>"
                "• <b>Missing Values:</b> Khali cells ko median ya mode se sensible tareeqe se bharna.<br/>"
                "• <b>IQR (Interquartile Range):</b> Data ke beech ke 50% hisse ko dekh kar ajeeb extreme values ko pakadna.<br/>"
                "• <b>EDA:</b> Data ka complete health checkup (mean, standard deviation, skewness, aur correlation)."
            ),
            "video_title": "StatQuest: Outliers and Boxplots with IQR",
            "video_search": "Search YouTube: 'StatQuest IQR Outliers'",
            "video_time": "Exact Duration: 0:00 to 8:45 (Only 9 minutes)",
            "code_file": "ingestion/validator.py & ingestion/eda_engine.py",
            "code_explanation": (
                "<code>validator.py</code> har row ko check karta hai ki price negative toh nahi hai aur duplicate IDs toh nahi hain. "
                "<code>eda_engine.py</code> mein line 40 dekhiye: <code>compute_summary_stats()</code> har column ka 25th percentile, "
                "median, 75th percentile aur IQR calculate karta hai taaki business owner ko summary pata chale."
            ),
            "qa": [
                ("Q: Why use Median instead of Mean for imputing missing values when outliers exist?",
                 "A: The mean is heavily pulled by extreme outliers (e.g., one $10M purchase pulls the average artificially high). The median represents the true 50th percentile middle and is mathematically robust against outliers."),
                ("Q: What is Pearson Correlation and how do you interpret it?",
                 "A: It measures linear association between two variables from -1.0 to +1.0. A +0.8 means as price increases, profit strongly increases; a -0.7 means as delivery delay increases, customer satisfaction drops drastically.")
            ]
        },
        {
            "day": "Day 3: Relational Databases & Core SQL (PostgreSQL)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Database ek aisi digital tijori hai jisme alag-alag folders (tables) mein data rehta hai. "
                "Har table ka doosre table se rishta (relation) hota hai.<br/>"
                "• <b>Primary Key (PK):</b> Har row ka unique identity card (jaise <code>customer_id</code>).<br/>"
                "• <b>Foreign Key (FK):</b> Bill table mein likha hua customer_id taaki pata chale bill kiska hai.<br/>"
                "• <b>INNER JOIN:</b> Sirf unhi records ko dikhana jo dono tables mein match hote hain.<br/>"
                "• <b>LEFT JOIN:</b> Left table ka saara data dikhana chahe right side mein match ho ya na ho."
            ),
            "video_title": "SQL Joins in 10 Minutes by Kudvenkat",
            "video_search": "Search YouTube: 'Kudvenkat SQL Joins in 10 minutes'",
            "video_time": "Exact Duration: 0:00 to 11:30 (Watch full 11 mins)",
            "code_file": "database/schema.sql & database/db_manager.py",
            "code_explanation": (
                "<code>schema.sql</code> mein 4 tables hain: <code>customers</code>, <code>transactions</code>, <code>products</code>, "
                "aur <code>sales_reps</code>. Line 25 mein <code>FOREIGN KEY (customer_id) REFERENCES customers(customer_id)</code> "
                "likha hai jo database ko kisi fake customer ka bill enter karne se rokta hai."
            ),
            "qa": [
                ("Q: What happens if an INNER JOIN key has no match in the second table?",
                 "A: The row is completely excluded from the result set. If you want to keep all records from the primary table regardless of matches, you must use a LEFT OUTER JOIN."),
                ("Q: Why did you create B-Tree indexes on transaction_date and customer_id?",
                 "A: Indexes reduce search complexity from a full table scan O(N) to logarithmic lookup O(log N), reducing analytical query latency on 12,000 rows from 150ms to under 5ms.")
            ]
        },
        {
            "day": "Day 4: Advanced PostgreSQL Mastery (Window Functions & CTEs)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Standard SQL mein GROUP BY karne par rows merge hokar collapse ho jaati hain. "
                "<b>Window Functions</b> bina rows ko collapse kiye calculation karti hain!<br/>"
                "• <b>LAG():</b> Pichle row ki value dekhna (jaise pichle mahine ki sales se compare karna).<br/>"
                "• <b>DENSE_RANK():</b> Top spenders ko 1, 2, 3 rank dena bina kisi rank number ko skip kiye.<br/>"
                "• <b>SUM(...) OVER:</b> Piggy bank running total jo har din badhta rehta hai.<br/>"
                "• <b>CTE (WITH ... AS):</b> Badi query ko chote readable blocks mein todna."
            ),
            "video_title": "SQL Window Functions by Alex The Analyst",
            "video_search": "Search YouTube: 'Alex The Analyst SQL Window Functions'",
            "video_time": "Exact Duration: 0:00 to 17:45 (Watch full 18 mins)",
            "code_file": "database/analytics_queries.py (Catalog Queries 1, 2 & 4)",
            "code_explanation": (
                "Query 1 dekhiye: <code>LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue</code>. Yeh SQL ko pichle mahine ka "
                "revenue dikhata hai taaki hum <code>ROUND(((revenue - prev) / prev) * 100, 2)</code> se Month-over-Month growth percentage nikaal sakein!"
            ),
            "qa": [
                ("Q: What is the key difference between RANK() and DENSE_RANK()?",
                 "A: If two rows tie for rank 1: RANK() assigns ranks 1, 1, 3 (leaving a gap). DENSE_RANK() assigns 1, 1, 2 without gaps. In InsightOS, we use DENSE_RANK() for continuous executive performance tiers."),
                ("Q: What is the operational benefit of a Common Table Expression (CTE)?",
                 "A: CTEs read sequentially from top to bottom like procedural logic, vastly improving maintainability over deeply nested subqueries and allowing query planners to optimize intermediate materialized results.")
            ]
        },
        {
            "day": "Day 5: ML: Customer Churn Prediction (Supervised Classification)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Customer Churn ka matlab hai subscription band karke chale jana. Hamara model ek smart alarm "
                "hai jo purane chhodkar gaye customers ki patterns seekhta hai aur current customers par warning deta hai.<br/>"
                "• <b>Random Forest:</b> 100 Decision Trees ka jungle. Sab trees vote karte hain aur majority vote jeetti hai.<br/>"
                "• <b>Recall:</b> Chale jaane wale 100 customers mein se model ne kitne pakde? (Recall is king in retention!).<br/>"
                "• <b>Feature Importance:</b> Model batata hai sabse bada reason kya tha (e.g. 3+ support calls)."
            ),
            "video_title": "StatQuest: Random Forests Clearly Explained",
            "video_search": "Search YouTube: 'StatQuest Random Forest'",
            "video_time": "Exact Duration: 0:00 to 15:00 (Watch full 15 mins)",
            "code_file": "ml/churn_predictor.py",
            "code_explanation": (
                "Line 38 mein <code>RandomForestClassifier(n_estimators=100, class_weight='balanced')</code> use kiya. "
                "Line 70 mein <code>get_feature_importances()</code> check karta hai ki churn ka sabse bada kaaran kya tha. "
                "Pata chala ki Support Tickets #1 kaaran tha (35% weight)!"
            ),
            "qa": [
                ("Q: Why did you optimize for Recall rather than Accuracy for Churn?",
                 "A: If 90% of clients stay, a naive model predicting 'no one leaves' gets 90% accuracy but catches zero churners. High Recall guarantees we capture the maximum number of potential cancellations before contracts renew."),
                ("Q: What is ROC-AUC and what does your 0.75+ score mean?",
                 "A: ROC-AUC measures the model's ability to discriminate between churners and non-churners across all classification thresholds. A score of 0.75+ means the model has a 75%+ probability of ranking a random churner higher than a non-churner.")
            ]
        },
        {
            "day": "Day 6: ML: Customer Segmentation (RFM + K-Means Clustering)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Har customer ke sath ek jaisa bartav nahi kar sakte. Unhe 4 clubs mein baanta jaata hai:<br/>"
                "• <b>R (Recency):</b> Aakhiri baar kab khareeda? (Kal vs 60 din pehle).<br/>"
                "• <b>F (Frequency):</b> Kitni baar khareeda? (1 order vs 20 orders).<br/>"
                "• <b>M (Monetary):</b> Total kitna spend kiya? ($50 vs $100,000).<br/>"
                "• <b>K-Means:</b> Unsupervised algorithm jo similar customers ka guchha (cluster) banata hai.<br/>"
                "• <b>StandardScaler:</b> Days aur Dollars ko ek scale par lana taaki bade numbers math ko dominate na karein."
            ),
            "video_title": "StatQuest: K-Means Clustering",
            "video_search": "Search YouTube: 'StatQuest K-Means Clustering'",
            "video_time": "Exact Duration: 0:00 to 10:45 (Watch full 11 mins)",
            "code_file": "ml/customer_segmentation.py",
            "code_explanation": (
                "Line 45 mein <code>compute_rfm()</code> har customer ke orders group karke Recency, Frequency aur Spend nikaalta hai. "
                "Line 70 mein <code>StandardScaler().fit_transform()</code> lagakar <code>KMeans(n_clusters=4)</code> chalaya aur "
                "customers ko Champions, Promising, At-Risk, aur Hibernating label kiya."
            ),
            "qa": [
                ("Q: Why is feature scaling mandatory before running K-Means?",
                 "A: K-Means uses Euclidean distance. If monetary spend is in thousands while frequency is 1-10, monetary values will dominate the distance metric. StandardScaler standardizes all features to mean 0 and variance 1."),
                ("Q: How did you select k=4 clusters?",
                 "A: We evaluated the Elbow Method (inertia drop) and Silhouette Score, finding that k=4 provided the cleanest separation corresponding to distinct business action personas (VIPs, Growth, At-Risk, and Sleepers).")
            ]
        },
        {
            "day": "Day 7: ML: Sales Forecasting (Autoregressive Lags & Confidence Bands)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Kal ya agle 30 din mein kitna paisa banega yeh predict karna. Jaise weather forecast kal ke "
                "mausam ke liye pichle dino ka trend dekhta hai, waise hi yeh model past patterns dekhta hai.<br/>"
                "• <b>Lag Features:</b> Pichle din (t-1), pichle hafte (t-7), aur pichle mahine (t-28) ki sales.<br/>"
                "• <b>Rolling Averages:</b> Pichle 7 ya 14 dino ka average jo temporary bumps ko smooth karta hai.<br/>"
                "• <b>90% Confidence Interval:</b> Ek shaded blue band jo batati hai ki 90% chances hain sales is limit ke andar rahegi."
            ),
            "video_title": "Time Series Forecasting with Lag Features by Rob Mulla",
            "video_search": "Search YouTube: 'Rob Mulla Time Series Forecasting Python'",
            "video_time": "Exact Duration: 0:00 to 14:00 (Watch first 14 mins)",
            "code_file": "ml/sales_forecaster.py",
            "code_explanation": (
                "Line 30 mein <code>_engineer_lag_features()</code> dekhiye: <code>df['lag_1'] = df['revenue'].shift(1)</code> aur "
                "<code>df['lag_7'] = df['revenue'].shift(7)</code> banaya. Isse model weekday vs weekend patterns aur end-of-quarter "
                "spikes seekh leta hai!"
            ),
            "qa": [
                ("Q: Why not use a straight trendline for revenue forecasting?",
                 "A: Revenue exhibits weekly cyclicality (low weekend sales, high weekday peaks) and quarterly budget spikes. Linear regression misses these oscillations entirely, whereas lag features directly capture cyclic continuity."),
                ("Q: How do you prevent data leakage during time series training?",
                 "A: Never shuffle data. We split chronologically: training strictly on past dates and testing strictly on future forward dates to mimic real-world production forecasting.")
            ]
        },
        {
            "day": "Day 8: ML: Transaction Anomaly Detection (Isolation Forest)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> 12,000 receipts mein se fraud ya galti pakadna (e.g. kisi order par 80% discount de diya "
                "aur company ka $2,000 ka nuksan ho gaya).<br/>"
                "• <b>Isolation Forest:</b> Normal points ko alag karna mushkil hota hai, lekin jo ajeeb points hote hain woh bohot kam "
                "cuts/splits mein alag ho jaate hain!<br/>"
                "• <b>Contamination:</b> Hum model ko batate hain ki hume lagta hai lagbhag 3% orders mein mistake ho sakti hai."
            ),
            "video_title": "StatQuest: Isolation Forests Clearly Explained",
            "video_search": "Search YouTube: 'StatQuest Isolation Forest'",
            "video_time": "Exact Duration: 0:00 to 11:30 (Watch full 12 mins)",
            "code_file": "ml/anomaly_detector.py",
            "code_explanation": (
                "Line 40 mein <code>IsolationForest(contamination=0.03, random_state=42)</code> use kiya. "
                "Line 65 mein model har flagged order ka reason batata hai: 'Excessive Discount' ya 'Negative Margin Loss'. "
                "Isne total $45,000 ka revenue leakage pakda!"
            ),
            "qa": [
                ("Q: How does Isolation Forest work conceptually?",
                 "A: It builds an ensemble of random decision trees. Anomalies have extreme attribute values and are isolated very close to the root of the trees (short path length), while normal data points require many deeper splits."),
                ("Q: What real-world business value did this provide in InsightOS?",
                 "A: It flagged checkout errors where sales reps entered unapproved 80% discount codes resulting in negative profit margins, giving finance an immediate recovery audit list.")
            ]
        },
        {
            "day": "Day 9: Generative AI & RAG (Retrieval-Augmented Generation)",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Standard ChatGPT se pucho 'Hamare business mein May mein loss kyu hua?', toh woh guess karega "
                "(hallucinate karega).<br/>"
                "• <b>RAG (Open-Book Exam):</b><br/>"
                "  1. <b>Retrieve:</b> User ke question se database se real facts aur numbers nikaalna.<br/>"
                "  2. <b>Augment:</b> AI ko prompt ke sath woh real numbers pakdana.<br/>"
                "  3. <b>Generate:</b> AI sirf unhi sachhe numbers ke basis par 4-step executive briefing likhta hai (Zero fake answers!)."
            ),
            "video_title": "What is RAG? Retrieval Augmented Generation by FreeCodeCamp",
            "video_search": "Search YouTube: 'FreeCodeCamp RAG architecture'",
            "video_time": "Exact Duration: 0:00 to 13:30 (Watch first 14 mins)",
            "code_file": "ai_analyst/rag_engine.py & ai_analyst/business_advisor.py",
            "code_explanation": (
                "<code>rag_engine.py</code> database schema, live KPIs aur query results ka vector index banata hai. "
                "<code>business_advisor.py</code> bina kisi API key ke 100% offline chalta hai aur 4-part briefing banata hai: "
                "1. What Happened, 2. Why Did It Happen, 3. What Happens Next, 4. 30-Day Action Plan."
            ),
            "qa": [
                ("Q: Why is RAG superior to fine-tuning an LLM for enterprise reporting?",
                 "A: Fine-tuning bakes static weights into a model and requires expensive retraining whenever transactions update. RAG queries live relational ground-truth dynamically, eliminating hallucinations at near-zero cost."),
                ("Q: How does your offline fallback work in InsightOS?",
                 "A: In business_advisor.py, when no cloud API key is provided, our local deterministic engine matches semantic intents using TF-IDF cosine similarity and populates factual executive briefing templates directly from the database.")
            ]
        },
        {
            "day": "Day 10: Full-Stack Integration, Streamlit & Interview Masterclass",
            "concept": (
                "<b>Simple Hinglish Concept:</b> Saare models aur SQL ka koi fayda nahi agar company ke CEO ko use karna na aaye. "
                "<b>Streamlit</b> Python code ko ek sleek modern web application bana deta hai.<br/>"
                "• <b>Plotly:</b> Interactive charts (zoom in, hover details, tooltips).<br/>"
                "• <b>Custom CSS:</b> High-contrast colors (Dark slate #0F172A, Royal Blue buttons) taaki text hamesha crisp dikhe."
            ),
            "video_title": "Streamlit in 10 Minutes by Streamlit Official",
            "video_search": "Search YouTube: 'Streamlit in 10 minutes'",
            "video_time": "Exact Duration: 0:00 to 12:00 (Watch full 12 mins)",
            "code_file": "app.py & ui/styles.py",
            "code_explanation": (
                "<code>app.py</code> main controller hai jo 5 views ko route karta hai: Executive Overview, Data Health, "
                "SQL Analytics, Predictive ML Studio, aur AI Advisor. <code>ui/styles.py</code> ensure karta hai ki button text "
                "aur metrics hamesha 100% visible rahein."
            ),
            "qa": [
                ("Q: Walk me through the end-to-end architecture of InsightOS.",
                 "A: Raw transactions enter through our validation pipeline into an ANSI-compatible relational schema. The analytical layer runs window functions and CTEs, feeding 4 Scikit-Learn predictive models. These outputs are indexed in an in-memory RAG vector space, providing context to an AI executive advisor and rendered in a modular Streamlit UI."),
                ("Q: What was the hardest engineering challenge in InsightOS?",
                 "A: Bridging the gap between raw data science outputs and non-technical business decision-makers: ensuring fast sub-5ms SQL latency, designing an explainable RAG pipeline that works 100% offline, and building a high-contrast executive design system.")
            ]
        }
    ]

    for item in days_content:
        story.append(PageBreak())
        story.append(Paragraph(item["day"], h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8))
        
        # Concept Box
        story.append(Paragraph(item["concept"], body_style))
        story.append(Spacer(1, 6))

        # Video Target Card
        video_box_data = [
            [
                Paragraph(f"<b>Exact Video Target:</b> {item['video_title']}<br/>"
                          f"• <b>YouTube Search:</b> {item['video_search']}<br/>"
                          f"• <b>{item['video_time']}</b> (Poori playlist nahi dekhni, sirf yeh video dekhein!)", body_style)
            ]
        ]
        vt = Table(video_box_data, colWidths=[504])
        vt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(vt)
        story.append(Spacer(1, 8))

        # Project Code Section
        story.append(Paragraph(f"<b>InsightOS Code Connection:</b> <code>{item['code_file']}</code>", h2_style))
        story.append(Paragraph(item["code_explanation"], body_style))
        story.append(Spacer(1, 8))

        # Interview Q&A Section
        story.append(Paragraph("<b>Expected Interview Questions & Killer Answers:</b>", h2_style))
        for q, a in item["qa"]:
            story.append(Paragraph(q, q_style))
            story.append(Paragraph(a, ans_style))
        story.append(Spacer(1, 10))

    # =========================================================================
    # ELEVATOR PITCH & FINAL SUMMARY PAGE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("The 2-Minute Resume Elevator Pitch", h1_style))
    story.append(Paragraph("Jab interviewer bole: <i>'Tell me about your project on your resume'</i>, yeh boliye:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_ACCENT, spaceAfter=10))

    pitch_box_data = [
        [
            Paragraph(
                "<i>\"In my project, <b>InsightOS</b>, I built an AI-Powered Decision Intelligence Platform that bridges "
                "relational data processing, PostgreSQL analytics, Scikit-Learn machine learning, and an AI Business Analyst "
                "workflow powered by RAG.<br/><br/>"
                "I started by synthesizing and validating an enterprise dataset of 12,000 transactions and 1,200 accounts. "
                "Using PostgreSQL, I designed analytical queries including window functions like <code>LAG()</code> for MoM revenue velocity, "
                "<code>DENSE_RANK()</code> for regional customer rankings, and CTEs for tiered sales quota attainment.<br/><br/>"
                "On the predictive side, I implemented four Scikit-Learn models: a Random Forest classifier for churn prediction with "
                "feature explainability, an RFM K-Means clustering model for customer personas, an autoregressive time-series model for "
                "30-to-90 day revenue forecasting with 90% confidence bands, and an Isolation Forest for transaction anomaly detection.<br/><br/>"
                "Finally, I built a conversational AI business analyst using RAG that grounds inquiries in actual database metrics to "
                "generate structured 4-part executive briefings, wrapping the entire platform in a responsive Streamlit executive dashboard.\"</i>",
                body_style
            )
        ]
    ]
    pt = Table(pitch_box_data, colWidths=[504])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(pt)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>5 Golden Interview Rules:</b>", h2_style))
    rules = [
        "1. <b>Never say 'I just ran a library':</b> Always say <i>'I analyzed the business requirement, selected the appropriate algorithm, and evaluated it with proper validation metrics.'</i>",
        "2. <b>Highlight Business Impact:</b> Don't just say <i>'I trained a Random Forest'</i>; say <i>'I trained a Random Forest model with high Recall to detect 85% of churning enterprise accounts before renewal, protecting recurring ARR.'</i>",
        "3. <b>Know Your Metrics:</b> Remember why <b>Recall</b> matters for Churn, <b>MAPE</b> matters for Forecasting, and <b>Silhouette Score</b> matters for K-Means Clustering.",
        "4. <b>Proudly Explain RAG:</b> Explain that RAG avoids LLM hallucinations by transforming questions into an open-book exam over real database facts.",
        "5. <b>Showcase Git & Testing:</b> Mention that your repository has 14 passing unit tests, clean modular separation, and is completely committed and documented on GitHub."
    ]
    for r in rules:
        story.append(Paragraph(r, bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {output_filename}")


if __name__ == "__main__":
    create_study_plan_pdf("InsightOS_10_Day_Master_Study_Plan.pdf")
