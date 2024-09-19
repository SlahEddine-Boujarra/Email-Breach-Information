<h1>📧 Email Breach Information Dashboard</h1>

<h2>🛡️ Overview</h2>
<p>
This project is a web-based dashboard that allows users to scan emails for potential breaches using the <strong>BreachDirectory API</strong>. Users can upload a list of emails in Excel or CSV format, which will be checked against breach databases. The results, including breach details, will be stored in a MongoDB database and displayed in the dashboard.
</p>

<h2>🚀 Features</h2>
<ul>
  <li><strong>Upload Email List</strong>: Upload a CSV or Excel file containing a list of email addresses.</li>
  <li><strong>Scan for Breaches</strong>: Scan uploaded emails against breach databases via the BreachDirectory API.</li>
  <li><strong>View Results in a Dashboard</strong>: Display breach results in an interactive table format using Dash.</li>
  <li><strong>MongoDB Integration</strong>: Store all scan results securely in a MongoDB database.</li>
</ul>

<h2>🛠️ Installation</h2>
<p>Follow these steps to install and run the project locally.</p>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/your-username/email-breach-dashboard.git</code></pre>

<h3>2. Navigate to the Project Directory</h3>
<pre><code>cd email-breach-dashboard</code></pre>

<h3>3. Install the Required Dependencies</h3>
<p>Ensure that you have Python installed. Then, install the required libraries using the <code>requirements.txt</code> file:</p>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>4. Run MongoDB Locally</h3>
<p>
Make sure you have a MongoDB instance running on your machine. The default MongoDB connection URI is <code>mongodb://localhost:27017/</code>. You can adjust this in the code if needed.
</p>

<h2>💡 Usage</h2>

<h3>1. Running the Application</h3>
<pre><code>python app.py</code></pre>
<p>The dashboard will start running on <code>http://127.0.0.1:8050/</code>.</p>

<h3>2. Save Your API Key</h3>
<p>Enter your <strong>BreachDirectory API Key</strong> in the provided input field and click "Save API Key".</p>

<h3>3. Upload Email List</h3>
<p>Upload an Excel or CSV file that contains a list of email addresses. The emails will be scanned for breaches.</p>

<h3>4. Start the Scan</h3>
<p>Click the "Start Scan" button to begin the scan process. The results will be displayed in the dashboard.</p>

<h2>⚙️ API Integration</h2>
<p>The app integrates with the <strong>BreachDirectory API</strong> to check for breached email addresses. The scan results are displayed in the dashboard and stored in a MongoDB database.</p>

<h3>API Request</h3>
<p>Each email in the uploaded list is sent to the API for a scan. The results are saved in the MongoDB collection <code>breachResults</code>.</p>

<h2>📂 File Structure</h2>
<pre><code>.
├── app.py               # Main app logic and Dash layout
├── requirements.txt     # Dependencies
└── README.md            # Documentation
</code></pre>

<h2>🌟 Example Output</h2>
<p>After scanning, the dashboard displays a table showing:</p>
<ul>
  <li>Email Address</li>
  <li>Scan Date</li>
  <li>Found Status</li>
  <li>Breach Info</li>
</ul>

<h2>🔧 Technologies Used</h2>
<ul>
  <li><strong>Dash</strong>: Web framework for creating dashboards.</li>
  <li><strong>Pandas</strong>: For handling and processing the uploaded files.</li>
  <li><strong>MongoDB</strong>: To store scan results.</li>
  <li><strong>BreachDirectory API</strong>: To check for breached email addresses.</li>
</ul>

<h2>📄 License</h2>
<p>This project is licensed under the MIT License.</p>

<h2>🤝 Contributions</h2>
<p>Feel free to fork the repository, submit pull requests, or open issues for any feature requests or bugs you encounter.</p>

