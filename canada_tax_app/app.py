from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('taxes.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tax_calculations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT NOT NULL,
                 employment_income REAL NOT NULL,
                 other_income REAL NOT NULL,
                 rrsp_contributions REAL NOT NULL,
                 federal_tax REAL NOT NULL,
                 ontario_tax REAL NOT NULL,
                 total_tax REAL NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Tax calculation functions
def calculate_federal_tax(taxable_income):
    brackets = [
        (53359, 0.15),
        (106717, 0.205),
        (165430, 0.26),
        (235675, 0.29),
        (float('inf'), 0.33)
    ]
    
    tax = 0
    previous_limit = 0
    
    for limit, rate in brackets:
        if taxable_income > previous_limit:
            taxable_amount = min(taxable_income, limit) - previous_limit
            tax += taxable_amount * rate
            previous_limit = limit
    
    return tax

def calculate_ontario_tax(taxable_income):
    brackets = [
        (49231, 0.0505),
        (98463, 0.0915),
        (150000, 0.1116),
        (220000, 0.1216),
        (float('inf'), 0.1316)
    ]
    
    tax = 0
    previous_limit = 0
    
    for limit, rate in brackets:
        if taxable_income > previous_limit:
            taxable_amount = min(taxable_income, limit) - previous_limit
            tax += taxable_amount * rate
            previous_limit = limit
    
    return tax

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        employment_income = float(request.form['employment_income'])
        other_income = float(request.form['other_income'])
        rrsp_contributions = float(request.form['rrsp_contributions'])
        
        # Calculate taxable income
        total_income = employment_income + other_income
        taxable_income = total_income - rrsp_contributions
        
        # Calculate taxes
        federal_tax = calculate_federal_tax(taxable_income)
        ontario_tax = calculate_ontario_tax(taxable_income)
        total_tax = federal_tax + ontario_tax
        
        # Store in database
        conn = get_db_connection()
        conn.execute('INSERT INTO tax_calculations (timestamp, employment_income, other_income, rrsp_contributions, federal_tax, ontario_tax, total_tax) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), employment_income, other_income, rrsp_contributions, federal_tax, ontario_tax, total_tax))
        conn.commit()
        conn.close()
        
        return redirect(url_for('results', 
                               employment_income=employment_income,
                               other_income=other_income,
                               rrsp_contributions=rrsp_contributions,
                               taxable_income=taxable_income,
                               federal_tax=federal_tax,
                               ontario_tax=ontario_tax,
                               total_tax=total_tax))
    
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html',
                           employment_income=request.args.get('employment_income'),
                           other_income=request.args.get('other_income'),
                           rrsp_contributions=request.args.get('rrsp_contributions'),
                           taxable_income=request.args.get('taxable_income'),
                           federal_tax=request.args.get('federal_tax'),
                           ontario_tax=request.args.get('ontario_tax'),
                           total_tax=request.args.get('total_tax'))

@app.route('/history')
def history():
    conn = get_db_connection()
    calculations = conn.execute('SELECT * FROM tax_calculations ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('history.html', calculations=calculations)

if __name__ == '__main__':
    app.run(debug=True)