from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
from datetime import datetime




cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_3")

app = Flask(__name__)
app.secret_key = "Secret Key"

def get_connection():
    con = cx_Oracle.connect("system","albastru", "localhost/xe")
    return con

def view_ticket():
    tickets = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from ticket order by ticketnumber")
    for res in cur:
        ticket = {}
        ticket['TicketNumber'] = res[0]
        ticket['Price'] = res[1]
        ticket['ConfirmationCode'] = res[2]
        ticket['FlightNumber'] = res[3]
        ticket['PassengerID'] = res[4]
        tickets.append(ticket)
    con.commit()
    cur.close()
    return tickets

def view_top_countries():
    tcs = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from (select a.country, count(*) as Tickets_Per_Country from ticket t, flight f, airport a where f.flightnumber=t.flightnumber and a.icao_code=f.airportid_arrival group by a.country order by Tickets_Per_Country desc)")
    for res in cur:
        tc = {}
        tc['Country'] = res[0]
        tc['Tickets_Per_Country'] = res[1]
        tcs.append(tc)
    con.commit()
    cur.close()
    return tcs

def view_least_countries():
    lcs = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from (select a.country, count(*) as Tickets_Per_Country from ticket t, flight f, airport a where f.flightnumber=t.flightnumber and a.icao_code=f.airportid_arrival group by a.country order by Tickets_Per_Country)")
    for res in cur:
        tc = {}
        tc['Country'] = res[0]
        tc['Tickets_Per_Country'] = res[1]
        lcs.append(tc)
    con.commit()
    cur.close()
    return lcs

def view_top_months():
    mts = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from (select to_char(f.departuretime, 'yyyy-MONTH') month, count(*) numberofflights from flight f, ticket t where t.flightnumber=f.flightnumber group by to_char(f.departuretime, 'yyyy-MONTH') order by numberofflights desc)")
    for res in cur:
        mt = {}
        mt['Month'] = res[0]
        mt['NumberOfFlights'] = res[1]
        mts.append(mt)
    con.commit()
    cur.close()
    return mts


