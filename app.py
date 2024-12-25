from flask import Flask, request, render_template, redirect, url_for, flash, session
import main

app = Flask(__name__)
app.secret_key = 'admin'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url1 = request.form['url1']
        url2 = request.form['url2']
        num_runs = int(request.form['num_runs'])
        results = main.run_parallel_tests([url1, url2], num_runs)
        session['results'] = main.generate_html_report(results)
        return redirect(url_for('results'))

    return render_template('form_template.html')


@app.route('/results')
def results():
    report_html = session.get('results', None)

    if report_html:
        session.pop('results', None)
        return report_html
    else:
        flash('Please submit a form to generate results.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
