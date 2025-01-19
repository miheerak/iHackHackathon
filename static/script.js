const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = 5000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public')); 


const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',      
    password: 'root',      
    database: 'users',
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to the database');
});


app.post('/templates/registrationpage.html', (req, res) => {
    const { name, email, password } = req.body; 
    const query = 'INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)';

    db.query(query, [name, email, password], (err) => {
        if (err) throw err;
        console.log('User registered successfully');
        res.redirect('/templates/registrationpage.html');
    });
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
