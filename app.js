const express = require('express'); 
var cors = require('cors');
const app = express();
const port = 5000;   
app.use(cors());

const Stopwatch = require('statman-stopwatch');

function msToTime(duration) {
    var milliseconds = Math.floor((duration % 1000) / 100),
      seconds = Math.floor((duration / 1000) % 60),
      minutes = Math.floor((duration / (1000 * 60)) % 60),
      hours = Math.floor((duration / (1000 * 60 * 60)) % 24);
  
    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;
  
    return hours + ":" + minutes + ":" + seconds;
  }

const stopwatch = new Stopwatch();

const timer = new Stopwatch();

//var timerTime = 0;
const timerMillis = 25000;


function startTimer() {
    timer.start();
}

function stopTimer() {
    timer.split(); 
}

function resumeTimer() {
  timer.unsplit();
}

function resetTimer() {
  timer.reset(); 
  //timerTime = 0;
}


//var timeLeft = '';

/*
function startTimer(minutes) {
    
    // Get today's date and time
    var now = new Date().getTime();
    const endTime = (minutes * 60000) + now;


    var x = setInterval(function() {


        now = new Date().getTime();
        // Find the distance between now and the count down date
        var distance = endTime - now;
      
        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
      
        // Display the result in the element with id="demo"
        
        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;
        seconds = (seconds < 10) ? "0" + seconds : seconds;
        
        timeLeft = hours + ":"
        + minutes + ":" + seconds;
        //console.log(timeLeft);
      
        // If the count down is finished, write some text
        /*if (distance < 0) {
          clearInterval(x);
          document.getElementById("demo").innerHTML = "EXPIRED";
        }*/
     // }, 1000);

//}


//const tasks = new Array['jõldak'];

app.get('/stopper/time', (req, res) => { 
    res.json({stopwatch: msToTime(stopwatch.read())});
});

app.get('/timer/time', (req, res) => { 
  timerTime = timerMillis - timer.read();
  if (timerTime < 0) {
    timerTime = 0;
    //timer.stop();
    timer.reset();
  }
  res.json({timer: msToTime(timerTime)});
  
});


app.post('/stopper/start', (req, res) => {
  stopwatch.start();        
  //console.log(stopwatch.read());
  res.sendStatus(200);
});

app.post('/stopper/reset', (req, res) => {
  stopwatch.reset();
  //console.log(stopwatch.read());  
  res.sendStatus(200);      
});

app.post('/stopper/stop', (req, res) => {
  stopwatch.stop();  
  //console.log(stopwatch.read());       
  res.sendStatus(200);
});

app.post('/timer/start', (req, res) => {
  startTimer();     
  res.sendStatus(200);  
});

app.post('/timer/stop', (req, res) => {  
  stopTimer();    
  res.sendStatus(200);   
});

app.post('/timer/resume', (req, res) => {  
  resumeTimer();       
  res.sendStatus(200);
});

app.post('/timer/reset', (req, res) => {
  resetTimer();       
  res.sendStatus(200);
});


/*app.get('/timer', (req, res) => {        
    res.json({timer: timeLeft});
});*/

app.listen(port, () => {            
    console.log(`Now listening on port ${port}`);
    
    
});


