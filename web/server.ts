import express = require('express');

const app: express.Application = express();

app.use(express.static('public'));

app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', (req, res) => {
    res.render('index', {'active': ''});
});

app.get('/features', (req, res) => {
    res.render('features', {'active': 'Features'});
});

app.get('/general', (req, res) => {
    res.render('general', {'active': 'General'});
});

app.get('/network', (req, res) => {
    res.render('network', {'active': 'Network'});
});

app.get('/voice', (req, res) => {
    res.render('voice', {'active': 'Voice'});
});

app.listen(3333, () => {
    console.log('App is listening on localhost:3333');
});