def view_flight():
    flights = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from flight order by flightnumber")
    for res in cur:
        fl = {}
        fl['FlightNumber'] = res[0]
        fl['DepartureTime'] = res[1]
        if fl['DepartureTime']:
            fl['DepartureTime'] = datetime.strptime(str(res[1]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M')
        fl['ArrivalTime'] = res[2]
        if fl['ArrivalTime']:
            fl['ArrivalTime'] = datetime.strptime(str(res[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M')
        fl['DistanceInKm'] = res[3]
        fl['AirportID_Departure'] = res[4]
        fl['AirportID_Arrival'] = res[5]
        fl['NumberOfSeats'] = res[6]
        fl['Airline_ID'] = res[7]
        flights.append(fl)
    con.commit()
    cur.close()
    return flights

def view_pd():
    pds = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from passengerDetails")
    for res in cur:
        pd = {}
        pd['CNP'] = res[0]
        pd['Telephone'] = res[1]
        pd['Email'] = res[2]
        pd['Birth_Date'] = res[3]
        if pd['Birth_Date']:
            pd['Birth_Date'] = datetime.strptime(str(res[3]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        print(pd['Birth_Date'])
        pds.append(pd)
    con.commit()
    cur.close()
    return pds

def view_pas():
    pas = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from passenger")
    for res in cur:
        pa = {}
        pa['PassengerID'] = res[0]
        pa['LastName_FirstName'] = res[1]
        pa['CNP'] = res[2]
        pas.append(pa)
    con.commit()
    cur.close()
    return pas

def view_aps():
    aps = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from airport")
    for res in cur:
        ap = {}
        ap['ICAO_Code'] = res[0]
        ap['Name'] = res[1]
        ap['City'] = res[2]
        ap['Country'] = res[3]
        aps.append(ap)
    print(aps)
    con.commit()
    cur.close()
    return aps

def view_air():
    airs = []
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from airline order by airline_ID")
    for res in cur:
        air = {}
        air['Airline_ID'] = res[0]
        air['Name'] = res[1]
        airs.append(air)
    con.commit()
    cur.close()
    return airs

def insert_ticket():
    con = get_connection()
    cur = con.cursor()
    cur.execute("insert into ticket (ticketnumber,price,confirmationcode,flightnumber,passengerid) values (14,200,'123sdad3234',3,201)")
    con.commit()
    cur.close()
    print("data added")






@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':



        pr = "'"+request.form['Price']+"'"
        cc = "'"+request.form['ConfirmationCode']+"'"
        fn = "'"+request.form['FlightNumber']+"'"
        pi = "'"+request.form['PassengerID']+"'"
        my_tn = "'"+request.form.get('tn')+"'"
        con = get_connection()
        cur = con.cursor()
        query = "UPDATE ticket SET Price=%s, ConfirmationCode=%s, FlightNumber=%s, PassengerID=%s where TicketNumber=%s" % (pr, cc, fn, pi, my_tn)
        cur.execute(query)
        con.commit()
        cur.close()
        flash("Bilet actualizat cu succes.", category='success')

        return redirect(url_for('Index'))


@app.route('/deleteTicket/<id>/', methods=['GET', 'POST'])
def deleteTicket(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("delete from ticket where TicketNumber = "+id)
    con.commit()
    cur.close()
    flash("Bilet sters cu succes.",'success')

    return redirect(url_for('Index'))

@app.route('/flight')
def flight():
    flights = view_flight()
    return render_template('flight.html', flights=flights)


@app.route('/deleteFlight/<id>/', methods=['GET', 'POST'])
def deleteFlight(id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("delete from Flight where FlightNumber = "+id)
        con.commit()
        cur.close()
        flash("Zbor sters cu succes.", category='success')
        return redirect(url_for('flight'))
    except:
        flash("Eroare: Zborul nu poate fi sters pentru ca exista bilete cumparate.", category='error')
        return redirect(url_for('flight'))

    return redirect(url_for('flight'))

@app.route('/buyTicket', methods=['GET', 'POST'])
def buy_ticket():
    if request.method == 'POST':
        tn = "'"+request.form['TicketNumber']+"'"
        pr = "'"+request.form['Price']+"'"
        cc = "'"+request.form['ConfirmationCode']+"'"
        ff = "'"+request.form['FlightNumber']+"'"
        pi = "'"+request.form['PassengerID']+"'"
        print(cc)
        con = get_connection()
        cur = con.cursor()
        values = []
        values.append("'" + request.form['TicketNumber'] + "'")
        values.append("'" + request.form['Price'] + "'")
        values.append("'" + request.form['ConfirmationCode'] + "'")
        values.append("'" + request.form['FlightNumber'] + "'")
        values.append("'" + request.form['PassengerID'] + "'")
        fields = ['TicketNumber', 'Price', 'ConfirmationCode', 'FlightNumber', 'PassengerID']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('ticket', ', '.join(fields), ', '.join(values))
        cur.execute(query)
        con.commit()
        cur.close()
        flash("Bilet adaugat cu succes.")
    else:
        airs = []
        con = get_connection()
        cur = con.cursor()
        cur.execute('select airline_id from airline')
        for result in cur:
            airs.append(result[0])
        cur.close()
        print("buy ticket airs")
        print(airs)

        fs = []
        con = get_connection()
        cur = con.cursor()
        cur.execute('select flightnumber from flight')
        for result in cur:
            fs.append(result[0])
        cur.close()
    return render_template('buyTicket.html', Airlines=airs, Flights=fs)

@app.route('/insertTicket', methods=['POST'])
def insert():
    if request.method == 'POST':
        pr = "'"+request.form['Price']+"'"
        cc = "'"+request.form['ConfirmationCode']+"'"
        ff = "'"+request.form['FlightNumber']+"'"
        pi = "'"+request.form['PassengerID']+"'"
        con = get_connection()
        cur = con.cursor()
        try:
            values = []
            values.append("'" + request.form['Price'] + "'")
            values.append("'" + request.form['ConfirmationCode'] + "'")
            values.append("'" + request.form['FlightNumber'] + "'")
            values.append("'" + request.form['PassengerID'] + "'")
            fields = ['Price', 'ConfirmationCode', 'FlightNumber', 'PassengerID']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('ticket', ', '.join(fields), ', '.join(values))
            cur.execute(query)
            con.commit()
            cur.close()
            flash("Bilet adaugat cu succes.", category='success')
            return redirect(url_for('Index'))
        except:
            flash("Eroare: Verificati datele introduse sa fie corecte. Daca sunt corecte inseamna ca nu mai exista bilete pentru acest zbor", 'error')
    return redirect(url_for('Index'))

@app.route('/passengerDetails')
def passenger_details():
    pds = view_pd()
    return render_template('passengerDetails.html', passengerDetails=pds)

@app.route('/insertPassengerDetails', methods=['POST'])
def insertPassengerDetails():
    if request.method == 'POST':
        cnp = "'"+request.form['CNP']+"'"
        tl = "'"+request.form['Telephone']+"'"
        em = "'"+request.form['Email']+"'"
        bd = "'"+request.form['Birth_Date']+"'"
        con = get_connection()
        cur = con.cursor()
        values = []
        values.append("'" + request.form['CNP'] + "'")
        values.append("'" + request.form['Telephone'] + "'")
        values.append("'" + request.form['Email'] + "'")
        if str(request.form['Birth_Date']):
            values.append("'" + datetime.strptime(str(request.form['Birth_Date']), '%d.%m.%Y').strftime('%d-%b-%y') + "'")
        else:
            try:
                fields = ['CNP', 'Telephone', 'Email']
                query = 'INSERT INTO %s (%s) VALUES (%s)' % ('PassengerDetails', ', '.join(fields), ', '.join(values))
                cur.execute(query)
                con.commit()
                cur.close()
                flash("Detalii pasager adaugate cu succes.", category='success')
                return redirect(url_for('passenger_details'))
            except:
                flash("Eroare: date introduse gresit. Incearca din nou.", category='error')
                return redirect(url_for('passenger_details'))
        try:
            fields = ['CNP', 'Telephone', 'Email', 'Birth_Date']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('PassengerDetails', ', '.join(fields), ', '.join(values))
            cur.execute(query)
            con.commit()
            cur.close()
            flash("Detalii pasager adaugate cu succes.", category='success')
            return redirect(url_for('passenger_details'))
        except:
            flash("Eroare: date introduse gresit. Incearca din nou.", category='error')
            return redirect(url_for('passenger_details'))


@app.route('/deletePassengerDetails/<id>/', methods=['GET', 'POST'])
def delete_passenger_details(id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("delete from passengerDetails where CNP = "+id)
        con.commit()
        cur.close()
        flash('Detalii pasager sterse cu succes.', category='success')
        return redirect(url_for('passenger_details'))
    except:
        flash('Eroare: exista un pasager cu CNP-ul pe care vreti sa-l stergeti.', category='error')
        return redirect(url_for('passenger_details'))


@app.route('/passenger')
def passenger():
    pas = view_pas()
    return render_template('passenger.html', pas=pas)

@app.route('/deletePassenger/<id>/', methods=['GET', 'POST'])
def delete_passenger(id):
    con = get_connection()
    cur = con.cursor()

    cur.execute("select cnp from passenger where PassengerID = " + id)
    for res in cur:
        temp_cnp = res[0]
    cur.execute("delete from passenger where PassengerID = "+id)
    con.commit()
    cur.close()
    delete_passenger_details(temp_cnp)
    flash('Pasager sters cu succes.', category='success')
    return redirect(url_for('passenger'))


@app.route('/airport')
def airport():
    aps = view_aps()
    return render_template('airport.html', airports=aps)

@app.route('/deleteAirport/<id>/', methods=['GET', 'POST'])
def delete_airport(id):
    con = get_connection()
    cur = con.cursor()
    id = "'" + id + "'"
    try:
        cur.execute("delete from Airport where ICAO_Code = "+id)
        con.commit()
        cur.close()
        flash('Aeroport sters cu succes.', category='success')
        return redirect(url_for('airport'))
    except:
        flash('Eroare: exista un zbor pe acest aeroport.', category='error')
        return redirect(url_for('airport'))


@app.route('/airline')
def airline():
    airs = view_air()
    return render_template('airline.html', airlines=airs)

@app.route('/deleteAirline/<id>/', methods=['GET', 'POST'])
def delete_airline(id):
    con = get_connection()
    cur = con.cursor()
    id = "'" + id + "'"
    try:
        cur.execute("delete from airline where Airline_ID = "+id)
        con.commit()
        cur.close()
        flash('Companie stearsa cu succes.', category='success')
        return redirect(url_for('airline'))
    except:
        flash('Eroare: exista un zbor cu aceasta companie.', category='error')
        return redirect(url_for('airline'))

@app.route('/insertPassenger', methods=['GET','POST'])
def insert_passenger():
    if request.method == 'POST':
        ln = "'"+request.form['LastName_FirstName']+"'"
        cnp = "'"+request.form['CNP']+"'"
        con = get_connection()
        cur = con.cursor()
        try:
            values = []
            values.append(ln)
            values.append(cnp)
            fields = ['LastName_FirstName', 'CNP']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Passenger', ', '.join(fields), ', '.join(values))
            cur.execute(query)
            con.commit()
            cur.close()
            flash("Pasager adaugat cu succes.", 'success')
            return redirect(url_for('passenger'))
        except:
            flash("CNP sau nume incorect, introdu CNP-ul introdus la pasul anterior. (Passenger_Details)", 'error')
            return redirect(url_for('passenger'))


@app.route('/insertAirline', methods=['POST'])
def insert_airline():
    if request.method == 'POST':
        nm = "'"+request.form['Name']+"'"
        con = get_connection()
        cur = con.cursor()
        try:
            values = []
            values.append(nm)
            fields = ['Name']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Airline', ', '.join(fields), ', '.join(values))
            cur.execute(query)
            con.commit()
            cur.close()
            flash("Companie adaugata cu succes.", 'success')
            return redirect(url_for('airline'))
        except:
            flash("Eroare: Exista o companie cu acest ID. ID-ul companiei trebuie sa fie unic", 'error')
            return redirect(url_for('airline'))


@app.route('/insertAirport', methods=['POST'])
def insert_airport():
    if request.method == 'POST':
        ic = "'"+request.form['ICAO_Code']+"'"
        nm = "'"+request.form['Name']+"'"
        ct = "'" + request.form['City'] + "'"
        cr = "'" + request.form['Country'] + "'"
        con = get_connection()
        cur = con.cursor()
        try:
            values = []
            values.append(ic)
            values.append(nm)
            values.append(ct)
            values.append(cr)
            fields = ['ICAO_Code', 'Name', 'City', 'Country']
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Airport', ', '.join(fields), ', '.join(values))
            cur.execute(query)
            con.commit()
            cur.close()
            flash("Aeroport adaugat cu succes.", 'success')
            return redirect(url_for('airport'))
        except:
            flash("Eroare: Exista un aeroport cu acest ICAO_Code. ICAO_Code trebuie sa fie unic", 'error')
            return redirect(url_for('airport'))

@app.route('/insertFlight', methods=['GET','POST'])
def insert_flight():
    if request.method == 'POST':
        dt = "'"+request.form['DepartureTime']+"'"
        at = "'" + request.form['ArrivalTime'] + "'"
        print("before")
        print(dt)
        print(at)
        dst = "'" + request.form['DistanceInKm'] + "'"
        adid = "'" + request.form['AirportID_Departure'] + "'"
        aaid = "'" + request.form['AirportID_Arrival'] + "'"
        ns = "'" + request.form['NumberOfSeats'] + "'"
        arid = "'" + request.form['Airline_ID'] + "'"
        con = get_connection()
        cur = con.cursor()


        values = []
        values.append("'" + datetime.strptime(str(request.form['DepartureTime']), '%d.%m.%Y %H:%M').strftime('%d-%b-%y') + "'")
        values.append("'" + datetime.strptime(str(request.form['ArrivalTime']), '%d.%m.%Y %H:%M').strftime('%d-%b-%y') + "'")
        values.append(dst)
        values.append(adid)
        values.append(aaid)
        values.append(ns)
        values.append(arid)
        fields = ['DepartureTime', 'ArrivalTime', 'DistanceInKm','AirportID_Departure','AirportID_Arrival','NumberOfSeats','Airline_ID']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Flight', ', '.join(fields), ', '.join(values))
        cur.execute(query)
        con.commit()
        cur.close()
        flash("Zbor adaugat cu succes.", 'success')
        return redirect(url_for('flight'))

@app.route('/topCountries')
def top_countries():
    tcs = view_top_countries()
    return render_template('topCountries.html', tcs=tcs)

@app.route('/leastCountries')
def least_countries():
    tcs = view_least_countries()
    return render_template('leastCountries.html', tcs=tcs)

@app.route('/topMonths')
def top_months():
    mts = view_top_months()
    return render_template('topMonths.html', mts=mts)


@app.route('/')
def Index():
    tickets = view_ticket()
    return render_template("index.html", tickets=tickets)




if __name__ == "__main__":
    app.run(debug=True)