from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def next_period_dates(start_date, cycle_length=27, discrepancy=1, num_periods=12):
    periods = []
    current_date = start_date

    for _ in range(num_periods):
        next_period = current_date + datetime.timedelta(days=cycle_length)
        start_window = next_period - datetime.timedelta(days=discrepancy)
        end_window = next_period + datetime.timedelta(days=discrepancy)
        periods.append((start_window, end_window))
        current_date = next_period

    return periods

# Store dates in memory for simplicity (consider using a database for persistence)
period_start_dates = []

@app.route('/')
def index():
    return render_template('index.html', dates=json.dumps(period_start_dates))

@app.route('/add_date', methods=['POST'])
def add_date():
    date_str = request.form['date']
    start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    period_start_dates.append(date_str)
    return redirect(url_for('index'))

@app.route('/get_periods', methods=['POST'])
def get_periods():
    date_str = request.json['start_date']
    start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    periods = next_period_dates(start_date)
    periods_formatted = [{'start': start.isoformat(), 'end': end.isoformat()} for start, end in periods]
    return jsonify(periods_formatted)

if __name__ == '__main__':
    app.run(debug=True)
