const express = require('express'); 
const app = express();
const port = 5000;   
 
app.post('/time', (req, res) => {        
    res.sendFile('index.html', {root: __dirname});
});

app.listen(port, () => {            
    console.log(`Now listening on port ${port}`); 
});