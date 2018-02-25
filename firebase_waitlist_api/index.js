var config = {
    apiKey: "AIzaSyChZfgaMdEk2hRX9czDZy5I_uvUoz5n2ic",
    authDomain: "hackillinois2018-d357f.firebaseapp.com",
    databaseURL: "https://hackillinois2018-d357f.firebaseio.com",
    projectId: "hackillinois2018-d357f",
    storageBucket: "hackillinois2018-d357f.appspot.com",
    messagingSenderId: "607645919867"
};
var firebase = require('firebase');
firebase.initializeApp(config);
var database = firebase.database();
var express = require('express')
var cors = require('cors')
var app = express()
app.use(cors())

function setupData(ticketNumber) {
    firebase.database().ref('waitlist/' + ticketNumber).set({
        dr: 0,
        age: 0,
        blood: 0,
        gender: 0,
        ethnicity: 0,
        bmi: 0,
        lod: 0,
        time: new Date().toISOString()
    });
    num = ticketNumber++;
    firebase.database().ref('ticket_number').update({ticket_number: num });
}

// function getNumberInQueue(callback) {
//     firebase.database().ref().once('value').then((snapshot) => {
//         callback(snapshot);
//     });
// }

app.post('/api/signup/:isDoctor/:username/:password/:email', function(req, res) {
    firebase.database().ref('login/' + req.params.username).set({
        isDoctor: req.params.isDoctor,
        username: req.params.username,
        password: req.params.password,
        email: req.params.email
    });
});
app.get('/api/login/:username/', function(req, res) {
    firebase.database().ref('login/' + req.params.username).once('value').then((snapshot) => {
        res.send(snapshot.val());
    });
});

// app.post('/api/newTicket', function (req, res) {
//     firebase.database().ref('ticket_number').once('value').then((snapshot) => {
//         var ticket_number = snapshot.val().ticket_number + 1;
//         console.log(ticket_number);
//         setupData(ticket_number);
//         res.send(ticket_number + '');
//     })
// });

app.post('/api/insertValue/:user/:dr/:age/:blood/:gender/:ethnicity/:bmi/:lod', function (req, res) {
    var data = {'dr': req.params.dr, 'age': req.params.age, 'blood': req.params.blood, 'gender': req.params.gender, 'ethnicity': req.params.ethnicity, 'bmi': req.params.bmi, 'lod': req.params.lod};
    firebase.database().ref('waitlist/' + req.params.user).update({
        dr: data.dr,
        age: data.age,
        blood: data.blood,
        gender: data.gender,
        ethnicity: data.ethnicity,
        bmi: data.bmi,
        lod: data.bmi,
        time: new Date().toISOString()
    });
    res.sendStatus(200).send('Data scuccessfully received.');
})

app.get('/api/getAll', (req, res) => {
    firebase.database().ref('waitlist').once('value').then((snapshot) => {
        console.log(snapshot.val());
        res.send(snapshot.val());
    });
});

app.get('/api/getLineLength', (req, res) => {
    firebase.database().ref('waitlist/').once('value').then((snapshot) => {
        console.log(snapshot.val());
        res.send(snapshot.val().size());
    });
});

app.get('/api/getNextFourInLine', (req, res) => {
    firebase.database().ref().once('value').then((snapshot) => {

    });
});

app.post('/api/removeNumber/:removeNumber', (req, res) => {
    firebase.database().ref().once('value').then((snapshot) => {

    });
});

app.listen(3000, () => console.log('Example app listening on port 3000!'));