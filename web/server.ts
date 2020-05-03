import express = require('express');

const app: express.Application = express();

app.use(express.static('public'));

app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', (req, res) => {
    res.render('index');
});

app.listen(3333, () => {
    console.log('App is listening on localhost:3333');
});
