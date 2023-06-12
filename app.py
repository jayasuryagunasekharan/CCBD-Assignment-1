from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('myindexpage.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('myuploadpage.html')


@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        uploaded_file = request.files['csvfile']

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            data = []
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            print(data)
            return render_template('mydatapage.html', data=data)

    return render_template('mydatapage.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('mysearchpage.html')


@app.route("/searchimage", methods=['GET', 'POST'])
def search_image():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/uploads/people.csv'))
        temp_path = ''
        for row in csv_reader:
            if name == row['Name']:
                temp_path = '../static/' + row['Picture']
        if temp_path != '':
            return render_template('mysearchpage.html', image_path=temp_path, message="Found Data!!")
        else:
            return render_template('mysearchpage.html', error="Picture not found :(")


@app.route("/searchbysal", methods=['GET', 'POST'])
def search_by_salary():
    if request.method == 'POST':
        csv_reader = csv.DictReader(open('static/uploads/people.csv'))
        start_range = request.form['startRange']
        end_range = request.form['endRange']
        is_number_range = False

        if start_range and end_range:
            is_number_range = True
            start_range = int(start_range)
            end_range = int(end_range)

        temp_path = []
        data = []

        for row in csv_reader:
            if is_number_range:
                if row['Num'].strip() != '' and start_range <= int(row['Num']) <= end_range or row['Year'].strip() != '' and start_range <= int(row['Year']) <= end_range:
                    if row['Picture'] != ' ':
                        temp_path.append('static/' + row['Picture'])
                    data.append(row)

        if temp_path:
            return render_template('mysearchbysalpage.html', data=data, image_path=temp_path, message="Found Data!!")
        else:
            return render_template('mysearchbysalpage.html', error="No information or picture available.")

    return render_template('mysearchbysalpage.html')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return render_template('myeditpage.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def edit_details():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/uploads/people.csv'))
        temp_name = ''
        for row in csv_reader:
            if name == row['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('mydisplaypage.html', name=temp_name)
        else:
            return render_template('mydisplaypage.html', error="Record not found :(")


@app.route("/updatedetails", methods=['GET', 'POST'])
def update_details():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        num = request.form['num']
        room = request.form['room']
        year = request.form['year']
        telnum = request.form['telnum']
        picture = request.form['picture']
        comments = request.form['comments']
        cnt = 0

        temp = [name, state, salary, num, room,
                year, telnum, picture, comments]
        line = list()

        with open('static/uploads/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for row in csv_reader:
                if name == row[0]:
                    line.append(temp)
                else:
                    line.append(row)
                cnt += 1

            csv_write = open('static/uploads/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

            if cnt != 0:
                return render_template('mydisplaypage.html', update="One Record Updated Successfully.")
            else:
                return render_template('mydisplaypage.html', error="Record not found :(")


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    return render_template('myremovepage.html')


@app.route("/removedetails", methods=['GET', 'POST'])
def remove_details():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/uploads/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for row in csv_reader:
                line.append(row)
                if name == row[0]:
                    line.remove(row)
                    cnt += 1

            csv_write = open('static/uploads/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

        if cnt != 0:
            return render_template('myremovedetailspage.html', message="Record Removed Successfully.")
        else:
            return render_template('myremovedetailspage.html', error="Record not found :(")


@app.route("/uploadpic", methods=['GET', 'POST'])
def upload_pic():
    return render_template('myuploadpicpage.html')


@app.route("/uploadnew", methods=['GET', 'POST'])
def upload_new():
    if request.method == 'POST':
        file = request.files['img']
        file.save('static/' + file.filename)
        return render_template('myuploaddisplaypage.html', msg="Image Uploaded Successfully.")


if __name__ == "__main__":
    app.run(debug=True)
