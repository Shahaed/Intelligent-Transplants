import firebase from 'firebase';

var config = {
    apiKey: "AIzaSyChZfgaMdEk2hRX9czDZy5I_uvUoz5n2ic",
    authDomain: "hackillinois2018-d357f.firebaseapp.com",
    databaseURL: "https://hackillinois2018-d357f.firebaseio.com",
    projectId: "hackillinois2018-d357f",
    storageBucket: "hackillinois2018-d357f.appspot.com",
    messagingSenderId: "607645919867"
};
var fire = firebase.initializeApp(config);
export default fire;
